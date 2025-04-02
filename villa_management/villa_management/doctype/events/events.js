// Copyright (c) 2025, soorya and contributors
// For license information, please see license.txt

frappe.provide("frappe.ui");

frappe.ui.MonthlyEventReport = class MonthlyEventReport {
    constructor() {
        this.make_dialog();
    }

    make_dialog() {
        this.dialog = new frappe.ui.Dialog({
            title: __('Monthly Events Report'),
            fields: [
                {
                    label: __('Month'),
                    fieldname: 'month',
                    fieldtype: 'Date',
                    reqd: 1,
                    default: frappe.datetime.month_start(),
                    options: {
                        date_format: 'YYYY-MM',
                        mode: 'Month'
                    }
                },
                {
                    label: __('Event Type'),
                    fieldname: 'event_type',
                    fieldtype: 'Link',
                    options: 'Event Type'
                }
            ],
            primary_action: ({ month, event_type }) => {
                this.generate_report({
                    month: frappe.datetime.month_start(month),
                    event_type: event_type
                });
            },
            primary_action_label: __('Generate Report')
        });
    }

    show() {
        this.dialog.show();
    }

    generate_report(filters) {
        frappe.call({
            method: 'events.events.get_monthly_event_report',
            args: { filters },
            callback: (r) => {
                if (r.message) {
                    this.render_report(r.message);
                }
            },
            freeze: true,
            freeze_message: __('Generating Monthly Report...')
        });
    }

    render_report(data) {
        this.dialog.hide();
        
        const month_name = frappe.datetime.str_to_user(data.filters.month).split('-')[0];
        const year = frappe.datetime.str_to_user(data.filters.month).split('-')[1];
        
        let html = `
            <div class="monthly-event-report">
                <h3 class="text-center">
                    ${__('Events Report for')} ${month_name} ${year}
                </h3>
                
                <div class="report-summary">
                    <div class="summary-item">
                        <span>${__('Total Events')}:</span>
                        <strong>${data.totals.event_count}</strong>
                    </div>
                    <div class="summary-item">
                        <span>${__('Total Expected Budget')}:</span>
                        <strong>${this.format_currency(data.totals.expected_budget)}</strong>
                    </div>
                    <div class="summary-item">
                        <span>${__('Total Actual Budget')}:</span>
                        <strong>${this.format_currency(data.totals.actual_budget)}</strong>
                    </div>
                    <div class="summary-item">
                        <span>${__('Total Expenses')}:</span>
                        <strong>${this.format_currency(data.totals.total_expense)}</strong>
                    </div>
                </div>
                
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th>${__('Event')}</th>
                            <th>${__('Type')}</th>
                            <th>${__('Date')}</th>
                            <th>${__('Expected Budget')}</th>
                            <th>${__('Actual Budget')}</th>
                            <th>${__('Expenses')}</th>
                            <th>${__('Status')}</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        data.events.forEach(event => {
            html += `
                <tr>
                    <td>${event.event_name || ''}</td>
                    <td>${event.event_type || ''}</td>
                    <td>${event.starts_on ? frappe.datetime.str_to_user(event.starts_on) : ''}</td>
                    <td class="text-right">${this.format_currency(event.expected_budget)}</td>
                    <td class="text-right">${this.format_currency(event.actual_budget)}</td>
                    <td class="text-right">${this.format_currency(event.total_expense)}</td>
                    <td>${event.status || ''}</td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
            </div>
        `;

        this.print_report(html);
    }

    print_report(html) {
        const print_html = `
            <!DOCTYPE html>
            <html>
            <head>
                <title>Monthly Events Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h3 { color: #2e7d32; text-align: center; }
                    .report-summary {
                        display: grid;
                        grid-template-columns: repeat(4, 1fr);
                        gap: 15px;
                        margin: 20px 0;
                    }
                    .summary-item {
                        background: #f5f5f5;
                        padding: 10px;
                        border-radius: 4px;
                        text-align: center;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }
                    th { background-color: #f2f2f2; }
                    .text-right { text-align: right; }
                </style>
            </head>
            <body>
                ${html}
            </body>
            </html>
        `;

        const print_window = window.open('', '_blank');
        print_window.document.write(print_html);
        print_window.document.close();
        setTimeout(() => print_window.print(), 500);
    }

    format_currency(value) {
        return frappe.format(flt(value || 0), { fieldtype: 'Currency' });
    }
};

frappe.ui.form.on("Events", {
    refresh(frm) {
        if (frm.is_list_view()) {
            frm.page.add_menu_item(__('Monthly Report'), () => {
                new frappe.ui.MonthlyEventReport().show();
            });
        }
    }
});