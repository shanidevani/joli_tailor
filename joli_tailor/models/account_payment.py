# -*- encoding: UTF-8 -*-


from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    map_id = fields.Many2one('tailor.map')
    amount_type = fields.Selection(
        [('advance', 'Advance Amount'), ('delivery', 'Delivery Amount'),
         ('refund_advance', 'Refund Advance'), ('refund', 'Refund Amount')], string='Amount Type')

    _sql_constraints = [
        (
            'check_amount_not_negative',
            'CHECK(1=1)',
            "The payment amount cannot be negative.",
        ),
    ]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        partner_id = self._search(expression.AND([['|', '|', ('name', operator, name), (
            'phone', operator, name), ('mobile', operator, name)], args]), limit=limit, access_rights_uid=name_get_uid)
        return partner_id

    @api.constrains('mobile', 'phone')
    def check_mobile_number(self):
        for res in self:
            if res.mobile:
                if len(res.mobile) != 11:
                    raise UserError(_("Please Enter Valid Mobile Number"))
            if res.phone:
                if len(res.phone) != 11:
                    raise UserError(_("Please Enter Valid Phone Number"))

    @api.model
    def create(self, vals):
        if 'phone' in vals:
            phone_number = vals['phone']
            if len(phone_number) == 10:
                vals['phone'] = str(phone_number)[:5] + ' ' + str(phone_number)[5:]
        if 'mobile' in vals:
            mobile_number = vals['mobile']
            if len(mobile_number) == 10:
                vals['mobile'] = str(mobile_number)[:5] + ' ' + str(mobile_number)[5:]
        res = super(ResPartner, self).create(vals)
        return res