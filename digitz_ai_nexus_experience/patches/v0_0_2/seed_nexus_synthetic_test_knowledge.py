import json
import frappe


UPDATE_EXISTING = True
DUMMY_EMBEDDING = json.dumps([0.0, 1.0, 0.0])


SYNTHETIC = {
    "tenant": "TEST-NEXUS",
    "alt_tenant": "TEST-NEXUS-ALT",
    "business_unit": "Nexus Synthetic BU",
    "other_business_unit": "Other Synthetic BU",
    "project": "Alpha Orbit Project",
    "other_project": "Beta Orbit Project",
    "context": "Synthetic ERP",
    "sub_context": "Orbit Operations",
    "entity_type": "Synthetic Product",
    "entity": "Nexus Test Orbit",
    "overview_topic": "Orbit Overview",
    "valuation_topic": "Orbit Valuation Protocol",
    "draft_topic": "Orbit Draft Topic",
    "disabled_topic": "Orbit Disabled Topic",
    "deny_topic": "Orbit Deny Priority",
    "missing_embedding_topic": "Orbit Missing Embedding",
    "ingested_topic": "Ingested Retrieval",
    "reprocess_topic": "Reprocess Governance",
    "observatory_topic": "Chunk Observatory",
    "retrieval_ready_topic": "Retrieval Readiness",
    "archived_chunk_topic": "Archived Chunk Governance",
}


