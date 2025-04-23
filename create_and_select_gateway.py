from sqlmesh import Context
from sqlmesh.core.config import Config, GatewayConfig, ModelDefaultsConfig
from sqlmesh.core.config.connection import DuckDBConnectionConfig

def run_plan(context):
    # Create new gateway configuration with only catalogs
    new_gateway_config = GatewayConfig(
        connection=DuckDBConnectionConfig(
            catalogs={
                "snowflake2": "/Users/sung/Desktop/git_repos/sqlmesh-cli-crash-course/snowflake2.db"
            }
        ),
        state_connection=DuckDBConnectionConfig(
            catalogs={
                "snowflake2_state": "/Users/sung/Desktop/git_repos/sqlmesh-cli-crash-course/snowflake2_state.db"
            }
        )
    )
    
    # Create a new Config object with the new gateway
    new_config = Config(
        model_defaults=ModelDefaultsConfig(dialect="duckdb", start="2025-03-26"),
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
    # First, load the context to ensure models are loaded
    context.load()

    print("Available models:")
    print(list(context.models.keys()))
    # breakpoint()
    # Create and execute the plan with a specific environment
    plan = context.plan(
        environment="dev",
        auto_apply=True,
        no_prompts=True,
        include_unmodified=True,
        start="2025-03-26",
        end="2025-03-27"
    )
    
    # Print plan details
    print("\nPlan Details:")
    print(f"Plan has changes: {plan.has_changes}")
    print(f"Plan requires backfill: {plan.requires_backfill}")
    if plan.has_changes:
        print("\nModified models:")
        for model in plan.modified_models:
            print(f"- {model}")

    return plan

# Initialize context
context = Context(paths="/Users/sung/Desktop/git_repos/sqlmesh-cli-crash-course")

# Execute the plan
try:
    plan = run_plan(context)
except Exception as e:
    print(f"\nError occurred: {str(e)}")
    import traceback; traceback.print_exc()