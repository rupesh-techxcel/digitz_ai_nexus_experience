import importlib
import frappe


SYNTHETIC_TENANT = "TEST-NEXUS"
SYNTHETIC_ALT_TENANT = "TEST-NEXUS-ALT"
SYNTHETIC_BUSINESS_UNIT = "Nexus Synthetic BU"
SYNTHETIC_OTHER_BUSINESS_UNIT = "Other Synthetic BU"

SYNTHETIC_CONTEXTS = [
    "Nexus Live",
    "Synthetic ERP",
    "Nexus Knowledge",
]

SYNTHETIC_ENTITIES = [
    "Nexus Live Synthetic Validation",
    "Nexus Test Orbit",
    "Quality Panel",
    "Text Extraction",
    "Knowledge Unit",
    "Generated Chunks",
    "Embedding Status",
    "Source Testing",
    "Reprocess Governance",
    "Chunk Observatory",
    "Retrieval Readiness",
    "Archived Chunks",
]

SYNTHETIC_PROJECTS = [
    "Alpha Orbit Project",
    "Beta Orbit Project",
]

SYNTHETIC_CHANNEL_CODES = [
    "SYN-WEBSITE-QA",
    "SYN-WEBSITE-CHAT",
    "website-chat",
]

SYNTHETIC_AGENT_CODES = [
    "SYN-LIVE-PUBLIC-AI",
    "SYN-LIVE-SALES-AI",
    "SYN-LIVE-SUPPORT-AI",
    "LIVE-TEST-SALES-AI",
    "LIVE-TEST-SUPPORT-AI",
    "LIVE-TEST-PUBLIC-AI",
    "LIVE-TEST-NO-ESCALATION-AI",
    "LIVE-TEST-LEGACY-PROFILE-AI",
]

SYNTHETIC_QUEUE_CODES = [
    "SYN-SALES-QUEUE",
    "SYN-SUPPORT-QUEUE",
    "LIVE-SALES-QUEUE",
    "LIVE-SUPPORT-QUEUE",
    "LIVE-PUBLIC-QUEUE",
]

SYNTHETIC_BEHAVIOUR_CODES = [
    "LIVE-BEHAVIOUR-SALES",
    "LIVE-BEHAVIOUR-SUPPORT",
    "LIVE-BEHAVIOUR-PUBLIC",
    "LIVE-BEHAVIOUR-NO-ESCALATION",
]

SYNTHETIC_ESCALATION_RULES = [
    "Synthetic Public AI Escalation",
    "Synthetic Sales AI Escalation",
    "Synthetic Support AI Escalation",
    "Live Behaviour Sales Escalation",
    "Live Behaviour Support Escalation",
    "Live Behaviour Public Escalation",
]

SYNTHETIC_ACCESS_POLICIES = [
    "Synthetic Public Guest Access",
]

SYNTHETIC_KNOWLEDGE_NAME_PREFIXES = [
    "TEST-NEXUS-SYNTHETIC-",
    "TEST-NEXUS-INGESTED-",
    "TEST-NEXUS-KNOWLEDGE-SOURCE-",
    "TEST-NEXUS-EXTRACTED-",
    "TEST-NEXUS-GENERATED-",
    "TEST-NEXUS-EMBEDDING-",
    "TEST-NEXUS-QUALITY-",
    "TEST-NEXUS-TEST-THIS-SOURCE",
    "TEST-NEXUS-REPROCESS-",
    "TEST-NEXUS-CHUNK-",
    "TEST-NEXUS-RETRIEVAL-",
    "TEST-NEXUS-ARCHIVED-",
]

TEST_CASE_DOCTYPES = {
    "Nexus Test Case",
    "Nexus Knowledge Test Case",
    "Nexus Administration Test Case",
    "Nexus Live Behaviour Test Case",
    "Nexus Tenant Runtime Test Case",
}

