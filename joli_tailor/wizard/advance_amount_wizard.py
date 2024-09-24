# -*- encoding: UTF-8 -*-
##############################################################################


from odoo import api, fields, models
from datetime import datetime


class AdvanceAmountTailorWiz(models.TransientModel):
    _name = "advance.amount.tailor.wiz"
    _description = "Wizard - Tailor Advance Amount"

    advance_amount = fields.Float(string="Advance Amount")
    delivery_amount = fields.Float(string="Delivery Amount")
    journal_id = fields.Many2one('account.journal', string='Payment Journal', domain=[
                                 ('type', 'in', ('bank', 'cash'))])
    map_id = fields.Many2one('tailor.map', string="tailor #")

    def update_advance_amount(self):
        self.ensure_one()
        self.map_id.advance_amount += self.advance_amount
        self.map_id.paid_amount += self.delivery_amount
        if self.advance_amount > 0:
            payment = self.env['account.payment'].with_context(from_rental=True).create(
                {'payment_type': 'inbound',
                 'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                 'partner_type': 'customer',
                 'partner_id': self.map_id.partner_id.id,
                 'amount': self.advance_amount,
                 'currency_id': self.env.user.company_id.currency_id.id,
                 'date': datetime.now().date(),
                 'journal_id': self.journal_id.id,
                 # 'name': 'TL/IN/' + self.map_id.name,
                 'amount_type': 'advance',
                 'map_id': self.map_id.id
                 })
            payment.action_post()
        if self.advance_amount < 0:
            payment = self.env['account.payment'].with_context(from_rental=True).create(
                {'payment_type': 'outbound',
                 'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                 'partner_type': 'customer',
                 'partner_id': self.map_id.partner_id.id,
                 'amount': -self.advance_amount,
                 'currency_id': self.env.user.company_id.currency_id.id,
                 'date': datetime.now().date(),
                 'journal_id': self.journal_id.id,
                 # 'name': 'TL/OUT/' + self.map_id.name,
                 'amount_type': 'refund_advance',
                 'map_id': self.map_id.id
                 })
            payment.action_post()
        if self.delivery_amount > 0:
            payment = self.env['account.payment'].with_context(from_rental=True).create(
                {'payment_type': 'inbound',
                 'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                 'partner_type': 'customer',
                 'partner_id': self.map_id.partner_id.id,
                 'amount': self.delivery_amount,
                 'currency_id': self.env.user.company_id.currency_id.id,
                 'date': datetime.now().date(),
                 'journal_id': self.journal_id.id,
                 # 'name': 'TL/D/IN/' + self.map_id.name,
                 'amount_type': 'delivery',
                 'map_id': self.map_id.id
                 })
            payment.action_post()
        if self.delivery_amount < 0:
            payment = self.env['account.payment'].with_context(from_rental=True).create(
                {'payment_type': 'outbound',
                 'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                 'partner_type': 'customer',
                 'partner_id': self.map_id.partner_id.id,
                 'amount': -self.delivery_amount,
                 'currency_id': self.env.user.company_id.currency_id.id,
                 'date': datetime.now().date(),
                 'journal_id': self.journal_id.id,
                 # 'name': 'TL/D/OUT/' + self.map_id.name,
                 'amount_type': 'refund',
                 'map_id': self.map_id.id,
                 })
            payment.action_post()
        return {'type': 'ir.actions.act_window_close'}
