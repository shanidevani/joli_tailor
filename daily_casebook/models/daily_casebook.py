from odoo import models, fields, api
from datetime import datetime

class DailyCaseBook(models.Model):

    _name = 'daily.cash.book'
    _description = "Daily Case Book"
    _rec_name = 'final_total'
 
    date_type = fields.Selection([('today', 'Today'), ('custom', 'Custom')], string='Date Type', default='today', required=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    total_rev = fields.Float(string='Total Received', readonly=True)
    total_paid = fields.Float(string='Total Paid', readonly=True)
    final_total = fields.Float(string='Final Balance', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done')], string="Status")

    vendor_bill = fields.Float(string='Vendor Bill')
    expense = fields.Float(string='Expense')
    customer_invoice = fields.Float(
        string='Customer Invoice')

    @api.model_create_multi
    def create(self, vals):
        res = super(DailyCaseBook, self).create(vals)
        res.compute_all()
        return res

    @api.onchange('date_type', 'start_date', 'end_date')
    def date_type_today(self):
        if self.date_type == 'today':
            self.start_date = str(datetime.today())
            self.end_date = str(datetime.today())

    def compute_all(self):
        domain = [('date', '>=', self.start_date), ('date',
                                                           '<=', self.end_date), ('state', 'in', ['posted', 'reconciled'])]

        for rec in self:
            print("........................................")
            # if rec.ren_total:
            #     customer_domain = [('amount_type', '=', False), ('rental_id', '=', False), ('payment_type', '=', 'inbound')] + domain
            #     # rec.customer_invoice
            #     customer_invoice = self.env['account.payment'].search(
            #         customer_domain)
            #     rec.customer_invoice = sum(
            #         [res.amount for res in customer_invoice if res.amount > 0])

            #     # Expense
            #     expense_domain = [('date', '>=', self.start_date), ('date',
            #                                                    '<=', self.end_date), ('state', 'in', ['done'])]
            #     print("expense_domain", expense_domain)
            #     expense = self.env['hr.expense'].search(expense_domain)
            #     print("expense:::::::::::::;;", expense)
            #     rec.expense = sum(
            #         [res.total_amount for res in expense if res.total_amount > 0])
            #     print("rec.expense:::::::::", rec.expense)

            #     # total_rev
            #     rec.total_rev = rec.ren_advance_amount + rec.ren_deliver_amount + rec.ren_damage
            #     rec.total_rev += rec.customer_invoice
            #     # total_paid
            #     rec.total_paid = rec.ren_refund_advance + \
            #         rec.ren_refund_amount + rec.vendor_bill + rec.expense

            #     # final total
            #     rec.final_total = rec.total_rev - rec.total_paid

            # if rec.ren_total and rec.tailor_total:
            #     customer_domain = [('amount_type', '=', False), ('rental_id', '=', False), (
            #         'map_id', '=', False), ('payment_type', '=', 'inbound')] + domain
            #     # rec.customer_invoice
            #     customer_invoice = self.env['account.payment'].search(
            #         customer_domain)
            #     rec.customer_invoice = sum(
            #         [res.amount for res in customer_invoice if res.amount > 0])

            #     # Expense
            #     expense_domain = [('date', '>=', self.start_date), ('date',
            #                                                    '<=', self.end_date), ('state', '=', 'done')]
            #     expense = self.env['hr.expense'].search(expense_domain)
            #     rec.expense = sum(
            #         [res.total_amount for res in expense if res.total_amount > 0])

            #     # total_rev
            #     rec.total_rev = rec.ren_advance_amount + rec.ren_deliver_amount + rec.ren_damage + rec.tailor_total
            #     rec.total_rev +=  rec.pos_total + rec.customer_invoice

            #     # total_paid
            #     rec.total_paid = rec.ren_refund_advance + \
            #         rec.ren_refund_amount + rec.vendor_bill +  rec.expense

            #     # final total
            #     rec.final_total = rec.total_rev - rec.total_paid

            # if rec.ren_total and rec.tailor_total and rec.safa_total:
            #     customer_domain = [('amount_type', '=', False), ('rental_id', '=', False), ('safa_rental_id', '=', False), (
            #         'map_id', '=', False), ('payment_type', '=', 'inbound')] + domain
            #     # rec.customer_invoice
            #     customer_invoice = self.env['account.payment'].search(
            #         customer_domain)
            #     rec.customer_invoice = sum(
            #         [res.amount for res in customer_invoice if res.amount > 0])

            #     # Expense
            #     expense_domain = [('date', '>=', self.start_date), ('date',
            #                                                    '<=', self.end_date), ('state', '=', 'done')]
            #     expense = self.env['hr.expense'].search(expense_domain)
            #     rec.expense = sum(
            #         [res.total_amount for res in expense if res.total_amount > 0])

            #     # total_rev
            #     rec.total_rev = rec.ren_advance_amount + rec.ren_deliver_amount + rec.ren_damage + \
            #         rec.safa_advance_amount + rec.safa_deliver_amount + rec.safa_damage + rec.tailor_total
            #     rec.total_rev +=  rec.pos_total + rec.customer_invoice

            #     # total_paid
            #     rec.total_paid = rec.ren_refund_advance + \
            #         rec.ren_refund_amount + rec.vendor_bill + rec.expense

            #     # final total
            #     rec.final_total = rec.total_rev - rec.total_paid

            # if rec.ren_total and rec.tailor_total and rec.safa_total and rec.pos_total:
            #     customer_domain = [('amount_type', '=', False), ('rental_id', '=', False), ('safa_rental_id', '=', False), (
            #         'map_id', '=', False), ('payment_type', '=', 'inbound')] + domain
            #     # rec.customer_invoice
            #     customer_invoice = self.env['account.payment'].search(
            #         customer_domain)
            #     rec.customer_invoice = sum(
            #         [res.amount for res in customer_invoice if res.amount > 0])

            #     # Expense
            #     expense_domain = [('date', '>=', self.start_date), ('date',
            #                                                    '<=', self.end_date), ('state', '=', 'done')]
            #     expense = self.env['hr.expense'].search(expense_domain)
            #     print("expence is............",expense )
            #     rec.expense = sum(
            #         [res.total_amount for res in expense if res.total_amount > 0])
            #     print("rec.expense.......", rec.expense)

            #     # total_rev
            #     rec.total_rev = rec.ren_advance_amount + rec.ren_deliver_amount + rec.ren_damage + \
            #         rec.safa_advance_amount + rec.safa_deliver_amount + rec.safa_damage + rec.tailor_total
            #     rec.total_rev +=  rec.pos_total + rec.customer_invoice

            #     # total_paid
            #     rec.total_paid = rec.ren_refund_advance + \
            #         rec.ren_refund_amount + rec.vendor_bill + rec.pos_refund + rec.expense

            #     # final total
            #     rec.final_total = rec.total_rev - rec.total_paid


    def action_vbill_total(self):
        return
        # domain = [('date', '>=', self.start_date), ('date',
        #                                                    '<=', self.end_date), ('state', 'in', ['posted', 'reconciled'])]
        # for rec in self:
        #     journal_pos = self.env['account.journal'].search([('is_expense_journal', '=', True)]).ids
        #     vendor_domain = [('amount_type', '=', False), ('rental_id', '=', False), ('safa_rental_id', '=', False), (
        #         'map_id', '=', False), ('journal_id', 'not in', journal_pos), ('payment_type', '=', 'outbound')] + domain
        # return {
        #     'name': 'Total Vendor Bill Amount',
        #     'domain': (vendor_domain),
        #     'view_type': 'form',
        #     'res_model': 'account.payment',
        #     'view_id': False,
        #     'view_mode': 'tree,form',
        #     'type': 'ir.actions.act_window'
        # }

    def action_cinvoice_total(self):
        return
        # domain = [('date', '>=', self.start_date), ('date',
        #                                                    '<=', self.end_date), ('state', 'in', ['posted', 'reconciled'])]
        # for rec in self:
        #     journal_pos = self.env['account.journal'].search(
        #         [('journal_user', '=', True)]).ids
        #     customer_domain = [('amount_type', '=', False), ('rental_id', '=', False), ('safa_rental_id', '=', False), (
        #         'map_id', '=', False), ('journal_id', 'not in', journal_pos), ('payment_type', '=', 'inbound')] + domain
        # return {
        #     'name': 'Total Customer Invoice Amount',
        #     'domain': (customer_domain),
        #     'view_type': 'form',
        #     'res_model': 'account.payment',
        #     'view_id': False,
        #     'view_mode': 'tree,form',
        #     'type': 'ir.actions.act_window'
        # }

    def action_expense_total(self):
        domain = [('date', '>=', self.start_date), ('date',
                                                           '<=', self.end_date), ('state', '=',  'done')]
#         for rec in self:
#             journal_pos = self.env['account.journal'].search(
#                 [('is_expense_journal', '=', True)]).ids
#             vendor_domain = [('amount_type', '=', False), ('rental_id', '=', False), ('safa_rental_id', '=', False), (
#                 'map_id', '=', False), ('journal_id', 'in', journal_pos), ('payment_type', '=', 'outbound')] + domain
        return {
            'name': 'Total Expense Amount',
            'domain': (domain),
            'view_type': 'form',
            'res_model': 'hr.expense',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

