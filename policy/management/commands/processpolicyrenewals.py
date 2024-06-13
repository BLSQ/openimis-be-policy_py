import logging

from django.core.management.base import BaseCommand

from policy.tasks import get_policies_for_renewal

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = ("This command will trigger the policy task that updates the status of expired policies and "
            "generates policy renewals. Its purpose is to be triggered by a cron task instead of using the default "
            "backend scheduled task (because of worker issues, see the warning notes on "
            "https://pypi.org/project/django-apscheduler/.")

    def add_arguments(self, parser):
        parser.add_argument("-r", "--region", type=int, required=False, default=None)
        parser.add_argument("-d", "--district", type=int, required=False, default=None)
        parser.add_argument("-w", "--ward", type=int, required=False, default=None)
        parser.add_argument("--village", type=int, required=False, default=None)
        parser.add_argument(
            "-i",
            "--interval",
            type=int,
            required=False,
            help="Number of days before expiration to send renewal",
            default=None,
        )
        parser.add_argument(
            "-o",
            "--officer",
            type=int,
            required=False,
            help="Limits the renewals to a specific officer (ID of the Officer who created the policies)",
            default=None,
        )
        parser.add_argument(
            '--from',
            required=False,
            default=None,
            help="Date range to send renewals (policy.expiry_date >= date_from)",
        )
        parser.add_argument(
            '--to',
            required=False,
            default=None,
            help="Date range to send renewals (policy.expiry_date <= date_to)",
        )

    def handle(self, *args, **options):
        region = options["region"]
        district = options["district"]
        ward = options["ward"]
        village = options["village"]
        interval = options["interval"]
        officer = options["officer"]
        date_from = options["from"]
        date_to = options["to"]

        logger.info("Process policy renewals command triggered - starting renewals task")
        get_policies_for_renewal(
            region=region,
            district=district,
            ward=ward,
            village=village,
            officer=officer,
            interval=interval,
            date_from=date_from,
            date_to=date_to,
        )
