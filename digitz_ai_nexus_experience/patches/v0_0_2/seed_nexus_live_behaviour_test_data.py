import frappe

UPDATE_EXISTING = True

LIVE = {
    "tenant": "TEST-NEXUS",
    "business_unit": "Nexus Synthetic BU",

    "sales_behaviour": "LIVE-BEHAVIOUR-SALES",
    "support_behaviour": "LIVE-BEHAVIOUR-SUPPORT",
    "public_behaviour": "LIVE-BEHAVIOUR-PUBLIC",
    "no_escalation_behaviour": "LIVE-BEHAVIOUR-NO-ESCALATION",

    "sales_agent": "LIVE-TEST-SALES-AI",
    "support_agent": "LIVE-TEST-SUPPORT-AI",
    "public_agent": "LIVE-TEST-PUBLIC-AI",
    "no_escalation_agent": "LIVE-TEST-NO-ESCALATION-AI",
    "legacy_profile_agent": "LIVE-TEST-LEGACY-PROFILE-AI",

    "chat_channel": "website-chat",

    "sales_queue": "LIVE-SALES-QUEUE",
    "support_queue": "LIVE-SUPPORT-QUEUE",
    "public_queue": "LIVE-PUBLIC-QUEUE",

    "context": "Nexus Live",
    "sub_context": "Operational Validation",
    "entity_type": "Live Scenario",
    "entity": "Nexus Live Synthetic Validation",
    "topic": "Live Interaction",
    "existing_synthetic_public_agent": "SYN-LIVE-PUBLIC-AI",
}


def execute():
    create_behaviours()
    create_channel()
    create_agents()
    create_legacy_ai_profile()
    create_onboarding()
    create_queues()
    create_escalation_rules()

    frappe.db.commit()

    print("Seeded Live Behaviour test data.")

def upsert_doc(doctype, filters, values):
    name = frappe.db.get_value(doctype, filters, "name")

    if name:
        if not UPDATE_EXISTING:
            print(f"Skipped existing {doctype}: {name}")
            return frappe.get_doc(doctype, name)

        doc = frappe.get_doc(doctype, name)
        action = "Updated"
    else:
        doc = frappe.new_doc(doctype)
        action = "Inserted"

    for key, value in values.items():
        if field_exists(doctype, key):
            doc.set(key, value)

    if doc.is_new():
        doc.insert(ignore_permissions=True)
    else:
        doc.save(ignore_permissions=True)

    label = (
        values.get("behaviour_code")
        or values.get("agent_code")
        or values.get("channel_code")
        or values.get("queue_code")
        or values.get("rule_name")
        or values.get("agent")
        or doc.name
    )

    print(f"{action}: {doctype} - {label}")

    return doc

def field_exists(doctype, fieldname):
    return fieldname in {
        field.fieldname
        for field in frappe.get_meta(doctype).fields
    }


def require_doctype(doctype):
    if not frappe.db.exists("DocType", doctype):
        frappe.throw("{0} DocType is required before seeding Live Behaviour test data.".format(doctype))


