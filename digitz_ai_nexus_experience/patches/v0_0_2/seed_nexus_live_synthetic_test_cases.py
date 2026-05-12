import frappe

UPDATE_EXISTING = True

LIVE = {
    "tenant": "TEST-NEXUS",
    "business_unit": "Nexus Synthetic BU",
    "qa_channel": "SYN-WEBSITE-QA",
    "chat_channel": "SYN-WEBSITE-CHAT",
    "public_agent": "SYN-LIVE-PUBLIC-AI",
    "sales_agent": "SYN-LIVE-SALES-AI",
    "support_agent": "SYN-LIVE-SUPPORT-AI",
    "context": "Nexus Live",
    "sub_context": "Operational Validation",
    "entity_type": "Live Scenario",
    "entity": "Nexus Live Synthetic Validation",
    "topic": "Live Interaction",
}


def execute():
    test_cases = [
        {
            "test_title": "Live Autonomous Q And A Test",
            "short_description": "Validates autonomous Q And A without assigning a live agent.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "qa",
            "query": "What is Nexus Test Orbit?",
            "user_roles": "Guest",
            "expected_access_status": "allowed",
            "expected_answer_contains": "Nexus Test Orbit",
            "expected_source_count_min": 1,
            "expected_fallback_used": 0,
            "channel": LIVE["qa_channel"],
            "expected_agent_based": 0,
            "expected_escalation": 0,
        },
        {
            "test_title": "Live Autonomous Q And A Fallback Test",
            "short_description": "Validates autonomous Q And A fallback without escalation.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "qa",
            "query": "Unknown synthetic live question",
            "user_roles": "Guest",
            "expected_access_status": "no_context",
            "expected_answer_contains": "I do not have enough approved knowledge",
            "expected_source_count_min": 0,
            "expected_fallback_used": 1,
            "channel": LIVE["qa_channel"],
            "expected_agent_based": 0,
            "expected_escalation": 0,
        },
        {
            "test_title": "Live Agent-Based Chat Test",
            "short_description": "Validates website chat starts through a designated AI agent.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "Hi, what is Nexus Test Orbit?",
            "user_roles": "Guest",
            "expected_access_status": "allowed",
            "expected_answer_contains": "Nexus Test Orbit",
            "expected_source_count_min": 1,
            "expected_fallback_used": 0,
            "channel": LIVE["chat_channel"],
            "expected_agent_based": 1,
            "expected_agent_code": LIVE["public_agent"],
            "expected_escalation": 0,
        },
        {
            "test_title": "Live Chat Low Confidence Escalation Test",
            "short_description": "Validates chat escalation when approved knowledge is not available.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "Explain unknown unsupported synthetic live capability",
            "user_roles": "Guest",
            "expected_access_status": "no_context",
            "expected_answer_contains": "I do not have enough approved knowledge",
            "expected_source_count_min": 0,
            "expected_fallback_used": 1,
            "channel": LIVE["chat_channel"],
            "expected_agent_based": 1,
            "expected_agent_code": LIVE["public_agent"],
            "expected_escalation": 1,
        },
        {
            "test_title": "Live Human Request Escalation Test",
            "short_description": "Validates escalation when visitor explicitly requests human support.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "I want to speak to a human",
            "user_roles": "Guest",
            "expected_access_status": "allowed",
            "expected_answer_contains": "",
            "expected_source_count_min": 0,
            "expected_fallback_used": 0,
            "channel": LIVE["chat_channel"],
            "expected_agent_based": 1,
            "expected_agent_code": LIVE["public_agent"],
            "expected_escalation": 1,
            "user_requested_human": 1,
        },
        {
            "test_title": "Live Sales Intent Routing Test",
            "short_description": "Validates sales intent is routed to Sales AI.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "Can I get pricing and demo details?",
            "user_roles": "Guest",
            "expected_access_status": "no_context",
            "expected_answer_contains": "I do not have enough approved knowledge",
            "expected_source_count_min": 0,
            "expected_fallback_used": 1,
            "channel": LIVE["chat_channel"],
            "expected_agent_based": 1,
            "expected_agent_role": "Sales",
            "expected_escalation": 0,
        },
        {
            "test_title": "Live Support Intent Routing Test",
            "short_description": "Validates support intent is routed to Support AI.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "I have an error and need support",
            "user_roles": "Guest",
            "expected_access_status": "no_context",
            "expected_answer_contains": "I do not have enough approved knowledge",
            "expected_source_count_min": 0,
            "expected_fallback_used": 1,
            "channel": LIVE["chat_channel"],
            "expected_agent_based": 1,
            "expected_agent_role": "Support",
            "expected_escalation": 0,
        },
        {
            "test_title": "Live Conversation Continuity Test",
            "short_description": "Validates a chat conversation can continue under the same conversation session.",
            "test_category": "Custom",
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "caller_system": "Nexus Live",
            "use_case": "chat",

            # IMPORTANT:
            # The test runner currently sends this as a standalone payload.
            # So the query must carry the previous topic anchor.
            "query": "Continue the previous explanation about Nexus Test Orbit",

            "user_roles": "Guest",
            "expected_access_status": "allowed",
            "expected_answer_contains": "Nexus Test Orbit",
            "expected_source_count_min": 1,
            "expected_fallback_used": 0,
            "channel": LIVE["chat_channel"],
            "expected_agent_based": 1,
            "expected_agent_code": LIVE["public_agent"],
            "expected_conversation_continuity": 1,
        },
    ]

    for row in test_cases:
        upsert_live_test_case(row)


def apply_required_defaults(data):
    data.setdefault("context", LIVE["context"])
    data.setdefault("sub_context", LIVE["sub_context"])
    data.setdefault("entity_type", LIVE["entity_type"])
    data.setdefault("entity", LIVE["entity"])
    data.setdefault("topic", LIVE["topic"])
    data.setdefault("top_k", 5)
    return data


def upsert_live_test_case(data):
    """
    Stores Live scenario cases in Nexus Test Case for Experience Lab display.
    Extra Live-specific fields are set only if they exist on the DocType.
    """
    data = apply_required_defaults(data)

    test_title = data.get("test_title")

    existing_name = frappe.db.get_value(
        "Nexus Test Case",
        {"test_title": test_title},
        "name",
    )

    if existing_name:
        if not UPDATE_EXISTING:
            print(f"Skipped existing Live test case: {existing_name}")
            return
        doc = frappe.get_doc("Nexus Test Case", existing_name)
        action = "Updated"
    else:
        doc = frappe.new_doc("Nexus Test Case")
        action = "Inserted"

    meta_fields = {field.fieldname for field in frappe.get_meta("Nexus Test Case").fields}

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