# Important:
# Live Synthetic / Live Behaviour must run before Administration and Tenant Runtime.
# Administration and Tenant Runtime reference channels / agents created by the Live seed files.
DATA_SEED_MODULES = [
    {
        "key": "live_synthetic",
        "label": "Live Synthetic Test Data",
        "module": "digitz_ai_nexus_experience.patches.v0_0_2.seed_nexus_live_synthetic_test_data",
    },
    {
        "key": "live_behaviour",
        "label": "Live Behaviour Test Data",
        "module": "digitz_ai_nexus_experience.patches.v0_0_2.seed_nexus_live_behaviour_test_data",
    },
    {
        "key": "administration",
        "label": "Administration Test Data",
        "module": "digitz_ai_nexus_experience.patches.v0_0_2.seed_nexus_administration_test_data",
    },
    {
        "key": "tenant_runtime",
        "label": "Tenant Runtime Test Data",
        "module": "digitz_ai_nexus_experience.patches.v0_0_2.seed_nexus_tenant_runtime_test_data",
    },
    {
        "key": "synthetic_knowledge",
        "label": "Synthetic Test Knowledge",
        "module": "digitz_ai_nexus_experience.patches.v0_0_2.seed_nexus_synthetic_test_knowledge",
    },
]


# ---------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------

def _doctype_exists(doctype):
    return frappe.db.exists("DocType", doctype)


def _field_exists(doctype, fieldname):
    if not _doctype_exists(doctype):
        return False

    return frappe.get_meta(doctype).has_field(fieldname)


def _safe_commit():
    frappe.db.commit()


def _safe_rollback():
    frappe.db.rollback()


def _get_existing_seed_modules():
    result = []

    for item in DATA_SEED_MODULES:
        try:
            importlib.import_module(item["module"])
            result.append({
                "key": item["key"],
                "label": item["label"],
                "module": item["module"],
                "available": 1,
                "error": None,
            })
        except Exception as exc:
            result.append({
                "key": item["key"],
                "label": item["label"],
                "module": item["module"],
                "available": 0,
                "error": str(exc),
            })

    return result


def _delete_doc(doctype, name, deleted, skipped):
    if not doctype or not name:
        return

    if not _doctype_exists(doctype):
        return

    if doctype in TEST_CASE_DOCTYPES:
        skipped.append({
            "doctype": doctype,
            "name": name,
            "reason": "Test case definition records are intentionally preserved.",
        })
        return

    try:
        frappe.delete_doc(
            doctype,
            name,
            ignore_permissions=True,
            force=True,
        )
        deleted.append({
            "doctype": doctype,
            "name": name,
        })
    except Exception as exc:
        skipped.append({
            "doctype": doctype,
            "name": name,
            "reason": str(exc),
        })


def _get_all_names(doctype, filters=None, or_filters=None, limit=1000):
    if not _doctype_exists(doctype):
        return []

    try:
        rows = frappe.get_all(
            doctype,
            filters=filters or {},
            or_filters=or_filters,
            fields=["name"],
            limit_page_length=limit,
        )
        return [row.name for row in rows]
    except Exception:
        return []


def _delete_names(doctype, names, deleted, skipped):
    if doctype in TEST_CASE_DOCTYPES:
        return

    for name in names or []:
        _delete_doc(doctype, name, deleted, skipped)


def _count_names(doctype, filters=None, or_filters=None):
    if not _doctype_exists(doctype):
        return 0

    try:
        return len(_get_all_names(doctype, filters=filters, or_filters=or_filters, limit=5000))
    except Exception:
        return 0


def _field_filters(doctype, candidate_filters):
    """
    Keep only filters whose fields exist in the target DocType.
    """
    filters = {}

    for fieldname, value in (candidate_filters or {}).items():
        if _field_exists(doctype, fieldname):
            filters[fieldname] = value

    return filters


def _build_context_or_filters(doctype):
    or_filters = []

    if _field_exists(doctype, "tenant"):
        or_filters.append([doctype, "tenant", "in", [SYNTHETIC_TENANT, SYNTHETIC_ALT_TENANT]])

    if _field_exists(doctype, "business_unit"):
        or_filters.append([doctype, "business_unit", "in", [SYNTHETIC_BUSINESS_UNIT, SYNTHETIC_OTHER_BUSINESS_UNIT]])

    if _field_exists(doctype, "context"):
        or_filters.append([doctype, "context", "in", SYNTHETIC_CONTEXTS])

    if _field_exists(doctype, "entity"):
        or_filters.append([doctype, "entity", "in", SYNTHETIC_ENTITIES])

    return or_filters or None


def _get_knowledge_doc_names(doctype):
    if not _doctype_exists(doctype):
        return []

    names = set()

    for prefix in SYNTHETIC_KNOWLEDGE_NAME_PREFIXES:
        names.update(_get_all_names(
            doctype,
            filters={
                "name": ["like", f"{prefix}%"],
            },
            limit=5000,
        ))

    filters = _field_filters(
        doctype,
        {
            "tenant": SYNTHETIC_TENANT,
            "business_unit": SYNTHETIC_BUSINESS_UNIT,
        },
    )

    if filters:
        names.update(_get_all_names(
            doctype,
            filters=filters,
            or_filters=_build_context_or_filters(doctype),
            limit=5000,
        ))

    return sorted(names)


