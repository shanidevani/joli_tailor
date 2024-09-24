# -*- encoding: UTF-8 -*-
##############################################################################

from odoo import api, fields, models, _
from datetime import datetime


class RefundAdvanceAmountOrderWiz(models.TransientModel):
    _name = "refund.advance.amount.order.wiz"
    _description = "Wizard - Refund Advance Amount Order"

    journal_id = fields.Many2one('account.journal', string='Payment Journal', domain=[
                                 ('type', 'in', ('bank', 'cash'))])
    # , ('is_deposit_journal', '=', False), ('is_expense_journal', '=', False)
    refund_amount = fields.Float(string="Refund Amount")
    map_id = fields.Many2one('tailor.map', string="Tailor Map")

    def set_refund_amount(self):
        self.ensure_one()
        self.map_id.advance_amount -= self.refund_amount
        if self.refund_amount > 0:
            payment = self.env['account.payment'].with_context(from_rental=True).create(
                {'payment_type': 'outbound',
                 'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                 'partner_type': 'customer',
                 'partner_id': self.map_id.partner_id.id,
                 'amount': -self.refund_amount,
                 'currency_id': self.env.user.company_id.currency_id.id,
                 'date': datetime.now().date(),
                 'journal_id': self.journal_id.id,
                 # 'name': 'R/OUT/' + self.map_id.name,
                 'amount_type': 'refund_advance',
                 'map_id': self.map_id.id,
                 })
            payment.action_post()
        self.map_id.message_post(body=_(
            'Refund Deposit : %s' % self.refund_amount))
        return {'type': 'ir.actions.act_window_close'}
