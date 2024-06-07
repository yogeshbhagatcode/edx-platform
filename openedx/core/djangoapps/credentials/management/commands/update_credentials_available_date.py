"""
A manangement command to populate or correct the `certificate_available_date` data of the
CourseCertificateConfiguration model instances stored by the Credentials IDA.

This management command is required when moving from using `visible_date` to the certificate available date (a field of
the CourseCertificateConfiguration model) for managing certificate visibility. It can also be run ad-hoc to fix up any
data inconsistencies that may stored in the Credentials IDA's database.
"""
from django.core.management.base import BaseCommand

from openedx.core.djangoapps.credentials.tasks.v1.tasks import backfill_date_for_all_course_runs


class Command(BaseCommand):
    """
    Enqueue an async (`backfill_date_for_all_course_runs`) Celery task responsible for enqueuing subtasks responsible
    for sending certificate visibility related date updates to the Credentials IDA.

    Example usage:
        $ ./manage.py lms update_credentials_available_date
    """
    def handle(self, *args, **options):
        backfill_date_for_all_course_runs.delay()