def create_behaviours():
    require_doctype("Nexus AI Behaviour")

    behaviours = [
        {
            "behaviour_code": LIVE["sales_behaviour"],
            "behaviour_name": "Live Test Sales Behaviour",
            "designation": "Sales",
            "enabled": 1,
            "description": "Synthetic sales behaviour for Live Behaviour testing.",
            "behavior_prompt": "You are a sales-focused AI representative for DIGITZ AI Nexus Live test scenarios.",
            "tone": "Consultative",
            "response_style": "Persuasive",
            "memory_mode": "Session",
            "confidence_threshold": 0.65,
            "escalation_enabled": 1,
            "welcome_message": "Hello, I can help with pricing, demo, and commercial questions.",
            "fallback_message": "Live Sales Behaviour fallback: I do not have enough approved knowledge to answer this.",
            "do_not_answer_rules": "Do not invent pricing. Escalate when commercial details are unavailable.",
        },
        {
            "behaviour_code": LIVE["support_behaviour"],
            "behaviour_name": "Live Test Support Behaviour",
            "designation": "Support",
            "enabled": 1,
            "description": "Synthetic support behaviour for Live Behaviour testing.",
            "behavior_prompt": "You are a support-focused AI representative for DIGITZ AI Nexus Live test scenarios.",
            "tone": "Supportive",
            "response_style": "Step-by-step",
            "memory_mode": "Session",
            "confidence_threshold": 0.70,
            "escalation_enabled": 1,
            "welcome_message": "Hello, I can help troubleshoot your support issue.",
            "fallback_message": "Live Support Behaviour fallback: I do not have enough approved support knowledge to answer this.",
            "do_not_answer_rules": "Do not guess technical fixes. Escalate unresolved support issues.",
        },
        {
            "behaviour_code": LIVE["public_behaviour"],
            "behaviour_name": "Live Test Public Responder Behaviour",
            "designation": "Public Responder",
            "enabled": 1,
            "description": "Synthetic public responder behaviour for Live Behaviour testing.",
            "behavior_prompt": "You are a public AI responder for DIGITZ AI Nexus Live test scenarios.",
            "tone": "Professional",
            "response_style": "Balanced",
            "memory_mode": "Session",
            "confidence_threshold": 0.65,
            "escalation_enabled": 1,
            "welcome_message": "Hello, I can help answer public questions.",
            "fallback_message": "Live Public Behaviour fallback: I do not have enough approved knowledge to answer this.",
            "do_not_answer_rules": "Only answer from approved public knowledge.",
        },
        {
            "behaviour_code": LIVE["no_escalation_behaviour"],
            "behaviour_name": "Live Test No Escalation Behaviour",
            "designation": "Public Responder",
            "enabled": 1,
            "description": "Synthetic public behaviour with escalation disabled.",
            "behavior_prompt": "You are a public AI responder with escalation disabled for test scenarios.",
            "tone": "Professional",
            "response_style": "Concise",
            "memory_mode": "Session",
            "confidence_threshold": 0.99,
            "escalation_enabled": 0,
            "welcome_message": "Hello, I can answer approved public questions.",
            "fallback_message": "Live No Escalation Behaviour fallback: I do not have enough approved knowledge to answer this.",
            "do_not_answer_rules": "Do not escalate automatically.",
        },
    ]

    for row in behaviours:
        upsert_doc(
            "Nexus AI Behaviour",
            {"behaviour_code": row["behaviour_code"]},
            row,
        )


def get_behaviour_name(behaviour_code):
    return frappe.db.get_value(
        "Nexus AI Behaviour",
        {
            "behaviour_code": behaviour_code
        },
        "name",
    )


def create_channel():
    upsert_doc(
        "Nexus Live Channel",
        {
            "channel_code": LIVE["chat_channel"]
        },
        {
            "channel_code": LIVE["chat_channel"],
            "channel_name": "Website Chat",
            "channel_type": "Website Chat",
            "enabled": 1,
            "public_access": 1,
            "requires_visitor_email": 0,
            "agent_based": 1,
            "default_agent": LIVE["public_agent"],
            "description": "Synthetic Live Behaviour validation chat channel.",
        },
    )


def create_agents():
    require_doctype("Nexus Live Agent")

    agents = [
        {
            "agent_code": LIVE["sales_agent"],
            "agent_name": "Live Test Sales AI",
            "display_name": "Live Test Sales AI Representative",
            "agent_role": "Sales",
            "behaviour": get_behaviour_name(LIVE["sales_behaviour"]),
            "description": "Synthetic sales AI for Live Behaviour validation.",
        },
        {
            "agent_code": LIVE["support_agent"],
            "agent_name": "Live Test Support AI",
            "display_name": "Live Test Support AI Executive",
            "agent_role": "Support",
            "behaviour": get_behaviour_name(LIVE["support_behaviour"]),
            "description": "Synthetic support AI for Live Behaviour validation.",
        },
        {
            "agent_code": LIVE["public_agent"],
            "agent_name": "Live Test Public AI",
            "display_name": "Live Test Public AI Assistant",
            "agent_role": "Public Responder",
            "behaviour": get_behaviour_name(LIVE["public_behaviour"]),
            "description": "Synthetic public AI for Live Behaviour validation.",
        },
        {
            "agent_code": LIVE["no_escalation_agent"],
            "agent_name": "Live Test No Escalation AI",
            "display_name": "Live Test No Escalation AI Assistant",
            "agent_role": "Public Responder",
            "behaviour": get_behaviour_name(LIVE["no_escalation_behaviour"]),
            "description": "Synthetic public AI with escalation disabled behaviour.",
        },
        {
            "agent_code": LIVE["existing_synthetic_public_agent"],
            "agent_name": "Synthetic Public AI",
            "display_name": "Synthetic Public AI Assistant",
            "agent_role": "Public Responder",
            "behaviour": get_behaviour_name(LIVE["public_behaviour"]),
            "description": "Existing synthetic public AI updated with Live Behaviour public behaviour.",
        },
        {
            "agent_code": LIVE["legacy_profile_agent"],
            "agent_name": "Live Test Legacy Profile AI",
            "display_name": "Live Test Legacy Profile AI Assistant",
            "agent_role": "Public Responder",
            "behaviour": None,
            "description": "Synthetic AI without Behaviour Master to validate legacy profile fallback.",
        },
    ]

    for row in agents:
        values = {
            "agent_code": row["agent_code"],
            "agent_name": row["agent_name"],
            "display_name": row["display_name"],
            "agent_type": "AI",
            "agent_role": row["agent_role"],
            "status": "Idle",
            "enabled": 1,
            "visibility": "Public",
            "default_channel": LIVE["chat_channel"],
            "priority": 10,
            "max_active_sessions": 10,
            "current_active_sessions": 0,
            "description": row["description"],
        }

        if field_exists("Nexus Live Agent", "behaviour"):
            values["behaviour"] = row["behaviour"]

        upsert_doc(
            "Nexus Live Agent",
            {
                "agent_code": row["agent_code"]
            },
            values,
        )