def _get_code_based_names(doctype, fieldname, values):
    if not _doctype_exists(doctype) or not _field_exists(doctype, fieldname):
        return []

    return _get_all_names(
        doctype,
        filters={
            fieldname: ["in", values],
        },
        limit=5000,
    )


def _get_like_based_names(doctype, fieldname, patterns):
    if not _doctype_exists(doctype) or not _field_exists(doctype, fieldname):
        return []

    names = set()

    for pattern in patterns:
        names.update(_get_all_names(
            doctype,
            filters={
                fieldname: ["like", pattern],
            },
            limit=5000,
        ))

    return sorted(names)


# ---------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------

@frappe.whitelist()
def get_synthetic_dataset_status():
    """
    Returns managed Nexus test data status for Platform Testing Lab.
    Does not mutate data.
    """

    seed_modules = _get_existing_seed_modules()

    counts = {
        "seed_modules_available": len([m for m in seed_modules if m.get("available")]),
        "seed_modules_total": len(seed_modules),

        "knowledge_units": len(_get_knowledge_doc_names("Nexus Knowledge Unit")),
        "knowledge_chunks": len(_get_knowledge_doc_names("Nexus Knowledge Chunk")),
        "knowledge_sources": len(_get_knowledge_doc_names("Nexus Knowledge Source")),

        "live_agents": len(
            set(_get_code_based_names("Nexus Live Agent", "agent_code", SYNTHETIC_AGENT_CODES))
            | set(_get_like_based_names("Nexus Live Agent", "agent_code", ["SYN-LIVE-%", "LIVE-TEST-%", "%TEST%"]))
        ),

        "live_channels": len(
            set(_get_code_based_names("Nexus Live Channel", "channel_code", SYNTHETIC_CHANNEL_CODES))
            | set(_get_like_based_names("Nexus Live Channel", "channel_code", ["SYN-%", "LIVE-TEST-%", "%TEST%"]))
        ),

        "agent_queues": len(
            set(_get_code_based_names("Nexus Agent Queue", "queue_code", SYNTHETIC_QUEUE_CODES))
            | set(_get_like_based_names("Nexus Agent Queue", "queue_code", ["SYN-%", "LIVE-TEST-%", "%TEST%"]))
        ),

        "ai_behaviours": len(
            set(_get_code_based_names("Nexus AI Behaviour", "behaviour_code", SYNTHETIC_BEHAVIOUR_CODES))
            | set(_get_like_based_names("Nexus AI Behaviour", "behaviour_code", ["SYN-%", "LIVE-BEHAVIOUR-%", "%TEST%"]))
        ),

        "ai_profiles": len(_get_code_based_names("Nexus AI Agent Profile", "agent", SYNTHETIC_AGENT_CODES)),
        "agent_onboarding": len(_get_code_based_names("Nexus Agent Onboarding", "agent", SYNTHETIC_AGENT_CODES)),

        "escalation_rules": len(_get_code_based_names("Nexus Escalation Rule", "rule_name", SYNTHETIC_ESCALATION_RULES)),

        "projects": len(
            set(_get_code_based_names("Nexus Project", "name", SYNTHETIC_PROJECTS))
            | set(_get_like_based_names("Nexus Project", "name", ["%Test%", "%TEST%", "%Synthetic%", "%SYN-%"]))
        ),

        "business_units": len(_get_code_based_names("Nexus Business Unit", "name", [
            SYNTHETIC_BUSINESS_UNIT,
            SYNTHETIC_OTHER_BUSINESS_UNIT,
        ])),
        "tenants": len(_get_code_based_names("Nexus Tenant", "name", [
            SYNTHETIC_TENANT,
            SYNTHETIC_ALT_TENANT,
        ])),

        "query_logs": _count_query_logs(),
        "test_runs": _count_test_runs(),
    }

    return {
        "success": True,
        "seed_modules": seed_modules,
        "counts": counts,
    }


# ---------------------------------------------------------------------
# Seed
# ---------------------------------------------------------------------

@frappe.whitelist()
def seed_synthetic_dataset():
    """
    Calls the existing data seed files on demand.
    Test case seed files are intentionally excluded.

    Seed order is intentional:
    1. Live Synthetic creates SYN-WEBSITE-QA / SYN-WEBSITE-CHAT and synthetic Live records.
    2. Live Behaviour creates LIVE-TEST-* agents/behaviours/runtime records.
    3. Administration config can then safely set default channels.
    4. Tenant Runtime config can then safely set runtime defaults.
    5. Synthetic Knowledge can then be added against the configured tenant context.
    """

    if not frappe.has_permission("System Settings", "write"):
        frappe.throw("Not permitted to seed Nexus test data.", frappe.PermissionError)

    results = []

    try:
        for item in DATA_SEED_MODULES:
            module_path = item["module"]

            try:
                module = importlib.import_module(module_path)

                if not hasattr(module, "execute"):
                    results.append({
                        "label": item["label"],
                        "module": module_path,
                        "success": False,
                        "message": "execute() not found.",
                    })
                    continue

                module.execute()

                results.append({
                    "label": item["label"],
                    "module": module_path,
                    "success": True,
                    "message": "Seed completed.",
                })

            except Exception as exc:
                frappe.log_error(
                    title=f"Seed failed: {item['label']}",
                    message=frappe.get_traceback(),
                )

                results.append({
                    "label": item["label"],
                    "module": module_path,
                    "success": False,
                    "message": str(exc),
                })

        failed = [row for row in results if not row.get("success")]

        _safe_commit()

        return {
            "success": False if failed else True,
            "message": (
                "Nexus test data seed completed with failures."
                if failed
                else "Nexus test data seed completed successfully."
            ),
            "failed_count": len(failed),
            "results": results,
            "status": get_synthetic_dataset_status(),
        }

    except Exception:
        _safe_rollback()
        frappe.log_error(
            title="Nexus Test Data Seed Failed",
            message=frappe.get_traceback(),
        )
        raise


@frappe.whitelist()
def seed_test_data():
    """
    UI-facing alias.

    Seeds all configured Nexus test data from existing data seed files.
    Test case definition seed files are intentionally not called here.
    """
    return seed_synthetic_dataset()


# ---------------------------------------------------------------------
# Clear data
# ---------------------------------------------------------------------

