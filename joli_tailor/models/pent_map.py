# -*- encoding: UTF-8 -*-
##############################################################################
#
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TailorPentMap(models.Model):
    _name = 'tailor.pent.map'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Tailor Pent'
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
    a = fields.Char(string="A")
    b = fields.Char(string="B")
    c = fields.Char(string="C")
    d = fields.Char(string="D")
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
    charge = fields.Float(string="Charge", required=True, related="tailor_map_id.total_qty_pent_charge")
    # charge = fields.Float(string="Charge", required=True, compute="compute_charge", store=True)
    # default=lambda self: self.env.user.company_id.pent_charge
    tailor_charge = fields.Float(string="Tailor Charge")
    map_require = fields.Boolean(related='tailor_map_id.map_require', string="Map Require")
    is_deliver = fields.Boolean()
    is_pair = fields.Boolean(string="Is Pair")
    pent_qty = fields.Integer(string="Quantity", related="tailor_map_id.pent_qty", readonly=True)
    pair_qty = fields.Integer(string="Quantity", related="tailor_map_id.pair_qty", readonly=True)

    # @api.onchange('is_pair')
    # def onchange_is_pair(self):
    #     for rec in self:
    #         if rec.is_pair:
    #             rec.charge = self.env.user.company_id.pair_pent_charge
    #         else:
    #             rec.charge = self.env.user.company_id.pent_charge

    # @api.onchange('greep')
    # def onchange_greep(self):
    #     for rec in self:
    #         if rec.greep:
    #             rec.charge += self.env.user.company_id.greep_charge
    #         if (rec.charge != self.env.user.company_id.pent_charge and not rec.greep) or (rec.charge != self.env.user.company_id.pair_pent_charge and not rec.greep):
    #             rec.charge -= self.env.user.company_id.greep_charge

    # @api.onchange('chirel_pocket')
    # def onchange_chirel_pocket(self):
    #     for rec in self:
    #         if rec.chirel_pocket:
    #             rec.charge += self.env.user.company_id.chirel_pocket_charge
    #         if (rec.charge != self.env.user.company_id.pent_charge and not rec.chirel_pocket)  or (rec.charge != self.env.user.company_id.pair_pent_charge and not rec.chirel_pocket):
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
        res = super(TailorPentMap, self).default_get(field_list)
        partner = self.env['res.partner'].search([('id','=',res.get('partner_id'))])
        res.update({
            'length': partner.pent_length,
            'kamar': partner.pent_kamar,
            'seat': partner.pent_seat,
            'jang': partner.pent_jang,
            'ghutan': partner.pent_ghutan,
            'gothan': partner.pent_gothan,
            'moli': partner.pent_moli,
            'jolo': partner.pent_jolo,
            'thigh': partner.pent_thigh,
            'chipti': partner.pent_chipti,
            'belt': partner.pent_belt,
            'greep': partner.pent_greep,
            'pocket': partner.pent_pocket,
            'chirel_pocket': partner.pent_chirel_pocket,
            'low_waist': partner.pent_low_waist,
            'gaaz': partner.pent_gaaz,
            'mobile_pocket': partner.pent_mobile_pocket,
            'watch_pocket': partner.pent_watch_pocket,
            'khicchi': partner.pent_khicchi,
            'note': partner.pent_note,
            'design_no': partner.pent_design_no,
            'a': partner.pent_a,
            'b': partner.pent_b,
            'c': partner.pent_c,
            'd': partner.pent_d,
            'back_pocket': partner.pent_back_pocket,
            })
        return res    

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'tailor.pent.map') or _('New')
            partner = self.env['res.partner'].search([('id','=',vals['partner_id'])])
            data_dict = {}
            if vals.get('length'):
                data_dict.update({'pent_length': vals.get('length')})
            if vals.get('kamar'):
                data_dict.update({'pent_kamar': vals.get('kamar')})
            if vals.get('seat'):
                data_dict.update({'pent_seat': vals.get('seat')})
            if vals.get('jang'):
                data_dict.update({'pent_jang': vals.get('jang')})
            if vals.get('ghutan'):
                data_dict.update({'pent_ghutan': vals.get('ghutan')})
            if vals.get('gothan'):
                data_dict.update({'pent_gothan': vals.get('gothan')})
            if vals.get('moli'):
                data_dict.update({'pent_moli': vals.get('moli')})
            if vals.get('jolo'):
                data_dict.update({'pent_jolo': vals.get('jolo')})
            if vals.get('thigh'):
                data_dict.update({'pent_thigh': vals.get('thigh')})
            if vals.get('chipti'):
                data_dict.update({'pent_chipti': vals.get('chipti')})
            if vals.get('belt'):
                data_dict.update({'pent_belt': vals.get('belt')})
            if vals.get('greep'):
                data_dict.update({'pent_greep': vals.get('greep')})
            if vals.get('pocket'):
                data_dict.update({'pent_pocket': vals.get('pocket')})
            if vals.get('chirel_pocket'):
                data_dict.update({'pent_chirel_pocket': vals.get('chirel_pocket')})
            if vals.get('low_waist'):
                data_dict.update({'pent_low_waist': vals.get('low_waist')})
            if vals.get('gaaz'):
                data_dict.update({'pent_gaaz': vals.get('gaaz')})
            if vals.get('mobile_pocket'):
                data_dict.update({'pent_mobile_pocket': vals.get('mobile_pocket')})
            if vals.get('watch_pocket'):
                data_dict.update({'pent_watch_pocket': vals.get('watch_pocket')})
            if vals.get('khicchi'):
                data_dict.update({'pent_khicchi': vals.get('khicchi')})
            if vals.get('note'):
                data_dict.update({'pent_note': vals.get('note')})
            if vals.get('design_no'):
                data_dict.update({'pent_design_no': vals.get('design_no')})
            if vals.get('a'):
                data_dict.update({'pent_a': vals.get('a')})
            if vals.get('b'):
                data_dict.update({'pent_b': vals.get('b')})
            if vals.get('c'):
                data_dict.update({'pent_c': vals.get('c')})
            if vals.get('d'):
                data_dict.update({'pent_d': vals.get('d')})
            if vals.get('back_pocket'):
                data_dict.update({'pent_back_pocket': vals.get('back_pocket')})
            partner.write(data_dict)
        return super(TailorPentMap, self).create(vals_list)

    def write(self, vals):
        for res in self:
            partner = self.env['res.partner'].search([('id','=',res.partner_id.id)])
            data_dict = {}
            if vals.get('length'):
                data_dict.update({'pent_length': vals.get('length')})
            if vals.get('kamar'):
                data_dict.update({'pent_kamar': vals.get('kamar')})
            if vals.get('seat'):
                data_dict.update({'pent_seat': vals.get('seat')})
            if vals.get('jang'):
                data_dict.update({'pent_jang': vals.get('jang')})
            if vals.get('ghutan'):
                data_dict.update({'pent_ghutan': vals.get('ghutan')})
            if vals.get('gothan'):
                data_dict.update({'pent_gothan': vals.get('gothan')})
            if vals.get('moli'):
                data_dict.update({'pent_moli': vals.get('moli')})
            if vals.get('jolo'):
                data_dict.update({'pent_jolo': vals.get('jolo')})
            if vals.get('thigh'):
                data_dict.update({'pent_thigh': vals.get('thigh')})
            if vals.get('chipti'):
                data_dict.update({'pent_chipti': vals.get('chipti')})
            if vals.get('belt'):
                data_dict.update({'pent_belt': vals.get('belt')})
            if vals.get('greep'):
                data_dict.update({'pent_greep': vals.get('greep')})
            if vals.get('pocket'):
                data_dict.update({'pent_pocket': vals.get('pocket')})
            if vals.get('chirel_pocket'):
                data_dict.update({'pent_chirel_pocket': vals.get('chirel_pocket')})
            if vals.get('low_waist'):
                data_dict.update({'pent_low_waist': vals.get('low_waist')})
            if vals.get('gaaz'):
                data_dict.update({'pent_gaaz': vals.get('gaaz')})
            if vals.get('mobile_pocket'):
                data_dict.update({'pent_mobile_pocket': vals.get('mobile_pocket')})
            if vals.get('watch_pocket'):
                data_dict.update({'pent_watch_pocket': vals.get('watch_pocket')})
            if vals.get('khicchi'):
                data_dict.update({'pent_khicchi': vals.get('khicchi')})
            if vals.get('note'):
                data_dict.update({'pent_note': vals.get('note')})
            if vals.get('design_no'):
                data_dict.update({'pent_design_no': vals.get('design_no')})
            if vals.get('a'):
                data_dict.update({'pent_a': vals.get('a')})
            if vals.get('b'):
                data_dict.update({'pent_b': vals.get('b')})
            if vals.get('c'):
                data_dict.update({'pent_c': vals.get('c')})
            if vals.get('d'):
                data_dict.update({'pent_d': vals.get('d')})
            if vals.get('back_pocket'):
                data_dict.update({'pent_back_pocket': vals.get('back_pocket')})
            partner.write(data_dict)
        return super(TailorPentMap, self).write(vals)

    def button_done(self):
        for rec in self:
            rec.state = 'done'

    def button_ready(self):
        for rec in self:
            rec.state = 'ready'

    def button_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'
