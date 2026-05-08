let nexus_session_run_history = [];
let nexus_session_run_counter = 0;

frappe.pages['nexus-knowledge-test'].on_page_load = function(wrapper) {
    nexus_session_run_history = [];
    nexus_session_run_counter = 0;

    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Knowledge Testing Lab',
        single_column: true
    });

    $(page.body).html(`
        <div class="nexus-lab-wrap">

            <div class="nexus-lab-hero">
                <div>
                    <div class="nexus-lab-badge">DIGITZ AI Nexus</div>
                    <h2>Knowledge Testing Lab</h2>
                    <p>
                        Validate AI answers using controlled enterprise knowledge, access policies,
                        Business Units, Projects, response behavior modes, and retrieval intelligence.
                    </p>
                </div>
            </div>

            <div class="nexus-tab-bar">
                <button class="nexus-tab-btn active" data-tab="workspace">
                    Testing Workspace
                </button>
                <button class="nexus-tab-btn" data-tab="retrieval">
                    Retrieval Observatory
                </button>
                <button class="nexus-tab-btn" data-tab="history">
                    Execution History
                    <span id="nexus_history_count" class="nexus-tab-count">0</span>
                </button>
            </div>

            <div id="nexus_workspace_tab" class="nexus-tab-panel active">

                <div class="nexus-lab-card">
                    <div class="nexus-card-title">Manual Test Input</div>

                    <div class="nexus-form-grid">
                        <div>
                            <label>Tenant</label>
                            <input id="nexus_tenant" class="form-control" value="TEST-NEXUS">
                        </div>

                        <div>
                            <label>Business Unit</label>
                            <input id="nexus_business_unit" class="form-control" value="ERP Product">
                        </div>

                        <div>
                            <label>Project</label>
                            <input id="nexus_project" class="form-control" placeholder="Optional project">
                        </div>

                        <div>
                            <label>Project Scope Mode</label>
                            <select id="nexus_project_scope_mode" class="form-control">
                                <option value="">Default</option>
                                <option value="with_general">Project + General</option>
                                <option value="strict">Strict Project Only</option>
                            </select>
                        </div>

                        <div>
                            <label>Context</label>
                            <input id="nexus_context" class="form-control" value="ERP">
                        </div>

                        <div>
                            <label>Sub Context</label>
                            <input id="nexus_sub_context" class="form-control" value="General">
                        </div>

                        <div>
                            <label>Entity Type</label>
                            <input id="nexus_entity_type" class="form-control" value="Product">
                        </div>

                        <div>
                            <label>Entity</label>
                            <input id="nexus_entity" class="form-control" value="DIGITZ ERP">
                        </div>

                        <div>
                            <label>Topic</label>
                            <input id="nexus_topic" class="form-control" value="Overview">
                        </div>

                        <div>
                            <label>Use Case</label>
                            <select id="nexus_use_case" class="form-control">
                                <option value="qa">Q&A</option>
                                <option value="chat">Chatbot</option>
                                <option value="support">Support</option>
                                <option value="training">Training</option>
                            </select>
                        </div>

                        <div>
                            <label>User Roles</label>
                            <input id="nexus_roles" class="form-control" value="Guest" placeholder="Comma separated roles">
                        </div>

                        <div>
                            <label>User Designation</label>
                            <input id="nexus_designation" class="form-control" placeholder="Optional designation">
                        </div>

                        <div>
                            <label>Top K</label>
                            <input id="nexus_top_k" class="form-control" type="number" value="5">
                        </div>
                    </div>

                    <div class="nexus-question-box">
                        <label>Question</label>
                        <textarea id="nexus_question" class="form-control" rows="4">What is DIGITZ ERP?</textarea>
                    </div>

                    <div class="nexus-actions">
                        <button class="btn btn-primary" id="nexus_run_test">Run Manual Test</button>
                        <button class="btn btn-default" id="nexus_clear_result">Clear History</button>
                    </div>
                </div>

                <div class="nexus-test-library">
                    <div class="nexus-test-library-head">
                        <div class="nexus-card-title">Executable Test Cases</div>
                        <button class="btn btn-primary btn-sm" id="nexus_run_all_tests">
                            Run All Tests
                        </button>
                    </div>

                    <div id="nexus_test_case_cards" class="nexus-test-case-grid">
                        Loading test cases...
                    </div>
                </div>

            </div>
            

            <div id="nexus_retrieval_tab" class="nexus-tab-panel" style="display:none;">
                <div class="nexus-lab-card">
                    <div class="nexus-card-title">Retrieval Observatory</div>

                    <div class="nexus-observatory-layout">
                        <div class="nexus-observatory-left">
    <div class="nexus-observatory-note">
        <b>Evaluation Controls</b>
        <span>
            Uses the Manual Test Input from the Testing Workspace and runs a deeper retrieval trace.
        </span>
    </div>

    <div class="nexus-observatory-control-card">
        <label>Evaluation Mode</label>
        <select id="nexus_eval_mode" class="form-control">
            <option value="standard">Standard Retrieval</option>
            <option value="debug">Debug Trace</option>
            <option value="governance">Governance Focus</option>
        </select>
    </div>

    <div class="nexus-observatory-control-card">
        <label>Observability Flags</label>

        <label class="nexus-check-line">
            <input type="checkbox" id="nexus_eval_debug" checked>
            Enable Debug Trace
        </label>

        <label class="nexus-check-line">
            <input type="checkbox" id="nexus_eval_mult_query">
            Multi-query Analysis
        </label>

        <label class="nexus-check-line">
            <input type="checkbox" id="nexus_eval_rerank">
            Re-ranking Analysis
        </label>
    </div>

    <div class="nexus-observatory-control-card">
        <label>Quick Hints</label>
        <div class="nexus-mini-hint">Candidate → Governance → Ranking → Sources → Answer</div>
        <div class="nexus-mini-hint">Use this view to explain why Nexus answered or refused.</div>
    </div>

    <button class="btn btn-primary nexus-observatory-run-btn" id="nexus_run_retrieval_evaluation">
        Run Retrieval Observatory
    </button>
</div>

                        <div class="nexus-observatory-right">
                            <div id="nexus_retrieval_evaluation_result" class="nexus-history-empty">
                                No retrieval evaluation executed yet.
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="nexus_history_tab" class="nexus-tab-panel" style="display:none;">
                <div class="nexus-lab-card">
                    <div class="nexus-card-title">Execution History & Results</div>

                    <div id="nexus_history_feed" class="nexus-history-feed">
                        <div class="nexus-history-empty">
                            No tests executed in this page session yet.
                        </div>
                    </div>
                </div>
            </div>

        </div>
    `);

    inject_nexus_lab_css();
    load_test_cases();

    $('.nexus-tab-btn').on('click', function() {
        switch_nexus_tab($(this).data('tab'));
    });

    $('#nexus_run_test').on('click', function() {
        run_nexus_test();
    });

    $('#nexus_clear_result').on('click', function() {
        clear_nexus_result();
    });

    $('#nexus_run_all_tests').on('click', function() {
        run_all_test_cases();
    });

    $('#nexus_run_retrieval_evaluation').on('click', function() {
        run_retrieval_evaluation();
    });
    update_history_count();
};

