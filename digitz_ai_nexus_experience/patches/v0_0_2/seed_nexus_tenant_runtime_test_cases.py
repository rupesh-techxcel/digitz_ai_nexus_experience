import frappe


UPDATE_EXISTING = True


RUNTIME = {
    "tenant": "TEST-NEXUS",
    "business_unit": "Nexus Synthetic BU",

    "context": "Nexus Live",
    "sub_context": "Operational Validation",
    "entity_type": "Live Scenario",
    "entity": "Nexus Live Synthetic Validation",
    "topic": "Live Interaction",

    "qa_channel": "SYN-WEBSITE-QA",
    "chat_channel": "SYN-WEBSITE-CHAT",

    "public_agent": "SYN-LIVE-PUBLIC-AI",
    "sales_agent": "SYN-LIVE-SALES-AI",
    "support_agent": "SYN-LIVE-SUPPORT-AI",

    "category": "Response Behaviour",
}


def execute():
    """
    Seeds tenant-aware runtime validation cases for Platform Validation Lab.

    These test cases intentionally use category 'Response Behaviour',
    not 'Administration', because Administration tests are excluded from
    Live runtime routing in testing.py.

    The titles start with 'Live Tenant Runtime...' so the Validation Lab
    clearly shows these as runtime validation cases.
    """
    test_cases = [
        {
            "test_title": "Live Tenant Runtime Q&A Default Context Test",
            "short_description": "Validates Live Q&A execution using TEST-NEXUS tenant ecosystem defaults and approved synthetic knowledge.",
            "test_category": RUNTIME["category"],
            "tenant": RUNTIME["tenant"],
            "business_unit": RUNTIME["business_unit"],
            "channel": RUNTIME["qa_channel"],
            "context": RUNTIME["context"],
            "sub_context": RUNTIME["sub_context"],
            "entity_type": RUNTIME["entity_type"],
            "entity": RUNTIME["entity"],
            "topic": RUNTIME["topic"],
            "caller_system": "Nexus Live",
            "use_case": "qa",
            "query": "What is Nexus Test Orbit?",
            "top_k": 5,
            "expected_access_status": "",
            "expected_answer_contains": "Nexus Test Orbit",
            "expected_source_count_min": 1,
            "expected_fallback_used": 0,
        },
        {
            "test_title": "Live Tenant Runtime Chat Default Public Agent Test",
            "short_description": "Validates Live Chat execution using tenant ecosystem defaults and the configured default public agent.",
            "test_category": RUNTIME["category"],
            "tenant": RUNTIME["tenant"],
            "business_unit": RUNTIME["business_unit"],
            "channel": RUNTIME["chat_channel"],
            "context": RUNTIME["context"],
            "sub_context": RUNTIME["sub_context"],
            "entity_type": RUNTIME["entity_type"],
            "entity": RUNTIME["entity"],
            "topic": RUNTIME["topic"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "Hi, what is Nexus Test Orbit?",
            "top_k": 5,
            "expected_access_status": "",
            "expected_agent_code": RUNTIME["public_agent"],
            "expected_agent_role": "Public Responder",
            "expected_answer_contains": "Nexus Test Orbit",
            "expected_source_count_min": 1,
            "expected_fallback_used": 0,
        },
        {
            "test_title": "Live Tenant Runtime Default Chat Channel Test",
            "short_description": "Validates that Live Chat works through the synthetic chat channel configured for TEST-NEXUS runtime.",
            "test_category": RUNTIME["category"],
            "tenant": RUNTIME["tenant"],
            "business_unit": RUNTIME["business_unit"],
            "channel": RUNTIME["chat_channel"],
            "context": RUNTIME["context"],
            "sub_context": RUNTIME["sub_context"],
            "entity_type": RUNTIME["entity_type"],
            "entity": RUNTIME["entity"],
            "topic": RUNTIME["topic"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "Can you explain Nexus Test Orbit in simple words?",
            "top_k": 5,
            "expected_access_status": "",
            "expected_agent_code": RUNTIME["public_agent"],
            "expected_agent_role": "Public Responder",
            "expected_answer_contains": "Nexus Test Orbit",
            "expected_source_count_min": 1,
            "expected_fallback_used": 0,
        },
        {
            "test_title": "Live Tenant Runtime Sales Intent Routing Test",
            "short_description": "Validates that sales intent is routed to the synthetic Sales AI agent within the TEST-NEXUS runtime tenant.",
            "test_category": RUNTIME["category"],
            "tenant": RUNTIME["tenant"],
            "business_unit": RUNTIME["business_unit"],
            "channel": RUNTIME["chat_channel"],
            "context": RUNTIME["context"],
            "sub_context": RUNTIME["sub_context"],
            "entity_type": RUNTIME["entity_type"],
            "entity": RUNTIME["entity"],
            "topic": RUNTIME["topic"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "Can I get pricing and demo details?",
            "top_k": 5,
            "expected_access_status": "",
            "expected_agent_code": RUNTIME["sales_agent"],
            "expected_agent_role": "Sales",
            "expected_fallback_used": 0,
        },
        {
            "test_title": "Live Tenant Runtime Support Intent Routing Test",
            "short_description": "Validates that support intent is routed to the synthetic Support AI agent within the TEST-NEXUS runtime tenant.",
            "test_category": RUNTIME["category"],
            "tenant": RUNTIME["tenant"],
            "business_unit": RUNTIME["business_unit"],
            "channel": RUNTIME["chat_channel"],
            "context": RUNTIME["context"],
            "sub_context": RUNTIME["sub_context"],
            "entity_type": RUNTIME["entity_type"],
            "entity": RUNTIME["entity"],
            "topic": RUNTIME["topic"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "I have a support issue and something is not working.",
            "top_k": 5,
            "expected_access_status": "",
            "expected_agent_code": RUNTIME["support_agent"],
            "expected_agent_role": "Support",
            "expected_fallback_used": 0,
        },
        {
            "test_title": "Live Tenant Runtime Explicit Channel Override Test",
            "short_description": "Validates that an explicit channel in the test payload is respected during tenant-aware Live Chat runtime.",
            "test_category": RUNTIME["category"],
            "tenant": RUNTIME["tenant"],
            "business_unit": RUNTIME["business_unit"],
            "channel": RUNTIME["chat_channel"],
            "context": RUNTIME["context"],
            "sub_context": RUNTIME["sub_context"],
            "entity_type": RUNTIME["entity_type"],
            "entity": RUNTIME["entity"],
            "topic": RUNTIME["topic"],
            "caller_system": "Nexus Live",
            "use_case": "chat",
            "query": "Hello from the explicit channel override runtime test.",
            "top_k": 5,
            "expected_access_status": "",
            "expected_agent_code": RUNTIME["public_agent"],
            "expected_agent_role": "Public Responder",
            "expected_fallback_used": 0,
        },
    ]

    for row in test_cases:
        upsert_test_case(row)


def upsert_test_case(data):
    """
    Upsert Nexus Test Case records safely.

    Pattern:
    - lookup by test_title
    - update existing when UPDATE_EXISTING is True
    - set only fields that exist
    - skip invalid Select values
    - print each insert/update
    """
    test_title = data.get("test_title")

    existing_name = frappe.db.get_value(
        "Nexus Test Case",
        {
            "test_title": test_title,
        },
        "name",
    )

    if existing_name:
        if not UPDATE_EXISTING:
            print(f"Skipped existing Tenant Runtime test case: {test_title}")
            return

        doc = frappe.get_doc("Nexus Test Case", existing_name)
        action = "Updated"
    else:
        doc = frappe.new_doc("Nexus Test Case")
        action = "Inserted"

    for fieldname, value in data.items():
        set_if_valid_field(doc, fieldname, value)

    set_if_valid_field(doc, "enabled", 1)

    if doc.is_new():
        doc.insert(ignore_permissions=True)
    else:
        doc.save(ignore_permissions=True)

    frappe.db.commit()

    print(f"{action}: {test_title}")


def set_if_valid_field(doc, fieldname, value):
    field = get_field(doc.meta, fieldname)

    if not field:
        return

    if not is_select_value_allowed(field, value):
        print(
            f"Skipped invalid Select value for {fieldname}: {value}"
        )
        return

    doc.set(fieldname, value)


def get_field(meta, fieldname):
    for field in meta.fields:
        if field.fieldname == fieldname:
            return field

    return None


def is_select_value_allowed(field, value):
    if not field:
        return True

    if field.fieldtype != "Select":
        return True

    if value in (None, ""):
        return True

    options = [
        option.strip()
        for option in (field.options or "").split("\n")
        if option.strip()
    ]

    if not options:
        return True

    return str(value) in options