import typing as t

from sqlmesh.core.linter.rule import Rule, RuleViolation
from sqlmesh.core.model import Model
from sqlmesh.core.node import IntervalUnit


class CronValidator(Rule):
    """Upstream model has a cron expression with longer intervals than this model's."""

    def check_model(self, model: Model) -> t.Optional[RuleViolation]:
        # Get the current model's cron expression
        this_model_cron = model.cron

        # Get upstream models through the context
        for upstream_model_name in model.depends_on:
            try:
                upstream_model = self.context.get_model(upstream_model_name)

                # Skip model kinds since they don't have cron schedules
                skip_kinds = ["EXTERNAL", "EMBEDDED", "SEED"]
                if upstream_model.kind.name in skip_kinds:
                    continue

                upstream_model_cron = upstream_model.cron

                # Compare cron expressions
                if self._is_cron_longer(upstream_model_cron, this_model_cron):
                    return self.violation(
                        f"Upstream model {upstream_model_name} has longer interval ({upstream_model_cron}) "
                        f"than this model ({this_model_cron})"
                    )
            except Exception:
                # Handle case where upstream model doesn't exist
                continue
        return None

    def _is_cron_longer(self, upstream_cron, current_cron) -> bool:
        """Compare two cron expressions to determine if upstream has longer intervals."""

        # Convert cron expressions to IntervalUnits for comparison
        upstream_interval = IntervalUnit.from_cron(upstream_cron)
        current_interval = IntervalUnit.from_cron(current_cron)

        # Compare the interval durations in seconds
        return upstream_interval.seconds > current_interval.seconds