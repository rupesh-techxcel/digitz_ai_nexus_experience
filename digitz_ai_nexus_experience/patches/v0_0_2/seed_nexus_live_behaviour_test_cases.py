import frappe

UPDATE_EXISTING = True

LIVE = {
    "tenant": "TEST-NEXUS",
    "business_unit": "Nexus Synthetic BU",

    "chat_channel": "website-chat",

    "sales_agent": "LIVE-TEST-SALES-AI",
    "support_agent": "LIVE-TEST-SUPPORT-AI",
    "public_agent": "LIVE-TEST-PUBLIC-AI",
    "no_escalation_agent": "LIVE-TEST-NO-ESCALATION-AI",
    "legacy_profile_agent": "LIVE-TEST-LEGACY-PROFILE-AI",

    "context": "Nexus Live",
    "sub_context": "Operational Validation",
    "entity_type": "Live Scenario",
    "entity": "Nexus Live Synthetic Validation",
    "topic": "Live Interaction",
}


def execute():
    test_cases = [
        {
            "test_title": "Live Behaviour Sales Runtime Test",
            "short_description": "Validates that a pricing/demo chat is routed to Sales AI and uses assigned Sales behaviour.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "Can I get pricing and demo details?",
            "user_roles": "Guest",
            "channel": LIVE["chat_channel"],
            "expected_agent_based": 1,
            "expected_agent_role": "Sales",
            "expected_behaviour_code": "LIVE-BEHAVIOUR-SALES",
            "expected_behaviour_designation": "Sales",
            "expected_uses_assigned_behaviour": 1,
            "expected_access_status": "no_context",
        },
        {
            "test_title": "Live Behaviour Support Runtime Test",
            "short_description": "Validates that a support/issue chat is routed to Support AI and uses assigned Support behaviour.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "I have an issue and need support because something is not working.",
            "user_roles": "Guest",
            "channel": LIVE["chat_channel"],
            "expected_agent_based": 1,
            "expected_agent_role": "Support",
            "expected_behaviour_code": "LIVE-BEHAVIOUR-SUPPORT",
            "expected_behaviour_designation": "Support",
            "expected_uses_assigned_behaviour": 1,
            "expected_access_status": "no_context",
        },
        {
    "test_title": "Live Behaviour Fallback Message Test",
    "short_description": "Validates that assigned behaviour fallback message is used when approved knowledge is unavailable.",
    "test_category": "Custom",
    "tenant": LIVE["tenant"],
    "business_unit": LIVE["business_unit"],
    "caller_system": "Nexus Live",
    "use_case": "chat",
    "query": "Tell me about a completely unknown behaviour-runtime-only topic.",
    "user_roles": "Guest",
    "channel": LIVE["chat_channel"],
    "agent": LIVE["public_agent"],
    "expected_agent_based": 1,
    "expected_agent_code": LIVE["public_agent"],
    "expected_agent_role": "Public Responder",
    "expected_behaviour_code": "LIVE-BEHAVIOUR-PUBLIC",
    "expected_uses_assigned_behaviour": 1,
    "expected_answer_contains": "Live Public Behaviour fallback",
    "expected_fallback_used": 1,
},
        {
            "test_title": "Live Behaviour Escalation Disabled Test",
            "short_description": "Validates that behaviour-level escalation_enabled = 0 prevents automatic escalation.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "This should trigger fallback but not escalation when behaviour disables escalation.",
            "user_roles": "Guest",
            "channel": LIVE["chat_channel"],
            "agent": LIVE["no_escalation_agent"],
            "expected_agent_based": 1,
            "expected_agent_code": LIVE["no_escalation_agent"],
            "expected_agent_role": "Public Responder",
            "expected_behaviour_code": "LIVE-BEHAVIOUR-NO-ESCALATION",
            "expected_uses_assigned_behaviour": 1,
            "expected_escalation": 0,
        },
        {
            "test_title": "Live Behaviour Confidence Threshold Test",
            "short_description": "Validates that assigned behaviour confidence threshold is used for escalation decision.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "I have a technical issue but the answer may require escalation.",
            "user_roles": "Guest",
            "channel": LIVE["chat_channel"],
            "expected_agent_based": 1,
            "expected_agent_role": "Support",
            "expected_behaviour_code": "LIVE-BEHAVIOUR-SUPPORT",
            "expected_uses_assigned_behaviour": 1,
            "expected_confidence_threshold": 0.70,
            "expected_confidence_threshold_source": "Nexus AI Behaviour",
        },
        {
            "test_title": "Live Behaviour Continuity Test",
            "short_description": "Validates chat continuity while assigned behaviour remains active.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "Continue the previous explanation about Nexus Test Orbit",
            "user_roles": "Guest",
            "channel": LIVE["chat_channel"],
            "expected_agent_based": 1,
            "expected_agent_role": "Public Responder",
            "expected_behaviour_code": "LIVE-BEHAVIOUR-PUBLIC",
            "expected_uses_assigned_behaviour": 1,
            "expected_conversation_continuity": 1,
            "expected_answer_contains": "Nexus Test Orbit",
        },
        {
            "test_title": "Live Behaviour Legacy Profile Fallback Test",
            "short_description": "Validates fallback to legacy Nexus AI Agent Profile when no Behaviour Master is assigned.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "Hi, what is Nexus Test Orbit?",
            "user_roles": "Guest",
            "channel": LIVE["chat_channel"],
            "agent": LIVE["legacy_profile_agent"],
            "expected_agent_based": 1,
            "expected_agent_code": LIVE["legacy_profile_agent"],
            "expected_agent_role": "Public Responder",
            "expected_behaviour_fallback_to_profile": 1,
            "expected_answer_contains": "Nexus Test Orbit",
        },
    ]

    for row in test_cases:
        upsert_live_behaviour_test_case(row)


def apply_required_defaults(data):
    data.setdefault("context", LIVE["context"])
    data.setdefault("sub_context", LIVE["sub_context"])
    data.setdefault("entity_type", LIVE["entity_type"])
    data.setdefault("entity", LIVE["entity"])
    data.setdefault("topic", LIVE["topic"])
    data.setdefault("top_k", 5)
    return data


def upsert_live_behaviour_test_case(data):
    data = apply_required_defaults(data)

    test_title = data.get("test_title")

    existing_name = frappe.db.get_value(
        "Nexus Test Case",
        {"test_title": test_title},
        "name",
    )

    if existing_name:
        if not UPDATE_EXISTING:
            print(f"Skipped existing Live Behaviour test case: {test_title}")
            return

        doc = frappe.get_doc("Nexus Test Case", existing_name)
        action = "Updated"
    else:
        doc = frappe.new_doc("Nexus Test Case")
        action = "Inserted"

    meta_fields = {
        field.fieldname
        for field in frappe.get_meta("Nexus Test Case").fields
    }

    for key, value in data.items():
        if key in meta_fields:
            doc.set(key, value)

    doc.enabled = 1

    if doc.is_new():
        doc.insert(ignore_permissions=True)
    else:
        doc.save(ignore_permissions=True)

    frappe.db.commit()

    print(f"{action}: {test_title}")