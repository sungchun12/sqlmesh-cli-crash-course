from sqlmesh import Context
from sqlmesh.core.config import Config, GatewayConfig, ModelDefaultsConfig
from sqlmesh.core.config.connection import DuckDBConnectionConfig

# First, load the existing context with config.yaml
base_context = Context(paths="/Users/sung/Desktop/git_repos/sqlmesh-cli-crash-course")

def run_plan(base_context):
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
        gateways={"snowflake2": new_gateway_config}
    )
    
    # Update the existing config with the new gateway while preserving other settings
    updated_config = base_context.config.update_with(new_config)
    
    # Create a new context with the updated config
    context = Context(
        paths="/Users/sung/Desktop/git_repos/sqlmesh-cli-crash-course",
        config=updated_config,
        gateway="snowflake2"
    )

    # Load the context
    context.load()

    print("Available models:")
    print(list(context.models.keys()))

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

    return plan, context

# Execute the plan
try:
    plan, context = run_plan(base_context)
    
    # Print the final config to verify all settings are preserved
    print("\nFinal Config:")
    print(f"All gateways: {context.config.gateways}")
    
except Exception as e:
    print(f"\nError occurred: {str(e)}")
    import traceback; traceback.print_exc()