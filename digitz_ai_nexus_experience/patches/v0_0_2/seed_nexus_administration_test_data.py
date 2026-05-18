# Administration test data seeding for tenant-aware platform tests.
import frappe

from digitz_ai_nexus.services.tenant_context import set_user_context
from digitz_ai_nexus.api.nexus_administration import (
    create_tenant_onboarding,
    save_ecosystem_configuration,
)


UPDATE_EXISTING = True


ADMIN = {
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

    "user": "Administrator",
}


def execute():
    """
    Seeds minimum administration data required for tenant-aware platform tests.

    Creates / updates:
    - Nexus Tenant
    - Nexus User Context
    - Nexus Ecosystem
    - default Q&A / Chat ecosystem settings
    """
    ensure_tenant()
    ensure_user_context()
    ensure_ecosystem_defaults()

    frappe.db.commit()

    print("Seeded Nexus Administration test data.")


def ensure_tenant():
    """
    Ensure the synthetic tenant exists.
    """
    result = create_tenant_onboarding(
        tenant_name=ADMIN["tenant_name"],
        tenant_code=ADMIN["tenant_code"],
        business_unit_name=ADMIN["business_unit"],
    )

    print("Ensured Tenant Onboarding: {0}".format(result.get("tenant")))

    return result


def ensure_user_context():
    """
    Ensure Administrator has TEST-NEXUS as active tenant context.
    """
    doc = set_user_context(
        user=ADMIN["user"],
        tenant=ADMIN["tenant"],
        business_unit=ADMIN["business_unit"],
        channel=ADMIN["chat_channel"],
        is_default=1,
    )

    print("Updated Nexus User Context: {0}".format(doc.name))

    return doc


def ensure_ecosystem_defaults():
    """
    Ensure Nexus Ecosystem defaults are configured for platform tests.
    """
    values = {
        "tenant": ADMIN["tenant"],
        "enabled": 1,
        "activation_status": "Configured",

        "default_business_unit": ADMIN["business_unit"],
        "default_public_context": ADMIN["context"],

        "require_approved_knowledge": 1,
        "strict_tenant_mode": 1,
        "default_top_k": 5,

        "qa_enabled": 1,
        "default_qa_channel": ADMIN["qa_channel"],
        "qa_fallback_message": "I do not have enough approved knowledge to answer this.",
        "source_citation_required": 1,

        "live_chat_enabled": 1,
        "default_chat_channel": ADMIN["chat_channel"],
        "default_live_channel": ADMIN["chat_channel"],
        "default_public_agent": ADMIN["public_agent"],
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