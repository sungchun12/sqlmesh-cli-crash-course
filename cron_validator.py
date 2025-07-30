import typing as t

from sqlmesh.core.linter.rule import Rule, RuleViolation
from sqlmesh.core.model import Model

# example: daily -> hourly -> every 5 minutes
class CronValidator(Rule):
    """Upstream model has a cron expression with longer intervals than this model's cron expression."""

    def check_model(self, model: Model) -> t.Optional[RuleViolation]:
        # get the current model's cron expression
        current_model_cron = model.cron
        breakpoint()
        # get the first upstream model's cron expression
        upstream_model_cron = next(iter(model.depends_on)).cron
        # breakpoint() 
        # if the upstream model's cron expression is longer than the current model's cron expression, return a violation
        if upstream_model_cron > current_model_cron:
            return self.violation()
        else:
            return None