function run_retrieval_evaluation() {
    const payload = build_payload();

    if (!payload.query) {
        frappe.msgprint('Please enter a question in the Testing Workspace first.');
        return;
    }

    payload.retrieval_debug = $('#nexus_eval_debug').is(':checked');
    payload.debug = $('#nexus_eval_debug').is(':checked');
    payload.observability_mode = true;
    payload.evaluation_mode = get_value('nexus_eval_mode');

    if ($('#nexus_eval_mult_query').is(':checked')) {
        payload.multi_query = true;
    }

    if ($('#nexus_eval_rerank').is(':checked')) {
        payload.reranking = true;
    }

    $('#nexus_retrieval_evaluation_result').html(`
        <div class="nexus-popup-running">
            Running retrieval evaluation...
        </div>
    `);

    frappe.call({
        method: 'digitz_ai_nexus.api.query.ask',
        args: {
            payload: payload
        },
        callback: function(r) {
            if (!r.message) {
                $('#nexus_retrieval_evaluation_result').html(`
                    <div class="nexus-popup-failed">
                        No response received from Nexus API.
                    </div>
                `);
                return;
            }

            const result = r.message;

            $('#nexus_retrieval_evaluation_result').html(`
                ${build_retrieval_observatory_html(result, payload)}
            `);

            $('.nexus-history-toggle').off('click').on('click', function() {
                $(this).next('.nexus-history-details').toggle();
            });
        },
        error: function(err) {
            $('#nexus_retrieval_evaluation_result').html(`
                <div class="nexus-popup-failed">
                    ${frappe.utils.escape_html(err.message || 'Retrieval evaluation failed.')}
                </div>
            `);
        }
    });
}

function switch_nexus_tab(tab) {
    $('.nexus-tab-btn').removeClass('active');
    $(`.nexus-tab-btn[data-tab="${tab}"]`).addClass('active');

    $('.nexus-tab-panel').removeClass('active').hide();

    if (tab === 'history') {
        $('#nexus_history_tab').addClass('active').show();
    } else if (tab === 'retrieval') {
        $('#nexus_retrieval_tab').addClass('active').show();
    } else {
        $('#nexus_workspace_tab').addClass('active').show();
    }
}

function update_history_count() {
    $('#nexus_history_count').text(nexus_session_run_history.length || 0);
}


function get_value(id) {
    return ($(`#${id}`).val() || '').trim();
}


function build_payload() {
    const roles = get_value('nexus_roles')
        .split(',')
        .map(r => r.trim())
        .filter(Boolean);

    const payload = {
        tenant: get_value('nexus_tenant'),
        business_unit: get_value('nexus_business_unit'),
        context: get_value('nexus_context'),
        sub_context: get_value('nexus_sub_context'),
        entity_type: get_value('nexus_entity_type'),
        entity: get_value('nexus_entity'),
        topic: get_value('nexus_topic'),
        query: get_value('nexus_question'),
        top_k: cint(get_value('nexus_top_k') || 5),
        use_case: get_value('nexus_use_case'),
        caller_system: 'Knowledge Testing Lab',
        user: {
            roles: roles.length ? roles : ['Guest']
        }
    };

    const project = get_value('nexus_project');
    const project_scope_mode = get_value('nexus_project_scope_mode');
    const designation = get_value('nexus_designation');

    if (project) payload.project = project;
    if (project_scope_mode) payload.project_scope_mode = project_scope_mode;
    if (designation) payload.user.designation = designation;

    return payload;
}


function run_nexus_test() {
    const payload = build_payload();

    if (!payload.query) {
        frappe.msgprint('Please enter a question.');
        return;
    }

    frappe.call({
        method: 'digitz_ai_nexus.api.query.ask',
        args: {
            payload: payload
        },
        callback: function(r) {
            if (!r.message) {
                render_error('No response received from Nexus API.');
                return;
            }

            const result = r.message;
            const passed = result.status === 'success';

            add_run_history_entry(
                'Manual Test',
                result,
                passed,
                '',
                payload,
                false,
                true
            );
        },
        error: function(err) {
            render_error(err.message || 'Nexus test failed.');
        }
    });
}


function load_test_cases() {
    $('#nexus_test_case_cards').html(`
        <div class="nexus-empty-card">Loading test cases...</div>
    `);

    frappe.call({
        method: 'digitz_ai_nexus_experience.api.testing.get_test_cases',
        callback: function(r) {
            render_test_case_cards(r.message || []);
        },
        error: function(err) {
            $('#nexus_test_case_cards').html(`
                <div class="nexus-empty-card">
                    Failed to load test cases. ${frappe.utils.escape_html(err.message || '')}
                </div>
            `);
        }
    });
}


function render_test_case_cards(test_cases) {
    if (!test_cases.length) {
        $('#nexus_test_case_cards').html(`
            <div class="nexus-empty-card">
                No test cases found. Create records in Nexus Test Case.
            </div>
        `);
        return;
    }

    const html = test_cases.map(tc => `
        <div class="nexus-test-case-card" data-name="${frappe.utils.escape_html(tc.name)}">

            <div class="nexus-test-card-header">
                <span class="nexus-test-category">
                    ${frappe.utils.escape_html(tc.test_category || 'Test')}
                </span>

                <span class="nexus-last-status ${tc.last_run_status === 'Passed' ? 'passed' : tc.last_run_status === 'Failed' ? 'failed' : ''}">
                    ${frappe.utils.escape_html(tc.last_run_status || 'Not Run')}
                </span>
            </div>

            <div class="nexus-test-card-body">
                <h4>${frappe.utils.escape_html(tc.test_title || tc.name)}</h4>
                <p>${frappe.utils.escape_html(tc.short_description || '')}</p>
            </div>

            <div class="nexus-test-card-footer">
                <div class="nexus-expected-line">
                    <span>Expected</span>
                    <b>${frappe.utils.escape_html(tc.expected_access_status || '-')}</b>
                </div>

                <div class="nexus-test-card-actions">
                    <button class="btn btn-xs btn-default nexus-configure-test" data-name="${frappe.utils.escape_html(tc.name)}">
                        Configure
                    </button>

                    <button class="btn btn-xs btn-primary nexus-run-test-case"
                        data-name="${frappe.utils.escape_html(tc.name)}"
                        data-title="${frappe.utils.escape_html(tc.test_title || tc.name)}">
                        Run
                    </button>

                    <a class="btn btn-xs btn-default nexus-open-test-case"
                       href="/app/nexus-test-case/${frappe.utils.escape_html(tc.name)}"
                       target="_blank">
                        Open
                    </a>
                </div>
            </div>
        </div>
    `).join('');

    $('#nexus_test_case_cards').html(html);

    $('.nexus-configure-test').on('click', function(e) {
        e.stopPropagation();
        configure_test_case($(this).data('name'));
    });

    $('.nexus-run-test-case').on('click', function(e) {
        e.stopPropagation();
        run_saved_test_case($(this).data('name'), $(this).data('title'));
    });

    $('.nexus-test-case-card').on('click', function(e) {
        if ($(e.target).closest('button, a').length) return;
        configure_test_case($(this).data('name'));
    });
}


