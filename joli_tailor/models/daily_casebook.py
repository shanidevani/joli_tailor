from odoo import models, fields

class DailyCaseBook(models.Model):
    _inherit = 'daily.cash.book'

    tailor_advance_amount = fields.Float(
        string='Advance Amount', readonly=True)
    tailor_deliver_amount = fields.Float(
        string='Deliver Amount', readonly=True)
    tailor_refund_advance = fields.Float(
        string='Refund Advance', readonly=True)
    tailor_refund_amount = fields.Float(
        string='Refund Amount', readonly=True)
    tailor_total = fields.Float(string='Tailor Total', readonly=True)

    def compute_all(self):

        res = super(DailyCaseBook, self).compute_all()

        domain = [('date', '>=', self.start_date), ('date',
                                                           '<=', self.end_date), ('state', 'in', ['posted', 'reconciled'])]
        for rec in self:

            final_advance_amount = [('amount_type', '=', 'advance'), (
                'map_id', '!=', False), ('payment_type', '=', 'inbound')] + domain
            tailor_advance_amount = self.env['account.payment'].search(
                final_advance_amount)
            rec.tailor_advance_amount = sum(
                [res.amount for res in tailor_advance_amount if res.amount > 0])

            final_deliver_amount = [('amount_type', '=', 'delivery'), (
                'map_id', '!=', False), ('payment_type', '=', 'inbound')] + domain
            tailor_deliver_amount = self.env['account.payment'].search(
                final_deliver_amount)
            rec.tailor_deliver_amount = sum(
                [res.amount for res in tailor_deliver_amount if res.amount > 0])

            final_refund_amount1 = [('amount_type', '=', 'refund'), (
                'map_id', '!=', False), ('payment_type', '=', 'outbound')] + domain
            tailor_refund_amount = self.env['account.payment'].search(
                final_refund_amount1)
            rec.tailor_refund_amount = abs(sum(
                [res.amount for res in tailor_refund_amount if res.amount > 0]))

            final_refund_advance = [('amount_type', '=', 'refund_advance'), (
                'map_id', '!=', False), ('payment_type', '=', 'outbound')] + domain
            tailor_refund_advance = self.env['account.payment'].search(
                final_refund_advance)
            rec.tailor_refund_advance = abs(sum(
                [res.amount for res in tailor_refund_advance if res.amount > 0]))

            
            rec.tailor_total = rec.tailor_advance_amount + rec.tailor_deliver_amount -\
                rec.tailor_refund_advance - rec.tailor_refund_amount
                
            final_tailor_total = [('map_id', '!=', False),
                                  ('payment_type', '=', 'inbound')] + domain
            tailor_total = self.env['account.payment'].search(
                final_tailor_total)
            rec.tailor_total = sum(
                [res.amount for res in tailor_total if res.amount > 0])

            if rec.tailor_total:
                customer_domain = [('amount_type', '=', False), (
                    'map_id', '=', False), ('payment_type', '=', 'inbound')] + domain
                # rec.customer_invoice
                customer_invoice = self.env['account.payment'].search(
                    customer_domain)
                rec.customer_invoice = sum(
                    [res.amount for res in customer_invoice if res.amount > 0])

                # Expense
                expense_domain = [('date', '>=', self.start_date), ('date',
                                                               '<=', self.end_date), ('state', '=', 'done')]
                expense = self.env['hr.expense'].search(expense_domain)
                rec.expense = sum(
                    [res.total_amount for res in expense if res.total_amount > 0])

                # total_rev
                rec.total_rev =  rec.tailor_total
                rec.total_rev += rec.customer_invoice

                # total_paid
                rec.total_paid = rec.vendor_bill +  rec.expense

                # final total
                rec.final_total = rec.total_rev - rec.total_paid
        return res


    def action_tailor_advance(self):
        domain = [('date', '>=', self.start_date), ('date',
                                                           '<=', self.end_date), ('state', 'in', ['posted', 'reconciled'])]
        for rec in self:
            final_advance_amount = [('amount_type', '=', 'advance'), (
                'map_id', '!=', False), ('payment_type', '=', 'inbound')] + domain
        return {
            'name': 'Tailor Advance Amount',
            'domain': (final_advance_amount),
            'view_type': 'form',
            'res_model': 'account.payment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    def action_tailor_deliver(self):
        domain = [('date', '>=', self.start_date), ('date',
                                                           '<=', self.end_date), ('state', 'in', ['posted', 'reconciled'])]
        for rec in self:
            final_deliver_amount = [('amount_type', '=', 'delivery'), (
                'map_id', '!=', False), ('payment_type', '=', 'inbound')] + domain
        return {
            'name': 'Tailor Deliver Amount',
            'domain': (final_deliver_amount),
            'view_type': 'form',
            'res_model': 'account.payment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    def action_tailor_refund_amt(self):
        domain = [('date', '>=', self.start_date), ('date',
                                                           '<=', self.end_date), ('state', 'in', ['posted', 'reconciled'])]
        for rec in self:
            final_refund_amount = [('amount_type', '=', 'refund'), (
                'map_id', '!=', False)] + domain
        return {
            'name': 'Tailor Refund Amount',
            'domain': (final_refund_amount),
            'view_type': 'form',
            'res_model': 'account.payment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    def action_tailor_refund_adv(self):
        domain = [('date', '>=', self.start_date), ('date',
                                                           '<=', self.end_date), ('state', 'in', ['posted', 'reconciled'])]
        for rec in self:
            final_refund_advance = [('amount_type', '=', 'refund_advance'), (
                'map_id', '!=', False)] + domain
        return {
            'name': 'Tailor Refund Advance Amount',
            'domain': (final_refund_advance),
            'view_type': 'form',
            'res_model': 'account.payment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    def action_tailor_total(self):
        domain = [('date', '>=', self.start_date), ('date',
                                                           '<=', self.end_date), ('state', 'in', ['posted', 'reconciled'])]
        for rec in self:
            final_tailor_total = [('map_id', '!=', False),
                                  ('payment_type', '=', 'inbound')] + domain
        return {
            'name': 'Total Tailor Amount',
            'domain': (final_tailor_total),
            'view_type': 'form',
            'res_model': 'account.payment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }
