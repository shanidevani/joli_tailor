# -*- encoding: UTF-8 -*-
##############################################################################


from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime


class ConfirmWizard(models.TransientModel):
    _name = "confirm.wizard"
    _description = "Wizard - Confirmation"

    @api.model
    def _default_journal(self):
        journals = self.env['account.journal'].search([('type', '=', 'cash')])
        if journals:
            return journals[0]
        return self.env['account.journal']

    advance_amount = fields.Float('Advance Amount')
    journal_id = fields.Many2one('account.journal', string='Payment Journal', domain=[
                                 ('type', 'in', ('bank', 'cash'))], default=_default_journal)
    map_id = fields.Many2one('tailor.map', string="Tailor Map")

    @api.onchange('advance_amount')
    def onchange_advance_amount(self):
        if self.advance_amount and self.map_id.final_amount < self.advance_amount:
            raise UserError(
                _("Advance amount should be less than Final Amount!"))

    def button_confirm(self):
        seq = self.map_id.name
        if self.map_id.name == 'New' or self.map_id.name == _('New'):
            seq = self.env['ir.sequence'].next_by_code(
                'tailor.map') or _('New')
            self.map_id.name = seq
        if self.advance_amount > 0:
            payment = self.env['account.payment'].with_context(from_rental=True).create(
                {'payment_type': 'inbound',
                 'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                 'partner_type': 'customer',
                 'partner_id': self.map_id.partner_id.id,
                 'amount': self.advance_amount,
                 # 'name': 'TL/IN/' + self.map_id.name,
                 'currency_id': self.env.user.company_id.currency_id.id,
                 'date': datetime.now().date(),
                 'journal_id': self.journal_id.id,
                 'amount_type': 'advance',
                 'map_id': self.map_id.id,
                 })
            payment.action_post()
            self.map_id.advance_amount += self.advance_amount
            self.map_id.state = "confirm"
        return {'type': 'ir.actions.act_window_close'}
