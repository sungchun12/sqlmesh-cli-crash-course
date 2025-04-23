class SQLMeshSession(Session):
    """A session for the MySQL proxy server which uses SQLMesh with DuckDB."""

    context: sqlmesh.Context

    def add_gateway(self, name, connection, state_connection):
        self.context.config.gateways[name] = GatewayConfig(connection=connection, state_connection=state_connection)
        self.context._engine_adapters[name] = connection.create_engine_adapter()

    def select_gateway(self, gateway_name):
        self.context.selected_gateway = gateway_name

    def create_and_select_gateway_for_poc(self):
        """Testing whether we can create gateways on runtime
        This creates a new gateway and selects it as a target to run queries"""
        gateway_name = "duckdb2"
        self.add_gateway(
            gateway_name,
            create_duckdb_connection("src/sqlmesh_final/db1.db"),
            create_duckdb_connection("src/sqlmesh_final/sqlmesh_state.db")
        )
        self.select_gateway(gateway_name)
        self.context.plan(auto_apply=True)


    async def query(
        self, expression: exp.Expression, sql: str, attrs: t.Dict[str, str]
    ) -> t.Tuple[t.Tuple[t.Tuple[t.Any], ...], t.List[str]]:
        """Execute a query using SQLMesh with DuckDB backend."""

        self.create_and_select_gateway_for_poc()

        try:
            # Check for semantic tables (SQLMesh-specific)
            tables = list(expression.find_all(exp.Table))
            if any((table.db, table.name) == ("__semantic", "__table") for table in tables):
                expression = self.context.rewrite(sql)
                logger.info("Compiled semantic expression: %s", expression.sql())
            
            # Log the SQL query in DuckDB dialect
            logger.info("Executing query: %s", expression.sql(dialect="duckdb"))
            
            # Execute the query using SQLMesh's fetchdf (DuckDB backend)
            df = self.context.fetchdf(expression)
            logger.debug("Query result: %s", df)
            
            # Replace NaN with None for MySQL compatibility
            df.replace({np.nan: None}, inplace=True)
            
            return tuple(df.itertuples(index=False)), list(df.columns)
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise