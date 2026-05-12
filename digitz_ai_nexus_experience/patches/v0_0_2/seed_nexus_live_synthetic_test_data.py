import json
import hashlib

import frappe

UPDATE_EXISTING = True

LIVE = {
    "tenant": "TEST-NEXUS",
    "business_unit": "Nexus Synthetic BU",

    "public_agent": "SYN-LIVE-PUBLIC-AI",
    "sales_agent": "SYN-LIVE-SALES-AI",
    "support_agent": "SYN-LIVE-SUPPORT-AI",

    "qa_channel": "SYN-WEBSITE-QA",
    "chat_channel": "SYN-WEBSITE-CHAT",

    "sales_queue": "SYN-SALES-QUEUE",
    "support_queue": "SYN-SUPPORT-QUEUE",

    "context": "Nexus Live",
    "sub_context": "Operational Validation",
    "entity_type": "Live Scenario",
    "entity": "Nexus Live Synthetic Validation",
    "topic": "Live Interaction",

    "knowledge_unit_title": "Nexus Live Synthetic Validation",
}


SYNTHETIC_TEST_EMBEDDING = [0.0, 1.0, 0.0]


LIVE_KNOWLEDGE_TEXT = """
Nexus Test Orbit is a synthetic validation scenario used by DIGITZ AI Nexus to verify live Q&A, website chat, AI agent routing, escalation handling, and conversation continuity.

In the live validation flow, Nexus Test Orbit confirms that approved public knowledge can be retrieved for guest users through the website Q&A channel and the website chat channel.

The scenario validates that autonomous Q&A can answer directly from approved Nexus knowledge, while agent-based chat can respond through the assigned public AI agent.

Nexus Test Orbit also supports operational validation of low-confidence fallback, human escalation requests, sales intent routing, support intent routing, and session-style conversation continuity.

For continuity testing, a follow-up request such as "Continue the previous explanation about Nexus Test Orbit" means the user is asking to continue the Nexus Test Orbit live validation explanation. This request should remain connected to the Nexus Test Orbit live validation topic when the same live session context is being tested.
""".strip()


def execute():
    create_agents()
    create_ai_profiles()
    create_onboarding()

    create_channels()

    create_queues()
    create_escalation_rules()

    create_live_knowledge()

    frappe.db.commit()


def upsert_doc(doctype, filters, values):
    name = frappe.db.get_value(doctype, filters, "name")

    if name:
        if not UPDATE_EXISTING:
            return frappe.get_doc(doctype, name)
        doc = frappe.get_doc(doctype, name)
    else:
        doc = frappe.new_doc(doctype)

    for key, value in values.items():
        doc.set(key, value)

    if doc.is_new():
        doc.insert(ignore_permissions=True)
    else:
        doc.save(ignore_permissions=True)

    return doc


def ensure_tenant():
    if not frappe.db.exists("Nexus Tenant", LIVE["tenant"]):
        doc = frappe.new_doc("Nexus Tenant")
        doc.tenant_name = LIVE["tenant"]
        doc.insert(ignore_permissions=True)


def get_public_access_policy():
    existing = frappe.db.get_value(
        "Nexus Access Policy",
        {"policy_name": "Synthetic Public Guest Access"},
        "name",
    )

    if existing:
        return existing

    doc = frappe.new_doc("Nexus Access Policy")
    doc.policy_name = "Synthetic Public Guest Access"

    meta_fields = {field.fieldname for field in frappe.get_meta("Nexus Access Policy").fields}

    if "enabled" in meta_fields:
        doc.enabled = 1
    if "allowed_roles" in meta_fields:
        doc.allowed_roles = json.dumps(["Guest"])
    if "denied_roles" in meta_fields:
        doc.denied_roles = json.dumps([])
    if "sensitivity" in meta_fields:
        doc.sensitivity = "public"
    if "description" in meta_fields:
        doc.description = "Synthetic public access policy for Live validation seeds."

    doc.insert(ignore_permissions=True)
    return doc.name


def create_live_knowledge():
    ensure_tenant()

    access_policy = get_public_access_policy()

    unit = upsert_doc(
        "Nexus Knowledge Unit",
        {
            "title": LIVE["knowledge_unit_title"],
            "tenant": LIVE["tenant"],
        },
        build_knowledge_unit_values(access_policy),
    )

    chunk_hash = hashlib.sha256(LIVE_KNOWLEDGE_TEXT.encode("utf-8")).hexdigest()

    existing_chunk = frappe.db.get_value(
        "Nexus Knowledge Chunk",
        {
            "knowledge_unit": unit.name,
            "tenant": LIVE["tenant"],
            "business_unit": LIVE["business_unit"],
            "context": LIVE["context"],
            "sub_context": LIVE["sub_context"],
            "entity_type": LIVE["entity_type"],
            "entity": LIVE["entity"],
            "topic": LIVE["topic"],
            "chunk_index": 1,
        },
        "name",
    )

    chunk_values = {
        "knowledge_unit": unit.name,
        "tenant": LIVE["tenant"],
        "business_unit": LIVE["business_unit"],
        "project": "",
        "disabled": 0,
        "archived": 0,
        "chunk_index": 1,
        "priority": 100,
        "chunk_text": LIVE_KNOWLEDGE_TEXT,
        "chunk_hash": chunk_hash,
        "context": LIVE["context"],
        "sub_context": LIVE["sub_context"],
        "entity_type": LIVE["entity_type"],
        "entity": LIVE["entity"],
        "topic": LIVE["topic"],
        "context_path": "Nexus Live / Operational Validation / Nexus Live Synthetic Validation / Live Interaction",
        "access_policy": access_policy,
        "sensitivity": "public",
        "embedding": json.dumps(SYNTHETIC_TEST_EMBEDDING),
        "embedding_model": "synthetic-test-embedding",
        "embedding_status": "Completed",
        "allowed_roles": json.dumps(["Guest"]),
        "denied_roles": json.dumps([]),
        "source_version": 1,
        "character_count": len(LIVE_KNOWLEDGE_TEXT),
        "diagnostics_status": "Healthy",
        "diagnostics_message": "Synthetic Live validation chunk seeded successfully.",
    }

    if existing_chunk:
        chunk = frappe.get_doc("Nexus Knowledge Chunk", existing_chunk)
        for key, value in chunk_values.items():
            if field_exists("Nexus Knowledge Chunk", key):
                chunk.set(key, value)
        chunk.save(ignore_permissions=True)
    else:
        chunk = frappe.new_doc("Nexus Knowledge Chunk")
        for key, value in chunk_values.items():
            if field_exists("Nexus Knowledge Chunk", key):
                chunk.set(key, value)
        chunk.insert(ignore_permissions=True)

    print(f"Live knowledge seeded: {unit.name} / {chunk.name}")


def build_knowledge_unit_values(access_policy):
    values = {
        "title": LIVE["knowledge_unit_title"],
        "content": LIVE_KNOWLEDGE_TEXT,

        "tenant": LIVE["tenant"],
        "business_unit": LIVE["business_unit"],
        "project": "",

        "disabled": 0,

        "context": LIVE["context"],
        "sub_context": LIVE["sub_context"],
        "entity_type": LIVE["entity_type"],
        "entity": LIVE["entity"],
        "topic": LIVE["topic"],
        "context_path": "Nexus Live / Operational Validation / Nexus Live Synthetic Validation / Live Interaction",

        "default_access_policy": access_policy,
        "access_policy": access_policy,

        "sensitivity": "public",
        "allowed_roles": json.dumps(["Guest"]),
        "denied_roles": json.dumps([]),
    }

    return {
        key: value
        for key, value in values.items()
        if field_exists("Nexus Knowledge Unit", key)
    }


def field_exists(doctype, fieldname):
    return fieldname in {
        field.fieldname
        for field in frappe.get_meta(doctype).fields
    }


def create_channels():
    upsert_doc("Nexus Live Channel", {"channel_code": LIVE["qa_channel"]}, {
        "channel_code": LIVE["qa_channel"],
        "channel_name": "Synthetic Website Q And A",
        "channel_type": "Website Q&A",
        "enabled": 1,
        "public_access": 1,
        "requires_visitor_email": 0,
        "agent_based": 0,
        "description": "Synthetic autonomous Q And A validation channel.",
    })

    upsert_doc("Nexus Live Channel", {"channel_code": LIVE["chat_channel"]}, {
        "channel_code": LIVE["chat_channel"],
        "channel_name": "Synthetic Website Chat",
        "channel_type": "Website Chat",
        "enabled": 1,
        "public_access": 1,
        "requires_visitor_email": 0,
        "agent_based": 1,
        "default_agent": LIVE["public_agent"],
        "description": "Synthetic agent-based chat validation channel.",
    })


