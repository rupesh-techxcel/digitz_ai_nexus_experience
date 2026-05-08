# Copyright (c) 2026, Techxcel Technologies and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document


class NexusTestCase(Document):
    def validate(self):
        self.query_contract_json = json.dumps(
            build_query_contract_from_test_case(self),
            indent=2,
            ensure_ascii=False,
        )


def parse_roles(value):
    if not value:
        return ["Guest"]

    roles = []

    for role in str(value).split(","):
        role = role.strip()
        if role:
            roles.append(role)

    return roles or ["Guest"]


def build_query_contract_from_test_case(doc):
    payload = {
        "tenant": doc.tenant,
        "business_unit": doc.business_unit,
        "context": doc.context,
        "sub_context": doc.sub_context,
        "entity_type": doc.entity_type,
        "entity": doc.entity,
        "topic": doc.topic,
        "query": doc.query,
        "top_k": int(doc.top_k or 5),
        "use_case": doc.use_case or "qa",
        "caller_system": "Nexus Knowledge Test",
        "user": {
            "roles": parse_roles(doc.user_roles),
        },
    }

    if doc.project:
        payload["project"] = doc.project

    if doc.project_scope_mode:
        payload["project_scope_mode"] = doc.project_scope_mode

    if doc.user_designation:
        payload["user"]["designation"] = doc.user_designation

    if doc.user_id:
        payload["user"]["user_id"] = doc.user_id

    return payload