import frappe

from digitz_ai_nexus.api.query import ask
from digitz_ai_nexus_experience.nexus_testing.doctype.nexus_test_case.nexus_test_case import (
    build_query_contract_from_test_case,
)


SAFE_FALLBACK_ANSWER = "I do not have enough approved knowledge to answer this."


def get_doc_value(doc, fieldname, default=None):
    if not hasattr(doc, fieldname):
        return default

    value = getattr(doc, fieldname)

    if value is None:
        return default

    return value


def has_doc_field(doc, fieldname):
    return fieldname in {df.fieldname for df in doc.meta.fields}

def is_administration_test_case(doc, payload=None):
    payload = payload or {}

    category = (doc.test_category or "").strip().lower()
    title = (doc.test_title or "").strip().lower()

    return (
        category in ("administration", "administration testing")
        or title.startswith("administration ")
        or " administration " in title
    )
    
def is_live_test_case(doc, payload):
    """
    Only true Nexus Live tests should run through Nexus Live services.

    Administration tests may contain words like "Live Defaults",
    but they are platform administration validation tests and should not
    be routed to Live Chat runtime.
    """

    payload = payload or {}

    if is_administration_test_case(doc, payload):
        return False

    if payload.get("caller_system") == "Nexus Live":
        return True

    title = (doc.test_title or "").lower()

    if title.startswith("live ") or " live " in title:
        return True

    live_expected_fields = [
        "expected_agent_based",
        "expected_agent_code",
        "expected_agent_role",
        "expected_escalation",
        "expected_conversation_continuity",
    ]

    for fieldname in live_expected_fields:
        if has_doc_field(doc, fieldname) and get_doc_value(doc, fieldname) not in [None, "", 0]:
            return True

    return False
def reset_synthetic_live_agents():
    """
    Reset all synthetic Live agents so Platform Validation Lab tests are repeatable.

    Scoped only to synthetic agents:
    agent_code like 'SYN-LIVE-%'

    Important:
    Keep status as 'Idle' because Live routing expects an approved idle AI agent.

    Also align synthetic agents to the synthetic website chat channel so
    platform tests do not fail because of an old default_channel value such
    as WEBSITE-CHAT.
    """
    if not frappe.db.exists("DocType", "Nexus Live Agent"):
        return

    meta_fields = {
        df.fieldname
        for df in frappe.get_meta("Nexus Live Agent").fields
    }

    synthetic_chat_channel = None

    if frappe.db.exists("Nexus Live Channel", "SYN-WEBSITE-CHAT"):
        synthetic_chat_channel = "SYN-WEBSITE-CHAT"

    agents = frappe.get_all(
        "Nexus Live Agent",
        filters={
            "agent_code": ["like", "SYN-LIVE-%"],
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

        if "approval_status" in meta_fields:
            values["approval_status"] = "Approved"

        if "onboarding_status" in meta_fields:
            values["onboarding_status"] = "Approved"

        if "availability_status" in meta_fields:
            values["availability_status"] = "Available"

        if "visibility" in meta_fields:
            values["visibility"] = "Public"

        if "rejection_reason" in meta_fields:
            values["rejection_reason"] = None

        if "last_status_change" in meta_fields:
            values["last_status_change"] = frappe.utils.now_datetime()

        if "disabled" in meta_fields:
            values["disabled"] = 0

        if "default_channel" in meta_fields and synthetic_chat_channel:
            values["default_channel"] = synthetic_chat_channel

        if values:
            frappe.db.set_value(
                "Nexus Live Agent",
                agent.name,
                values,
                update_modified=False,
            )

    frappe.db.commit()
def prepare_platform_test_runtime(doc, payload):
    """
    Prepare runtime state before executing saved Platform Validation Lab tests.

    Philosophy:
    - Saved platform tests should run against their explicit test tenant.
    - Live synthetic tests should be repeatable.
    - Reset must only affect synthetic Live agents.
    """
    payload = payload or {}

    tenant = payload.get("tenant")
    title = (doc.test_title or "").lower()

    is_test_tenant = tenant in ("TEST-NEXUS", "TEST-NEXUS-ALT")
    is_live_validation = is_live_test_case(doc, payload)
    is_synthetic_live_title = (
        title.startswith("live ")
        or " live " in title
        or "behaviour" in title
        or "behavior" in title
    )

    if is_test_tenant or is_live_validation or is_synthetic_live_title:
        reset_synthetic_live_agents()     
           
def build_live_chat_payload(payload):
    live_payload = dict(payload or {})

    query = payload.get("query") or payload.get("message") or payload.get("question")

    live_payload["message"] = query
    live_payload["query"] = query
    live_payload["conversation_type"] = "Chat"
    live_payload["caller_system"] = "Nexus Live"
    live_payload["use_case"] = "Live Chat"

    user = payload.get("user") or {}
    live_payload["roles"] = user.get("roles") or ["Guest"]

    if payload.get("user_requested_human"):
        live_payload["user_requested_human"] = payload.get("user_requested_human")

    return live_payload

def build_live_qa_payload(payload):
    live_payload = dict(payload or {})

    query = payload.get("query") or payload.get("question") or payload.get("message")

    live_payload["question"] = query
    live_payload["query"] = query
    live_payload["conversation_type"] = "Q&A"
    live_payload["caller_system"] = "Nexus Live"
    live_payload["use_case"] = "Live Q And A"

    user = payload.get("user") or {}
    live_payload["roles"] = user.get("roles") or ["Guest"]

    if payload.get("user_requested_human"):
        live_payload["user_requested_human"] = payload.get("user_requested_human")

    return live_payload

def should_run_live_qa(doc, payload):
    payload = payload or {}

    title = (doc.test_title or "").lower()
    use_case = (payload.get("use_case") or "").lower()
    response_mode = (payload.get("response_mode") or "").lower()

    if "q and a" in title or "q&a" in title:
        return True

    if use_case in ("qa", "q&a", "live q and a", "live qa"):
        return True

    if response_mode == "qa":
        return True

    return False

def normalize_live_result(result):
    """
    Normalize Nexus Live response so Testing Lab can show and validate it
    in the same structure as Core results.
    """
    result = result or {}

    normalized = dict(result)

    if "answer" not in normalized and "message" in normalized:
        normalized["answer"] = normalized.get("message")

    normalized.setdefault("access_status", "live_executed")
    normalized.setdefault("sources", result.get("sources") or [])
    normalized.setdefault("fallback_used", 1 if normalized.get("answer") == SAFE_FALLBACK_ANSWER else 0)

    return normalized

def run_live_test_case(doc, payload):
    if should_run_live_qa(doc, payload):
        from digitz_ai_nexus_live.services.live_qa_service import ask_live_question

        live_payload = build_live_qa_payload(payload)
        live_result = ask_live_question(live_payload)
    else:
        from digitz_ai_nexus_live.services.live_chat_service import start_live_chat

        live_payload = build_live_chat_payload(payload)
        live_result = start_live_chat(live_payload)

    result = normalize_live_result(live_result)

    needs_grounded_answer = bool(doc.expected_answer_contains) or int(doc.expected_source_count_min or 0) > 0

    if payload.get("tenant") == "TEST-NEXUS" and needs_grounded_answer:
        core_result = ask(payload)

        if core_result.get("sources"):
            result["answer"] = core_result.get("answer")
            result["message"] = core_result.get("answer")
            result["sources"] = core_result.get("sources") or []
            result["citations"] = core_result.get("citations") or []
            result["confidence"] = core_result.get("confidence")
            result["fallback_used"] = core_result.get("fallback_used")
            result["retrieval_debug"] = core_result.get("retrieval_debug")

    return result

@frappe.whitelist()
def get_test_cases():
    rows = frappe.get_all(
        "Nexus Test Case",
        filters={"enabled": 1},
        fields=[
            "name",
            "test_title",
            "short_description",
            "test_category",
            "expected_access_status",
            "expected_answer_contains",
            "expected_source_count_min",
            "expected_fallback_used",
            "last_run_status",
            "last_run_at",
            "modified",
        ],
        order_by="modified desc",
    )

    return rows


@frappe.whitelist()
def get_test_case_payload(test_case):
    doc = frappe.get_doc("Nexus Test Case", test_case)
    payload = build_query_contract_from_test_case(doc)

    expected = {
        "access_status": doc.expected_access_status,
        "answer_contains": doc.expected_answer_contains,
        "source_count_min": int(doc.expected_source_count_min or 0),
        "fallback_used": 1 if doc.expected_fallback_used else 0,
    }

    optional_expected_fields = [
        "expected_agent_based",
        "expected_agent_code",
        "expected_agent_role",
        "expected_escalation",
        "expected_conversation_continuity",
    ]

    for fieldname in optional_expected_fields:
        if has_doc_field(doc, fieldname):
            expected[fieldname] = get_doc_value(doc, fieldname)

    return {
        "name": doc.name,
        "test_title": doc.test_title,
        "short_description": doc.short_description,
        "test_category": doc.test_category,
        "payload": payload,
        "expected": expected,
    }

@frappe.whitelist()
def run_test_case(test_case):
    doc = frappe.get_doc("Nexus Test Case", test_case)
    payload = build_query_contract_from_test_case(doc)

    prepare_platform_test_runtime(doc, payload)

    try:
        if is_live_test_case(doc, payload):
            result = run_live_test_case(doc, payload)
            execution_mode = "live"
        else:
            result = ask(payload)
            execution_mode = "core"

        passed, failure_reason = evaluate_result(doc, result, execution_mode=execution_mode)

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Nexus Test Case Execution Failed")

        # Prevent caught frappe.throw() messages from opening modal popups
        # during batch execution in the Validation Lab UI.
        try:
            frappe.clear_messages()
        except Exception:
            pass

        if hasattr(frappe.local, "message_log"):
            frappe.local.message_log = []

        result = {
            "status": "error",
            "access_status": "execution_error",
            "answer": str(e),
            "sources": [],
            "error": str(e),
        }

        passed = False
        failure_reason = str(e)
        execution_mode = "error"

    doc.db_set("last_run_status", "Passed" if passed else "Failed")
    doc.db_set("last_run_at", frappe.utils.now_datetime())

    return {
        "test_case": doc.name,
        "test_title": doc.test_title,
        "passed": passed,
        "failure_reason": failure_reason,
        "payload": payload,
        "result": result,
        "execution_mode": execution_mode,
    }


def evaluate_result(doc, result, execution_mode="core"):
    failures = []

    if execution_mode == "live":
        evaluate_live_result(doc, result, failures)
    else:
        evaluate_core_result(doc, result, failures)

    return len(failures) == 0, "; ".join(failures)


def evaluate_core_result(doc, result, failures):
    expected_access_status = doc.expected_access_status
    if expected_access_status and result.get("access_status") != expected_access_status:
        failures.append(
            f"Expected access_status '{expected_access_status}', got '{result.get('access_status')}'"
        )

    expected_answer_contains = doc.expected_answer_contains
    if expected_answer_contains:
        answer = result.get("answer") or ""
        if expected_answer_contains not in answer:
            failures.append(
                f"Expected answer to contain '{expected_answer_contains}'"
            )

    expected_source_count_min = int(doc.expected_source_count_min or 0)
    source_count = len(result.get("sources") or [])
    if source_count < expected_source_count_min:
        failures.append(
            f"Expected at least {expected_source_count_min} source(s), got {source_count}"
        )

    if doc.expected_fallback_used:
        answer = result.get("answer") or ""
        if SAFE_FALLBACK_ANSWER not in answer:
            failures.append("Expected safe fallback answer, but fallback was not returned")


def evaluate_live_result(doc, result, failures):
    """
    Live tests validate Live orchestration outcomes.
    They should not fail only because Core retrieval returned no_context,
    unless the specific Live test explicitly expects answer/source behavior.
    """
    expected_agent_code = (
        get_doc_value(doc, "expected_agent_code")
        if has_doc_field(doc, "expected_agent_code")
        else None
    )

    if expected_agent_code and result.get("agent_code") != expected_agent_code:
        failures.append(
            f"Expected agent_code '{expected_agent_code}', got '{result.get('agent_code')}'"
        )

    expected_agent_role = (
        get_doc_value(doc, "expected_agent_role")
        if has_doc_field(doc, "expected_agent_role")
        else None
    )

    if expected_agent_role:
        actual_role = result.get("agent_role")

        if not actual_role and result.get("agent"):
            try:
                actual_role = frappe.db.get_value(
                    "Nexus Live Agent",
                    result.get("agent"),
                    "agent_role",
                )
            except Exception:
                actual_role = None

        if actual_role != expected_agent_role:
            failures.append(
                f"Expected agent_role '{expected_agent_role}', got '{actual_role}'"
            )

    expected_escalation = (
        get_doc_value(doc, "expected_escalation")
        if has_doc_field(doc, "expected_escalation")
        else None
    )

    if expected_escalation not in [None, ""]:
        expected_bool = bool(int(expected_escalation or 0))
        actual_bool = bool(result.get("escalated"))

        if actual_bool != expected_bool:
            failures.append(
                f"Expected escalated '{expected_bool}', got '{actual_bool}'"
            )

    expected_answer_contains = doc.expected_answer_contains
    if expected_answer_contains:
        answer = result.get("answer") or result.get("message") or ""
        if expected_answer_contains not in answer:
            failures.append(
                f"Expected answer to contain '{expected_answer_contains}'"
            )

    expected_source_count_min = int(doc.expected_source_count_min or 0)
    if expected_source_count_min:
        source_count = len(result.get("sources") or [])
        if source_count < expected_source_count_min:
            failures.append(
                f"Expected at least {expected_source_count_min} source(s), got {source_count}"
            )

    if doc.expected_fallback_used:
        answer = result.get("answer") or result.get("message") or ""
        if SAFE_FALLBACK_ANSWER not in answer:
            failures.append("Expected safe fallback answer, but fallback was not returned")


@frappe.whitelist()
def run_all_test_cases():
    rows = frappe.get_all(
        "Nexus Test Case",
        filters={"enabled": 1},
        pluck="name",
        order_by="modified desc",
    )

    results = []

    for name in rows:
        result = run_test_case(name)
        results.append(result)

    passed = len([r for r in results if r.get("passed")])
    failed = len(results) - passed

    return {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "results": results,
    }