def create_legacy_ai_profile():
    upsert_doc(
        "Nexus AI Agent Profile",
        {
            "agent": LIVE["legacy_profile_agent"]
        },
        {
            "agent": LIVE["legacy_profile_agent"],
            "behavior_prompt": (
                "You are a legacy synthetic public AI assistant. "
                "This profile is used only when no Behaviour Master is assigned."
            ),
            "tone": "Professional",
            "response_style": "Balanced",
            "welcome_message": "Hello, I am ready to assist you.",
            "fallback_message": "Legacy Profile fallback: I do not have enough approved knowledge to answer this.",
            "default_response_mode": "chat",
            "knowledge_scope": "Public Only",
            "confidence_threshold": 0.65,
            "escalation_enabled": 1,
            "memory_mode": "Session",
        },
    )


def create_onboarding():
    agents = [
        LIVE["sales_agent"],
        LIVE["support_agent"],
        LIVE["public_agent"],
        LIVE["no_escalation_agent"],
        LIVE["legacy_profile_agent"],
        LIVE["existing_synthetic_public_agent"],
    ]

    for agent in agents:
        values = {
            "agent": agent,
            "onboarding_status": "Approved",
            "identity_completed": 1,
            "behavior_completed": 1,
            "behaviour_completed": 1,
            "knowledge_completed": 1,
            "channel_completed": 1,
            "escalation_completed": 1,
            "testing_completed": 1,
            "activation_notes": "Approved Live Behaviour validation agent.",
        }

        upsert_doc(
            "Nexus Agent Onboarding",
            {
                "agent": agent
            },
            values,
        )


def create_queues():
    upsert_doc(
        "Nexus Agent Queue",
        {
            "queue_code": LIVE["sales_queue"]
        },
        {
            "queue_code": LIVE["sales_queue"],
            "queue_name": "Live Sales Queue",
            "queue_type": "Sales",
            "enabled": 1,
            "description": "Live Behaviour sales escalation queue.",
        },
    )

    upsert_doc(
        "Nexus Agent Queue",
        {
            "queue_code": LIVE["support_queue"]
        },
        {
            "queue_code": LIVE["support_queue"],
            "queue_name": "Live Support Queue",
            "queue_type": "Support",
            "enabled": 1,
            "description": "Live Behaviour support escalation queue.",
        },
    )

    upsert_doc(
        "Nexus Agent Queue",
        {
            "queue_code": LIVE["public_queue"]
        },
        {
            "queue_code": LIVE["public_queue"],
            "queue_name": "Live Public Queue",
            "queue_type": "Support",
            "enabled": 1,
            "description": "Live Behaviour public escalation queue.",
        },
    )


def create_escalation_rules():
    rules = [
        {
            "rule_name": "Live Behaviour Sales Escalation",
            "agent_role": "Sales",
            "target_queue": LIVE["sales_queue"],
        },
        {
            "rule_name": "Live Behaviour Support Escalation",
            "agent_role": "Support",
            "target_queue": LIVE["support_queue"],
        },
        {
            "rule_name": "Live Behaviour Public Escalation",
            "agent_role": "Public Responder",
            "target_queue": LIVE["public_queue"],
        },
    ]

    for row in rules:
        upsert_doc(
            "Nexus Escalation Rule",
            {
                "rule_name": row["rule_name"]
            },
            {
                "rule_name": row["rule_name"],
                "enabled": 1,
                "agent_role": row["agent_role"],
                "minimum_confidence": 0.65,
                "confidence_threshold": 0.65,
                "escalate_on_no_knowledge": 1,
                "escalate_on_human_request": 1,
                "target_queue": row["target_queue"],
            },
        )