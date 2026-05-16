import frappe


UPDATE_EXISTING = True


ADMIN = {
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
    "test_group": "Administration Testing",
}


def execute():
    test_cases = [
        {
            "test_title": "Administration User Context Resolution Test",
            "short_description": "Validates that active user context resolves tenant, business unit, and active channel.",
            "test_category": "Administration",
            "tenant": ADMIN["tenant"],
            "business_unit": ADMIN["business_unit"],
            "caller_system": "Nexus Platform",
            "use_case": "qa",
            "query": "Resolve my active Nexus user context.",
            "expected_tenant": ADMIN["tenant"],
            "expected_business_unit": ADMIN["business_unit"],
            "expected_channel": ADMIN["chat_channel"],
            "expected_user_context": 1,
        },
        {
            "test_title": "Administration Ecosystem Defaults Test",
            "short_description": "Validates tenant ecosystem defaults for Q&A, Live Chat, public context, and public agent.",
            "test_category": "Administration",
            "tenant": ADMIN["tenant"],
            "business_unit": ADMIN["business_unit"],
            "caller_system": "Nexus Platform",
            "use_case": "qa",
            "query": "Validate ecosystem defaults for the active tenant.",
            "expected_default_public_context": ADMIN["context"],
            "expected_default_qa_channel": ADMIN["qa_channel"],
            "expected_default_chat_channel": ADMIN["chat_channel"],
            "expected_default_public_agent": ADMIN["public_agent"],
            "expected_qa_enabled": 1,
            "expected_live_chat_enabled": 1,
        },
        {
            "test_title": "Administration Readiness Summary Test",
            "short_description": "Validates that readiness summary safely returns knowledge, chunk, channel, and AI agent counts.",
            "test_category": "Administration",
            "tenant": ADMIN["tenant"],
            "business_unit": ADMIN["business_unit"],
            "caller_system": "Nexus Platform",
            "use_case": "qa",
            "query": "Validate administration readiness summary.",
            "expected_knowledge_min": 1,
            "expected_chunk_min": 1,
            "expected_channel_min": 1,
            "expected_ai_agent_min": 1,
        },
        {
            "test_title": "Administration Business Unit Plain Value Test",
            "short_description": "Validates that Business Unit works as a plain value and does not depend on a Nexus Business Unit doctype.",
            "test_category": "Administration",
            "tenant": ADMIN["tenant"],
            "business_unit": ADMIN["business_unit"],
            "caller_system": "Nexus Platform",
            "use_case": "qa",
            "query": "Validate business unit selector values without Business Unit doctype dependency.",
            "expected_business_unit": ADMIN["business_unit"],
            "expected_no_business_unit_doctype_required": 1,
        },
        {
            "test_title": "Administration Tenant Selector Test",
            "short_description": "Validates that tenant selector options include the synthetic validation tenant.",
            "test_category": "Administration",
            "tenant": ADMIN["tenant"],
            "business_unit": ADMIN["business_unit"],
            "caller_system": "Nexus Platform",
            "use_case": "qa",
            "query": "Validate tenant selector options.",
            "expected_tenant": ADMIN["tenant"],
            "expected_selector_contains_tenant": 1,
        },
        {
            "test_title": "Administration Q&A Defaults Test",
            "short_description": "Validates that Q&A defaults are configured in the tenant ecosystem.",
            "test_category": "Administration",
            "tenant": ADMIN["tenant"],
            "business_unit": ADMIN["business_unit"],
            "caller_system": "Nexus Platform",
            "use_case": "qa",
            "query": "Validate Q&A default context and Q&A channel from ecosystem.",
            "expected_default_public_context": ADMIN["context"],
            "expected_default_qa_channel": ADMIN["qa_channel"],
            "expected_qa_enabled": 1,
        },
        {
            "test_title": "Administration Live Defaults Test",
            "short_description": "Validates that Live Chat defaults are configured in the tenant ecosystem.",
            "test_category": "Administration",
            "tenant": ADMIN["tenant"],
            "business_unit": ADMIN["business_unit"],
            "caller_system": "Nexus Platform",
            "use_case": "chat",
            "query": "Validate Live Chat default channel and public agent from ecosystem.",
            "expected_default_chat_channel": ADMIN["chat_channel"],
            "expected_default_public_agent": ADMIN["public_agent"],
            "expected_live_chat_enabled": 1,
        },
    ]

    for row in test_cases:
        upsert_administration_test_case(row)


def apply_required_defaults(data):
    data.setdefault("context", ADMIN["context"])
    data.setdefault("sub_context", ADMIN["sub_context"])
    data.setdefault("entity_type", ADMIN["entity_type"])
    data.setdefault("entity", ADMIN["entity"])
    data.setdefault("topic", ADMIN["topic"])
    data.setdefault("top_k", 5)
    return data


def upsert_administration_test_case(data):
    """
    Stores Nexus Administration / tenant-aware ecosystem test cases
    in Nexus Test Case for the Platform Testing Lab.

    Pattern follows the existing synthetic test case seeds:
    - lookup by test_title
    - update existing when UPDATE_EXISTING is True
    - set only fields that exist on Nexus Test Case
    - skip invalid Select values
    - print each insert/update
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
            print(f"Skipped existing Nexus Administration test case: {test_title}")
            return

        doc = frappe.get_doc("Nexus Test Case", existing_name)
        action = "Updated"
    else:
        doc = frappe.new_doc("Nexus Test Case")
        action = "Inserted"

    for key, value in data.items():
        set_if_valid_field(doc, key, value)

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