function configure_test_case(test_case) {
    frappe.call({
        method: 'digitz_ai_nexus_experience.api.testing.get_test_case_payload',
        args: {
            test_case: test_case
        },
        callback: function(r) {
            if (!r.message || !r.message.payload) {
                frappe.msgprint('Unable to load test case.');
                return;
            }

            const data = r.message;
            const payload_text = JSON.stringify(data.payload, null, 2);
            const expected_text = JSON.stringify(data.expected || {}, null, 2);

            const dialog = new frappe.ui.Dialog({
                title: `Configure Test: ${data.test_title || test_case}`,
                size: 'large',
                fields: [
                    {
                        fieldtype: 'HTML',
                        fieldname: 'test_config_html',
                        options: `
                            <div class="nexus-popup-block">
                                <div class="nexus-popup-title">Description</div>
                                <p>${frappe.utils.escape_html(data.short_description || '')}</p>

                                <div class="nexus-popup-title">Query Contract</div>
                                <pre class="nexus-popup-code">${frappe.utils.escape_html(payload_text)}</pre>

                                <div class="nexus-popup-title">Expected Result</div>
                                <pre class="nexus-popup-code">${frappe.utils.escape_html(expected_text)}</pre>
                            </div>
                        `
                    }
                ],
                primary_action_label: 'Load to Form',
                primary_action: function() {
                    populate_form_from_payload(data.payload);

                    $('.nexus-test-case-card').removeClass('active');
                    $(`.nexus-test-case-card[data-name="${test_case}"]`).addClass('active');

                    dialog.hide();

                    frappe.show_alert({
                        message: `Loaded test case: ${data.test_title || test_case}`,
                        indicator: 'blue'
                    });
                }
            });

            dialog.show();
        }
    });
}


function run_saved_test_case(test_case, test_title) {
    const dialog = new frappe.ui.Dialog({
        title: `Running Test: ${test_title || test_case}`,
        size: 'large',
        fields: [
            {
                fieldtype: 'HTML',
                fieldname: 'run_result_html',
                options: `
                    <div class="nexus-popup-running">
                        Running saved test case...
                    </div>
                `
            }
        ]
    });

    dialog.show();

    frappe.call({
        method: 'digitz_ai_nexus_experience.api.testing.run_test_case',
        args: {
            test_case: test_case
        },
        callback: function(r) {
            if (!r.message) {
                dialog.fields_dict.run_result_html.$wrapper.html(`
                    <div class="nexus-popup-failed">No response from test runner.</div>
                `);
                render_error('No response from test runner.');
                return;
            }

            const data = r.message;
            const result = data.result || {};

            if (data.payload) {
                populate_form_from_payload(data.payload);
            }

            dialog.set_title(`Running Test: ${data.test_title || test_title || test_case}`);

            dialog.fields_dict.run_result_html.$wrapper.html(
                build_result_output_html(
                    data.test_title || test_title || test_case,
                    result,
                    data.passed,
                    data.failure_reason || '',
                    data.payload || {},
                    false
                )
            );

            add_run_history_entry(
                data.test_title || test_title || test_case,
                result,
                data.passed,
                data.failure_reason || '',
                data.payload || {},
                false,
                true
            );

            load_test_cases();
        },
        error: function(err) {
            const message = err.message || 'Saved test case failed.';

            dialog.fields_dict.run_result_html.$wrapper.html(`
                <div class="nexus-popup-failed">${frappe.utils.escape_html(message)}</div>
            `);

            render_error(message);
        }
    });
}


function run_all_test_cases() {
    const dialog = new frappe.ui.Dialog({
        title: 'Running All Nexus Test Cases',
        size: 'large',
        fields: [
            {
                fieldtype: 'HTML',
                fieldname: 'run_all_html',
                options: `
                    <div class="nexus-popup-running">
                        Running all enabled test cases...
                    </div>
                `
            }
        ]
    });

    dialog.show();

    frappe.call({
        method: 'digitz_ai_nexus_experience.api.testing.run_all_test_cases',
        callback: function(r) {
            const data = r.message || {};
            const results = data.results || [];

            let summaryClass = 'nexus-popup-passed';

            if ((data.failed || 0) > 0 && (data.passed || 0) > 0) {
                summaryClass = 'nexus-popup-warning';
            }

            if ((data.failed || 0) > 0 && (data.passed || 0) === 0) {
                summaryClass = 'nexus-popup-failed';
            }

            const rows = results.map((item, index) => {
                const title = item.test_title || item.test_case || `Test ${index + 1}`;
                const failure = item.failure_reason
                    ? frappe.utils.escape_html(item.failure_reason).replace(/;/g, '<br>')
                    : '';

                const raw_result = frappe.utils.escape_html(
                    JSON.stringify(item.result || {}, null, 2)
                );

                add_run_history_entry(
                    title,
                    item.result || {},
                    item.passed,
                    item.failure_reason || '',
                    item.payload || {},
                    true,
                    false
                );

                return `
                    <div class="nexus-test-run-row ${item.passed ? 'passed' : 'failed'}">
                        <div class="nexus-test-run-main">
                            <div class="nexus-run-row-head">
                                <b>${frappe.utils.escape_html(title)}</b>
                                <span>${item.passed ? 'Passed' : 'Failed'}</span>
                            </div>

                            ${failure ? `
                                <div class="nexus-run-row-reason">
                                    ${failure}
                                </div>
                            ` : ''}

                            <button class="btn btn-xs btn-default nexus-run-row-toggle">
                                View Details
                            </button>

                            <pre class="nexus-run-row-details" style="display:none;">${raw_result}</pre>
                        </div>
                    </div>
                `;
            }).join('');

            dialog.fields_dict.run_all_html.$wrapper.html(`
                <div class="${summaryClass}">
                    Total: ${data.total || 0} |
                    Passed: ${data.passed || 0} |
                    Failed: ${data.failed || 0}
                </div>

                <div class="nexus-run-all-list">
                    ${rows || '<div class="nexus-empty-card">No enabled test cases found.</div>'}
                </div>
            `);

            dialog.fields_dict.run_all_html.$wrapper
                .find('.nexus-run-row-toggle')
                .on('click', function() {
                    $(this).next('.nexus-run-row-details').toggle();
                });

            switch_nexus_tab('history');
            load_test_cases();
        },
        error: function(err) {
            dialog.fields_dict.run_all_html.$wrapper.html(`
                <div class="nexus-popup-failed">
                    ${frappe.utils.escape_html(err.message || 'Failed to run all tests.')}
                </div>
            `);
        }
    });
}


