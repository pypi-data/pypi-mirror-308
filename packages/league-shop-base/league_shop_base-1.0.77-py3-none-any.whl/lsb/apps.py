from typing import Any
from typing import List
from typing import Optional
from typing import Sequence

from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error
from django.core.checks import register
from django.core.checks.messages import CheckMessage


@register()
def example_check(app_configs: Optional[Sequence[AppConfig]], **kwargs: Any):
    errors: List[CheckMessage] = []
    if not hasattr(settings, "ENCRYPTION_KEY"):
        errors.append(
            Error(
                "ENCRYPTION_KEY is not defined",
                hint=(
                    "Please define a fernet key in ENCRYPTION_KEY. "
                    "Use Fernet.generate_key() to create a random key."
                ),
                id="lsb.E001",
            )
        )
    return errors


class LsbConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lsb"
