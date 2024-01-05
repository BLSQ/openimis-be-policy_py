from policy.reports import policy_renewals, nhia_new_enrollments, primary_operational_indicators, \
                           nhia_non_active_members, nhia_policy_renewals
from policy.reports.nhia_policy_renewals import nhia_policy_renewals_query
from policy.reports.nhia_non_active_members import nhia_non_active_members_query
from policy.reports.policy_renewals import policy_renewals_query
from policy.reports.primary_operational_indicators import policies_primary_indicators_query
from policy.reports.nhia_new_enrollments import nhia_new_enrollments_query

report_definitions = [
    {
        "name": "policy_renewals",
        "engine": 0,
        "default_report": policy_renewals.template,
        "description": "Policy renewals",
        "module": "policy",
        "python_query": policy_renewals_query,
        "permission": ["131217"],
    },
    {
        "name": "policy_primary_operational_indicators",
        "engine": 0,
        "default_report": primary_operational_indicators.template,
        "description": "Policy primary operational indicators",
        "module": "policy",
        "python_query": policies_primary_indicators_query,
        "permission": ["131201"],
    },
    {
        "name": "nhia_new_enrollments",
        "engine": 0,
        "default_report": nhia_new_enrollments.template,
        "description": "NHIA - New Enrollments",
        "module": "policy",
        "python_query": nhia_new_enrollments_query,
        "permission": ["131227"],
    },
    {
        "name": "nhia_non_active_members",
        "engine": 0,
        "default_report": nhia_non_active_members.template,
        "description": "NHIA - Non-Active Members",
        "module": "policy",
        "python_query": nhia_non_active_members_query,
        "permission": ["131228"],
    },
    {
        "name": "nhia_policy_renewals",
        "engine": 0,
        "default_report": nhia_policy_renewals.template,
        "description": "NHIA - Policy Renewals",
        "module": "policy",
        "python_query": nhia_policy_renewals_query,
        "permission": ["131229"],
    },
]