function build_result_output_html(title, result, passed, failure_reason, payload, compact=false) {
    const payload_text = frappe.utils.escape_html(JSON.stringify(payload || {}, null, 2));
    const result_text = frappe.utils.escape_html(JSON.stringify(result || {}, null, 2));

    return `
        <div class="${passed ? 'nexus-popup-passed' : 'nexus-popup-failed'}">
            ${frappe.utils.escape_html(title || 'Test Result')}
            <span style="float:right;">${passed ? 'Passed' : 'Failed'}</span>
        </div>

        ${failure_reason ? `
            <div class="nexus-popup-title">Failure Reason</div>
            <div class="nexus-popup-reason">
                ${frappe.utils.escape_html(failure_reason).replace(/;/g, '<br>')}
            </div>
        ` : ''}

        <div class="nexus-popup-title">Answer</div>
        <div class="nexus-popup-answer">
            ${frappe.utils.escape_html(result.answer || 'No answer returned.').replace(/\n/g, '<br>')}
        </div>

        <div class="nexus-popup-title">Summary</div>
        <div class="nexus-popup-summary">
            <div><b>Status</b><span>${frappe.utils.escape_html(result.status || '-')}</span></div>
            <div><b>Access</b><span>${frappe.utils.escape_html(result.access_status || '-')}</span></div>
            <div><b>Sources</b><span>${((result.sources || []).length)}</span></div>
            <div><b>Query Log</b><span>${result.log ? `<a href="/app/nexus-query-log/${frappe.utils.escape_html(result.log)}" target="_blank">${frappe.utils.escape_html(result.log)}</a>` : '-'}</span></div>
        </div>

        ${build_retrieval_debug_html(result, compact)}

        <button class="btn btn-xs btn-default nexus-history-toggle">
            View Payload & Raw Result
        </button>

        <div class="nexus-history-details" style="display:none;">
            <div class="nexus-popup-title">Payload</div>
            <pre class="nexus-popup-code">${payload_text}</pre>

            <div class="nexus-popup-title">Raw Result</div>
            <pre class="nexus-popup-code">${result_text}</pre>
        </div>
    `;
}

function build_retrieval_observatory_html(result, payload) {
    const retrieval = result.retrieval_debug || {};
    const sources = result.sources || [];
    const denied = result.denied || retrieval.denied_chunks || [];
    const queryVariants = retrieval.query_variants || [];

    const candidateCount = retrieval.candidate_count || 0;
    const allowedCount = retrieval.allowed_count || sources.length || 0;
    const deniedCount = retrieval.denied_count || denied.length || 0;

    const payload_text = frappe.utils.escape_html(JSON.stringify(payload || {}, null, 2));
    const result_text = frappe.utils.escape_html(JSON.stringify(result || {}, null, 2));

    return `
        <div class="nexus-observatory-header">
            <div>
                <h3>Retrieval Pipeline Evaluation</h3>
                <p>${frappe.utils.escape_html(payload.query || '')}</p>
            </div>

            <div class="nexus-observatory-status ${result.access_status === 'allowed' ? 'passed' : result.access_status === 'restricted' ? 'failed' : 'warning'}">
                ${frappe.utils.escape_html(result.access_status || '-')}
            </div>
        </div>

        <div class="nexus-observatory-metrics">
            <div>
                <b>Candidate Chunks</b>
                <span>${candidateCount}</span>
            </div>
            <div>
                <b>Allowed</b>
                <span>${allowedCount}</span>
            </div>
            <div>
                <b>Denied</b>
                <span>${deniedCount}</span>
            </div>
            <div>
                <b>Sources Used</b>
                <span>${sources.length}</span>
            </div>
            <div>
                <b>Confidence</b>
                <span>${result.confidence || 0}</span>
            </div>
            <div>
                <b>Fallback</b>
                <span>${result.fallback_used ? 'Yes' : 'No'}</span>
            </div>
        </div>

        <div class="nexus-retrieval-timeline">
        <div>Query</div>
        <div>Expansion</div>
        <div>Candidates</div>
        <div>Access Governance</div>
        <div>Ranking Intelligence</div>
        <div>Grounded Answer</div>
        </div>

        ${queryVariants.length ? `
            <div class="nexus-debug-section">
                <div class="nexus-popup-title">Query Variants</div>
                <div class="nexus-query-variants">
                    ${queryVariants.map(q => `
                        <div class="nexus-query-pill">${frappe.utils.escape_html(q)}</div>
                    `).join('')}
                </div>
            </div>
        ` : ''}

        <div class="nexus-popup-title">Answer</div>
        <div class="nexus-popup-answer">
            ${frappe.utils.escape_html(result.answer || 'No answer returned.').replace(/\n/g, '<br>')}
        </div>

        ${build_source_preview_html(sources)}

        ${build_retrieval_debug_html(result, false)}

        <button class="btn btn-xs btn-default nexus-history-toggle">
            View Payload & Raw Result
        </button>

        <div class="nexus-history-details" style="display:none;">
            <div class="nexus-popup-title">Payload</div>
            <pre class="nexus-popup-code">${payload_text}</pre>

            <div class="nexus-popup-title">Raw Result</div>
            <pre class="nexus-popup-code">${result_text}</pre>
        </div>
    `;
}

