# -*- encoding: UTF-8 -*-
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime


class DeliveryTailorOrderWiz(models.TransientModel):
    _name = "delivery.tailor.order.wiz"
    _description = "Wizard - Delivery Order"

    @api.model
    def _default_journal(self):
        # journals = self.env['account.journal'].search([('type', '=', 'cash')])
        # if journals:
        #     return journals[0]
        return self.env['account.journal']

    line_ids = fields.One2many('delivery.tailor.order.wiz.line', 'wiz_id')
    due_amount = fields.Float("Due Amount")
    map_id = fields.Many2one('tailor.map', string="Tailor Map")
    journal_id = fields.Many2one('account.journal', string='Payment Journal', domain=[
                                 ('type', 'in', ('bank', 'cash'))])
    partial_payment = fields.Boolean('Partially?')

    def select_all(self):
        for line in self.line_ids:
            line.write({'is_deliver': True})
        return {
            'name': _("Delivery Order"),
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'delivery.tailor.order.wiz',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
        }

    def clear_all(self):
        for line in self.line_ids:
            line.write({'is_deliver': False})
        return {
            'name': _("Delivery Order"),
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'delivery.tailor.order.wiz',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
        }

    def delivery_done(self):
        self.ensure_one()
        if not self.journal_id and self.due_amount > 0:
            raise UserError(
                _("Please select Journal!!"))
        if self.due_amount > self.map_id.due_amount:
            raise UserError(
                _("Due Amount is %s only!" % self.map_id.due_amount))
        self.map_id.paid_amount += self.due_amount
        for line in self.line_ids.filtered(lambda l: l.is_deliver):
            if line.shirt_line_id:
                line.shirt_line_id.state = 'done'
            if line.pent_line_id:
                line.pent_line_id.state = 'done'
        state = False
        for record in self.map_id:
            if record.is_shirt and record.shirt_map_ids.filtered(lambda x: x.state != 'done'):
                state = True
            if record.is_pent and record.pent_map_ids.filtered(lambda x: x.state != 'done'):
                state = True
        if self.due_amount > 0:
            payment = self.env['account.payment'].with_context(from_rental=True).create(
                {'payment_type': 'inbound',
                 'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                 'partner_type': 'customer',
                 'partner_id': self.map_id.partner_id.id,
                 'amount': self.due_amount,
                 'currency_id': self.env.user.company_id.currency_id.id,
                 'date': datetime.now().date(),
                 'journal_id': self.journal_id.id,
                 # 'name': 'TL/D/IN/' + self.map_id.name,
                 'amount_type': 'delivery',
                 'map_id': self.map_id.id,
                 })
            payment.action_post()
        if not state:
            self.map_id.state = 'done'
            # self.map_id.create_customer_invoice()
            # self.map_id.create_vendor_bill()
        return {'type': 'ir.actions.act_window_close'}


class DeliveryTailorOrderWizLine(models.TransientModel):
    _name = "delivery.tailor.order.wiz.line"
    _description = "Wizard - Delivery Order Line"

    delivery_date = fields.Date('Delivery Date')
    name = fields.Char('Ref#')
    partner_id = fields.Many2one('res.partner', 'Customer')
    wiz_id = fields.Many2one('delivery.tailor.order.wiz')
    shirt_line_id = fields.Many2one('tailor.shirt.map')
    pent_line_id = fields.Many2one('tailor.pent.map')
    is_deliver = fields.Boolean('Is Deliver?')

    def action_true(self):
        for line in self:
            line.write({'is_deliver': True})
            return {
                'name': _("Delivery Order"),
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'delivery.tailor.order.wiz',
                'res_id': line.wiz_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
            }

    def action_false(self):
        for line in self:
            line.write({'is_deliver': False})
            return {
                'name': _("Delivery Order"),
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'delivery.tailor.order.wiz',
                'res_id': line.wiz_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
            }
