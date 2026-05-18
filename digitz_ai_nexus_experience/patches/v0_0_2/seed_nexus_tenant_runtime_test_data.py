# Tenant-runtime test data seeding for DIGITZ AI Nexus platform validation.
import frappe

from digitz_ai_nexus.api.nexus_administration import (
    create_tenant_onboarding,
    save_ecosystem_configuration,
)
from digitz_ai_nexus.services.tenant_context import set_user_context


UPDATE_EXISTING = True


RUNTIME = {
    "tenant": "TEST-NEXUS",
    "tenant_name": "Test Nexus Tenant",
    "tenant_code": "TEST-NEXUS",

    "business_unit": "Nexus Synthetic BU",

    "context": "Nexus Live",
    "sub_context": "Operational Validation",
    "entity_type": "Live Scenario",
    "entity": "Nexus Live Synthetic Validation",
    "topic": "Live Interaction",

    "qa_channel": "SYN-WEBSITE-QA",
    "chat_channel": "SYN-WEBSITE-CHAT",
    "public_agent": "SYN-LIVE-PUBLIC-AI",

    "synthetic_agent_prefix": "SYN-LIVE-",
    "user": "Administrator",
}


def execute():
    """
    Seeds minimum tenant-runtime configuration for Platform Validation Lab.

    This seed does not create knowledge chunks.
    It assumes the existing synthetic knowledge/live seeds already exist.

    It ensures:
    - TEST-NEXUS tenant exists
    - Nexus Ecosystem defaults are configured
    - Administrator has a stable active context
    - Synthetic Live agents are enabled, idle, and aligned to SYN-WEBSITE-CHAT
    - Synthetic channels are enabled and have stable defaults where fields exist
    """
    ensure_tenant()
    ensure_channels()
    ensure_ecosystem_defaults()
    ensure_user_context()
    reset_synthetic_live_agents()

    frappe.db.commit()

    print("Seeded Nexus Tenant Runtime test data.")


def ensure_tenant():
    """
    Ensure TEST-NEXUS tenant exists.
    """
    if frappe.db.exists("Nexus Tenant", RUNTIME["tenant"]):
        print(f"Tenant already exists: {RUNTIME['tenant']}")
        return RUNTIME["tenant"]

    result = create_tenant_onboarding(
        tenant_name=RUNTIME["tenant_name"],
        tenant_code=RUNTIME["tenant_code"],
        business_unit_name=RUNTIME["business_unit"],
    )

    print("Ensured Tenant Onboarding: {0}".format(result.get("tenant")))

    return result.get("tenant")


def ensure_channels():
    """
    Ensure synthetic channels are enabled and configured consistently.
    Only updates fields that exist.
    """
    ensure_channel(
        channel=RUNTIME["chat_channel"],
        default_agent=RUNTIME["public_agent"],
        agent_based=1,
    )

    ensure_channel(
        channel=RUNTIME["qa_channel"],
        default_agent=None,
        agent_based=0,
    )


def ensure_channel(channel, default_agent=None, agent_based=None):
    if not frappe.db.exists("DocType", "Nexus Live Channel"):
        print("Skipped channel update. Nexus Live Channel doctype not found.")
        return

    if not frappe.db.exists("Nexus Live Channel", channel):
        print(f"Skipped channel update. Channel not found: {channel}")
        return

    meta_fields = {
        df.fieldname: df
        for df in frappe.get_meta("Nexus Live Channel").fields
    }

    values = {}

    if "enabled" in meta_fields:
        values["enabled"] = 1

    if "public_access" in meta_fields:
        fieldtype = meta_fields["public_access"].fieldtype

        if fieldtype in ("Check", "Int"):
            values["public_access"] = 1
        else:
            values["public_access"] = "Public"

    if "agent_based" in meta_fields and agent_based is not None:
        values["agent_based"] = agent_based

    if "default_agent" in meta_fields and default_agent:
        values["default_agent"] = get_agent_name(default_agent) or default_agent

    if values:
        frappe.db.set_value(
            "Nexus Live Channel",
            channel,
            values,
            update_modified=False,
        )

        print(f"Updated Nexus Live Channel: {channel}")

