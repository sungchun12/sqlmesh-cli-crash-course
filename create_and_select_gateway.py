from sqlmesh import Context
from sqlmesh.core.config import Config, GatewayConfig, ModelDefaultsConfig
from sqlmesh.core.config.connection import DuckDBConnectionConfig

def run_plan():
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
    
    # Create the initial config with the new gateway
    new_config = Config(
        model_defaults=ModelDefaultsConfig(dialect="duckdb", start="2025-03-26"),
        gateways={"snowflake2": new_gateway_config},
        default_gateway="snowflake2"  # Set this as the default gateway
    )
    
    # Initialize context with the new configuration
    context = Context(
        paths="/Users/sung/Desktop/git_repos/sqlmesh-cli-crash-course",
        config=new_config,
        gateway="snowflake2"
    )

    print(context.config.gateways)

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

    return plan

# Execute the plan
try:
    plan = run_plan()
except Exception as e:
    print(f"\nError occurred: {str(e)}")
    import traceback; traceback.print_exc()