def execute():
    ensure_master_data()

    knowledge_units = [
        {
            "name": "TEST-NEXUS-SYNTHETIC-ORBIT-OVERVIEW",
            "title": "Nexus Test Orbit Public Overview",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["overview_topic"],
            "access_policy": "public",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Guest", "Orbit Viewer", "Orbit Analyst"],
            "content": """
Nexus Test Orbit is a synthetic knowledge object created only for DIGITZ AI Nexus engine certification tests.

Nexus Test Orbit is not a real product, module, or business process.

It is used to validate public retrieval, website Q&A, website chat, response mode behavior, source selection, and safe grounding.

The synthetic overview belongs to the Nexus Synthetic BU business unit, Synthetic ERP context, Orbit Operations sub context, Synthetic Product entity type, Nexus Test Orbit entity, and Orbit Overview topic.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-SYNTHETIC-ORBIT-VALUATION-GENERAL",
            "title": "Nexus Test Orbit General Valuation Protocol",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["valuation_topic"],
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Nexus Test Orbit valuation is calculated using the Blue Radius Index.

If the Blue Radius Index is unavailable, the synthetic fallback index is the Silver Anchor Index.

The Orbit Valuation Protocol is restricted synthetic knowledge and should be available only to the Orbit Analyst role.

The Blue Radius Index phrase is intentionally unique so test retrieval does not accidentally match real DIGITZ ERP knowledge.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-SYNTHETIC-ORBIT-VALUATION-ALPHA",
            "title": "Alpha Orbit Project Valuation Protocol",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "project": SYNTHETIC["project"],
            "scope_type": "project",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["valuation_topic"],
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Alpha Orbit Project has project-specific Nexus Test Orbit valuation rules.

Project Alpha Override is the project-specific rule for Alpha Orbit Project.

Under Project Alpha Override, Nexus Test Orbit valuation is still calculated using the Blue Radius Index.

If the Blue Radius Index is unavailable, Alpha Orbit Project uses the Silver Anchor Index as fallback.

This project-specific fixture validates strict project retrieval, with_general project retrieval, and project preference over general knowledge.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-SYNTHETIC-ORBIT-DRAFT",
            "title": "Orbit Draft Knowledge Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["draft_topic"],
            "access_policy": "role_based",
            "status": "Draft",
            "enabled": 1,
            "is_active": 1,
            "disabled": 1,
            "embedding_status": "Pending",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Orbit draft only knowledge should not be retrieved because the knowledge status is Draft.

This synthetic fixture exists only to validate approval governance.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-SYNTHETIC-ORBIT-DISABLED",
            "title": "Orbit Disabled Knowledge Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["disabled_topic"],
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 0,
            "is_active": 0,
            "disabled": 1,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Orbit disabled only knowledge should not be retrieved because the knowledge is disabled.

This synthetic fixture exists only to validate enabled and is_active filtering.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-SYNTHETIC-ORBIT-DENY-PRIORITY",
            "title": "Orbit Deny Priority Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["deny_topic"],
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "denied_roles": ["Orbit Analyst"],
            "content": """
Orbit deny priority rule means denial must win when the same role appears in both allowed roles and denied roles.

This synthetic fixture validates deny-over-allow precedence.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-SYNTHETIC-ORBIT-MISSING-EMBEDDING",
            "title": "Orbit Missing Embedding Safety Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["missing_embedding_topic"],
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Pending",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Orbit missing embedding safety knowledge intentionally has no embedding.

Retrieval should not crash when this approved chunk has empty embedding.
""",
            "embedding": "",
        },

               # ------------------------------------------------------------
        # INGESTED RETRIEVAL FIXTURES
        # ------------------------------------------------------------
        {
            "name": "TEST-NEXUS-INGESTED-PUBLIC-RETRIEVAL",
            "title": "Ingested Public Retrieval Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["ingested_topic"],
            "access_policy": "public",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Guest", "Orbit Analyst"],
            "content": """
Ingested public knowledge confirms that Nexus Test Orbit observability can be retrieved from ingestion-generated chunks.

Nexus Test Orbit observability is validated through governed knowledge retrieval, chunk generation, embedding generation, and approved Q&A availability.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-INGESTED-ROLE-ALLOWED",
            "title": "Ingested Role Allowed Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["ingested_topic"],
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Restricted ingested Orbit Calibration knowledge is available only to the Orbit Analyst role.

Orbit Calibration uses the Blue Radius Index to validate that role-based access works correctly for ingestion-generated knowledge.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-INGESTED-ROLE-DENIED",
            "title": "Ingested Role Denied Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["ingested_topic"],
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "denied_roles": ["Orbit Viewer"],
            "content": """
        Restricted Orbit Signal knowledge is available only to the Orbit Analyst role.

        Orbit Viewer must not retrieve this restricted ingested Orbit Signal knowledge.
        """,
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-INGESTED-KEYWORD-RETRIEVAL",
            "title": "Ingested Keyword Retrieval Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["ingested_topic"],
            "access_policy": "public",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Guest", "Orbit Analyst"],
            "content": """
Blue Radius Discovery is a synthetic public keyword retrieval validation phrase.

The phrase Blue Radius Discovery is intentionally repeated for retrieval stability.

Blue Radius Discovery confirms that public ingestion-generated chunks can be retrieved through keyword scoring.

Synthetic business keyword validation uses Blue Radius Discovery for deterministic retrieval testing.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-INGESTED-MISSING-EMBEDDING",
            "title": "Ingested Missing Embedding Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": SYNTHETIC["context"],
            "sub_context": SYNTHETIC["sub_context"],
            "entity_type": SYNTHETIC["entity_type"],
            "entity": SYNTHETIC["entity"],
            "topic": SYNTHETIC["ingested_topic"],
            "access_policy": "public",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Pending",
            "allowed_roles": ["Guest", "Orbit Analyst"],
            "content": """
Missing embedding safety fixture for ingested retrieval.

This chunk intentionally has no embedding and should not crash retrieval.
""",
            "embedding": "",
        },
                # ------------------------------------------------------------
        # KNOWLEDGE SOURCE QUALITY PANEL / INGESTION GOVERNANCE FIXTURES
        # ------------------------------------------------------------
        {
            "name": "TEST-NEXUS-KNOWLEDGE-SOURCE-PROCESSING",
            "title": "Knowledge Source Processing Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": "Nexus Knowledge",
            "sub_context": "Ingestion",
            "entity_type": "Knowledge Source",
            "entity": "Quality Panel",
            "topic": "Knowledge Source Processing",
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Nexus processes a knowledge source by extracting readable text, normalizing the content, creating a generated knowledge unit, splitting the content into chunks, creating embeddings, and updating the source quality fields.

The knowledge source processing flow gives administrators visibility into processing status, chunk count, embedding status, last processed time, extracted text preview, generated knowledge unit, and generated chunks.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-EXTRACTED-TEXT-PREVIEW",
            "title": "Extracted Text Preview Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": "Nexus Knowledge",
            "sub_context": "Extraction",
            "entity_type": "Knowledge Source",
            "entity": "Text Extraction",
            "topic": "Extracted Text Preview",
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Extracted text preview in Nexus shows the readable text captured from a manual source or uploaded document before the content is used for chunking and embeddings.

The extracted text preview helps administrators identify bad extraction, missing text, corrupted PDF content, formatting issues, and incomplete source material before publishing knowledge.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-GENERATED-KNOWLEDGE-UNIT",
            "title": "Generated Knowledge Unit Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": "Nexus Knowledge",
            "sub_context": "Knowledge Unit",
            "entity_type": "Knowledge Source",
            "entity": "Knowledge Unit",
            "topic": "Generated Knowledge Unit",
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Nexus links a processed knowledge source to a generated knowledge unit.

The generated knowledge unit is the normalized master knowledge object created from the source. It connects the original source to generated chunks, embeddings, retrieval, and governed AI answers.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-GENERATED-CHUNKS",
            "title": "Generated Chunks Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": "Nexus Knowledge",
            "sub_context": "Chunking",
            "entity_type": "Knowledge Chunk",
            "entity": "Generated Chunks",
            "topic": "Chunk Generation",
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Nexus generates chunks by splitting normalized source text into smaller knowledge segments.

Generated chunks improve retrieval quality because each chunk can be embedded, scored, filtered by metadata, governed by access rules, and used as grounded source material for AI answers.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-EMBEDDING-STATUS-COMPLETED",
            "title": "Embedding Status Completed Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": "Nexus Knowledge",
            "sub_context": "Embeddings",
            "entity_type": "Knowledge Source",
            "entity": "Embedding Status",
            "topic": "Embedding Completion",
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Nexus verifies embedding completion by checking whether generated chunks have embeddings.

When all generated chunks are embedded, the embedding status can be marked Completed on the knowledge source and the generated knowledge unit. The chunk embedding state remains the real source of truth.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-QUALITY-PANEL-REFRESH",
            "title": "Quality Panel Refresh Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": "Nexus Knowledge",
            "sub_context": "Quality Panel",
            "entity_type": "Knowledge Source",
            "entity": "Quality Panel",
            "topic": "Quality Panel Refresh",
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
The Nexus quality panel refresh reloads the latest ingestion observability data for a knowledge source.

It returns processing status, embedding status, chunk count, last processed time, extracted text preview, generated knowledge unit, and generated chunks so administrators can verify knowledge readiness.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
            "name": "TEST-NEXUS-TEST-THIS-SOURCE",
            "title": "Test This Source Fixture",
            "tenant": SYNTHETIC["tenant"],
            "business_unit": SYNTHETIC["business_unit"],
            "scope_type": "general",
            "context": "Nexus Knowledge",
            "sub_context": "Source Testing",
            "entity_type": "Knowledge Source",
            "entity": "Source Testing",
            "topic": "Grounded Validation",
            "access_policy": "role_based",
            "status": "Approved",
            "enabled": 1,
            "is_active": 1,
            "disabled": 0,
            "embedding_status": "Completed",
            "allowed_roles": ["Orbit Analyst"],
            "content": """
Nexus tests a processed source by asking a grounded question against approved chunks created from that source.

The Test This Source action helps administrators confirm whether the processed source can produce a grounded answer before the knowledge is exposed to public Q&A or website chat.
""",
            "embedding": DUMMY_EMBEDDING,
        },
        {
    "name": "TEST-NEXUS-REPROCESS-GOVERNANCE",
    "title": "Reprocess Governance Fixture",
    "tenant": SYNTHETIC["tenant"],
    "business_unit": SYNTHETIC["business_unit"],
    "scope_type": "general",
    "context": "Nexus Knowledge",
    "sub_context": "Ingestion Governance",
    "entity_type": "Knowledge Source",
    "entity": "Reprocess Governance",
    "topic": SYNTHETIC["reprocess_topic"],
    "access_policy": "role_based",
    "status": "Approved",
    "enabled": 1,
    "is_active": 1,
    "disabled": 0,
    "embedding_status": "Completed",
    "allowed_roles": ["Orbit Analyst"],
    "content": """
Nexus reprocess governance prevents retrieval pollution by archiving old chunks and disabling old generated knowledge versions before creating fresh chunks.

Each processing run increments the processing version and assigns the new source version to active chunks.
""",
    "embedding": DUMMY_EMBEDDING,
},
{
    "name": "TEST-NEXUS-CHUNK-OBSERVATORY",
    "title": "Chunk Observatory Fixture",
    "tenant": SYNTHETIC["tenant"],
    "business_unit": SYNTHETIC["business_unit"],
    "scope_type": "general",
    "context": "Nexus Knowledge",
    "sub_context": "Observability",
    "entity_type": "Knowledge Chunk",
    "entity": "Chunk Observatory",
    "topic": SYNTHETIC["observatory_topic"],
    "access_policy": "role_based",
    "status": "Approved",
    "enabled": 1,
    "is_active": 1,
    "disabled": 0,
    "embedding_status": "Completed",
    "allowed_roles": ["Orbit Analyst"],
    "content": """
The Chunk Observatory shows processing version, chunk count, active chunks, embedded chunks, missing embeddings, duplicate chunks, diagnostics status, and retrieval readiness.

It helps administrators inspect generated chunks, chunk text, metadata, embedding state, archived state, and retrieval readiness.
""",
    "embedding": DUMMY_EMBEDDING,
},
{
    "name": "TEST-NEXUS-RETRIEVAL-READINESS",
    "title": "Retrieval Readiness Fixture",
    "tenant": SYNTHETIC["tenant"],
    "business_unit": SYNTHETIC["business_unit"],
    "scope_type": "general",
    "context": "Nexus Knowledge",
    "sub_context": "Readiness",
    "entity_type": "Knowledge Source",
    "entity": "Retrieval Readiness",
    "topic": SYNTHETIC["retrieval_ready_topic"],
    "access_policy": "role_based",
    "status": "Approved",
    "enabled": 1,
    "is_active": 1,
    "disabled": 0,
    "embedding_status": "Completed",
    "allowed_roles": ["Orbit Analyst"],
    "content": """
Retrieval readiness means a knowledge source is safe for production retrieval.

A source becomes retrieval ready only when it is published, processed, embedded, diagnostically healthy, and has active chunks available for retrieval.
""",
    "embedding": DUMMY_EMBEDDING,
},
{
    "name": "TEST-NEXUS-ARCHIVED-CHUNK-GOVERNANCE",
    "title": "Archived Chunk Governance Fixture",
    "tenant": SYNTHETIC["tenant"],
    "business_unit": SYNTHETIC["business_unit"],
    "scope_type": "general",
    "context": "Nexus Knowledge",
    "sub_context": "Chunk Lifecycle",
    "entity_type": "Knowledge Chunk",
    "entity": "Archived Chunks",
    "topic": SYNTHETIC["archived_chunk_topic"],
    "access_policy": "role_based",
    "status": "Approved",
    "enabled": 1,
    "is_active": 1,
    "disabled": 0,
    "embedding_status": "Completed",
    "allowed_roles": ["Orbit Analyst"],
    "content": """
Archived chunks remain visible for observability and audit history, but they are disabled and excluded from active retrieval readiness calculations.

Only active chunks should determine retrieval readiness, duplicate diagnostics, and production retrieval eligibility.
""",
    "embedding": DUMMY_EMBEDDING,
},
    ]

    for row in knowledge_units:
        upsert_knowledge_unit_and_chunk(row)

    frappe.db.commit()
    print("Synthetic Nexus test knowledge seed completed.")


def ensure_master_data():
    ensure_default_access_policy("PUBLIC")
    ensure_default_access_policy("Role Based")
    ensure_default_access_policy("RESTRICTED")

    ensure_doc("Nexus Tenant", SYNTHETIC["tenant"], {
        "tenant_code": SYNTHETIC["tenant"],
        "tenant_name": SYNTHETIC["tenant"],
        "title": SYNTHETIC["tenant"],
    })

    ensure_doc("Nexus Tenant", SYNTHETIC["alt_tenant"], {
        "tenant_code": SYNTHETIC["alt_tenant"],
        "tenant_name": SYNTHETIC["alt_tenant"],
        "title": SYNTHETIC["alt_tenant"],
    })

    ensure_doc("Nexus Business Unit", SYNTHETIC["business_unit"], {
        "business_unit_name": SYNTHETIC["business_unit"],
        "title": SYNTHETIC["business_unit"],
        "tenant": SYNTHETIC["tenant"],
    })

    ensure_doc("Nexus Business Unit", SYNTHETIC["other_business_unit"], {
        "business_unit_name": SYNTHETIC["other_business_unit"],
        "title": SYNTHETIC["other_business_unit"],
        "tenant": SYNTHETIC["tenant"],
    })

    ensure_doc("Nexus Project", SYNTHETIC["project"], {
        "project_name": SYNTHETIC["project"],
        "title": SYNTHETIC["project"],
        "business_unit": SYNTHETIC["business_unit"],
        "tenant": SYNTHETIC["tenant"],
    })

    ensure_doc("Nexus Project", SYNTHETIC["other_project"], {
        "project_name": SYNTHETIC["other_project"],
        "title": SYNTHETIC["other_project"],
        "business_unit": SYNTHETIC["business_unit"],
        "tenant": SYNTHETIC["tenant"],
    })


def ensure_default_access_policy(policy_name):
    doctype = "Nexus Access Policy"

    if not frappe.db.exists("DocType", doctype):
        print(f"Skipped: {doctype} DocType not found")
        return

    if frappe.db.exists(doctype, policy_name):
        return

    doc = frappe.new_doc(doctype)
    doc.name = policy_name

    for fieldname in [
        "policy_name",
        "access_policy",
        "access_policy_name",
        "default_access_policy",
        "title",
        "label",
    ]:
        if doc.meta.has_field(fieldname):
            doc.set(fieldname, policy_name)

    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    print(f"Inserted master: {doctype} - {policy_name}")


def ensure_doc(doctype, name, values=None):
    if not frappe.db.exists("DocType", doctype):
        return

    if frappe.db.exists(doctype, name):
        return

    doc = frappe.new_doc(doctype)

    try:
        doc.name = name
    except Exception:
        pass

    values = values or {}

    for fieldname, value in values.items():
        set_if_field(doc, fieldname, value)

    for fallback_field in [
        "tenant",
        "tenant_code",
        "tenant_name",
        "business_unit",
        "business_unit_name",
        "project",
        "project_name",
        "title",
    ]:
        if doc.meta.has_field(fallback_field) and not doc.get(fallback_field):
            doc.set(fallback_field, name)

    doc.insert(ignore_permissions=True)
    print(f"Inserted master: {doctype} - {name}")


def upsert_knowledge_unit_and_chunk(data):
    unit_name = data["name"]

    if frappe.db.exists("Nexus Knowledge Unit", unit_name):
        unit = frappe.get_doc("Nexus Knowledge Unit", unit_name)
        action = "Updated"
    else:
        unit = frappe.new_doc("Nexus Knowledge Unit")
        unit.name = unit_name
        action = "Inserted"

    set_common_fields(unit, data)
    set_if_field(unit, "title", data.get("title"))
    set_content_fields(unit, data.get("content"))
    set_roles(unit, data.get("allowed_roles") or [], data.get("denied_roles") or [])

    if unit.is_new():
        unit.insert(ignore_permissions=True)
    else:
        unit.save(ignore_permissions=True)

    upsert_chunk(unit, data)

    print(f"{action}: {data.get('title')}")


def upsert_chunk(unit, data):
    chunk_name = f"{data['name']}-CHUNK-001"

    if frappe.db.exists("Nexus Knowledge Chunk", chunk_name):
        chunk = frappe.get_doc("Nexus Knowledge Chunk", chunk_name)
    else:
        chunk = frappe.new_doc("Nexus Knowledge Chunk")
        chunk.name = chunk_name

    set_if_field(chunk, "knowledge_unit", unit.name)
    if data.get("knowledge_source") and frappe.db.exists("Nexus Knowledge Source", data.get("knowledge_source")):
        set_if_field(chunk, "knowledge_source", data.get("knowledge_source"))
    set_if_field(chunk, "chunk_index", 1)

    set_common_fields(chunk, data)
    set_content_fields(chunk, data.get("content"))

    set_if_field(chunk, "source_version", data.get("source_version") or 1)
    set_if_field(chunk, "archived", data.get("archived", 0))
    set_if_field(chunk, "disabled", data.get("disabled", 0))
    set_if_field(chunk, "enabled", data.get("enabled", 1))
    set_if_field(chunk, "is_active", data.get("is_active", 1))

    set_if_field(chunk, "character_count", len(clean_text(data.get("content"))))
    set_if_field(chunk, "diagnostics_status", data.get("diagnostics_status") or "Healthy")
    set_if_field(chunk, "diagnostics_message", data.get("diagnostics_message") or "Seed chunk passed diagnostics")
    set_if_field(chunk, "embedding_status", data.get("embedding_status") or "Completed")
    set_roles(chunk, data.get("allowed_roles") or [], data.get("denied_roles") or [])

    if chunk.meta.has_field("embedding"):
        chunk.embedding = data.get("embedding") or ""

    if chunk.is_new():
        chunk.insert(ignore_permissions=True)
    else:
        chunk.save(ignore_permissions=True)


def set_common_fields(doc, data):
    linked_policy = normalize_access_policy(data.get("access_policy"))

    for fieldname in [
        "tenant",
        "business_unit",
        "project",
        "scope_type",
        "context",
        "sub_context",
        "entity_type",
        "entity",
        "topic",
        "access_policy",
        "default_access_policy",
        "status",
        "enabled",
        "is_active",
        "disabled",
        "embedding_status",
        "source_version",
        "archived",
        "character_count",
        "diagnostics_status",
        "diagnostics_message",
    ]:
        if fieldname in ["access_policy", "default_access_policy"]:
            set_if_field(doc, fieldname, linked_policy)
        elif fieldname == "disabled":
            set_if_field(doc, fieldname, data.get("disabled", 0))
        elif fieldname == "embedding_status":
            set_if_field(doc, fieldname, data.get("embedding_status") or "Completed")
        else:
            set_if_field(doc, fieldname, data.get(fieldname))


def normalize_access_policy(value):
    if not value:
        return None

    existing = {d.name for d in frappe.get_all("Nexus Access Policy", fields=["name"])}

    candidates = {
        "public": ["PUBLIC", "Public", "public"],
        "role_based": ["Role Based", "ROLE BASED", "role_based"],
        "restricted": ["RESTRICTED", "Restricted", "restricted"],
    }

    for candidate in candidates.get(value, [value]):
        if candidate in existing:
            return candidate

    return candidates.get(value, [value])[0]


def set_content_fields(doc, content):
    cleaned = clean_text(content)

    for fieldname in ["content", "chunk_text", "text", "source_text"]:
        set_if_field(doc, fieldname, cleaned)


def set_roles(doc, allowed_roles, denied_roles):
    allowed_value = json.dumps(allowed_roles)
    denied_value = json.dumps(denied_roles)

    for fieldname in ["allowed_roles", "roles", "user_roles"]:
        set_if_field(doc, fieldname, allowed_value)

    for fieldname in ["denied_roles", "excluded_roles", "deny_roles"]:
        set_if_field(doc, fieldname, denied_value)

    for table_field in ["allowed_role_list", "allowed_roles_table", "role_permissions"]:
        if doc.meta.has_field(table_field):
            doc.set(table_field, [])
            for role in allowed_roles:
                row = doc.append(table_field, {})
                set_child_role(row, role)

    for table_field in ["denied_role_list", "denied_roles_table", "excluded_roles_table"]:
        if doc.meta.has_field(table_field):
            doc.set(table_field, [])
            for role in denied_roles:
                row = doc.append(table_field, {})
                set_child_role(row, role)


def set_child_role(row, role):
    for fieldname in ["role", "user_role", "allowed_role", "denied_role"]:
        if hasattr(row, fieldname):
            setattr(row, fieldname, role)
            return


def set_if_field(doc, fieldname, value):
    if value is None:
        return

    if doc.meta.has_field(fieldname):
        doc.set(fieldname, value)


def clean_text(value):
    return " ".join((value or "").split())