def ensure_ecosystem_defaults():
    """
    Ensure Nexus Ecosystem defaults are configured for tenant-runtime tests.
    """
    values = {
        "tenant": RUNTIME["tenant"],
        "enabled": 1,
        "activation_status": "Configured",

        "default_business_unit": RUNTIME["business_unit"],
        "default_public_context": RUNTIME["context"],

        "require_approved_knowledge": 1,
        "strict_tenant_mode": 1,
        "default_top_k": 5,

        "qa_enabled": 1,
        "default_qa_channel": RUNTIME["qa_channel"],
        "qa_fallback_message": "I do not have enough approved knowledge to answer this.",
        "source_citation_required": 1,

        "live_chat_enabled": 1,
        "default_chat_channel": RUNTIME["chat_channel"],
        "default_live_channel": RUNTIME["chat_channel"],
        "default_public_agent": RUNTIME["public_agent"],
        "default_escalation_enabled": 1,

        "website_widget_enabled": 1,
        "widget_title": "DIGITZ AI Nexus",
        "widget_welcome_message": "Hello, how can I help you?",
        "widget_brand_color": "#214dbb",

        "testing_required_before_activation": 1,
        "certification_status": "Not Certified",
    }

    result = save_ecosystem_configuration(values)

    print("Updated Nexus Ecosystem: {0}".format(result.get("ecosystem")))

    return result


def ensure_user_context():
    """
    Ensure Administrator active context is stable for fallback/runtime tests.
    """
    doc = set_user_context(
        user=RUNTIME["user"],
        tenant=RUNTIME["tenant"],
        business_unit=RUNTIME["business_unit"],
        project=None,
        channel=RUNTIME["chat_channel"],
        is_default=1,
    )

    print("Updated Nexus User Context: {0}".format(doc.name))

    return doc


def reset_synthetic_live_agents():
    """
    Reset all synthetic Live agents so runtime platform tests are repeatable.

    Scoped only to:
    agent_code like 'SYN-LIVE-%'
    """
    if not frappe.db.exists("DocType", "Nexus Live Agent"):
        print("Skipped synthetic agent reset. Nexus Live Agent doctype not found.")
        return

    meta_fields = {
        df.fieldname
        for df in frappe.get_meta("Nexus Live Agent").fields
    }

    agents = frappe.get_all(
        "Nexus Live Agent",
        filters={
            "agent_code": ["like", f"{RUNTIME['synthetic_agent_prefix']}%"],
        },
        fields=["name", "agent_code"],
        limit_page_length=500,
    )

    for agent in agents:
        values = {}

        if "enabled" in meta_fields:
            values["enabled"] = 1

        if "status" in meta_fields:
            values["status"] = "Idle"

        if "current_active_sessions" in meta_fields:
            values["current_active_sessions"] = 0

        if "visibility" in meta_fields:
            values["visibility"] = "Public"

        if "default_channel" in meta_fields:
            values["default_channel"] = RUNTIME["chat_channel"]

        if "disabled" in meta_fields:
            values["disabled"] = 0

        if "approval_status" in meta_fields:
            values["approval_status"] = "Approved"

        if "onboarding_status" in meta_fields:
            values["onboarding_status"] = "Approved"

        if "availability_status" in meta_fields:
            values["availability_status"] = "Available"

        if "rejection_reason" in meta_fields:
            values["rejection_reason"] = None

        if "last_status_change" in meta_fields:
            values["last_status_change"] = frappe.utils.now_datetime()

        if values:
            frappe.db.set_value(
                "Nexus Live Agent",
                agent.name,
                values,
                update_modified=False,
            )

            print(f"Reset Synthetic Live Agent: {agent.agent_code}")


def get_agent_name(agent_code_or_name):
    if not agent_code_or_name:
        return None

    if frappe.db.exists("Nexus Live Agent", agent_code_or_name):
        return agent_code_or_name

    return frappe.db.get_value(
        "Nexus Live Agent",
        {
            "agent_code": agent_code_or_name,
        },
        "name",
    )