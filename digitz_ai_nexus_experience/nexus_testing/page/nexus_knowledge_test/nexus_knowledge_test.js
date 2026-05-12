let nexus_session_run_history = [];
let nexus_session_run_counter = 0;
let nexus_loaded_test_cases = [];

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

                <div id="nexus_execution_progress" class="nexus-execution-progress" style="display:none;">
                    <div class="nexus-progress-head">
                        <div>
                            <b id="nexus_progress_title">Running Tests</b>
                            <span id="nexus_progress_subtitle">Preparing execution...</span>
                        </div>
                        <div id="nexus_progress_percent">0%</div>
                    </div>

                    <div class="nexus-progress-track">
                        <div id="nexus_progress_bar" class="nexus-progress-bar" style="width:0%;"></div>
                    </div>

                    <div class="nexus-progress-stats">
                        <span id="nexus_progress_done">Done: 0</span>
                        <span id="nexus_progress_passed">Passed: 0</span>
                        <span id="nexus_progress_failed">Failed: 0</span>
                        <span id="nexus_progress_total">Total: 0</span>
                    </div>
                </div>

                <div class="nexus-workspace-actions">
                    <button class="btn btn-primary" id="nexus_open_manual_input">
                        Manual Test Input
                    </button>

                    <button class="btn btn-default" id="nexus_clear_result">
                        Clear History
                    </button>
                </div>

                <div id="nexus_manual_test_form_holder" style="display:none;">
                    <div class="nexus-lab-card nexus-manual-input-card">
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
                        </div>
                    </div>
                </div>

                <div class="nexus-test-library">
                    <div class="nexus-test-library-head">
                        <div class="nexus-card-title">Executable Test Cases</div>

                        <div class="nexus-test-library-actions">
                            <button class="btn btn-default btn-sm" id="nexus_show_all_tests">
                                Show All
                            </button>

                            <button class="btn btn-danger btn-sm" id="nexus_show_failed_tests">
                                Show Failed
                            </button>

                            <button class="btn btn-warning btn-sm" id="nexus_run_failed_tests">
                                Run Failed Tests
                            </button>

                            <button class="btn btn-primary btn-sm" id="nexus_run_all_tests">
                                Run All Tests
                            </button>
                        </div>
                    </div>

                    <div id="nexus_test_case_cards" class="nexus-test-case-groups">
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
                                    Select a saved test case, load its payload into the observatory, then run a deeper retrieval trace.
                                </span>
                            </div>

                            <div class="nexus-observatory-control-card nexus-observatory-test-loader">
                                <label>Saved Test Case</label>
                                <select id="nexus_observatory_test_case" class="form-control">
                                    <option value="">Loading test cases...</option>
                                </select>

                                <div class="nexus-observatory-loader-actions">
                                    <button class="btn btn-default btn-sm" id="nexus_load_observatory_test_case">
                                        Load Test Case
                                    </button>

                                    <button class="btn btn-warning btn-sm" id="nexus_load_and_run_observatory_test_case">
                                        Load & Run
                                    </button>
                                </div>

                                <div id="nexus_observatory_loaded_hint" class="nexus-observatory-loaded-hint">
                                    No test case loaded yet.
                                </div>
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
        <div class="nexus-history-head">
            <div class="nexus-card-title">Execution History & Results</div>

            <div class="nexus-history-actions">
                <button class="btn btn-default btn-sm active" id="nexus_history_show_all">
                    Show All Results
                </button>

                <button class="btn btn-danger btn-sm" id="nexus_history_show_failed">
                    Show Failed Results
                </button>

                <button class="btn btn-success btn-sm" id="nexus_history_show_passed">
                    Show Passed Results
                </button>
            </div>
        </div>

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

    $('#nexus_open_manual_input').on('click', function() {
        open_manual_test_input_dialog();
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

    $('#nexus_run_failed_tests').on('click', function() {
        run_failed_test_cases();
    });

    $('#nexus_show_all_tests').on('click', function() {
        show_all_test_cases();
    });

    $('#nexus_show_failed_tests').on('click', function() {
        show_failed_test_cases();
    });

    $('#nexus_run_retrieval_evaluation').on('click', function() {
        run_retrieval_evaluation();
    });

    $('#nexus_load_observatory_test_case').on('click', function() {
        load_selected_test_case_to_observatory(false);
    });

    $('#nexus_load_and_run_observatory_test_case').on('click', function() {
        load_selected_test_case_to_observatory(true);
    });

    $(document).on('click', '#nexus_history_show_all', function() {
    filter_execution_history('all');
});

$(document).on('click', '#nexus_history_show_failed', function() {
    filter_execution_history('failed');
});

$(document).on('click', '#nexus_history_show_passed', function() {
    filter_execution_history('passed');
});

    update_history_count();
};

function filter_execution_history(filter_type='all') {
    $('.nexus-history-actions .btn').removeClass('active');

    if (filter_type === 'failed') {
        $('#nexus_history_show_failed').addClass('active');
    } else if (filter_type === 'passed') {
        $('#nexus_history_show_passed').addClass('active');
    } else {
        $('#nexus_history_show_all').addClass('active');
    }

    let visible_count = 0;

    $('.nexus-history-result-card').each(function() {
        const $card = $(this);

        let show = true;

        if (filter_type === 'failed') {
            show = $card.hasClass('failed');
        } else if (filter_type === 'passed') {
            show = $card.hasClass('passed');
        }

        $card.toggle(show);

        if (show) {
            visible_count += 1;
        }
    });

    $('#nexus_history_empty_filter_message').remove();

    if (!visible_count && nexus_session_run_history.length) {
        $('#nexus_history_feed').append(`
            <div id="nexus_history_empty_filter_message" class="nexus-history-empty">
                No ${filter_type} execution result found in this session.
            </div>
        `);
    }
}
function filter_execution_history(filter_type='all') {
    $('.nexus-history-actions .btn').removeClass('active');

    if (filter_type === 'failed') {
        $('#nexus_history_show_failed').addClass('active');
    } else if (filter_type === 'passed') {
        $('#nexus_history_show_passed').addClass('active');
    } else {
        $('#nexus_history_show_all').addClass('active');
    }

    let visible_count = 0;

    $('.nexus-history-result-card').each(function() {
        const $card = $(this);

        let show = true;

        if (filter_type === 'failed') {
            show = $card.hasClass('failed');
        } else if (filter_type === 'passed') {
            show = $card.hasClass('passed');
        }

        $card.toggle(show);

        if (show) {
            visible_count += 1;
        }
    });

    $('#nexus_history_empty_filter_message').remove();

    if (!visible_count && nexus_session_run_history.length) {
        $('#nexus_history_feed').append(`
            <div id="nexus_history_empty_filter_message" class="nexus-history-empty">
                No ${filter_type} execution result found in this session.
            </div>
        `);
    }
}
function open_manual_test_input_dialog() {
    const $form = $('#nexus_manual_test_form_holder .nexus-manual-input-card').detach();

    const dialog = new frappe.ui.Dialog({
        title: 'Manual Test Input',
        size: 'large',
        fields: [
            {
                fieldtype: 'HTML',
                fieldname: 'manual_input_html'
            }
        ]
    });

    dialog.fields_dict.manual_input_html.$wrapper.html($form);

    dialog.onhide = function() {
        $('#nexus_manual_test_form_holder').append($form);
    };

    dialog.show();
}

function show_execution_progress(title, subtitle, total) {
    $('#nexus_execution_progress').show();

    $('#nexus_progress_title').text(title || 'Running Tests');
    $('#nexus_progress_subtitle').text(subtitle || 'Preparing execution...');
    $('#nexus_progress_total').text(`Total: ${total || 0}`);
    $('#nexus_progress_done').text('Done: 0');
    $('#nexus_progress_passed').text('Passed: 0');
    $('#nexus_progress_failed').text('Failed: 0');
    $('#nexus_progress_percent').text('0%');
    $('#nexus_progress_bar').css('width', '0%');
}

function update_execution_progress(done, total, passed, failed, label) {
    const percent = total ? Math.round((done / total) * 100) : 0;

    $('#nexus_progress_subtitle').text(label || 'Executing tests...');
    $('#nexus_progress_done').text(`Done: ${done}`);
    $('#nexus_progress_passed').text(`Passed: ${passed}`);
    $('#nexus_progress_failed').text(`Failed: ${failed}`);
    $('#nexus_progress_total').text(`Total: ${total}`);
    $('#nexus_progress_percent').text(`${percent}%`);
    $('#nexus_progress_bar').css('width', `${percent}%`);
}

function finish_execution_progress(total, passed, failed) {
    const label = failed
        ? `Completed with ${failed} failed test${failed === 1 ? '' : 's'}.`
        : 'Completed successfully.';

    update_execution_progress(total, total, passed, failed, label);
}

function collect_test_cases(filter_failed_only=false) {
    const test_cases = [];

    $('.nexus-test-case-card').each(function() {
        const $card = $(this);

        if (filter_failed_only && !$card.find('.nexus-last-status').hasClass('failed')) {
            return;
        }

        const name = $card.data('name');
        const title = $card.find('h4').text().trim() || name;

        if (name) {
            test_cases.push({
                name: name,
                title: title
            });
        }
    });

    return test_cases;
}

function show_all_test_cases() {
    $('.nexus-test-case-card').show();

    frappe.show_alert({
        message: 'Showing all test cases.',
        indicator: 'blue'
    });
}

function show_failed_test_cases() {
    let visible_count = 0;

    $('.nexus-test-case-card').each(function() {
        const is_failed = $(this).find('.nexus-last-status').hasClass('failed');
        $(this).toggle(is_failed);

        if (is_failed) {
            visible_count += 1;
        }
    });

    if (!visible_count) {
        frappe.show_alert({
            message: 'No failed test cases found.',
            indicator: 'orange'
        });
    }
}

function set_execution_buttons_disabled(disabled) {
    $('#nexus_run_all_tests').prop('disabled', disabled);
    $('#nexus_run_failed_tests').prop('disabled', disabled);
    $('#nexus_show_all_tests').prop('disabled', disabled);
    $('#nexus_show_failed_tests').prop('disabled', disabled);
    $('.nexus-run-test-case').prop('disabled', disabled);
    $('#nexus_run_test').prop('disabled', disabled);
    $('.nexus-observe-test-case').prop('disabled', disabled);
}

function run_retrieval_evaluation() {
    const payload = build_payload();

    if (!payload.query) {
        frappe.msgprint('Please enter a question in the Manual Test Input first.');
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

    show_execution_progress('Running Manual Test', payload.query, 1);
    set_execution_buttons_disabled(true);

    frappe.call({
        method: 'digitz_ai_nexus.api.query.ask',
        args: {
            payload: payload
        },
        callback: function(r) {
            set_execution_buttons_disabled(false);

            if (!r.message) {
                finish_execution_progress(1, 0, 1);
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

            finish_execution_progress(1, passed ? 1 : 0, passed ? 0 : 1);
        },
        error: function(err) {
            set_execution_buttons_disabled(false);
            finish_execution_progress(1, 0, 1);
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
            nexus_loaded_test_cases = r.message || [];
            render_test_case_cards(nexus_loaded_test_cases);
            render_observatory_test_case_selector(nexus_loaded_test_cases);
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

function render_observatory_test_case_selector(test_cases) {
    const $selector = $('#nexus_observatory_test_case');

    if (!$selector.length) return;

    if (!test_cases || !test_cases.length) {
        $selector.html('<option value="">No test cases found</option>');
        return;
    }

    const options = [
        '<option value="">Select a test case...</option>'
    ].concat(
        test_cases.map(tc => {
            const title = frappe.utils.escape_html(tc.test_title || tc.name);
            const name = frappe.utils.escape_html(tc.name);
            const status = frappe.utils.escape_html(tc.last_run_status || 'Not Run');
            return `<option value="${name}">${title} — ${status}</option>`;
        })
    ).join('');

    $selector.html(options);
}

function load_selected_test_case_to_observatory(auto_run=false) {
    const test_case = get_value('nexus_observatory_test_case');

    if (!test_case) {
        frappe.msgprint('Please select a test case first.');
        return;
    }

    load_test_case_payload_to_observatory(test_case, auto_run);
}

function load_test_case_payload_to_observatory(test_case, auto_run=false, test_title='') {
    $('#nexus_retrieval_evaluation_result').html(`
        <div class="nexus-popup-running">
            Loading selected test case into Retrieval Observatory...
        </div>
    `);

    switch_nexus_tab('retrieval');

    frappe.call({
        method: 'digitz_ai_nexus_experience.api.testing.get_test_case_payload',
        args: {
            test_case: test_case
        },
        callback: function(r) {
            if (!r.message || !r.message.payload) {
                $('#nexus_retrieval_evaluation_result').html(`
                    <div class="nexus-popup-failed">
                        Unable to load selected test case payload.
                    </div>
                `);
                return;
            }

            const data = r.message;
            const loadedTitle = data.test_title || test_title || test_case;

            populate_form_from_payload(data.payload);
            $('#nexus_observatory_test_case').val(test_case);
            $('#nexus_observatory_loaded_hint').html(`Loaded: <b>${frappe.utils.escape_html(loadedTitle)}</b>`);

            $('.nexus-test-case-card').removeClass('active');
            $(`.nexus-test-case-card[data-name="${test_case}"]`).addClass('active');

            frappe.show_alert({
                message: `Loaded for observability: ${loadedTitle}`,
                indicator: 'blue'
            });

            if (auto_run) {
                run_retrieval_evaluation();
            } else {
                $('#nexus_retrieval_evaluation_result').html(`
                    <div class="nexus-history-empty">
                        Test case loaded. Click <b>Run Retrieval Observatory</b> to inspect retrieval, grounding, and source selection.
                    </div>
                `);
            }
        },
        error: function(err) {
            $('#nexus_retrieval_evaluation_result').html(`
                <div class="nexus-popup-failed">
                    ${frappe.utils.escape_html(err.message || 'Failed to load selected test case.')}
                </div>
            `);
        }
    });
}

function get_test_case_group(tc) {
    const category = (tc.test_category || '').trim();
    const title = (tc.test_title || tc.name || '').toLowerCase();
    const use_case = (tc.use_case || '').toLowerCase();

    if (title.includes('live') || use_case === 'chat' || category === 'Custom') {
        return 'Nexus Live Operational Validation';
    }

    if (category) {
        return category;
    }

    return 'General Validation';
}

function get_group_description(group) {
    const descriptions = {
        'Public Knowledge': 'Public Q&A and general approved knowledge behavior.',
        'Access Control': 'Role-based access, restricted content, denied chunks, and governance behavior.',
        'Business Unit Scope': 'Business Unit isolation, tenant boundary, and scoped retrieval validation.',
        'Project Scope': 'Project-specific knowledge, strict project retrieval, and general fallback behavior.',
        'Fallback': 'Safe fallback behavior when approved knowledge is not available.',
        'Response Behaviour': 'Answer mode, response style, Q&A behavior, and chatbot behavior validation.',
        'Governance': 'Governance, diagnostics, retrieval readiness, quality, and ingestion validation.',
        'Nexus Live Operational Validation': 'Live Q&A, agent-based chat, routing, escalation, and conversation continuity.',
        'Custom': 'Custom validation scenarios.',
        'General Validation': 'General test cases not assigned to a specific group.'
    };

    return descriptions[group] || 'Grouped Nexus validation scenarios.';
}

function get_group_order(group) {
    const order = [
        'Public Knowledge',
        'Access Control',
        'Business Unit Scope',
        'Project Scope',
        'Fallback',
        'Response Behaviour',
        'Governance',
        'Nexus Live Operational Validation',
        'Custom',
        'General Validation'
    ];

    const index = order.indexOf(group);
    return index === -1 ? 999 : index;
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

    const grouped = {};

    test_cases.forEach(tc => {
        const group = get_test_case_group(tc);

        if (!grouped[group]) {
            grouped[group] = [];
        }

        grouped[group].push(tc);
    });

    const group_names = Object.keys(grouped).sort((a, b) => {
        const order_a = get_group_order(a);
        const order_b = get_group_order(b);

        if (order_a !== order_b) {
            return order_a - order_b;
        }

        return a.localeCompare(b);
    });

    const html = group_names.map(group => {
        const cases = grouped[group] || [];
        const passed_count = cases.filter(tc => tc.last_run_status === 'Passed').length;
        const failed_count = cases.filter(tc => tc.last_run_status === 'Failed').length;
        const not_run_count = cases.length - passed_count - failed_count;

        return `
            <div class="nexus-test-group" data-group="${frappe.utils.escape_html(group)}">
                <div class="nexus-test-group-head">
                    <div>
                        <div class="nexus-test-group-title">
                            ${frappe.utils.escape_html(group)}
                        </div>
                        <div class="nexus-test-group-desc">
                            ${frappe.utils.escape_html(get_group_description(group))}
                        </div>
                    </div>

                    <div class="nexus-test-group-stats">
                        <span>Total ${cases.length}</span>
                        <span class="passed">Passed ${passed_count}</span>
                        <span class="failed">Failed ${failed_count}</span>
                        <span>Not Run ${not_run_count}</span>
                    </div>
                </div>

                <div class="nexus-test-case-grid">
                    ${cases.map(tc => `
                        <div class="nexus-test-case-card" data-name="${frappe.utils.escape_html(tc.name)}" data-group="${frappe.utils.escape_html(group)}">

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

                                    <button class="btn btn-xs btn-warning nexus-observe-test-case"
                                        data-name="${frappe.utils.escape_html(tc.name)}"
                                        data-title="${frappe.utils.escape_html(tc.test_title || tc.name)}">
                                        Observe
                                    </button>

                                    <a class="btn btn-xs btn-default nexus-open-test-case"
                                       href="/app/nexus-test-case/${frappe.utils.escape_html(tc.name)}"
                                       target="_blank">
                                        Open
                                    </a>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }).join('');

    $('#nexus_test_case_cards').html(html);

    $('.nexus-configure-test').on('click', function(e) {
        e.stopPropagation();
        configure_test_case($(this).data('name'));
    });

    $('.nexus-run-test-case').on('click', function(e) {
        e.stopPropagation();
        run_saved_test_case($(this).data('name'), $(this).data('title'));
    });

    $('.nexus-observe-test-case').on('click', function(e) {
        e.stopPropagation();
        observe_test_case($(this).data('name'), $(this).data('title'));
    });

    $('.nexus-test-case-card').on('click', function(e) {
        if ($(e.target).closest('button, a').length) return;
        configure_test_case($(this).data('name'));
    });
}

function observe_test_case(test_case, test_title) {
    if (!test_case) {
        frappe.msgprint('Unable to identify the selected test case.');
        return;
    }

    load_test_case_payload_to_observatory(test_case, true, test_title);
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

function run_test_case_for_progress(test_case, test_title, compact=true) {
    return new Promise(resolve => {
        frappe.call({
            method: 'digitz_ai_nexus_experience.api.testing.run_test_case',
            args: {
                test_case: test_case
            },
            callback: function(r) {
                const data = r.message || {};
                const result = data.result || {};

                if (data.payload) {
                    populate_form_from_payload(data.payload);
                }

                add_run_history_entry(
                    data.test_title || test_title || test_case,
                    result,
                    !!data.passed,
                    data.failure_reason || '',
                    data.payload || {},
                    compact,
                    false
                );

                resolve({
                    passed: !!data.passed,
                    data: data
                });
            },
            error: function(err) {
                const message = err.message || 'Saved test case failed.';

                const result = {
                    status: 'failed',
                    access_status: '-',
                    answer: message,
                    sources: [],
                    log: ''
                };

                add_run_history_entry(
                    test_title || test_case,
                    result,
                    false,
                    message,
                    {},
                    compact,
                    false
                );

                resolve({
                    passed: false,
                    error: message
                });
            }
        });
    });
}

async function run_saved_test_case(test_case, test_title) {
    show_execution_progress(
        'Running Test',
        test_title || test_case,
        1
    );

    set_execution_buttons_disabled(true);

    const outcome = await run_test_case_for_progress(test_case, test_title, false);

    set_execution_buttons_disabled(false);

    finish_execution_progress(1, outcome.passed ? 1 : 0, outcome.passed ? 0 : 1);

    switch_nexus_tab('history');
    load_test_cases();
}

async function run_all_test_cases() {
    const test_cases = collect_test_cases(false);

    if (!test_cases.length) {
        frappe.msgprint('No test cases found to run.');
        return;
    }

    await run_test_case_batch(test_cases, 'Running All Tests');
}

async function run_failed_test_cases() {
    const test_cases = collect_test_cases(true);

    if (!test_cases.length) {
        frappe.msgprint('No failed test cases found.');
        return;
    }

    await run_test_case_batch(test_cases, 'Running Failed Tests');
}

async function run_test_case_batch(test_cases, title) {
    let done = 0;
    let passed = 0;
    let failed = 0;

    show_execution_progress(
        title,
        'Starting test execution...',
        test_cases.length
    );

    set_execution_buttons_disabled(true);

    for (const tc of test_cases) {
        update_execution_progress(
            done,
            test_cases.length,
            passed,
            failed,
            `Running: ${tc.title}`
        );

        const outcome = await run_test_case_for_progress(tc.name, tc.title, false);

        done += 1;

        if (outcome.passed) {
            passed += 1;
        } else {
            failed += 1;
        }

        update_execution_progress(
            done,
            test_cases.length,
            passed,
            failed,
            `Completed: ${tc.title}`
        );
    }

    set_execution_buttons_disabled(false);
    finish_execution_progress(test_cases.length, passed, failed);

    switch_nexus_tab('history');
    load_test_cases();
}

function build_result_output_html(title, result, passed, failure_reason, payload, compact=false) {
    const payload_raw = JSON.stringify(payload || {}, null, 2);
    const result_raw = JSON.stringify(result || {}, null, 2);

    const combined_raw = [
        'FAILURE REASON',
        failure_reason || '-',
        '',
        'PAYLOAD',
        payload_raw,
        '',
        'RAW RESULT',
        result_raw
    ].join('\n');

    const combined_text = frappe.utils.escape_html(combined_raw);

    return `
        <div class="${passed ? 'nexus-popup-passed' : 'nexus-popup-failed'}">
            ${frappe.utils.escape_html(title || 'Test Result')}
            <span style="float:right;">${passed ? 'Passed' : 'Failed'}</span>
        </div>

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

        <div class="nexus-combined-actions">
            <button class="btn btn-xs btn-default nexus-history-toggle">
                View Combined Diagnostics
            </button>

            <button class="btn btn-xs btn-primary nexus-copy-diagnostics">
                Copy Combined Diagnostics
            </button>
        </div>

        <div class="nexus-history-details" style="display:none;">
            <pre class="nexus-popup-code nexus-combined-diagnostics-code">${combined_text}</pre>
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

        ${build_source_preview_html(sources, denied)}

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

function build_source_preview_html(sources, denied=[]) {
    if (sources && sources.length) {
        return `
            <div class="nexus-debug-section">
                <div class="nexus-popup-title">Grounded Sources Used in Answer</div>

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

    if (denied && denied.length) {
        return `
            <div class="nexus-debug-section nexus-governance-block-section">
                <div class="nexus-popup-title">Governance Blocked Sources</div>

                <div class="nexus-governance-block-summary">
                    Nexus retrieved candidate chunks, but access governance denied them. Therefore no grounded answer sources were selected.
                </div>

                <div class="nexus-governance-block-list">
                    ${denied.map((item, index) => {
                        const reason = item.reason || item.denied_reason || item.access_reason || 'Access denied by governance policy.';
                        const policy = item.access_policy || item.policy || '-';
                        const contextPath = item.context_path || item.context || item.source_context || '';
                        const requiredRoles = item.allowed_roles || item.required_roles || item.roles_allowed || '';
                        const excludedRoles = item.excluded_roles || item.denied_roles || item.roles_denied || '';

                        return `
                            <div class="nexus-governance-block-card">
                                <div class="nexus-governance-block-head">
                                    <b>Blocked Chunk #${index + 1}</b>
                                    <span>${frappe.utils.escape_html(item.chunk || item.name || '-')}</span>
                                </div>

                                <div class="nexus-governance-block-reason">
                                    ${frappe.utils.escape_html(reason)}
                                </div>

                                <div class="nexus-governance-meta-grid">
                                    <div>
                                        <label>Access Policy</label>
                                        <span>${frappe.utils.escape_html(policy)}</span>
                                    </div>
                                    <div>
                                        <label>Required Roles</label>
                                        <span>${frappe.utils.escape_html(format_debug_value(requiredRoles) || '-')}</span>
                                    </div>
                                    <div>
                                        <label>Denied Roles</label>
                                        <span>${frappe.utils.escape_html(format_debug_value(excludedRoles) || '-')}</span>
                                    </div>
                                    <div>
                                        <label>Context Path</label>
                                        <span>${frappe.utils.escape_html(contextPath || '-')}</span>
                                    </div>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    }

    return `
        <div class="nexus-debug-section">
            <div class="nexus-popup-title">Grounded Sources Used in Answer</div>
            <div class="nexus-history-empty">
                No grounded sources were selected for this answer.
            </div>
        </div>
    `;
}

function format_debug_value(value) {
    if (!value) return '';

    if (Array.isArray(value)) {
        return value.join(', ');
    }

    if (typeof value === 'object') {
        return JSON.stringify(value);
    }

    return String(value);
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
        $(this)
            .closest('.nexus-history-result-card')
            .find('.nexus-history-details')
            .first()
            .toggle();
    });

    $('.nexus-copy-diagnostics').off('click').on('click', function() {
        const text = $(this)
            .closest('.nexus-history-result-card')
            .find('.nexus-combined-diagnostics-code')
            .first()
            .text();

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(() => {
                frappe.show_alert({
                    message: 'Combined diagnostics copied.',
                    indicator: 'green'
                });
            });
        } else {
            frappe.utils.copy_to_clipboard(text);
            frappe.show_alert({
                message: 'Combined diagnostics copied.',
                indicator: 'green'
            });
        }
    });

    filter_execution_history(
    $('#nexus_history_show_failed').hasClass('active')
        ? 'failed'
        : $('#nexus_history_show_passed').hasClass('active')
            ? 'passed'
            : 'all'
);
}
function bind_nexus_history_actions() {
    $('.nexus-history-toggle').off('click').on('click', function() {
        $(this).siblings('.nexus-history-details').toggle();
    });

    $('.nexus-copy-diagnostics').off('click').on('click', function() {
        const text = $(this).attr('data-copy') || '';

        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(() => {
                frappe.show_alert({
                    message: 'Diagnostics copied to clipboard.',
                    indicator: 'green'
                });
            });
        } else {
            frappe.utils.copy_to_clipboard(text);
            frappe.show_alert({
                message: 'Diagnostics copied to clipboard.',
                indicator: 'green'
            });
        }
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
    $('#nexus_execution_progress').hide();
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

            .nexus-workspace-actions {
                display: flex;
                justify-content: flex-end;
                gap: 10px;
                margin-bottom: 16px;
            }

            .nexus-test-library-actions {
                display: flex;
                align-items: center;
                justify-content: flex-end;
                gap: 10px;
            }

            .nexus-execution-progress {
                margin-bottom: 18px;
                padding: 18px;
                border-radius: 20px;
                background:
                    radial-gradient(circle at 8% 20%, rgba(224,166,47,.16), transparent 28%),
                    linear-gradient(135deg, #f8fbff, #eef6ff);
                border: 1px solid rgba(77,163,255,.32);
                box-shadow: 0 12px 28px rgba(33,77,187,.08);
            }

            .nexus-progress-head {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 14px;
                margin-bottom: 12px;
            }

            .nexus-progress-head b {
                display: block;
                color: #102b67;
                font-size: 16px;
                font-weight: 950;
            }

            .nexus-progress-head span {
                display: block;
                color: #53688f;
                font-size: 12px;
                font-weight: 800;
                margin-top: 4px;
            }

            #nexus_progress_percent {
                min-width: 58px;
                height: 38px;
                border-radius: 999px;
                background: #214dbb;
                color: #fff;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 950;
            }

            .nexus-progress-track {
                height: 12px;
                border-radius: 999px;
                overflow: hidden;
                background: #dbeafe;
                border: 1px solid rgba(33,77,187,.12);
            }

            .nexus-progress-bar {
                height: 100%;
                border-radius: 999px;
                background: linear-gradient(90deg, #214dbb, #4da3ff, #e0a62f);
                transition: width .25s ease;
            }

            .nexus-progress-stats {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 12px;
            }

            .nexus-progress-stats span {
                padding: 7px 11px;
                border-radius: 999px;
                background: #ffffff;
                color: #27416f;
                border: 1px solid rgba(77,163,255,.22);
                font-size: 12px;
                font-weight: 900;
            }

            .nexus-test-library,
            .nexus-lab-card {
                border: 1px solid rgba(77, 163, 255, 0.28);
                border-radius: 22px;
                background: #fff;
                padding: 20px;
                box-shadow: 0 12px 30px rgba(33, 77, 187, 0.07);
            }

            .nexus-manual-input-card {
                box-shadow: none;
                margin: 0;
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

            .nexus-test-case-groups {
                display: grid;
                gap: 18px;
            }

            .nexus-test-group {
                padding: 16px;
                border-radius: 22px;
                background:
                    radial-gradient(circle at 4% 0%, rgba(224,166,47,.10), transparent 28%),
                    linear-gradient(180deg, #ffffff, #f8fbff);
                border: 1px solid rgba(77, 163, 255, 0.26);
                box-shadow: 0 10px 24px rgba(33,77,187,.05);
            }

            .nexus-test-group-head {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 14px;
                margin-bottom: 14px;
                padding: 12px 14px;
                border-radius: 18px;
                background: linear-gradient(135deg, #eef6ff, #ffffff);
                border: 1px solid rgba(77, 163, 255, 0.22);
            }

            .nexus-test-group-title {
                color: #102b67;
                font-size: 17px;
                font-weight: 950;
                letter-spacing: -0.01em;
            }

            .nexus-test-group-desc {
                margin-top: 5px;
                color: #53688f;
                font-size: 12px;
                font-weight: 750;
                line-height: 1.45;
            }

            .nexus-test-group-stats {
                display: flex;
                flex-wrap: wrap;
                justify-content: flex-end;
                gap: 7px;
                min-width: 280px;
            }

            .nexus-test-group-stats span {
                padding: 6px 10px;
                border-radius: 999px;
                background: #ffffff;
                border: 1px solid rgba(77, 163, 255, 0.20);
                color: #27416f;
                font-size: 11px;
                font-weight: 900;
                white-space: nowrap;
            }

            .nexus-test-group-stats span.passed {
                background: #ecfdf3;
                color: #16794c;
                border-color: #bdebd2;
            }

            .nexus-test-group-stats span.failed {
                background: #fff0f0;
                color: #b42318;
                border-color: #ffd1d1;
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
                flex-wrap: wrap;
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
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
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

            .nexus-governance-meta-grid,
                .nexus-source-preview-meta {
                    grid-template-columns: 1fr;
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

            .nexus-governance-block-section {
                padding: 16px;
                border-radius: 18px;
                background: #fff7e6;
                border: 1px solid #f2d49b;
            }

            .nexus-governance-block-summary {
                padding: 13px 14px;
                border-radius: 14px;
                background: #fff0f0;
                border: 1px solid #ffd1d1;
                color: #b42318;
                font-weight: 900;
                line-height: 1.55;
                margin-bottom: 14px;
            }

            .nexus-governance-block-list {
                display: grid;
                gap: 12px;
            }

            .nexus-governance-block-card {
                padding: 15px;
                border-radius: 16px;
                background: #ffffff;
                border: 1px solid rgba(180,35,24,.18);
                box-shadow: 0 8px 18px rgba(180,35,24,.05);
            }

            .nexus-governance-block-head {
                display: flex;
                justify-content: space-between;
                gap: 12px;
                margin-bottom: 10px;
            }

            .nexus-governance-block-head b {
                color: #b42318;
                font-weight: 950;
            }

            .nexus-governance-block-head span {
                color: #53688f;
                font-size: 12px;
                font-weight: 900;
            }

            .nexus-governance-block-reason {
                padding: 10px 12px;
                border-radius: 12px;
                background: #fff0f0;
                color: #8a1f16;
                border: 1px solid #ffd1d1;
                font-weight: 850;
                line-height: 1.5;
                margin-bottom: 12px;
            }

            .nexus-governance-meta-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 8px;
            }

            .nexus-governance-meta-grid > div {
                padding: 9px;
                border-radius: 12px;
                background: #f8fbff;
                border: 1px solid rgba(77,163,255,.18);
            }

            .nexus-governance-meta-grid label {
                display: block;
                color: #53688f;
                font-size: 10px;
                font-weight: 900;
                text-transform: uppercase;
                margin-bottom: 4px;
            }

            .nexus-governance-meta-grid span {
                color: #173b8c;
                font-size: 12px;
                font-weight: 900;
                word-break: break-word;
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

            .nexus-observatory-loader-actions {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 8px;
                margin-top: 10px;
            }

            .nexus-observatory-loader-actions .btn {
                border-radius: 999px;
                font-weight: 900;
            }

            .nexus-observatory-loaded-hint {
                margin-top: 10px;
                padding: 10px 11px;
                border-radius: 12px;
                background: #fff7e6;
                border: 1px solid #f2d49b;
                color: #8a5d00;
                font-size: 12px;
                font-weight: 800;
                line-height: 1.45;
            }

            .nexus-observatory-loaded-hint b {
                color: #173b8c;
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

            .nexus-combined-diagnostics {
                margin-top: 10px;
                padding: 14px;
                border-radius: 16px;
                background: #f8fbff;
                border: 1px solid rgba(77, 163, 255, 0.22);
            }

            .nexus-copy-diagnostics {
                margin-top: 14px;
                margin-left: 8px;
            }

            .nexus-combined-actions {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 14px;
            }

            .nexus-combined-diagnostics-code {
                max-height: 420px;
                white-space: pre-wrap;
            }

            .nexus-history-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
}

.nexus-history-head .nexus-card-title {
    margin-bottom: 0;
}

.nexus-history-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

    .nexus-history-actions .btn {
        border-radius: 999px;
        font-weight: 900;
    }

    .nexus-history-actions .btn.active {
        box-shadow: 0 8px 18px rgba(33, 77, 187, 0.16);
        transform: translateY(-1px);
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

                .nexus-tab-bar,
                .nexus-test-library-head,
                .nexus-test-library-actions,
                .nexus-workspace-actions,
                .nexus-test-group-head {
                    flex-direction: column;
                    align-items: stretch;
                }

                .nexus-test-group-stats {
                    justify-content: flex-start;
                    min-width: 0;
                }

                .nexus-tab-btn,
                .nexus-test-library-actions .btn,
                .nexus-workspace-actions .btn {
                    width: 100%;
                }

                .nexus-observatory-header {
                    flex-direction: column;
                }
            }
        </style>
    `);


}
