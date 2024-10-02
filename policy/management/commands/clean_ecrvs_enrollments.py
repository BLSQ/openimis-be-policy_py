import logging

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from django.core.paginator import Paginator

from insuree.models import Insuree
from policy.models import Policy
from product.models import Product

logger = logging.getLogger(__name__)

UPDATE_PAGE_SIZE = 1000


def update_policy_for_children(policy: Policy, insuree: Insuree, product_id: int):
    expiry_date = insuree.dob + relativedelta(years=5) - relativedelta(days=1)  # Policy until their 5th birthday
    start_date = insuree.dob
    update_policy(policy=policy,
                  product_id=product_id,
                  enroll_date=start_date,
                  start_date=start_date,
                  effective_date=start_date,
                  expiry_date=expiry_date)


def update_policy_for_elderly(policy: Policy, insuree: Insuree, product_id: int):
    expiry_date = insuree.dob + relativedelta(years=125)  # Policy until their 125th birthday
    start_date = insuree.dob + relativedelta(years=65)
    update_policy(policy=policy,
                  product_id=product_id,
                  enroll_date=start_date,
                  start_date=start_date,
                  effective_date=start_date,
                  expiry_date=expiry_date)


def update_policy(policy: Policy, product_id: int, enroll_date, start_date, effective_date, expiry_date):
    policy.product_id = product_id
    policy.enroll_date = enroll_date
    policy.start_date = start_date
    policy.effective_date = effective_date
    policy.expiry_date = expiry_date
    policy.save()


class Command(BaseCommand):
    help = ("This command will clean all automatic enrollments that were made when uploading the eCRVS initial CSV data dump (circa July 2023)."
            "There was only one Product at that time (the default paid one), so +65 and -5 people were enrolled in it. Policy duration dates were therefore also wrong."
            "This command will redispatch these people into their correct Product and will also correct policy dates."
            "This command is meant as a one shot - once it has been run, it shouldn't be run anymore")

    def handle(self, *args, **options):
        logger.info("Clean eCRVS enrollments command triggered")

        logger.info("*** Fetching products ***")
        elderly_product_id = Product.objects.filter(validity_to__isnull=True, code="BASIC65+").first().id
        children_product_id = Product.objects.filter(validity_to__isnull=True, code="BASIC-5").first().id
        default_product_id = Product.objects.filter(validity_to__isnull=True, code="BASIC").first().id

        logger.info("*** Fetching policies ***")
        policies = (Policy.objects.filter(validity_to__isnull=True,
                                          product_id=default_product_id)
                                  .select_related("family__head_insuree")
                                  .prefetch_related("premiums")
                                  .order_by("id"))

        total_policies = 0
        total_children = 0
        total_elderly = 0
        total_pages = 0
        errors = []

        paginator = Paginator(policies, UPDATE_PAGE_SIZE)
        for page_number in paginator.page_range:
            page = paginator.page(page_number)

            total_pages += 1
            logger.info(f"\t Processing policy batch {total_pages}")

            for policy in page.object_list:
                insuree = policy.family.head_insuree

                if policy.premiums.exists():
                    logger.info(f"\t Error policy ID {policy.id} - there is a Premium for this policy! Insuree NIN = {insuree.chf_id}")
                    errors.append((policy.id, insuree.chf_id, "existing premium"))

                age_at_enrollment = insuree.age(policy.enroll_date)

                if age_at_enrollment < 5:
                    update_policy_for_children(policy, insuree, children_product_id)
                    total_children += 1
                elif age_at_enrollment >= 65:
                    update_policy_for_elderly(policy, insuree, elderly_product_id)
                    total_elderly += 1
                else:
                    logger.info(f"\t Error policy ID {policy.id} "
                                f"- the Insuree's ({insuree.chf_id}) age at enrollment is incorrect: {age_at_enrollment} "
                                f"- DOB={insuree.dob} - enrollment date={policy.enroll_date}")
                    errors.append((policy.id,
                                   insuree.chf_id,
                                   f"incorrect age ({age_at_enrollment}) - DOB={insuree.dob} - enrollment date={policy.enroll_date}"))

                total_policies += 1

        logger.info("**********************************")
        logger.info("Results:")
        logger.info(f"\t total policies: {total_policies}")
        logger.info(f"\t total children: {total_children}")
        logger.info(f"\t total elderly: {total_elderly}")
        logger.info(f"\t total errors: {len(errors)}")
        logger.info(f"\t detail errors:")
        for error in errors:
            logger.info(f"\t\t error policy {error[0]} - insuree {error[1]} - reason: {error[2]}")
