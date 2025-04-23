# import os
# import json
# from sqlmesh.core.config import (
#     GatewayConfig,
#     ModelDefaultsConfig,
#     # SnowflakeConnectionConfig,
#     DuckDBConnectionConfig,
# )

# from sqlmesh.utils.errors import SQLMeshError

from sqlmesh import Context
from sqlmesh.core.config import Config, GatewayConfig, ModelDefaultsConfig
from sqlmesh.core.config.connection import DuckDBConnectionConfig

# # get the loaded config context and print the gateways
context = Context(paths="/Users/sung/Desktop/git_repos/sqlmesh-cli-crash-course")

# print(f"initial gateways: {context.config.gateways}") # {'duckdb': GatewayConfig<connection: DuckDBConnectionConfig<database: db.db>>, 'snowflake': GatewayConfig<connection: DuckDBConnectionConfig<database: snowflake.db>>}


def run_plan(context):
    # Create new gateway configuration
    new_gateway_config = GatewayConfig(
        connection=DuckDBConnectionConfig(
            database="/Users/sung/Desktop/git_repos/sqlmesh-cli-crash-course/snowflake2.db"
        ),
        state_connection=DuckDBConnectionConfig(
            database="/Users/sung/Desktop/git_repos/sqlmesh-cli-crash-course/snowflake2_state.db"
        )
    )
    
    # Create a new Config object with the new gateway
    new_config = Config(
        model_defaults=ModelDefaultsConfig(dialect="duckdb"),
        gateways={"snowflake2": new_gateway_config}
    )
    
    # Update the existing config with the new gateway
    context.config = context.config.update_with(new_config)
    
    # Create and add the new engine adapter for the gateway
    new_adapter = context.config.get_connection("snowflake2").create_engine_adapter()
    context._engine_adapters["snowflake2"] = new_adapter

    print(f"gateways after adding new gateway: {context.config.gateways}")
    
    # Select the new gateway
    context.selected_gateway = "snowflake2"
    context.load()
    
    # Now you can use the new gateway for your plan
    plan = context.plan(auto_apply=True, no_prompts=True)
    # context.apply(plan)
    # breakpoint()
    # Create and execute the plan
    # plan_builder = context.plan_builder(
    #     environment="dev",  # or your target environment
    #     auto_apply=True,
    #     no_prompts=True  # Skip interactive prompts
    # )
    return plan

run_plan(context)
# attempt to create a new gateway on runtime

    # {'duckdb': GatewayConfig<connection: DuckDBConnectionConfig<database: db.db>>, 'snowflake': GatewayConfig<connection: DuckDBConnectionConfig<database: snowflake.db>>}
    # {'duckdb': GatewayConfig<connection: DuckDBConnectionConfig<database: db.db>>, 'snowflake': GatewayConfig<connection: DuckDBConnectionConfig<database: snowflake.db>>, 'snowflake2': GatewayConfig<connection: DuckDBConnectionConfig<database: src/sqlmesh_final/snowflake.db>, state_connection: DuckDBConnectionConfig<database: src/sqlmesh_final/sqlmesh_state.db>>}

# add_and_select_gateway()

# def run_plan():
#     context.selected_gateway('snowflake2')
#     context.plan(auto_apply=True)

# def run_plan(context: Context) -> None:
#     def add_and_select_gateway():
#         snowflake_connection = DuckDBConnectionConfig( # placeholder for snowflake connection
#             database="src/sqlmesh_final/snowflake.db"
#         )
#         state_connection = DuckDBConnectionConfig(
#             database="src/sqlmesh_final/sqlmesh_state.db"
#         )

#         context.config.gateways['snowflake2'] = GatewayConfig(
#             connection=snowflake_connection,
#             state_connection=state_connection
#         )
#         context.selected_gateway = 'snowflake2'
#         print(f"gateways after adding new gateway: {context.config.gateways}") 
#     try:
#         add_and_select_gateway()
#         # Initialize context with specific gateway
#         context = Context(
#             paths="/Users/sung/Desktop/git_repos/sqlmesh-cli-crash-course",
#             gateway="snowflake2",
#             load=True  # Ensure models are loaded
#         )
        
#         # Run plan with auto-apply
#         context.plan(
#             environment="prod",
#             auto_apply=True,
#             no_prompts=True,  # Useful for automated runs
#             skip_tests=False  # Set to True if you want to skip tests
#         )
        
#     except SQLMeshError as e:
#         print(f"SQLMesh error occurred: {e}")
#         raise

# run_plan(context)

# Notes
# may NOT be possible to create a new gateway on runtime because it's meant to be immutable given how state can easily be corrupted


# from sqlmesh.core.config import Config, ModelDefaultsConfig

# config = Config(
#     model_defaults=ModelDefaultsConfig(dialect="duckdb"),
# )