@frappe.whitelist()
def clear_synthetic_dataset():
    """
    Clears managed Nexus test/demo/runtime/generated data.

    Important:
    - This does NOT clear test case definition records.
    - It clears seeded synthetic data and broader test/demo runtime records.
    - The required seeded dataset can be recreated using seed_synthetic_dataset().
    """

    if not frappe.has_permission("System Settings", "write"):
        frappe.throw("Not permitted to clear Nexus test data.", frappe.PermissionError)

    deleted = []
    skipped = []

    try:
        # -----------------------------------------------------------------
        # Execution and generated output first
        # -----------------------------------------------------------------
        _clear_execution_logs_internal(deleted, skipped)

        # -----------------------------------------------------------------
        # Knowledge chunks before units/sources
        # -----------------------------------------------------------------
        _delete_names(
            "Nexus Knowledge Chunk",
            _get_knowledge_doc_names("Nexus Knowledge Chunk"),
            deleted,
            skipped,
        )

        _delete_names(
            "Nexus Knowledge Unit",
            _get_knowledge_doc_names("Nexus Knowledge Unit"),
            deleted,
            skipped,
        )

        _delete_names(
            "Nexus Knowledge Source",
            _get_knowledge_doc_names("Nexus Knowledge Source"),
            deleted,
            skipped,
        )

        # -----------------------------------------------------------------
        # Live / agent runtime data
        # -----------------------------------------------------------------
        _delete_names(
            "Nexus Escalation Rule",
            _get_code_based_names("Nexus Escalation Rule", "rule_name", SYNTHETIC_ESCALATION_RULES),
            deleted,
            skipped,
        )

        _delete_names(
            "Nexus Agent Onboarding",
            _get_code_based_names("Nexus Agent Onboarding", "agent", SYNTHETIC_AGENT_CODES),
            deleted,
            skipped,
        )

        _delete_names(
            "Nexus AI Agent Profile",
            _get_code_based_names("Nexus AI Agent Profile", "agent", SYNTHETIC_AGENT_CODES),
            deleted,
            skipped,
        )

        live_agent_names = sorted(
            set(_get_code_based_names("Nexus Live Agent", "agent_code", SYNTHETIC_AGENT_CODES))
            | set(_get_like_based_names("Nexus Live Agent", "agent_code", ["SYN-LIVE-%", "LIVE-TEST-%", "%TEST%"]))
        )
        _delete_names("Nexus Live Agent", live_agent_names, deleted, skipped)

        queue_names = sorted(
            set(_get_code_based_names("Nexus Agent Queue", "queue_code", SYNTHETIC_QUEUE_CODES))
            | set(_get_like_based_names("Nexus Agent Queue", "queue_code", ["SYN-%", "LIVE-TEST-%", "%TEST%"]))
        )
        _delete_names("Nexus Agent Queue", queue_names, deleted, skipped)

        channel_names = sorted(
            set(_get_code_based_names("Nexus Live Channel", "channel_code", SYNTHETIC_CHANNEL_CODES))
            | set(_get_like_based_names("Nexus Live Channel", "channel_code", ["SYN-%", "LIVE-TEST-%", "%TEST%"]))
        )
        _delete_names("Nexus Live Channel", channel_names, deleted, skipped)

        behaviour_names = sorted(
            set(_get_code_based_names("Nexus AI Behaviour", "behaviour_code", SYNTHETIC_BEHAVIOUR_CODES))
            | set(_get_like_based_names("Nexus AI Behaviour", "behaviour_code", ["SYN-%", "LIVE-BEHAVIOUR-%", "%TEST%"]))
        )
        _delete_names("Nexus AI Behaviour", behaviour_names, deleted, skipped)

        _delete_names(
            "Nexus Access Policy",
            _get_code_based_names("Nexus Access Policy", "name", SYNTHETIC_ACCESS_POLICIES),
            deleted,
            skipped,
        )

        # -----------------------------------------------------------------
        # User context / administration runtime context
        # -----------------------------------------------------------------
        if _doctype_exists("Nexus User Context"):
            filters = _field_filters(
                "Nexus User Context",
                {
                    "tenant": SYNTHETIC_TENANT,
                },
            )
            if filters:
                _delete_names(
                    "Nexus User Context",
                    _get_all_names("Nexus User Context", filters=filters, limit=5000),
                    deleted,
                    skipped,
                )

        # -----------------------------------------------------------------
        # Projects before BU/Tenant
        # -----------------------------------------------------------------
        project_names = sorted(
            set(_get_code_based_names("Nexus Project", "name", SYNTHETIC_PROJECTS))
            | set(_get_like_based_names("Nexus Project", "name", ["%Test%", "%TEST%", "%Synthetic%", "%SYN-%"]))
        )
        _delete_names("Nexus Project", project_names, deleted, skipped)

        # -----------------------------------------------------------------
        # Ecosystem records for test tenants
        # -----------------------------------------------------------------
        if _doctype_exists("Nexus Ecosystem"):
            ecosystem_names = set()

            for tenant in [SYNTHETIC_TENANT, SYNTHETIC_ALT_TENANT]:
                filters = _field_filters(
                    "Nexus Ecosystem",
                    {
                        "tenant": tenant,
                    },
                )
                if filters:
                    ecosystem_names.update(_get_all_names("Nexus Ecosystem", filters=filters, limit=5000))

            _delete_names("Nexus Ecosystem", sorted(ecosystem_names), deleted, skipped)

        # -----------------------------------------------------------------
        # Broader test/demo/runtime records by known context markers.
        # Test case doctypes are intentionally excluded.
        # -----------------------------------------------------------------
        _clear_context_marked_test_records(deleted, skipped)

        # -----------------------------------------------------------------
        # Tenant / Business Unit attempted last.
        # If test case definitions link to them, they may be skipped.
        # -----------------------------------------------------------------
        _delete_names(
            "Nexus Business Unit",
            _get_code_based_names("Nexus Business Unit", "name", [
                SYNTHETIC_BUSINESS_UNIT,
                SYNTHETIC_OTHER_BUSINESS_UNIT,
            ]),
            deleted,
            skipped,
        )

        _delete_names(
            "Nexus Tenant",
            _get_code_based_names("Nexus Tenant", "name", [
                SYNTHETIC_TENANT,
                SYNTHETIC_ALT_TENANT,
            ]),
            deleted,
            skipped,
        )

        _safe_commit()

        return {
            "success": True,
            "message": "All managed Nexus test data cleared. Test case definitions were kept.",
            "deleted_count": len(deleted),
            "skipped_count": len(skipped),
            "deleted": deleted,
            "skipped": skipped,
            "status": get_synthetic_dataset_status(),
        }

    except Exception:
        _safe_rollback()
        frappe.log_error(
            title="Nexus Test Data Clear Failed",
            message=frappe.get_traceback(),
        )
        raise