def create_queues():
    upsert_doc("Nexus Agent Queue", {"queue_code": LIVE["sales_queue"]}, {
        "queue_code": LIVE["sales_queue"],
        "queue_name": "Synthetic Sales Queue",
        "queue_type": "Sales",
        "enabled": 1,
        "description": "Synthetic sales escalation queue.",
    })

    upsert_doc("Nexus Agent Queue", {"queue_code": LIVE["support_queue"]}, {
        "queue_code": LIVE["support_queue"],
        "queue_name": "Synthetic Support Queue",
        "queue_type": "Support",
        "enabled": 1,
        "description": "Synthetic support escalation queue.",
    })


def create_agents():
    agents = [
        {
            "agent_code": LIVE["public_agent"],
            "agent_name": "Synthetic Public AI",
            "display_name": "Synthetic Public AI Assistant",
            "agent_role": "Public Responder",
            "description": "Synthetic public-facing AI responder.",
        },
        {
            "agent_code": LIVE["sales_agent"],
            "agent_name": "Synthetic Sales AI",
            "display_name": "Synthetic Sales AI Representative",
            "agent_role": "Sales",
            "description": "Synthetic sales AI representative.",
        },
        {
            "agent_code": LIVE["support_agent"],
            "agent_name": "Synthetic Support AI",
            "display_name": "Synthetic Support AI Executive",
            "agent_role": "Support",
            "description": "Synthetic support AI executive.",
        },
    ]

    for row in agents:
        upsert_doc("Nexus Live Agent", {"agent_code": row["agent_code"]}, {
            "agent_code": row["agent_code"],
            "agent_name": row["agent_name"],
            "display_name": row["display_name"],
            "agent_type": "AI",
            "agent_role": row["agent_role"],
            "status": "Idle",
            "enabled": 1,
            "visibility": "Public",
            "priority": 10,
            "max_active_sessions": 5,
            "current_active_sessions": 0,
            "description": row["description"],
        })


def create_ai_profiles():
    profiles = [
        {
            "agent": LIVE["public_agent"],
            "behavior_prompt": (
                "You are a synthetic public AI assistant. Respond to public product, "
                "platform, and knowledge questions using only approved Nexus knowledge."
            ),
            "tone": "Professional",
            "response_style": "Balanced",
        },
        {
            "agent": LIVE["sales_agent"],
            "behavior_prompt": (
                "You are a synthetic sales AI representative. Respond in a consultative "
                "commercial tone and escalate commercial intent when required."
            ),
            "tone": "Consultative",
            "response_style": "Balanced",
        },
        {
            "agent": LIVE["support_agent"],
            "behavior_prompt": (
                "You are a synthetic support AI executive. Help users with support-style "
                "questions and escalate unresolved or low-confidence issues."
            ),
            "tone": "Supportive",
            "response_style": "Step-by-step",
        },
    ]

    for row in profiles:
        upsert_doc("Nexus AI Agent Profile", {"agent": row["agent"]}, {
            "agent": row["agent"],
            "behavior_prompt": row["behavior_prompt"],
            "tone": row["tone"],
            "response_style": row["response_style"],
            "welcome_message": "Hello, I am ready to assist you.",
            "fallback_message": "I do not have enough approved knowledge to answer this.",
            "default_response_mode": "chat",
            "knowledge_scope": "Public Only",
            "confidence_threshold": 0.65,
            "escalation_enabled": 1,
            "memory_mode": "Session",
        })


def create_onboarding():
    for agent in [LIVE["public_agent"], LIVE["sales_agent"], LIVE["support_agent"]]:
        upsert_doc("Nexus Agent Onboarding", {"agent": agent}, {
            "agent": agent,
            "onboarding_status": "Approved",
            "identity_completed": 1,
            "behavior_completed": 1,
            "knowledge_completed": 1,
            "channel_completed": 1,
            "escalation_completed": 1,
            "testing_completed": 1,
            "activation_notes": "Approved synthetic Live validation agent.",
        })


def create_escalation_rules():
    rules = [
        {
            "rule_name": "Synthetic Public AI Escalation",
            "agent_role": "Public Responder",
            "target_queue": LIVE["support_queue"],
        },
        {
            "rule_name": "Synthetic Sales AI Escalation",
            "agent_role": "Sales",
            "target_queue": LIVE["sales_queue"],
        },
        {
            "rule_name": "Synthetic Support AI Escalation",
            "agent_role": "Support",
            "target_queue": LIVE["support_queue"],
        },
    ]

    for row in rules:
        upsert_doc("Nexus Escalation Rule", {"rule_name": row["rule_name"]}, {
            "rule_name": row["rule_name"],
            "enabled": 1,
            "agent_role": row["agent_role"],
            "minimum_confidence": 0.65,
            "escalate_on_no_knowledge": 1,
            "escalate_on_human_request": 1,
            "target_queue": row["target_queue"],
        })