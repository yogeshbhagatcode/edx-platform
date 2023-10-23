"""
This module contains various configuration settings via
waffle switches for the Certificates app.
"""

from edx_toggles.toggles import SettingToggle, WaffleSwitch

# Namespace
WAFFLE_NAMESPACE = 'certificates'

# .. toggle_name: certificates.auto_certificate_generation
# .. toggle_implementation: WaffleSwitch
# .. toggle_default: False
# .. toggle_description: This toggle will enable certificates to be automatically generated
# .. toggle_use_cases: open_edx
# .. toggle_creation_date: 2017-09-14
AUTO_CERTIFICATE_GENERATION = WaffleSwitch(f"{WAFFLE_NAMESPACE}.auto_certificate_generation", __name__)


# .. toggle_name: SEND_CERTIFICATE_CREATED_SIGNAL
# .. toggle_implementation: SettingToggle
# .. toggle_default: False
# .. toggle_description: When True, the system will publish `CERTIFICATE_CREATED` signals to the event bus. The
#   `CERTIFICATE_CREATED` signal is emit when a certificate has been awarded to a learner and the creation process has
#   completed.
# .. toggle_warning: Will be deprecated in favor of SEND_LEARNING_CERTIFICATE_LIFECYCLE_EVENTS_TO_BUS
# .. toggle_use_cases: temporary
# .. toggle_creation_date: 2023-04-11
# .. toggle_target_removal_date: 2023-07-31
# .. toggle_tickets: TODO
SEND_CERTIFICATE_CREATED_SIGNAL = SettingToggle('SEND_CERTIFICATE_CREATED_SIGNAL', default=False, module_name=__name__)


# .. toggle_name: SEND_CERTIFICATE_REVOKED_SIGNAL
# .. toggle_implementation: SettingToggle
# .. toggle_default: False
# .. toggle_description: When True, the system will publish `CERTIFICATE_REVOKED` signals to the event bus. The
#   `CERTIFICATE_REVOKED` signal is emit when a certificate has been revoked from a learner and the revocation process
#   has completed.
# .. toggle_warning: Will be deprecated in favor of SEND_LEARNING_CERTIFICATE_LIFECYCLE_EVENTS_TO_BUS
# .. toggle_use_cases: temporary
# .. toggle_creation_date: 2023-09-15
# .. toggle_target_removal_date: 2024-01-01
# .. toggle_tickets: TODO
SEND_CERTIFICATE_REVOKED_SIGNAL = SettingToggle('SEND_CERTIFICATE_REVOKED_SIGNAL', default=False, module_name=__name__)


from django.db.models import signals
from django.dispatch import receiver

import waffle.models

def report_waffle_change(model_short_name, instance, created, fields):
    verb = "created" if created else "updated"
    state_desc = ", ".join(f"{field}={repr(getattr(instance, field))}" for field in fields)
    print(f"📨📨📨📨📨 Waffle {model_short_name} {instance.name!r} was {verb}. New config: {state_desc}")

def report_waffle_delete(model_short_name, instance):
    print(f"📨📨📨📨📨 Waffle {model_short_name} {instance.name!r} was deleted")

WAFFLE_MODELS_TO_OBSERVE = [
    {
        'model': waffle.models.Flag,
        'short_name': 'flag',
        'fields': ['everyone', 'percent', 'superusers', 'staff', 'authenticated', 'note', 'languages'],
    },
    {
        'model': waffle.models.Switch,
        'short_name': 'switch',
        'fields': ['active', 'note'],
    },
    {
        'model': waffle.models.Sample,
        'short_name': 'sample',
        'fields': ['percent', 'note'],
    },
]


def register_waffle_observation(config):
    @receiver(signals.post_save, sender=config['model'])
    def log_waffle_change(*args, instance, created, **kwargs):
        report_waffle_change(config['short_name'], instance, created, config['fields'])

    @receiver(signals.post_delete, sender=config['model'])
    def log_waffle_change(*args, instance, **kwargs):
        report_waffle_delete(config['short_name'], instance)


for config in WAFFLE_MODELS_TO_OBSERVE:
    # Pass config to function to capture value properly.
    register_waffle_observation(config)