@frappe.whitelist()
def clear_all_test_data():
    """
    UI-facing alias.

    Clears all managed Nexus test/demo/runtime/generated data that belongs
    to the synthetic/test dataset scope.

    Important:
    - Does NOT clear test case definition records.
    - Keeps validation suite records intact.
    - Cleared seeded data can be recreated using seed_test_data().
    """
    return clear_synthetic_dataset()


@frappe.whitelist()
def reset_synthetic_dataset():
    """
    Clears managed Nexus test data first, then calls all data seed files again.
    Test case definition records are not cleared.
    """

    clear_result = clear_synthetic_dataset()
    seed_result = seed_synthetic_dataset()

    return {
        "success": bool(seed_result.get("success")),
        "message": (
            "Nexus test data reset completed successfully."
            if seed_result.get("success")
            else "Nexus test data reset completed with seed failures."
        ),
        "clear_result": clear_result,
        "seed_result": seed_result,
        "status": get_synthetic_dataset_status(),
    }


@frappe.whitelist()
def reset_test_data():
    """
    UI-facing alias.

    Clears all managed test data first, then seeds it again.
    Test case definition records are not cleared.
    """
    return reset_synthetic_dataset()


# ---------------------------------------------------------------------
# Execution logs
# ---------------------------------------------------------------------

@frappe.whitelist()
def clear_execution_logs():
    """
    Clears test execution output/logs only.
    Does not clear seed data or test case definitions.
    """

    if not frappe.has_permission("System Settings", "write"):
        frappe.throw("Not permitted to clear synthetic execution logs.", frappe.PermissionError)

    deleted = []
    skipped = []

    try:
        _clear_execution_logs_internal(deleted, skipped)
        _safe_commit()

        return {
            "success": True,
            "message": "Synthetic execution logs cleared.",
            "deleted_count": len(deleted),
            "skipped_count": len(skipped),
            "deleted": deleted,
            "skipped": skipped,
            "status": get_synthetic_dataset_status(),
        }

    except Exception:
        _safe_rollback()
        frappe.log_error(
            title="Synthetic Execution Log Clear Failed",
            message=frappe.get_traceback(),
        )
        raise


def _clear_context_marked_test_records(deleted, skipped):
    """
    Clears broader Nexus test/demo/runtime records using safe markers.

    Does NOT clear test case doctypes.
    """

    candidate_doctypes = [
        "Nexus Conversation",
        "Nexus Conversation Message",
        "Nexus Live Conversation",
        "Nexus Live Message",
        "Nexus Live Session",
        "Nexus Runtime Context",
        "Nexus Runtime Event",
        "Nexus Diagnostics",
        "Nexus Validation Result",
        "Nexus Knowledge Gap",
        "Nexus Retrieval Diagnostic",
        "Nexus Source Diagnostic",
        "Nexus Conversation Continuity",
        "Nexus Live Escalation",
        "Nexus Live Routing Log",
        "Nexus Agent Assignment",
        "Nexus Queue Assignment",
    ]

    for doctype in candidate_doctypes:
        if not _doctype_exists(doctype):
            continue

        if doctype in TEST_CASE_DOCTYPES:
            continue

        names = set()

        context_filters = _field_filters(
            doctype,
            {
                "tenant": SYNTHETIC_TENANT,
                "business_unit": SYNTHETIC_BUSINESS_UNIT,
            },
        )

        if context_filters:
            names.update(_get_all_names(
                doctype,
                filters=context_filters,
                limit=5000,
            ))

        alt_context_filters = _field_filters(
            doctype,
            {
                "tenant": SYNTHETIC_ALT_TENANT,
            },
        )

        if alt_context_filters:
            names.update(_get_all_names(
                doctype,
                filters=alt_context_filters,
                limit=5000,
            ))

        if _field_exists(doctype, "caller_system"):
            names.update(_get_all_names(
                doctype,
                filters={
                    "caller_system": ["in", [
                        "Nexus Knowledge Test",
                        "Nexus Intelligence Validation Lab",
                        "Nexus Platform Testing Lab",
                    ]]
                },
                limit=5000,
            ))

        if _field_exists(doctype, "context"):
            names.update(_get_all_names(
                doctype,
                filters={
                    "context": ["in", SYNTHETIC_CONTEXTS],
                },
                limit=5000,
            ))

        if _field_exists(doctype, "entity"):
            names.update(_get_all_names(
                doctype,
                filters={
                    "entity": ["in", SYNTHETIC_ENTITIES],
                },
                limit=5000,
            ))

        for pattern in ["%TEST-NEXUS%", "%Synthetic%", "%SYN-%", "%LIVE-TEST%", "%Nexus Test%"]:
            names.update(_get_like_based_names(doctype, "name", [pattern]))

        _delete_names(doctype, sorted(names), deleted, skipped)


