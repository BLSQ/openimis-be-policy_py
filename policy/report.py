from policy.reports import policy_renewals, new_enrollments, primary_operational_indicators, non_active_members
from policy.reports.non_active_members import non_active_members_query
from policy.reports.policy_renewals import policy_renewals_query
from policy.reports.primary_operational_indicators import policies_primary_indicators_query
from policy.reports.new_enrollments import new_enrollments_query

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
        "name": "policy_new_enrollments",
        "engine": 0,
        "default_report": new_enrollments.template,
        "description": "New Enrollments",
        "module": "policy",
        "python_query": new_enrollments_query,
        "permission": ["131227"],
    },
    {
        "name": "non_active_members",
        "engine": 0,
        "default_report": non_active_members.template,
        "description": "Non-active members",
        "module": "policy",
        "python_query": non_active_members_query,
        "permission": ["131228"],
    },
]
