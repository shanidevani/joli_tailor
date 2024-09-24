# -*- encoding: UTF-8 -*-
##############################################################################
#
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TailorLenghoMap(models.Model):
    _name = 'tailor.lengho.map'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Tailor Lengho'
    _order = 'id desc'

    name = fields.Char(string="Ref#", required=True, readonly=True, index=True, default=lambda self: _('New'))
    tailor_map_id = fields.Many2one('tailor.map')
    order_date = fields.Date(string='Date', related='tailor_map_id.order_date', store=True)
    length = fields.Char(string="Length")
    kamar = fields.Char(string="Kamar")
    seat = fields.Char(string="Seat")
    jang = fields.Char(string="Jang")
    ghutan = fields.Char(string="Ghutan")
    gothan = fields.Char(string="Gothan")
    moli = fields.Char(string="Moli")
    jolo = fields.Char(string="Jolo")
    thigh = fields.Char(string="Thigh")
    weight = fields.Char(string="Weight")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], string='Status', readonly=True, copy=False, index=True, default='draft')
    chipti = fields.Selection([
        ('No Chipti', 'No Chipti'),
        ('V Chipti', 'V Chipti'),
        ('2 Chipti', '2 Chipti'),
    ], string='Chipti', copy=False)
    belt = fields.Selection([
        ('Long', 'Long'),
        ('Cutt Belt', 'Cutt Belt'),
    ], string='Belt', copy=False)
    greep = fields.Boolean('Greep')
    pocket = fields.Selection([
        ('Side Pocket', 'Side Pocket'),
        ('Cross Pocket', 'Cross Pocket'),
    ], string='Pocket', copy=False, default='Side Pocket')
    back_pocket = fields.Selection([
        ('Single Pocket', 'Single Pocket'),
        ('Double Pocket', 'Double Pocket'),
    ], string="Back Pocket", copy=False, default="Single Pocket")
    chirel_pocket = fields.Boolean(string="Chirel Pocket")
    low_waist = fields.Boolean(string="Low Waist")
    gaaz = fields.Boolean(string="Gaaz")
    mobile_pocket = fields.Boolean(string="Mobile Pocket")
    watch_pocket = fields.Boolean(string="2 Watch Pocket")
    khicchi = fields.Boolean(string="Khichchi")
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    note = fields.Text(string="Note")
    design_no = fields.Char(string="Design no")
    image = fields.Binary(string="Image")
    delivery_date = fields.Date(string="Delivery Date", required=True)
    order_status = fields.Selection(related="tailor_map_id.state", store=True, string="Order Status")
    charge = fields.Float(string="Charge", required=True, related="tailor_map_id.lengho_charge")
    tailor_charge = fields.Float(string="Tailor Charge")
    map_require = fields.Boolean(related='tailor_map_id.map_require', string="Map Require")
    is_deliver = fields.Boolean()
    lengho_qty = fields.Integer(string="Quantity", readonly=True, tracking=True, related="tailor_map_id.lengho_qty")

    # @api.onchange('greep')
    # def onchange_greep(self):
    #     for rec in self:
    #         if rec.greep:
    #             rec.charge += self.env.user.company_id.greep_charge
    #         if rec.charge != self.env.user.company_id.pent_charge and not rec.greep:
    #             rec.charge -= self.env.user.company_id.greep_charge

    # @api.onchange('chirel_pocket')
    # def onchange_chirel_pocket(self):
    #     for rec in self:
    #         if rec.chirel_pocket:
    #             rec.charge += self.env.user.company_id.chirel_pocket_charge
    #         if rec.charge != self.env.user.company_id.pent_charge and not rec.chirel_pocket:
    #             rec.charge -= self.env.user.company_id.chirel_pocket_charge


    @api.constrains('delivery_date', 'order_date')
    def onchange_delivery_date(self):
        for res in self:
            if res.order_date and res.delivery_date:
                if res.order_date > res.delivery_date:
                    raise UserError(
                        _("You can not select previous Delivery date"))

    @api.model
    def default_get(self, field_list):
        res = super(TailorLenghoMap, self).default_get(field_list)
        partner = self.env['res.partner'].search([('id','=',res.get('partner_id'))])
        res.update({
            'length': partner.lengho_length,
            'kamar': partner.lengho_kamar,
            'seat': partner.lengho_seat,
            'jang': partner.lengho_jang,
            'ghutan': partner.lengho_ghutan,
            'gothan': partner.lengho_gothan,
            'moli': partner.lengho_moli,
            'jolo': partner.lengho_jolo,
            'thigh': partner.lengho_thigh,
            'chipti': partner.lengho_chipti,
            'belt': partner.lengho_belt,
            'greep': partner.lengho_greep,
            'pocket': partner.lengho_pocket,
            'chirel_pocket': partner.lengho_chirel_pocket,
            'low_waist': partner.lengho_low_waist,
            'gaaz': partner.lengho_gaaz,
            'mobile_pocket': partner.lengho_mobile_pocket,
            'watch_pocket': partner.lengho_watch_pocket,
            'khicchi': partner.lengho_khicchi,
            'note': partner.lengho_note,
            'design_no': partner.lengho_design_no,
            'back_pocket': partner.lengho_back_pocket,
            })
        return res

    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'tailor.lengho.map') or _('New')
            partner = self.env['res.partner'].search([('id','=',vals['partner_id'])])
            data_dict = {}
            if vals.get('length'):
                data_dict.update({'lengho_length': vals.get('length')})
            if vals.get('kamar'):
                data_dict.update({'lengho_kamar': vals.get('kamar')})
            if vals.get('seat'):
                data_dict.update({'lengho_seat': vals.get('seat')})
            if vals.get('jang'):
                data_dict.update({'lengho_jang': vals.get('jang')})
            if vals.get('ghutan'):
                data_dict.update({'lengho_ghutan': vals.get('ghutan')})
            if vals.get('gothan'):
                data_dict.update({'lengho_gothan': vals.get('gothan')})
            if vals.get('moli'):
                data_dict.update({'lengho_moli': vals.get('moli')})
            if vals.get('jolo'):
                data_dict.update({'lengho_jolo': vals.get('jolo')})
            if vals.get('thigh'):
                data_dict.update({'lengho_thigh': vals.get('thigh')})
            if vals.get('chipti'):
                data_dict.update({'lengho_chipti': vals.get('chipti')})
            if vals.get('belt'):
                data_dict.update({'lengho_belt': vals.get('belt')})
            if vals.get('greep'):
                data_dict.update({'lengho_greep': vals.get('greep')})
            if vals.get('pocket'):
                data_dict.update({'lengho_pocket': vals.get('pocket')})
            if vals.get('chirel_pocket'):
                data_dict.update({'lengho_chirel_pocket': vals.get('chirel_pocket')})
            if vals.get('low_waist'):
                data_dict.update({'lengho_low_waist': vals.get('low_waist')})
            if vals.get('gaaz'):
                data_dict.update({'lengho_gaaz': vals.get('gaaz')})
            if vals.get('mobile_pocket'):
                data_dict.update({'lengho_mobile_pocket': vals.get('mobile_pocket')})
            if vals.get('watch_pocket'):
                data_dict.update({'lengho_watch_pocket': vals.get('watch_pocket')})
            if vals.get('khicchi'):
                data_dict.update({'lengho_khicchi': vals.get('khicchi')})
            if vals.get('note'):
                data_dict.update({'lengho_note': vals.get('note')})
            if vals.get('design_no'):
                data_dict.update({'lengho_design_no': vals.get('design_no')})
            if vals.get('back_pocket'):
                data_dict.update({'lengho_back_pocket': vals.get('back_pocket')})
            partner.write(data_dict)
        return super(TailorLenghoMap, self).create(vals_list)

    def write(self, vals):
        for res in vals:
            partner = self.env['res.partner'].search([('id','=',self.partner_id.id)])
            data_dict = {}
            if vals.get('length'):
                data_dict.update({'lengho_length': vals.get('length')})
            if vals.get('kamar'):
                data_dict.update({'lengho_kamar': vals.get('kamar')})
            if vals.get('seat'):
                data_dict.update({'lengho_seat': vals.get('seat')})
            if vals.get('jang'):
                data_dict.update({'lengho_jang': vals.get('jang')})
            if vals.get('ghutan'):
                data_dict.update({'lengho_ghutan': vals.get('ghutan')})
            if vals.get('gothan'):
                data_dict.update({'lengho_gothan': vals.get('gothan')})
            if vals.get('moli'):
                data_dict.update({'lengho_moli': vals.get('moli')})
            if vals.get('jolo'):
                data_dict.update({'lengho_jolo': vals.get('jolo')})
            if vals.get('thigh'):
                data_dict.update({'lengho_thigh': vals.get('thigh')})
            if vals.get('chipti'):
                data_dict.update({'lengho_chipti': vals.get('chipti')})
            if vals.get('belt'):
                data_dict.update({'lengho_belt': vals.get('belt')})
            if vals.get('greep'):
                data_dict.update({'lengho_greep': vals.get('greep')})
            if vals.get('Pocket'):
                data_dict.update({'lengho_pocket': vals.get('Pocket')})
            if vals.get('chirel_pocket'):
                data_dict.update({'lengho_chirel_pocket': vals.get('chirel_pocket')})
            if vals.get('low_waist'):
                data_dict.update({'lengho_low_waist': vals.get('low_waist')})
            if vals.get('gaaz'):
                data_dict.update({'lengho_gaaz': vals.get('gaaz')})
            if vals.get('mobile_pocket'):
                data_dict.update({'lengho_mobile_pocket': vals.get('mobile_pocket')})
            if vals.get('watch_pocket'):
                data_dict.update({'lengho_watch_pocket': vals.get('watch_pocket')})
            if vals.get('khicchi'):
                data_dict.update({'lengho_khicchi': vals.get('khicchi')})
            if vals.get('note'):
                data_dict.update({'lengho_note': vals.get('note')})
            if vals.get('design_no'):
                data_dict.update({'lengho_design_no': vals.get('design_no')})
            if vals.get('back_pocket'):
                data_dict.update({'lengho_back_pocket': vals.get('back_pocket')})
            partner.write(data_dict)
        return super(TailorLenghoMap, self).write(vals)

    def button_done(self):
        for rec in self:
            rec.state = 'done'

    def button_ready(self):
        for rec in self:
            rec.state = 'ready'

    def button_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'