function build_source_preview_html(sources) {
    if (!sources || !sources.length) {
        return `
            <div class="nexus-debug-section">
                <div class="nexus-popup-title">Selected Sources</div>
                <div class="nexus-history-empty">
                    No sources selected.
                </div>
            </div>
        `;
    }

    return `
        <div class="nexus-debug-section">
            <div class="nexus-popup-title">Selected Sources</div>

            <div class="nexus-source-preview-list">
                ${sources.map((source, index) => `
                    <div class="nexus-source-preview-card">
                        <div class="nexus-source-preview-head">
                            <b>Source #${index + 1}</b>
                            <span>${frappe.utils.escape_html(source.chunk || '-')}</span>
                        </div>

                        <div class="nexus-source-preview-meta">
                            <div><b>Score</b><span>${source.score || source.final_score || '-'}</span></div>
                            <div><b>Vector</b><span>${source.vector_score || '-'}</span></div>
                            <div><b>Keyword</b><span>${source.keyword_score || '-'}</span></div>
                            <div><b>Scope</b><span>${frappe.utils.escape_html(source.scope_type || '-')}</span></div>
                        </div>

                        <div class="nexus-source-preview-path">
                            ${frappe.utils.escape_html(source.context_path || 'Unknown Source')}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

function build_retrieval_debug_html(result, compact=false) {
    const retrieval = result.retrieval_debug || {};
    const ranked = retrieval.ranked_chunks || [];
    const denied = retrieval.denied_chunks || [];
    const query_variants = retrieval.query_variants || [];
    const features = retrieval.features || {};

    if (!ranked.length && !denied.length && !query_variants.length) {
        return '';
    }

    if (compact) {
        const topChunk = ranked.length ? ranked[0] : null;
        const primaryDeniedReason = denied.length
            ? (denied[0].reason || denied[0].denied_reason || '')
            : '';

        return `
            <div class="nexus-retrieval-debug-wrap compact">

                ${query_variants.length ? `
                    <div class="nexus-debug-section">
                        <div class="nexus-popup-title">Query Variants</div>
                        <div class="nexus-query-variants">
                            ${query_variants.slice(0, 3).map(q => `
                                <div class="nexus-query-pill">
                                    ${frappe.utils.escape_html(q)}
                                </div>
                            `).join('')}

                            ${query_variants.length > 3 ? `
                                <div class="nexus-query-pill muted">
                                    +${query_variants.length - 3} more
                                </div>
                            ` : ''}
                        </div>
                    </div>
                ` : ''}

                <div class="nexus-debug-section">
                    <div class="nexus-popup-title">Retrieval Summary</div>

                    <div class="nexus-feature-grid">
                        <div class="nexus-feature-card">
                            <b>Ranked Chunks</b>
                            <span>${ranked.length}</span>
                        </div>

                        <div class="nexus-feature-card">
                            <b>Denied Chunks</b>
                            <span>${denied.length}</span>
                        </div>

                        <div class="nexus-feature-card">
                            <b>Top Score</b>
                            <span>${topChunk ? ((topChunk.final_score || 0).toFixed(2)) : '-'}</span>
                        </div>
                    </div>

                    ${topChunk ? `
                        <div class="nexus-compact-top-chunk">
                            <b>Top Chunk</b>
                            <span>${frappe.utils.escape_html(topChunk.chunk || '')}</span>
                        </div>
                    ` : ''}

                    ${primaryDeniedReason ? `
                        <div class="nexus-compact-denied-reason">
                            <b>Primary Denied Reason</b>
                            <span>${frappe.utils.escape_html(primaryDeniedReason)}</span>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    const queryHtml = query_variants.length
        ? `
            <div class="nexus-debug-section">
                <div class="nexus-popup-title">Query Variants</div>

                <div class="nexus-query-variants">
                    ${query_variants.map(q => `
                        <div class="nexus-query-pill">
                            ${frappe.utils.escape_html(q)}
                        </div>
                    `).join('')}
                </div>
            </div>
        `
        : '';

    const featureHtml = `
        <div class="nexus-debug-section">
            <div class="nexus-popup-title">Retrieval Features</div>

            <div class="nexus-feature-grid">
                <div class="nexus-feature-card">
                    <b>Multi-query</b>
                    <span>${features.multi_query ? 'Enabled' : 'Disabled'}</span>
                </div>

                <div class="nexus-feature-card">
                    <b>Re-ranking</b>
                    <span>${features.reranking ? 'Enabled' : 'Disabled'}</span>
                </div>

                <div class="nexus-feature-card">
                    <b>Debug Mode</b>
                    <span>${(features.retrieval_debug || features.debug) ? 'Enabled' : 'Disabled'}</span>
                </div>
            </div>
        </div>
    `;

    const rankedHtml = ranked.length
        ? `
            <div class="nexus-debug-section">
                <div class="nexus-popup-title">Ranked Retrieval Chunks</div>

                <div class="nexus-ranked-list">
                    ${ranked.map(chunk => {
                        const reasons = chunk.rerank_reasons || [];
                        return `
                            <div class="nexus-ranked-card">

                                <div class="nexus-ranked-head">
                                    <div>
                                        <b>Rank #${chunk.rank_after_rerank || '-'}</b>
                                        <span>${frappe.utils.escape_html(chunk.chunk || '')}</span>
                                    </div>

                                    <div class="nexus-score-badge">
                                        ${(chunk.final_score || 0).toFixed(2)}
                                    </div>
                                </div>

                                <div class="nexus-score-grid">
                                    <div>
                                        <label>Vector</label>
                                        <span>${(chunk.vector_score || 0).toFixed(2)}</span>
                                    </div>

                                    <div>
                                        <label>Keyword</label>
                                        <span>${(chunk.keyword_score || 0).toFixed(2)}</span>
                                    </div>

                                    <div>
                                        <label>Hybrid</label>
                                        <span>${(chunk.hybrid_score || 0).toFixed(2)}</span>
                                    </div>

                                    <div>
                                        <label>Rerank</label>
                                        <span>${(chunk.rerank_bonus || 0).toFixed(2)}</span>
                                    </div>
                                </div>

                                ${reasons.length ? `
                                    <div class="nexus-rerank-reasons">
                                        ${reasons.map(reason => `
                                            <span>${frappe.utils.escape_html(reason)}</span>
                                        `).join('')}
                                    </div>
                                ` : ''}

                                <div class="nexus-rank-movement">
                                    Before: ${chunk.rank_before_rerank || '-'}
                                    →
                                    After: ${chunk.rank_after_rerank || '-'}
                                </div>

                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `
        : '';

    const deniedHtml = denied.length
        ? `
            <div class="nexus-debug-section">
                <div class="nexus-popup-title">Denied Chunks</div>

                <div class="nexus-denied-list">
                    ${denied.map(d => `
                        <div class="nexus-denied-card">
                            <b>${frappe.utils.escape_html(d.chunk || '')}</b>
                            <span>
                                ${frappe.utils.escape_html(d.reason || d.denied_reason || '')}
                            </span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `
        : '';

    return `
        <div class="nexus-retrieval-debug-wrap">
            ${queryHtml}
            ${featureHtml}
            ${rankedHtml}
            ${deniedHtml}
        </div>
    `;
}


function add_run_history_entry(title, res, passed, failure_reason, payload, compact=false, auto_switch=false) {
    nexus_session_run_counter += 1;

    const entry = {
        number: nexus_session_run_counter,
        title: title || 'Manual Test',
        passed: !!passed,
        failure_reason: failure_reason || '',
        payload: payload || {},
        result: res || {},
        compact: !!compact
    };

    nexus_session_run_history.unshift(entry);
    render_history_feed();
    update_history_count();

    if (auto_switch) {
        switch_nexus_tab('history');
    }
}


function render_history_feed() {
    if (!nexus_session_run_history.length) {
        $('#nexus_history_feed').html(`
            <div class="nexus-history-empty">
                No tests executed in this page session yet.
            </div>
        `);
        return;
    }

    const html = nexus_session_run_history.map(entry => {
        return `
            <div class="nexus-history-result-card ${entry.passed ? 'passed' : 'failed'}">
                ${build_result_output_html(
                    `#${entry.number} — ${entry.title}`,
                    entry.result,
                    entry.passed,
                    entry.failure_reason,
                    entry.payload,
                    entry.compact
                )}
            </div>
        `;
    }).join('');

    $('#nexus_history_feed').html(html);

    $('.nexus-history-toggle').off('click').on('click', function() {
        $(this).next('.nexus-history-details').toggle();
    });
}


function render_error(message) {
    const result = {
        status: 'failed',
        access_status: '-',
        answer: message,
        sources: [],
        log: ''
    };

    add_run_history_entry('Error', result, false, message, {}, false, true);
}


function clear_nexus_result() {
    nexus_session_run_history = [];
    nexus_session_run_counter = 0;
    render_history_feed();
    update_history_count();
}


function populate_form_from_payload(payload) {
    $('#nexus_tenant').val(payload.tenant || '');
    $('#nexus_business_unit').val(payload.business_unit || '');
    $('#nexus_project').val(payload.project || '');
    $('#nexus_project_scope_mode').val(payload.project_scope_mode || '');
    $('#nexus_context').val(payload.context || '');
    $('#nexus_sub_context').val(payload.sub_context || '');
    $('#nexus_entity_type').val(payload.entity_type || '');
    $('#nexus_entity').val(payload.entity || '');
    $('#nexus_topic').val(payload.topic || '');
    $('#nexus_use_case').val(payload.use_case || 'qa');
    $('#nexus_top_k').val(payload.top_k || 5);
    $('#nexus_question').val(payload.query || '');

    const user = payload.user || {};
    const roles = user.roles || ['Guest'];

    $('#nexus_roles').val(roles.join(', '));
    $('#nexus_designation').val(user.designation || '');
}


function inject_nexus_lab_css() {
    if ($('#nexus_lab_css').length) return;

    $('head').append(`
        <style id="nexus_lab_css">
            .nexus-lab-wrap {
                padding: 12px;
            }

            .nexus-lab-hero {
                position: relative;
                overflow: hidden;
                border-radius: 26px;
                padding: 30px 34px;
                margin-bottom: 18px;
                background:
                    radial-gradient(circle at 8% 20%, rgba(77, 163, 255, 0.28), transparent 30%),
                    radial-gradient(circle at 92% 10%, rgba(224, 166, 47, 0.22), transparent 28%),
                    linear-gradient(135deg, #ffffff 0%, #eef6ff 48%, #f8fbff 100%);
                border: 1px solid rgba(77, 163, 255, 0.38);
                box-shadow: 0 18px 45px rgba(33, 77, 187, 0.12);
            }

            .nexus-lab-badge {
                display: inline-flex;
                align-items: center;
                padding: 8px 14px;
                border-radius: 999px;
                background: rgba(33, 77, 187, 0.09);
                border: 1px solid rgba(33, 77, 187, 0.16);
                color: #214dbb;
                font-weight: 800;
                font-size: 12px;
                letter-spacing: .04em;
                text-transform: uppercase;
                margin-bottom: 12px;
            }

            .nexus-lab-hero h2 {
                margin: 0;
                font-size: 30px;
                font-weight: 900;
                color: #102b67;
                letter-spacing: -0.03em;
            }

            .nexus-lab-hero p {
                margin: 12px 0 0;
                max-width: 900px;
                font-size: 15px;
                line-height: 1.7;
                color: #27416f;
                font-weight: 500;
            }

            .nexus-tab-bar {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 18px;
                padding: 8px;
                border-radius: 18px;
                background: #f8fbff;
                border: 1px solid rgba(77, 163, 255, 0.24);
                box-shadow: 0 8px 20px rgba(33, 77, 187, 0.05);
            }

            .nexus-tab-btn {
                border: 0;
                border-radius: 999px;
                padding: 10px 18px;
                background: transparent;
                color: #53688f;
                font-weight: 900;
                cursor: pointer;
                transition: all .18s ease;
            }

            .nexus-tab-btn.active {
                background: #214dbb;
                color: #ffffff;
                box-shadow: 0 8px 18px rgba(33, 77, 187, 0.20);
            }

            .nexus-tab-count {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 22px;
                height: 22px;
                margin-left: 8px;
                border-radius: 999px;
                background: rgba(255,255,255,.22);
                color: inherit;
                font-size: 11px;
                font-weight: 900;
            }

            .nexus-tab-btn:not(.active) .nexus-tab-count {
                background: #eef6ff;
                color: #214dbb;
            }

            .nexus-tab-panel {
                animation: nexusFadeIn .18s ease;
            }

            @keyframes nexusFadeIn {
                from {
                    opacity: 0;
                    transform: translateY(4px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .nexus-test-library,
            .nexus-lab-card {
                border: 1px solid rgba(77, 163, 255, 0.28);
                border-radius: 22px;
                background: #fff;
                padding: 20px;
                box-shadow: 0 12px 30px rgba(33, 77, 187, 0.07);
            }

            .nexus-test-library {
                margin-top: 18px;
                margin-bottom: 0;
            }

            .nexus-card-title {
                display: inline-flex;
                align-items: center;
                gap: 12px;
                color: #173b8c;
                font-size: 16px;
                font-weight: 900;
                padding: 10px 16px;
                margin-bottom: 18px;
                border-radius: 999px;
                background: #eef6ff;
                border: 1px solid rgba(33, 77, 187, 0.14);
            }

            .nexus-card-title:after {
                content: "";
                width: 36px;
                height: 4px;
                border-radius: 999px;
                background: linear-gradient(90deg, #e0a62f, #f4ca64);
            }

            .nexus-test-library-head {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
                margin-bottom: 18px;
            }

            .nexus-test-library-head .nexus-card-title {
                margin-bottom: 0;
            }

            .nexus-test-case-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 14px;
            }

            .nexus-test-case-card {
                cursor: pointer;
                min-height: 218px;
                padding: 0;
                border-radius: 20px;
                overflow: hidden;
                background: linear-gradient(180deg, rgba(248,251,255,.96), #ffffff);
                border: 1px solid rgba(77, 163, 255, 0.28);
                box-shadow: 0 12px 26px rgba(33, 77, 187, 0.06);
                transition: all .18s ease;
                display: flex;
                flex-direction: column;
            }

            .nexus-test-case-card:hover,
            .nexus-test-case-card.active {
                border-color: rgba(33, 77, 187, 0.52);
                box-shadow: 0 18px 34px rgba(33, 77, 187, 0.13);
                transform: translateY(-2px);
            }

            .nexus-test-card-header {
                min-height: 48px;
                padding: 14px 16px 10px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
                border-bottom: 1px solid rgba(77, 163, 255, 0.14);
                background: linear-gradient(135deg, #f8fbff, #eef6ff);
            }

            .nexus-test-category,
            .nexus-last-status {
                display: inline-flex;
                align-items: center;
                min-height: 26px;
                padding: 6px 11px;
                border-radius: 999px;
                font-size: 11px;
                font-weight: 900;
                line-height: 1;
            }

            .nexus-test-category {
                background: #eaf3ff;
                color: #214dbb;
                border: 1px solid rgba(33, 77, 187, 0.10);
            }

            .nexus-last-status {
                background: #f5f7fb;
                color: #5d6f92;
                border: 1px solid rgba(93,111,146,.12);
            }

            .nexus-last-status.passed {
                background: #ecfdf3;
                color: #16794c;
                border-color: #bdebd2;
            }

            .nexus-last-status.failed {
                background: #fff0f0;
                color: #b42318;
                border-color: #ffd1d1;
            }

            .nexus-test-card-body {
                padding: 16px 18px 12px;
                flex: 1;
            }

            .nexus-test-case-card h4 {
                margin: 0 0 9px;
                color: #102b67;
                font-size: 17px;
                font-weight: 950;
                letter-spacing: -0.01em;
                line-height: 1.25;
            }

            .nexus-test-case-card p {
                margin: 0;
                color: #53688f;
                font-size: 13px;
                line-height: 1.55;
            }

            .nexus-test-card-footer {
                padding: 13px 16px 15px;
                border-top: 1px solid rgba(77, 163, 255, 0.14);
                background: #fbfdff;
            }

            .nexus-expected-line {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
                margin-bottom: 12px;
                color: #27416f;
                font-size: 12px;
                font-weight: 800;
            }

            .nexus-expected-line span {
                color: #6a7b99;
                text-transform: uppercase;
                font-size: 10px;
                letter-spacing: .06em;
            }

            .nexus-expected-line b {
                color: #173b8c;
                background: #eef6ff;
                border: 1px solid rgba(33, 77, 187, 0.12);
                border-radius: 999px;
                padding: 5px 10px;
                font-size: 12px;
            }

            .nexus-test-card-actions {
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .nexus-test-card-actions .btn {
                border-radius: 999px;
                font-weight: 850;
            }

            .nexus-form-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 14px;
            }

            .nexus-form-grid label,
            .nexus-question-box label {
                font-size: 12px;
                font-weight: 800;
                color: #27416f;
                margin-bottom: 6px;
                display: block;
            }

            .nexus-question-box {
                margin-top: 14px;
            }

            .nexus-actions {
                display: flex;
                gap: 10px;
                margin-top: 16px;
            }

            .nexus-empty-card,
            .nexus-history-empty {
                padding: 18px;
                border-radius: 16px;
                background: #fff7e6;
                border: 1px solid #f2d49b;
                color: #8a5d00;
                font-weight: 800;
            }

            .nexus-popup-title {
                margin: 16px 0 8px;
                color: #173b8c;
                font-size: 13px;
                font-weight: 900;
            }

            .nexus-popup-code {
                max-height: 260px;
                overflow: auto;
                padding: 14px;
                border-radius: 14px;
                background: #0f172a;
                color: #dbeafe;
                font-size: 12px;
            }

            .nexus-popup-running {
                padding: 16px;
                border-radius: 14px;
                background: #eef6ff;
                color: #214dbb;
                font-weight: 900;
            }

            .nexus-popup-passed {
                padding: 14px;
                border-radius: 14px;
                background: #ecfdf3;
                color: #16794c;
                border: 1px solid #bdebd2;
                font-weight: 900;
            }

            .nexus-popup-failed {
                padding: 14px;
                border-radius: 14px;
                background: #fff0f0;
                color: #b42318;
                border: 1px solid #ffd1d1;
                font-weight: 900;
            }

            .nexus-popup-warning {
                padding: 14px;
                border-radius: 14px;
                background: #fff7e6;
                color: #8a5d00;
                border: 1px solid #f2d49b;
                font-weight: 900;
            }

            .nexus-popup-reason {
                padding: 12px;
                border-radius: 12px;
                background: #fff7e6;
                color: #8a5d00;
                border: 1px solid #f2d49b;
                font-weight: 700;
            }

            .nexus-popup-answer {
                padding: 14px;
                border-radius: 14px;
                background: #f8fbff;
                border: 1px solid rgba(77, 163, 255, 0.22);
                color: #1c2f55;
                line-height: 1.7;
            }

            .nexus-popup-summary {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 10px;
            }

            .nexus-popup-summary > div {
                padding: 12px;
                border-radius: 12px;
                background: #f8fbff;
                border: 1px solid rgba(77, 163, 255, 0.18);
            }

            .nexus-popup-summary b {
                display: block;
                color: #173b8c;
                font-size: 12px;
                margin-bottom: 4px;
            }

            .nexus-popup-summary span {
                color: #27416f;
                font-weight: 700;
            }

            .nexus-run-all-list,
            .nexus-history-feed {
                display: grid;
                gap: 14px;
                margin-top: 14px;
            }

            .nexus-test-run-row {
                display: flex;
                justify-content: space-between;
                gap: 12px;
                padding: 12px;
                border-radius: 14px;
                border: 1px solid #e5edf8;
                background: #f8fbff;
            }

            .nexus-test-run-row.passed {
                background: #ecfdf3;
                border-color: #bdebd2;
            }

            .nexus-test-run-row.failed {
                background: #fff0f0;
                border-color: #ffd1d1;
            }

            .nexus-test-run-main {
                width: 100%;
            }

            .nexus-run-row-head {
                display: flex;
                justify-content: space-between;
                gap: 12px;
            }

            .nexus-run-row-head b {
                color: #173b8c;
            }

            .nexus-run-row-head span {
                font-weight: 900;
            }

            .nexus-test-run-row.passed span {
                color: #16794c;
            }

            .nexus-test-run-row.failed span {
                color: #b42318;
            }

            .nexus-run-row-reason {
                margin-top: 8px;
                color: #8a5d00;
                font-size: 12px;
                line-height: 1.5;
            }

            .nexus-run-row-toggle,
            .nexus-history-toggle {
                margin-top: 14px;
            }

            .nexus-run-row-details,
            .nexus-history-details {
                margin-top: 10px;
            }

            .nexus-history-result-card {
                padding: 14px;
                border-radius: 18px;
                background: #ffffff;
                border: 1px solid rgba(77, 163, 255, 0.24);
                box-shadow: 0 8px 18px rgba(33, 77, 187, 0.05);
            }

            .nexus-retrieval-debug-wrap {
                margin-top: 18px;
            }

            .nexus-retrieval-debug-wrap.compact {
                margin-top: 14px;
            }

            .nexus-debug-section {
                margin-top: 18px;
            }

            .nexus-query-variants {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
            }

            .nexus-query-pill {
                padding: 8px 12px;
                border-radius: 999px;
                background: #eef6ff;
                border: 1px solid rgba(33,77,187,.14);
                color: #214dbb;
                font-weight: 700;
                font-size: 12px;
            }

            .nexus-query-pill.muted {
                background: #f5f7fb;
                color: #6a7b99;
            }

            .nexus-feature-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(0,1fr));
                gap: 10px;
            }

            .nexus-feature-card {
                padding: 12px;
                border-radius: 14px;
                background: #f8fbff;
                border: 1px solid rgba(77,163,255,.18);
            }

            .nexus-feature-card b {
                display: block;
                color: #173b8c;
                margin-bottom: 6px;
            }

            .nexus-ranked-list {
                display: grid;
                gap: 12px;
            }

            .nexus-ranked-card {
                padding: 16px;
                border-radius: 16px;
                background: linear-gradient(180deg,#ffffff,#f8fbff);
                border: 1px solid rgba(77,163,255,.22);
            }

            .nexus-ranked-head {
                display: flex;
                justify-content: space-between;
                gap: 12px;
                margin-bottom: 14px;
            }

            .nexus-ranked-head b {
                display: block;
                color: #173b8c;
            }

            .nexus-ranked-head span {
                color: #53688f;
                font-size: 12px;
            }

            .nexus-score-badge {
                min-width: 56px;
                height: 40px;
                border-radius: 12px;
                background: #214dbb;
                color: #fff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 900;
            }

            .nexus-score-grid {
                display: grid;
                grid-template-columns: repeat(4,minmax(0,1fr));
                gap: 10px;
            }

            .nexus-score-grid > div {
                padding: 10px;
                border-radius: 12px;
                background: #eef6ff;
            }

            .nexus-score-grid label {
                display: block;
                font-size: 11px;
                color: #53688f;
                margin-bottom: 4px;
            }

            .nexus-score-grid span {
                color: #173b8c;
                font-weight: 900;
            }

            .nexus-rerank-reasons {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 14px;
            }

            .nexus-rerank-reasons span {
                padding: 6px 10px;
                border-radius: 999px;
                background: #ecfdf3;
                color: #16794c;
                border: 1px solid #bdebd2;
                font-size: 11px;
                font-weight: 800;
            }

            .nexus-rank-movement {
                margin-top: 12px;
                color: #8a5d00;
                font-weight: 800;
                font-size: 12px;
            }

            .nexus-denied-list {
                display: grid;
                gap: 10px;
            }

            .nexus-denied-card {
                padding: 12px;
                border-radius: 14px;
                background: #fff0f0;
                border: 1px solid #ffd1d1;
            }

            .nexus-denied-card b {
                display: block;
                color: #b42318;
                margin-bottom: 4px;
            }

            .nexus-denied-card span {
                color: #8a5d00;
                font-size: 12px;
            }

            .nexus-compact-top-chunk,
            .nexus-compact-denied-reason {
                margin-top: 12px;
                padding: 12px;
                border-radius: 14px;
                background: #f8fbff;
                border: 1px solid rgba(77,163,255,.18);
            }

            .nexus-compact-top-chunk b,
            .nexus-compact-denied-reason b {
                display: block;
                color: #173b8c;
                margin-bottom: 5px;
            }

            .nexus-compact-top-chunk span,
            .nexus-compact-denied-reason span {
                color: #27416f;
                font-weight: 800;
            }

            .nexus-observatory-layout {
                display: grid;
                grid-template-columns: 320px minmax(0, 1fr);
                gap: 18px;
            }

            .nexus-observatory-left,
            .nexus-observatory-right {
                min-width: 0;
            }

            .nexus-observatory-note {
                padding: 16px;
                border-radius: 16px;
                background: #f8fbff;
                border: 1px solid rgba(77,163,255,.22);
                color: #27416f;
                font-weight: 700;
                line-height: 1.6;
                margin-bottom: 14px;
            }

            .nexus-observatory-header {
                display: flex;
                justify-content: space-between;
                gap: 16px;
                align-items: flex-start;
                padding: 18px;
                border-radius: 18px;
                background: linear-gradient(135deg, #f8fbff, #eef6ff);
                border: 1px solid rgba(77,163,255,.24);
            }

            .nexus-observatory-header h3 {
                margin: 0;
                color: #102b67;
                font-weight: 950;
            }

            .nexus-observatory-header p {
                margin: 8px 0 0;
                color: #53688f;
                font-weight: 700;
            }

            .nexus-observatory-status {
                padding: 8px 14px;
                border-radius: 999px;
                font-weight: 900;
                text-transform: uppercase;
                font-size: 11px;
            }

            .nexus-observatory-status.passed {
                background: #ecfdf3;
                color: #16794c;
                border: 1px solid #bdebd2;
            }

            .nexus-observatory-status.failed {
                background: #fff0f0;
                color: #b42318;
                border: 1px solid #ffd1d1;
            }

            .nexus-observatory-status.warning {
                background: #fff7e6;
                color: #8a5d00;
                border: 1px solid #f2d49b;
            }

            .nexus-observatory-metrics {
                display: grid;
                grid-template-columns: repeat(6, minmax(0, 1fr));
                gap: 10px;
                margin-top: 14px;
            }

            .nexus-observatory-metrics > div {
                padding: 14px;
                border-radius: 14px;
                background: #ffffff;
                border: 1px solid rgba(77,163,255,.22);
                box-shadow: 0 6px 14px rgba(33,77,187,.04);
            }

            .nexus-observatory-metrics b {
                display: block;
                color: #53688f;
                font-size: 11px;
                margin-bottom: 6px;
                text-transform: uppercase;
            }

            .nexus-observatory-metrics span {
                color: #173b8c;
                font-size: 18px;
                font-weight: 950;
            }

            .nexus-retrieval-timeline {
                display: grid;
                grid-template-columns: repeat(6, minmax(0, 1fr));
                gap: 8px;
                margin-top: 16px;
            }

            .nexus-retrieval-timeline > div {
                position: relative;
                padding: 10px;
                border-radius: 999px;
                text-align: center;
                background: #214dbb;
                color: #fff;
                font-size: 11px;
                font-weight: 900;
            }

            .nexus-source-preview-list {
                display: grid;
                gap: 12px;
            }

            .nexus-source-preview-card {
                padding: 15px;
                border-radius: 16px;
                background: linear-gradient(180deg, #ffffff, #f8fbff);
                border: 1px solid rgba(77,163,255,.22);
            }

            .nexus-source-preview-head {
                display: flex;
                justify-content: space-between;
                gap: 12px;
                margin-bottom: 12px;
            }

            .nexus-source-preview-head b {
                color: #173b8c;
            }

            .nexus-source-preview-head span {
                color: #53688f;
                font-size: 12px;
                font-weight: 800;
            }

            .nexus-source-preview-meta {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 8px;
            }

            .nexus-source-preview-meta > div {
                padding: 9px;
                border-radius: 12px;
                background: #eef6ff;
            }

            .nexus-source-preview-meta b {
                display: block;
                color: #53688f;
                font-size: 10px;
                margin-bottom: 4px;
            }

            .nexus-source-preview-meta span {
                color: #173b8c;
                font-weight: 900;
            }

            .nexus-source-preview-path {
                margin-top: 10px;
                color: #27416f;
                font-size: 12px;
                font-weight: 700;
            }

            @media (max-width: 1200px) {
                .nexus-test-case-grid {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }

                .nexus-form-grid {
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }

                .nexus-observatory-layout {
                    grid-template-columns: 1fr;
                }

                .nexus-observatory-metrics {
                    grid-template-columns: repeat(3, minmax(0, 1fr));
                }
            }

            .nexus-observatory-control-card {
                padding: 14px;
                border-radius: 16px;
                background: #ffffff;
                border: 1px solid rgba(77,163,255,.22);
                box-shadow: 0 6px 14px rgba(33,77,187,.04);
                margin-bottom: 12px;
            }

            .nexus-observatory-control-card label {
                display: block;
                color: #173b8c;
                font-size: 12px;
                font-weight: 900;
                margin-bottom: 8px;
            }

            .nexus-observatory-note b {
                display: block;
                color: #173b8c;
                font-size: 13px;
                font-weight: 950;
                margin-bottom: 6px;
            }

            .nexus-observatory-note span {
                display: block;
                color: #53688f;
                font-size: 12px;
                line-height: 1.6;
            }

            .nexus-check-line {
                display: flex !important;
                align-items: center;
                gap: 8px;
                color: #27416f !important;
                font-size: 12px !important;
                font-weight: 800 !important;
                margin-bottom: 8px !important;
            }

            .nexus-check-line input {
                margin: 0;
            }

            .nexus-mini-hint {
                padding: 9px 10px;
                border-radius: 12px;
                background: #eef6ff;
                color: #27416f;
                font-size: 12px;
                font-weight: 800;
                line-height: 1.45;
                margin-bottom: 8px;
            }

            .nexus-observatory-run-btn {
                width: 100%;
                border-radius: 999px;
                font-weight: 900;
                box-shadow: 0 10px 20px rgba(33,77,187,.18);
            }

            .nexus-retrieval-timeline > div {
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            @media (max-width: 700px) {
                .nexus-form-grid,
                .nexus-popup-summary,
                .nexus-test-case-grid,
                .nexus-feature-grid,
                .nexus-score-grid,
                .nexus-observatory-metrics,
                .nexus-retrieval-timeline,
                .nexus-source-preview-meta {
                    grid-template-columns: 1fr;
                }

                .nexus-tab-bar {
                    flex-direction: column;
                    align-items: stretch;
                }

                .nexus-tab-btn {
                    width: 100%;
                }

                .nexus-observatory-header {
                    flex-direction: column;
                }
            }
        </style>
    `);
}