def _clear_execution_logs_internal(deleted, skipped):
    # Query logs
    if _doctype_exists("Nexus Query Log"):
        filters = _field_filters(
            "Nexus Query Log",
            {
                "tenant": SYNTHETIC_TENANT,
            },
        )

        names = []

        if filters:
            names.extend(_get_all_names("Nexus Query Log", filters=filters, limit=5000))

        alt_filters = _field_filters(
            "Nexus Query Log",
            {
                "tenant": SYNTHETIC_ALT_TENANT,
            },
        )

        if alt_filters:
            names.extend(_get_all_names("Nexus Query Log", filters=alt_filters, limit=5000))

        if _field_exists("Nexus Query Log", "caller_system"):
            names.extend(_get_all_names(
                "Nexus Query Log",
                filters={
                    "caller_system": ["in", [
                        "Nexus Knowledge Test",
                        "Nexus Intelligence Validation Lab",
                        "Nexus Platform Testing Lab",
                    ]]
                },
                limit=5000,
            ))

            names.extend(_get_all_names(
                "Nexus Query Log",
                filters={
                    "caller_system": ["like", "%Nexus%Test%"],
                },
                limit=5000,
            ))

        _delete_names("Nexus Query Log", sorted(set(names)), deleted, skipped)

    # Test run doctypes vary during development, so check possible names.
    for doctype in [
        "Nexus Knowledge Test Run",
        "Nexus Test Run",
        "Nexus Platform Test Run",
        "Nexus Validation Test Run",
    ]:
        if not _doctype_exists(doctype):
            continue

        names = []

        if _field_exists(doctype, "tenant"):
            names.extend(_get_all_names(
                doctype,
                filters={
                    "tenant": ["in", [SYNTHETIC_TENANT, SYNTHETIC_ALT_TENANT]],
                },
                limit=5000,
            ))

        if _field_exists(doctype, "test_suite"):
            names.extend(_get_all_names(
                doctype,
                filters={
                    "test_suite": ["like", "%Synthetic%"],
                },
                limit=5000,
            ))

            names.extend(_get_all_names(
                doctype,
                filters={
                    "test_suite": ["like", "%Test%"],
                },
                limit=5000,
            ))

        if _field_exists(doctype, "caller_system"):
            names.extend(_get_all_names(
                doctype,
                filters={
                    "caller_system": ["in", [
                        "Nexus Knowledge Test",
                        "Nexus Intelligence Validation Lab",
                        "Nexus Platform Testing Lab",
                    ]]
                },
                limit=5000,
            ))

        _delete_names(doctype, sorted(set(names)), deleted, skipped)


def _count_query_logs():
    if not _doctype_exists("Nexus Query Log"):
        return 0

    total = 0

    filters = _field_filters(
        "Nexus Query Log",
        {
            "tenant": SYNTHETIC_TENANT,
        },
    )

    if filters:
        total += frappe.db.count("Nexus Query Log", filters)

    alt_filters = _field_filters(
        "Nexus Query Log",
        {
            "tenant": SYNTHETIC_ALT_TENANT,
        },
    )

    if alt_filters:
        total += frappe.db.count("Nexus Query Log", alt_filters)

    return total


def _count_test_runs():
    total = 0

    for doctype in [
        "Nexus Knowledge Test Run",
        "Nexus Test Run",
        "Nexus Platform Test Run",
        "Nexus Validation Test Run",
    ]:
        if not _doctype_exists(doctype):
            continue

        if _field_exists(doctype, "tenant"):
            total += frappe.db.count(doctype, {"tenant": ["in", [SYNTHETIC_TENANT, SYNTHETIC_ALT_TENANT]]})

    return total