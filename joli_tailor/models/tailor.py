# -*- encoding: UTF-8 -*-
##############################################################################

from odoo import models, fields, _, api
from odoo.exceptions import UserError
from datetime import datetime
from werkzeug.urls import url_encode
import uuid


class TailorMap(models.Model):
    _name = 'tailor.map'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Trailor Map'
    _order = 'id desc'

    @api.depends('total_charge', 'paid_amount', 'discount', 'advance_amount')
    def get_final_amount(self):
        for res in self:
            res.final_amount = res.total_charge - res.discount
            res.due_amount = res.final_amount - res.advance_amount - res.paid_amount

    @api.depends('shirt_map_ids', 'pent_map_ids', 'kurto_map_ids', 'pathani_map_ids', 'lengho_map_ids', 'chorni_map_ids',
                 'blazer_map_ids', 'coti_map_ids', 'shirt_map_ids.charge', 'pent_map_ids.charge', 'kurto_map_ids.charge', 'pathani_map_ids.charge',
                 'lengho_map_ids.charge', 'chorni_map_ids.charge', 'coti_map_ids.charge', 'blazer_map_ids.charge', 'fancy_button_charge', 'greep_charge', 'chirel_pocket_charge')
    def get_total_charge(self):
        for res in self:
            res.total_shirt_charge = sum([x.charge for x in res.shirt_map_ids])
            res.total_pent_charge = sum([x.charge for x in res.pent_map_ids])
            res.total_kurto_charge = sum([x.charge for x in res.kurto_map_ids])
            res.total_pathani_charge = sum([x.charge for x in res.pathani_map_ids])
            res.total_lengho_charge = sum([x.charge for x in res.lengho_map_ids])
            res.total_chorni_charge = sum([x.charge for x in res.chorni_map_ids])
            res.total_blazer_charge = sum([x.charge for x in res.blazer_map_ids])
            res.total_coti_charge = sum([x.charge for x in res.coti_map_ids])
            total_charge = res.total_shirt_charge + res.total_pent_charge + res.total_kurto_charge +\
                res.total_pathani_charge + res.total_lengho_charge + res.total_chorni_charge +\
                res.total_blazer_charge + res.total_coti_charge + res.fancy_button_charge +\
                res.greep_charge + res.chirel_pocket_charge
            res.total_charge = total_charge

    name = fields.Char(string="Name", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    mobile1 = fields.Char(string="Mobile No1", required=True, store=True)
    mobile2 = fields.Char(string="Mobile No2", store=True)
    address = fields.Text(string="Address")
    order_date = fields.Date('Booking Date', default=fields.Date.today())
    delivery_date = fields.Date(string="Delivery Date", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='Status', readonly=True, copy=False, index=True, default='draft')
    total_charge = fields.Float(string="Subtotal", compute="get_total_charge", store=True, copy=False)
    paid_amount = fields.Float(string="Paid Amount", readonly=True, copy=False)
    advance_amount = fields.Float(string="Advance Amount", readonly=True, copy=False)
    final_amount = fields.Float(string="Final Amount", compute="get_final_amount", store=True, readonly=True, copy=False)
    discount = fields.Float(string="Discount")
    due_amount = fields.Float(string="Due amount", compute="get_final_amount", store=True, copy=False)
    invoice_id = fields.Many2one('account.move')
    payment_ids = fields.One2many('account.payment', 'map_id', string="Payments")
    payment_count = fields.Integer(string='Payment Count', compute='_get_payment_ids', readonly=True)
    map_require = fields.Boolean(string="Map Required", default=True)
    is_advance = fields.Boolean('Is Advance?')

    remarks = fields.Text('Remarks')    
    is_shirt = fields.Boolean(string="શર્ટ (Shirt)", tracking=True)
    shirt_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)
    total_shirt = fields.Integer(
        string="Total Shirt", compute="get_total_charge", store=True)
    shirt_map_ids = fields.One2many('tailor.shirt.map', 'tailor_map_id')
    total_shirt_charge = fields.Float(
        string="Total Shirt Charge", compute="get_total_charge", store=True)

    is_pair = fields.Boolean(string="જોડી (Pair)", tracking=True)
    pair_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)

    is_pent = fields.Boolean(string="પેન્ટ (Pent)", tracking=True)
    pent_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)
    total_pent = fields.Integer(
        string="Total Pent", compute="get_total_charge", store=True)
    pent_map_ids = fields.One2many('tailor.pent.map', 'tailor_map_id')
    total_pent_charge = fields.Float(
        string="Total Pent Charge", compute="get_total_charge", store=True)

    is_kurto = fields.Boolean(string="કુર્તો (Kurto)", tracking=True)
    kurto_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)
    total_kurto = fields.Integer(
        string="Total Kurto", compute="get_total_charge", store=True)
    kurto_map_ids = fields.One2many('tailor.kurto.map', 'tailor_map_id')
    total_kurto_charge = fields.Float(
        string="Total Kurto Charge", compute="get_total_charge", store=True)
        
    is_pathani = fields.Boolean(string="પઠાણી (Pathani)", tracking=True)
    pathani_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)
    total_pathani = fields.Integer(
        string="Total Pathani", compute="get_total_charge", store=True)
    pathani_map_ids = fields.One2many('tailor.pathani.map', 'tailor_map_id')
    total_pathani_charge = fields.Float(
        string="Total Pathani Charge", compute="get_total_charge", store=True)

    is_lengho = fields.Boolean(string="લેંઘો (Lengho)", tracking=True)
    lengho_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)
    total_lengho = fields.Integer(
        string="Total Lengho", compute="get_total_charge", store=True)
    lengho_map_ids = fields.One2many('tailor.lengho.map', 'tailor_map_id')
    total_lengho_charge = fields.Float(
        string="Total Lengho Charge", compute="get_total_charge", store=True)

    is_chorni = fields.Boolean(string="ચોરણી (Chorni)", tracking=True)
    chorni_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)
    total_chorni = fields.Integer(
        string="Total Chorni", compute="get_total_charge", store=True)
    chorni_map_ids = fields.One2many('tailor.chorni.map', 'tailor_map_id')
    total_chorni_charge = fields.Float(
        string="Total Chorni Charge", compute="get_total_charge", store=True)

    is_blazer = fields.Boolean(string="બ્લૅઝર (Blazer)", tracking=True)
    blazer_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)
    total_blazer = fields.Integer(
        string="Total Blazer", compute="get_total_charge", store=True)
    blazer_map_ids = fields.One2many('tailor.blazer.map', 'tailor_map_id')
    total_blazer_charge = fields.Float(
        string="Total Blazer Charge", compute="get_total_charge", store=True)

    is_coti = fields.Boolean(string="કોટી (Coti)", tracking=True)
    coti_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)
    total_coti = fields.Integer(
        string="Total Coti", compute="get_total_charge", store=True)
    coti_map_ids = fields.One2many('tailor.coti.map', 'tailor_map_id')
    total_coti_charge = fields.Float(
        string="Total Coti Charge", compute="get_total_charge", store=True)

    is_fancy_button = fields.Boolean(string="ફેન્સી બટન(Fancy Button)", tracking=True)
    fancy_button_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)

    is_greep = fields.Boolean(string="ગ્રીપ (Greep)", tracking=True)
    greep_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)

    is_chirel_pocket = fields.Boolean(String="ચિરેલ પોકેટ(Chirel Pocket)", tracking=True)
    chirel_pocket_qty = fields.Integer(string="Quantity", readonly=True, tracking=True)

    shirt_charge = fields.Float(string="Total Shirt Charge", compute="get_charge", store=True, tracking=True)
    pair_charge = fields.Float(string="Total Pair Charge", compute="get_charge", store=True, tracking=True)
    pent_charge = fields.Float(string="Total Pent Charge", compute="get_charge", store=True, tracking=True)
    kurto_charge = fields.Float(string="Total Kurto Charge", compute="get_charge", store=True, tracking=True)
    pathani_charge = fields.Float(string="Total Pathani Charge", compute="get_charge", store=True, tracking=True)
    lengho_charge = fields.Float(string="Total Lengho Charge", compute="get_charge", store=True, tracking=True)
    chorni_charge = fields.Float(string="Total Chorni Charge", compute="get_charge", store=True, tracking=True)
    blazer_charge = fields.Float(string="Total Blazer Charge", compute="get_charge", store=True, tracking=True)
    coti_charge = fields.Float(string="Total Coti Charge", compute="get_charge", store=True, tracking=True)
    fancy_button_charge = fields.Float(string="Total Fancy Button Charge", compute="get_charge", store=True, tracking=True)
    chirel_pocket_charge = fields.Float(string="Total Chirel Pocket Charge", compute="get_charge", store=True, tracking=True)
    greep_charge = fields.Float(string="Total Greep Charge", compute="get_charge", store=True, tracking=True)
    total_qty_shirt_charge = fields.Float(string="Total Shirt Charge", compute="get_charge", store=True, tracking=True)
    total_qty_pent_charge = fields.Float(string="Total Pent Charge", compute="get_charge", store=True, tracking=True)

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company, required=True)
    # access_url = fields.Char('Portal Access URL', compute='_compute_access_url', help='Customer Portal URL')
    # access_token = fields.Char('Security Token', copy=False)

    @api.model
    def create(self, vals):
        if 'mobile1' in vals:
            mobile1_number = vals['mobile1']
            # mobile1_number = mobile1_number.replace(" ", "").replace("+", "").strip()
            if len(mobile1_number) == 10:
                vals['mobile1'] = str(mobile1_number)[:5] + ' ' + str(mobile1_number)[5:]
            print("jjahdgjag :- ", mobile1_number)
        if 'mobile2' in vals:
            mobile2_number = vals['mobile2']
            # mobile2_number = mobile2_number.replace(" ", "").replace("+", "").strip()
            if len(mobile2_number) == 10:
                vals['mobile2'] = str(mobile2_number)[:5] + ' ' + str(mobile2_number)[5:]
            print("hdjdhddhdhdhd :- ", mobile2_number)
        res = super(TailorMap, self).create(vals)
        return res

    def action_preview_tailor(self):
        return {
            'target': 'new',
            'type': 'ir.actions.act_url',
            'url': '/report/pdf/joli_tailor.report_tailor_customer_receipt/%s' % self.id
        }

    def action_preview_map(self):
        return {
            'target': 'new',
            'type': 'ir.actions.act_url',
            'url': '/report/pdf/joli_tailor.report_tailor_map_receipt/%s' % self.id
        }

    # @api.multi
    def _compute_access_url(self):
        for record in self:
            record.access_url = '/orders/'

    # @api.multi
    # def preview_tailor(self):
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'target': 'new',
    #         'url': self._get_share_url(),
    #     }

    # @api.multi
    # def _get_share_url(self, redirect=False, signup_partner=False, pid=None):
    #     """Override for rental order.

    #     If the SO is in a state where an action is required from the partner,
    #     return the URL with a login token. Otherwise, return the URL with a
    #     generic access token (no login).
    #     """
    #     self.ensure_one()
    #     if self.state not in ['draft', 'cancel']:
    #         auth_param = url_encode(self.partner_id.signup_get_auth_param()[self.partner_id.id])
    #         return self.get_entered_portal_url(query_string='&%s' % auth_param)

    # @api.multi
    # def get_entered_portal_url(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
    #     """
    #         Get a portal url for this model, including access_token.
    #         The associated route must handle the flags for them to have any effect.
    #         - suffix: string to append to the url, before the query string
    #         - report_type: report_type query string, often one of: html, pdf, text
    #         - download: set the download query string to true
    #         - query_string: additional query string
    #         - anchor: string to append after the anchor #
    #     """
    #     self.ensure_one()
    #     url = self.access_url + '%s?access_token=%s%s%s%s%s' % (
    #         self.id if self.id else '',
    #         self._portal_ensure_token(),
    #         '&report_type=%s' % report_type if report_type else '',
    #         '&download=true' if download else '',
    #         query_string if query_string else '',
    #         '#%s' % anchor if anchor else ''
    #     )
    #     print("url", url)
    #     return url

    # def _portal_ensure_token(self):
    #     """ Get the current record access token """
    #     if not self.access_token:
    #         # we use a `write` to force the cache clearing otherwise `return self.access_token` will return False
    #         self.sudo().write({'access_token': str(uuid.uuid4())})
    #     return self.access_token

    @api.depends('greep_qty', 'chirel_pocket_qty', 'shirt_qty', 'pair_qty', 'pent_qty', 'kurto_qty', 'pathani_qty', 'lengho_qty', 'chorni_qty', 'blazer_qty', 'coti_qty', 'fancy_button_qty')
    def get_charge(self):
        for rec in self:
            if rec.shirt_qty:
                rec.shirt_charge = self.env.user.company_id.shirt_charge * rec.shirt_qty
            if rec.pair_qty:
                total = self.env.user.company_id.pair_pent_charge + self.env.user.company_id.pair_shirt_charge
                rec.pair_charge = total * rec.pair_qty
            if rec.pent_qty:
                rec.pent_charge = self.env.user.company_id.pent_charge * rec.pent_qty
            if rec.kurto_qty:
                rec.kurto_charge = self.env.user.company_id.kurto_charge * rec.kurto_qty
            if rec.pathani_qty:
                rec.pathani_charge = self.env.user.company_id.pathani_charge * rec.pathani_qty
            if rec.lengho_qty:
                rec.lengho_charge = self.env.user.company_id.lengho_charge * rec.lengho_qty
            if rec.chorni_qty:
                rec.chorni_charge = self.env.user.company_id.chorni_charge * rec.chorni_qty
            if rec.blazer_qty:
                rec.blazer_charge = self.env.user.company_id.blazer_charge * rec.blazer_qty
            if rec.coti_qty:
                rec.coti_charge = self.env.user.company_id.coti_charge * rec.coti_qty
            if rec.fancy_button_qty:
                rec.fancy_button_charge = self.env.user.company_id.fancy_button_charge * rec.fancy_button_qty
            if rec.chirel_pocket_qty:
                rec.chirel_pocket_charge = self.env.user.company_id.chirel_pocket_charge * rec.chirel_pocket_qty
            if rec.greep_qty:
                rec.greep_charge = self.env.user.company_id.greep_charge * rec.greep_qty
            if rec.pair_qty or rec.shirt_qty:
                total = self.env.user.company_id.pair_shirt_charge * rec.pair_qty
                sub_total = self.env.user.company_id.shirt_charge * rec.shirt_qty
                rec.total_qty_shirt_charge = total + sub_total
            if rec.pair_qty or rec.pent_qty:
                total = self.env.user.company_id.pair_pent_charge * rec.pair_qty
                sub_total = self.env.user.company_id.pent_charge * rec.pent_qty
                rec.total_qty_pent_charge = total + sub_total

    @api.onchange('is_greep', 'is_chirel_pocket', 'is_shirt', 'is_pair', 'is_pent', 'is_kurto', 'is_pathani', 'is_lengho', 'is_chorni', 'is_blazer', 'is_coti', 'is_fancy_button')
    def qty_zero(self):
        if self.is_shirt == False:
            self.shirt_qty = 0
        if self.is_pair == False:
            self.pair_qty = 0
        if self.is_pent == False:
            self.pent_qty = 0
        if self.is_kurto == False:
            self.kurto_qty = 0
        if self.is_pathani == False:
            self.pathani_qty = 0
        if self.is_lengho == False:
            self.lengho_qty = 0
        if self.is_chorni == False:
            self.chorni_qty = 0
        if self.is_blazer == False:
            self.blazer_qty = 0
        if self.is_coti == False:
            self.coti_qty = 0
        if self.is_fancy_button == False:
            self.fancy_button_qty = 0
        if self.is_chirel_pocket == False:
            self.chirel_pocket_qty = 0
        if self.is_greep == False:
            self.greep_qty = 0

    @api.onchange('is_pair')
    def onchange_is_pair(self):
        if self.is_pair:
            self.is_shirt = True
            self.is_pent = True

    def add_pair(self):
        for rec in self:
            if rec.is_pair:
                rec.pair_qty += 1
            else:
                rec.pair_qty = 0

    def minus_pair(self):
        for rec in self:
            if rec.is_pair:
                rec.pair_qty -= 1
            else:
                rec.pair_qty = 0

    def add_shirt(self):
        for rec in self:
            if rec.is_shirt:
                rec.shirt_qty += 1
            else:
                rec.shirt_qty = 0

    def minus_shirt(self):
        for rec in self:
            if rec.is_shirt:
                rec.shirt_qty -= 1
            else:
                rec.shirt_qty = 0
    
    def add_pent(self):
        for rec in self:
            if rec.is_pent:
                rec.pent_qty += 1
            else:
                rec.pent_qty = 0

    def minus_pent(self):
        for rec in self:
            if rec.is_pent:
                rec.pent_qty -= 1
            else:
                rec.pent_qty = 0

    def add_kurto(self):
        for rec in self:
            if rec.is_kurto:
                rec.kurto_qty += 1
            else:
                rec.kurto_qty = 0

    def minus_kurto(self):
        for rec in self:
            if rec.is_kurto:
                rec.kurto_qty -= 1
            else:
                rec.kurto_qty = 0

    def add_pathani(self):
        for rec in self:
            if rec.is_pathani:
                rec.pathani_qty += 1
            else:
                rec.pathani_qty = 0

    def minus_pathani(self):
        for rec in self:
            if rec.is_pathani:
                rec.pathani_qty -= 1
            else:
                rec.pathani_qty = 0

    def add_lengho(self):
        for rec in self:
            if rec.is_lengho:
                rec.lengho_qty += 1
            else:
                rec.lengho_qty = 0

    def minus_lengho(self):
        for rec in self:
            if rec.is_lengho:
                rec.lengho_qty -= 1
            else:
                rec.lengho_qty = 0

    def add_chorni(self):
        for rec in self:
            if rec.is_chorni:
                rec.chorni_qty += 1
            else:
                rec.chorni_qty = 0

    def minus_chorni(self):
        for rec in self:
            if rec.is_chorni:
                rec.chorni_qty -= 1
            else:
                rec.chorni_qty = 0
    
    def add_blazer(self):
        for rec in self:
            if rec.is_blazer:
                rec.blazer_qty += 1
            else:
                rec.blazer_qty = 0

    def minus_blazer(self):
        for rec in self:
            if rec.is_blazer:
                rec.blazer_qty -= 1
            else:
                rec.blazer_qty = 0

    def add_coti(self):
        for rec in self:
            if rec.is_coti:
                rec.coti_qty += 1
            else:
                rec.coti_qty = 0

    def minus_coti(self):
        for rec in self:
            if rec.is_coti:
                rec.coti_qty -= 1
            else:
                rec.coti_qty = 0

    def add_fancy_button(self):
        for rec in self:
            if rec.is_fancy_button:
                rec.fancy_button_qty += 1
            else:
                rec.fancy_button_qty = 0

    def minus_fancy_button(self):
        for rec in self:
            if rec.is_fancy_button:
                rec.fancy_button_qty -= 1
            else:
                rec.fancy_button_qty = 0

    def add_chirel_pocket(self):
        for rec in self:
            if rec.is_chirel_pocket:
                rec.chirel_pocket_qty += 1
            else:
                rec.chirel_pocket_qty = 0

    def minus_chirel_pocket(self):
        for rec in self:
            if rec.is_chirel_pocket:
                rec.chirel_pocket_qty -= 1
            else:
                rec.chirel_pocket_qty = 0

    def add_greep(self):
        for rec in self:
            if rec.is_greep:
                rec.greep_qty += 1
            else:
                rec.greep_qty = 0

    def minus_greep(self):
        for rec in self:
            if rec.is_greep:
                rec.greep_qty -= 1
            else:
                rec.greep_qty = 0

    def button_refund_amount(self):
        return {
            'name': _('Refund Amount'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'refund.advance.amount.order.wiz',
            'views': [(self.env.ref('joli_tailor.view_refund_order_advance_amount_wiz').id, 'form')],
            'view_id': self.env.ref('joli_tailor.view_refund_order_advance_amount_wiz').id,
            'target': 'new',
            'map_id': self.id,
            'context': {'default_refund_amount': self.advance_amount, 'default_map_id': self.id}
        }

    def _get_payment_ids(self):
        for rec in self:
            payment = self.env['account.payment'].search_count(
                [('id', 'in', rec.payment_ids.ids)])
            rec.payment_count = payment

    @api.constrains('delivery_date', 'order_date')
    def check_delivery_date(self):
        for res in self:
            if res.order_date and res.delivery_date:
                if res.order_date > res.delivery_date:
                    raise UserError(
                        _("You can not select previous Delivery date!"))

    @api.constrains('mobile1', 'mobile2')
    def check_mobile_number(self):
        for res in self:
            if res.mobile1:
                if len(res.mobile1) != 11:
                    raise UserError(_("Please Enter Valid Mobile Number 1"))
            if res.mobile2:
                if len(res.mobile1) != 11:
                    raise UserError(_("Please Enter Valid Mobile Number 2"))

    @api.onchange('partner_id')
    def onchange_partner(self):
        self.mobile1 = ""
        self.mobile2 = ""
        if self.partner_id:
            if self.partner_id.phone:
                self.mobile1 = self.partner_id.phone
            if self.partner_id.mobile:
                self.mobile2 = self.partner_id.mobile
            if self.partner_id.street:
                self.address = self.partner_id.street

    def change_status(self, state):
        for res in self:
            for line in res.shirt_map_ids:
                line.state = state
            for line in res.pent_map_ids:
                line.state = state

    def button_confirm(self):
        for rec in self:
            if not rec.shirt_map_ids and not rec.pent_map_ids:
                raise UserError("Please select some Item detail to confirm!!!!")
            if rec.is_advance:
                wiz_id = self.env['confirm.wizard'].create(
                    {'map_id': rec.id})
                return {
                    'name': _('Confirmation'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'confirm.wizard',
                    'views': [(self.env.ref('joli_tailor.view_confirm_wizard').id, 'form')],
                    'res_id': wiz_id.id,
                    'target': 'new',
                }
            else:
                seq = rec.name
                if rec.name == 'New' or rec.name == _('New'):
                    seq = self.env['ir.sequence'].next_by_code(
                        'tailor.map') or _('New')
                    rec.name = seq
                rec.state = 'confirm'

    def delivery_order(self):
        wiz_id = self.env['delivery.tailor.order.wiz'].create(
            {'map_id': self.id, 'due_amount': self.due_amount})
        lines = []
        for rec in self:
            for line in rec.shirt_map_ids.filtered(lambda l: l.state == 'ready'):
                lines.append({'delivery_date': line.delivery_date,
                              'name': line.name,
                              'is_deliver': True,
                              'shirt_line_id': line.id,
                              'partner_id': line.partner_id.id,
                              })
            for line in rec.pent_map_ids.filtered(lambda l: l.state == 'ready'):
                lines.append({'delivery_date': line.delivery_date,
                              'name': line.name,
                              'is_deliver': True,
                              'pent_line_id': line.id,
                              'partner_id': line.partner_id.id,
                              })
            for line in rec.kurto_map_ids.filtered(lambda l: l.state == 'ready'):
                lines.append({'delivery_date': line.delivery_date,
                              'name': line.name,
                              'is_deliver': True,
                              'pent_line_id': line.id,
                              'partner_id': line.partner_id.id,
                              })
            for line in rec.pathani_map_ids.filtered(lambda l: l.state == 'ready'):
                lines.append({'delivery_date': line.delivery_date,
                              'name': line.name,
                              'is_deliver': True,
                              'shirt_line_id': line.id,
                              'partner_id': line.partner_id.id,
                              })
            for line in rec.lengho_map_ids.filtered(lambda l: l.state == 'ready'):
                lines.append({'delivery_date': line.delivery_date,
                              'name': line.name,
                              'is_deliver': True,
                              'pent_line_id': line.id,
                              'partner_id': line.partner_id.id,
                              })
            for line in rec.chorni_map_ids.filtered(lambda l: l.state == 'ready'):
                lines.append({'delivery_date': line.delivery_date,
                              'name': line.name,
                              'is_deliver': True,
                              'pent_line_id': line.id,
                              'partner_id': line.partner_id.id,
                              })
            for line in rec.blazer_map_ids.filtered(lambda l: l.state == 'ready'):
                lines.append({'delivery_date': line.delivery_date,
                              'name': line.name,
                              'is_deliver': True,
                              'pent_line_id': line.id,
                              'partner_id': line.partner_id.id,
                              })
            for line in rec.coti_map_ids.filtered(lambda l: l.state == 'ready'):
                lines.append({'delivery_date': line.delivery_date,
                              'name': line.name,
                              'is_deliver': True,
                              'pent_line_id': line.id,
                              'partner_id': line.partner_id.id,
                              })
        wiz_id.write({'line_ids': [(0, 0, l) for l in lines]})
        return {
            'name': _('Delivery Order'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'delivery.tailor.order.wiz',
            'views': [(self.env.ref('joli_tailor.view_delivery_tailor_order_wiz').id, 'form')],
            'view_id': self.env.ref('joli_tailor.view_delivery_tailor_order_wiz').id,
            'target': 'new',
            'res_id': wiz_id.id,
        }

    def update_advance_amount(self):
        wiz_id = self.env['advance.amount.tailor.wiz'].create(
            {'map_id': self.id})
        return {
            'name': _('Update Advance Amount'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'advance.amount.tailor.wiz',
            'views': [(self.env.ref('joli_tailor.view_advance_amount_tailor_wiz').id, 'form')],
            'view_id': self.env.ref('joli_tailor.view_advance_amount_tailor_wiz').id,
            'target': 'new',
            'res_id': wiz_id.id,
        }

    def button_done(self):
        wiz_id = self.env['payment.done.wizard'].create(
            {'map_id': self.id, 'paid_amount': self.due_amount})
        return {
            'name': _('Payment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'payment.done.wizard',
            'views': [(self.env.ref('joli_tailor.view_payment_done_wizard').id, 'form')],
            'res_id': wiz_id.id,
            'target': 'new',
        }

    def button_cancel(self):
        for rec in self:
            rec.change_status('cancel')
            rec.state = 'cancel'

    def button_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'
            rec.change_status('draft')

    def view_account_invoice(self):
        action = self.env.ref(
            'account.action_invoice_tree1').read()[0]
        action['views'] = [
            (self.env.ref('account.invoice_form').id, 'form')]
        action['res_id'] = self.invoice_id.id
        return action

    def view_account_payment(self):
        action = self.env.ref(
            'account.action_account_payments').read()[0]
        action['views'] = [
            (self.env.ref('account.view_account_payment_tree').id, 'tree')]
        action['domain'] = [('id', 'in', self.payment_ids.ids)]
        action['context'] = {}
        return action

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if vals.get('mobile1'):
    #             mobile = vals.get('mobile1')
    #             mobile_str = "%s %s" % (mobile[:5], mobile[5:])
    #             vals['mobile1'] = mobile_str
    #             # print(vals_list)
    #             # vals_list.update({'mobile1': mobile_str})
    #         return super(TailorMap, self).create(vals_list)

    # def create_customer_invoice(self):
    #     journal = self.env['account.journal'].search(
    #         [('type', '=', 'sale')])[0]
    #     account_id = self.env['account.account'].search(
    #         [('user_type_id', '=', self.env.ref('account.data_account_type_revenue').id)], limit=1).id
    #     lines = []
    #     for rec in self:
    #         payments = self.env['account.payment'].search([('map_id', '=', rec.id),
    #                                                        ('partner_id', '=', rec.customer_id.id)])
    #         invoice_rec = self.env['account.move'].create({
    #             'name': rec.name,
    #             'number': rec.name,
    #             # 'reference': rec.name,
    #             'journal_id': journal.id,
    #             'partner_id': rec.customer_id.id,
    #             'date_invoice': datetime.now().date(),
    #             'type': 'out_invoice',
    #             'discount': rec.discount,
    #         })
    #         if rec.tailor_order_line_ids:
    #             for line in rec.tailor_order_line_ids:
    #                 lines.append(({
    #                     'quantity': line.quantity,
    #                     'account_id': account_id,
    #                     'name': line.types_of_product_id.name,
    #                     'price_unit': line.charge}))
    #         invoice_rec.write({'invoice_line_ids': [(0, 0, l)for l in lines],
    #                            'payment_ids': [(6, 0, payments and payments.ids or [])]})
    #         invoice_rec._compute_amount()
    #         invoice_rec._compute_residual()
    #         invoice_rec.action_invoice_open()
    #         for payment in payments:
    #             invoice_rec.assign_outstanding_credit(
    #                 payment.move_line_ids.filtered('credit').id)
    #         invoice_rec.move_id.name = rec.name
    #         rec.invoice_id = invoice_rec.id

    # def create_vendor_bill(self):
    #     journal = self.env['account.journal'].search(
    #         [('type', '=', 'purchase')])[0]
    #     account_id = self.env['account.account'].search(
    #         [('user_type_id', '=', self.env.ref('account.data_account_type_expenses').id)], limit=1).id
    #     tailor_dict = {}
    #     tailors = []
    #     for rec in self:
    #         if rec.is_shirt:
    #             tailors += rec.shirt_map_ids.mapped('tailor_id')
    #         if rec.is_pent:
    #             tailors += rec.pent_map_ids.mapped('tailor_id')
    #         for t in tailors:
    #             tailor_dict[t] = []
    #         if rec.is_shirt:
    #             for s_line in rec.shirt_map_ids:
    #                 tailor_dict[s_line.tailor_id].append(s_line)
    #         if rec.is_pent:
    #             for p_line in rec.pent_map_ids:
    #                 tailor_dict[p_line.tailor_id].append(p_line)
    #         for key, val in tailor_dict.items():
    #             lines = []
    #             invoice_rec = self.env['account.move'].create({
    #                 'name': rec.name,
    #                 'number': rec.name,
    #                 # 'reference': rec.name,
    #                 'journal_id': journal.id,
    #                 'partner_id': key.partner_id.id,
    #                 'date_invoice': datetime.now().date(),
    #                 'type': 'in_invoice',
    #                 'tailor_id': key.id
    #             })
    #             for vi in val:
    #                 lines.append(({
    #                     'name': vi.name,
    #                     'account_id': account_id,
    #                     'price_unit': vi.tailor_charge}))
    #             invoice_rec.write(
    #                 {'invoice_line_ids': [(0, 0, l)for l in lines]})
    #             invoice_rec.action_invoice_open()
    #             key.invoice_ids = [(4, invoice_rec.id)]
