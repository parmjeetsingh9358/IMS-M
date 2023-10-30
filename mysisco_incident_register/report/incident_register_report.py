from odoo import models


class IncidentRegisterXlsx(models.AbstractModel):
    _name = "report.mysisco_incident_register.incident_register_report_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Incident Register Report xlsx"

    def generate_xlsx_report(self, workbook, data, incident):
        sheet = workbook.add_worksheet("Incident Register Report")
        head = workbook.add_format(
            {'bold': True, 'align': 'left', 'bg_color': '#FB5607'})
        cell_text_format = workbook.add_format(
            {'valign': 'top', 'align': 'center', 'text_wrap': True, 'bold': True, 'font_size': 12})
        sheet_investigation = workbook.add_format(
            {'bold': True, 'align': 'left', 'bg_color': '#0077b6'})
        sheet_feedback = workbook.add_format(
            {'bold': True, 'align': 'left', 'bg_color': '#fb8500'})
        date_format = workbook.add_format(
            {
                "num_format": "dd/mm/yyyy",
                "font_name": "Arial",
                "font_size": 10,
                'align': 'left',
            }
        )
        sheet.set_column('A:A', 10)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 10)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 30)
        sheet.set_column('F:F', 30)
        sheet.set_column('G:G', 25)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 20)
        sheet.set_column('K:K', 20)
        sheet.set_column('L:L', 15)
        sheet.set_column('M:M', 15)
        sheet.set_column('N:N', 25)
        sheet.set_column('O:O', 25)
        sheet.set_column('P:P', 30)
        sheet.set_column('Q:Q', 20)
        sheet.set_column('R:R', 20)
        sheet.set_column('S:S', 25)
        sheet.set_column('T:T', 25)
        sheet.set_column('U:U', 25)
        sheet.set_column('V:V', 20)
        sheet.set_column('W:W', 10)
        sheet.set_column('W:W', 15)
        sheet.set_column('X:X', 15)
        sheet.set_column('Y:Y', 15)
        sheet.set_column('Z:Z', 20)

        sheet.set_row(2, 80)
        sheet.freeze_panes(3, 4)

        row = 0
        column = 0
        sheet.merge_range(row, column, row, column + 3, 'Incidents Register for Infinite Ability', head)
        row += 1
        column = 0

        sheet.merge_range(row, column + 12, row, column + 17, "Investigation", sheet_investigation)
        sheet.merge_range(row, column + 18,  row, column + 22, "Feedback", sheet_feedback)
        row += 1

        sheet.write(row, 0, "Incident Number", cell_text_format)
        sheet.write(row, 1, "Participant Name", cell_text_format)
        sheet.write(row, 2, "Date Received", cell_text_format)
        sheet.write(row, 3, "Category", cell_text_format)
        sheet.write(row, 4, "Description of Incident", cell_text_format)
        sheet.write(row, 5, "Impact/Injury to Subject", cell_text_format)
        sheet.write(row, 6, "Immediate action taken to ensure the health and safety and wellbeing of person involved in the incident", cell_text_format)
        sheet.write(row, 7, "Notifications Required to Whom", cell_text_format)
        sheet.write(row, 8, "Type of reportable incident to NDIS Commission", cell_text_format)
        sheet.write(row, 9, "Family, carer, guardian notified", cell_text_format)
        sheet.write(row, 10, "Referred to Authorised Reportable Incidents Notifier/Approver ", cell_text_format)
        sheet.write(row, 11, "Date and Time Advised", cell_text_format)
        sheet.write(row, 12, "Investigation Undertaken into possible causes", cell_text_format)
        sheet.write(row, 13, "Investigation Record of What Happened", cell_text_format)
        sheet.write(row, 14, "Investigation Findings", cell_text_format)
        sheet.write(row, 15, "Outcome / Action following to mitigate further incidents", cell_text_format)
        sheet.write(row, 16, "Investigation Actions Completed", cell_text_format)
        sheet.write(row, 17, "Investigation Action Date Completed", cell_text_format)
        sheet.write(row, 18, "Participant feedback on incident handling process", cell_text_format)
        sheet.write(row, 19, "Participant Feedback Comments", cell_text_format)
        sheet.write(row, 20, "Improvement to Process. Actions Required?", cell_text_format)
        sheet.write(row, 21, "Process improvement Implemented ", cell_text_format)
        sheet.write(row, 22, "Process Improvement Strategies completed (Date)", cell_text_format)
        sheet.write(row, 23, "Status", cell_text_format)
        sheet.write(row, 24, "Date Incident Closed", cell_text_format)
        sheet.write(row, 25, "Links to relevant information", cell_text_format)

        for obj in incident:
            row += 1
            sheet.write(row, 0, obj.name)
            sheet.write(row, 1, obj.partner_name)
            sheet.write(row, 2, obj.date_received, date_format)
            sheet.write(row, 3, ','.join(obj.incident_type.mapped('name')))
            sheet.write(row, 4, obj.description)
            sheet.write(row, 5, obj.subject)
            sheet.write(row, 6, obj.immediate_action)
            sheet.write(row, 7, obj.send_notification_to.name or False)
            sheet.write(row, 8, obj.type_of_reportable.name or False)
            sheet.write(row, 9, dict(obj._fields['guardian_notified'].selection).get(obj.guardian_notified))
            sheet.write(row, 10, dict(obj._fields['referred_to_authorised'].selection).get(obj.referred_to_authorised))
            sheet.write(row, 11, obj.date_advised, date_format)
            sheet.write(row, 12, dict(obj._fields['investigation_possible_causes'].selection).get(obj.investigation_possible_causes))
            sheet.write(row, 13, obj.investigation_desc)
            sheet.write(row, 14, obj.investigation_findings)
            sheet.write(row, 15, obj.outcome_action)
            sheet.write(row, 16, dict(obj._fields['investigation_actions'].selection).get(obj.investigation_actions))
            sheet.write(row, 17, obj.action_complete_date, date_format)
            sheet.write(row, 18, dict(obj._fields['feedback_participat'].selection).get(obj.feedback_participat))
            sheet.write(row, 19, obj.comments)
            sheet.write(row, 20, obj.improvement_process_actions)
            sheet.write(row, 21, dict(obj._fields['process_improvement'].selection).get(obj.process_improvement))
            sheet.write(row, 22, obj.improvement_strategy_date, date_format)
            sheet.write(row, 23, dict(obj._fields['status'].selection).get(obj.status))
            sheet.write(row, 24, obj.closed_date, date_format)
            sheet.write(row, 25, obj.links)

