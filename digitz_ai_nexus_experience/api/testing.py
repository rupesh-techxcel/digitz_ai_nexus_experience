import json
import frappe

from digitz_ai_nexus.api.query import ask
from digitz_ai_nexus_experience.nexus_testing.doctype.nexus_test_case.nexus_test_case import (
    build_query_contract_from_test_case,
)


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

    return {
        "name": doc.name,
        "test_title": doc.test_title,
        "short_description": doc.short_description,
        "test_category": doc.test_category,
        "payload": payload,
        "expected": {
            "access_status": doc.expected_access_status,
            "answer_contains": doc.expected_answer_contains,
            "source_count_min": int(doc.expected_source_count_min or 0),
            "fallback_used": 1 if doc.expected_fallback_used else 0,
        },
    }


@frappe.whitelist()
def run_test_case(test_case):
    doc = frappe.get_doc("Nexus Test Case", test_case)
    payload = build_query_contract_from_test_case(doc)

    result = ask(payload)

    passed, failure_reason = evaluate_result(doc, result)

    doc.db_set("last_run_status", "Passed" if passed else "Failed")
    doc.db_set("last_run_at", frappe.utils.now_datetime())

    return {
        "test_case": doc.name,
        "test_title":doc.test_title,
        "passed": passed,
        "failure_reason": failure_reason,
        "payload": payload,
        "result": result,
    }


def evaluate_result(doc, result):
    failures = []

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
        if "I do not have enough approved knowledge to answer this." not in answer:
            failures.append("Expected safe fallback answer, but fallback was not returned")

    return len(failures) == 0, "; ".join(failures)

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