# -*- encoding: UTF-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TailorKurtoMap(models.Model):
    _name = 'tailor.kurto.map'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Tailor Kurto'
    _order = 'id desc'

    name = fields.Char(string="Ref#", required=True, readonly=True, index=True, default=lambda self: _('New'))
    tailor_map_id = fields.Many2one('tailor.map', string='Bill No', readonly=True)
    order_date = fields.Date(string='Date', related='tailor_map_id.order_date')
    length = fields.Char(string="Length")
    shoulder = fields.Char(string="Shoulder")
    sleeve_length = fields.Char(string="Sleeve Length")
    sleeve_length1 = fields.Char()
    sleeve_length2 = fields.Char()
    chest = fields.Char(string="Chest")
    half_sleeve = fields.Char()
    half_sleeve_patti = fields.Selection([
        ('Simple', 'Simple'),
        ('Patti', 'Patti')], string="Sleeve Patti", copy=False)
    petch = fields.Char(string="Petch")
    petch1 = fields.Char()
    petch2 = fields.Char()
    pet = fields.Char(string="Pet")
    cuff = fields.Char(string="Cuff")
    seat = fields.Char(string="Seat")
    weight = fields.Float(string="Weight")
    open_shirt = fields.Selection([
        ('Open', 'Open'),
        ('Bushirt', 'Bushirt')
    ], string='Open', readonly=True, copy=False)
    collar = fields.Selection([
        ('Simple Collar', 'Simple Collar'),
        ('Chinese Collar', 'Chinese Collar')
    ], string='Collar', copy=False)
    pocket = fields.Selection([
        ('No Pocket', 'No Pocket'),
        ('Single Pocket', 'Single Pocket'),
        ('Double Pocket', 'Double Pocket'),
    ], string='Pocket', copy=False)
    shoulder_type = fields.Selection([
        ('Shoulder', 'Shoulder'),
        ('No Shoulder', 'No Shoulder'),
    ], string='Shoulder', copy=False)
    patti = fields.Selection([
        ('Baay Patti', 'Baay Patti'),
        ('No Patti', 'No Patti'),
    ], string='Patti', copy=False)
    bombay_patti = fields.Boolean(string="Bombay Patti")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], string='Status', readonly=True, copy=False, index=True, default='draft')
    note = fields.Text(string="Note")
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    design_no = fields.Char(string="Design no")
    image = fields.Binary(string="Image")
    delivery_date = fields.Date(string="Delivery Date", required=True)
    order_status = fields.Selection(related="tailor_map_id.state", store=True, string="Order Status")
    charge = fields.Float(string="Charge", required=True, related="tailor_map_id.kurto_charge")
    fancy_button = fields.Float(string="Fancy Button")
    tailor_charge = fields.Float(string="Tailor Charge")
    map_require = fields.Boolean(related='tailor_map_id.map_require', string="Map Require")
    is_deliver = fields.Boolean()
    half_sleeve1 = fields.Char()
    collar_kurto = fields.Char()
    kurto_qty = fields.Integer(string="Quantity", readonly=True, tracking=True, related="tailor_map_id.kurto_qty")

    # @api.onchange('fancy_button')
    # def onchange_fancy_button(self):
    #     for rec in self:
    #         if rec.fancy_button:
    #             rec.charge += rec.fancy_button

    @api.constrains('delivery_date', 'order_date')
    def onchange_delivery_date(self):
        for res in self:
            if res.order_date and res.delivery_date:
                if res.order_date > res.delivery_date:
                    raise UserError(
                        _("You can not select previous Delivery date"))

    @api.model
    def default_get(self, field_list):
        res = super(TailorKurtoMap, self).default_get(field_list)
        partner = self.env['res.partner'].search([('id','=',res.get('partner_id'))])
        res.update({
            'length': partner.kurto_length,
            'shoulder': partner.kurto_shoulder,
            'sleeve_length': partner.kurto_sleeve_length,
            'sleeve_length1': partner.kurto_sleeve_length1,
            'sleeve_length2': partner.kurto_sleeve_length2,
            'chest': partner.kurto_chest,
            'pet': partner.kurto_pet,
            'cuff': partner.kurto_cuff,
            'seat': partner.kurto_seat,
            'open_shirt': partner.kurto_open_shirt,
            'collar': partner.kurto_collar,
            'pocket': partner.kurto_pocket,
            'shoulder_type': partner.kurto_shoulder_type,
            'patti': partner.kurto_patti,
            'bombay_patti': partner.kurto_bombay_patti,
            'note': partner.kurto_note,
            'fancy_button': partner.kurto_fancy_button,
            'design_no': partner.kurto_design_no,
            'half_sleeve': partner.kurto_half_sleeve,
            'half_sleeve_patti': partner.kurto_half_sleeve_patti,
            'petch': partner.kurto_petch,
            'petch1': partner.kurto_petch1,
            'petch2': partner.kurto_petch2,
            'half_sleeve1': partner.kurto_half_sleeve1,
            'collar_kurto': partner.kurto_collar_kurto,
        })
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'tailor.kurto.map') or _('New')
            partner = self.env['res.partner'].search([('id','=',vals['partner_id'])])
            data_dict = {}
            if vals.get('length'):
                data_dict.update({'kurto_length': vals.get('length')})
            if vals.get('shoulder'):
                data_dict.update({'kurto_shoulder': vals.get('shoulder')})
            if vals.get('sleeve_length'):
                data_dict.update({'kurto_sleeve_length': vals.get('sleeve_length')})
            if vals.get('sleeve_length1'):
                data_dict.update({'kurto_sleeve_length1': vals.get('sleeve_length1')})
            if vals.get('sleeve_length2'):
                data_dict.update({'kurto_sleeve_length2': vals.get('sleeve_length2')})
            if vals.get('chest'):
                data_dict.update({'kurto_chest': vals.get('chest')})
            if vals.get('pet'):
                data_dict.update({'kurto_pet': vals.get('pet')})
            if vals.get('cuff'):
                data_dict.update({'kurto_cuff': vals.get('cuff')})
            if vals.get('seat'):
                data_dict.update({'kurto_seat': vals.get('seat')})
            if vals.get('open_shirt'):
                data_dict.update({'kurto_open_shirt': vals.get('open_shirt')})
            if vals.get('collar'):
                data_dict.update({'kurto_collar': vals.get('collar')})
            if vals.get('pocket'):
                data_dict.update({'kurto_pocket': vals.get('pocket')})
            if vals.get('shoulder_type'):
                data_dict.update({'kurto_shoulder_type': vals.get('shoulder_type')})
            if vals.get('patti'):
                data_dict.update({'kurto_patti': vals.get('patti')})
            if vals.get('bombay_patti'):
                data_dict.update({'kurto_bombay_patti': vals.get('bombay_patti')})
            if vals.get('note'):
                data_dict.update({'kurto_note': vals.get('note')})
            if vals.get('fancy_button'):
                data_dict.update({'kurto_fancy_button': vals.get('fancy_button')})
            if vals.get('design_no'):
                data_dict.update({'kurto_design_no': vals.get('design_no')})
            if vals.get('half_sleeve'):
                data_dict.update({'kurto_half_sleeve': vals.get('half_sleeve')})
            if vals.get('half_sleeve_patti'):
                data_dict.update({'kurto_half_sleeve_patti': vals.get('half_sleeve_patti')})
            if vals.get('petch'):
                data_dict.update({'kurto_petch': vals.get('petch')})
            if vals.get('petch1'):
                data_dict.update({'kurto_petch1': vals.get('petch1')})
            if vals.get('petch2'):
                data_dict.update({'kurto_petch2': vals.get('petch2')})
            if vals.get('half_sleeve1'):
                data_dict.update({'kurto_half_sleeve1': vals.get('half_sleeve1')})
            if vals.get('collar_kurto'):
                data_dict.update({'kurto_collar_kurto': vals.get('collar_kurto')})
            partner.write(data_dict)
        return super(TailorKurtoMap, self).create(vals_list)

    def write(self, vals):
        for res in self:
            partner = self.env['res.partner'].search([('id','=',res.partner_id.id)])
            data_dict = {}
            if vals.get('length'):
                data_dict.update({'kurto_length': vals.get('length')})
            if vals.get('shoulder'):
                data_dict.update({'kurto_shoulder': vals.get('shoulder')})
            if vals.get('sleeve_length'):
                data_dict.update({'kurto_sleeve_length': vals.get('sleeve_length')})
            if vals.get('sleeve_length1'):
                data_dict.update({'kurto_sleeve_length1': vals.get('sleeve_length1')})
            if vals.get('sleeve_length2'):
                data_dict.update({'kurto_sleeve_length2': vals.get('sleeve_length2')})
            if vals.get('chest'):
                data_dict.update({'kurto_chest': vals.get('chest')})
            if vals.get('pet'):
                data_dict.update({'kurto_pet': vals.get('pet')})
            if vals.get('cuff'):
                data_dict.update({'kurto_cuff': vals.get('cuff')})
            if vals.get('seat'):
                data_dict.update({'kurto_seat': vals.get('seat')})
            if vals.get('open_shirt'):
                data_dict.update({'kurto_open_shirt': vals.get('open_shirt')})
            if vals.get('collar'):
                data_dict.update({'kurto_collar': vals.get('collar')})
            if vals.get('pocket'):
                data_dict.update({'kurto_pocket': vals.get('pocket')})
            if vals.get('shoulder_type'):
                data_dict.update({'kurto_shoulder_type': vals.get('shoulder_type')})
            if vals.get('patti'):
                data_dict.update({'kurto_patti': vals.get('patti')})
            if vals.get('bombay_patti'):
                data_dict.update({'kurto_bombay_patti': vals.get('bombay_patti')})
            if vals.get('note'):
                data_dict.update({'kurto_note': vals.get('note')})
            if vals.get('fancy_button'):
                data_dict.update({'kurto_fancy_button': vals.get('fancy_button')})
            if vals.get('design_no'):
                data_dict.update({'kurto_design_no': vals.get('design_no')})
            if vals.get('half_sleeve'):
                data_dict.update({'kurto_half_sleeve': vals.get('half_sleeve')})
            if vals.get('half_sleeve_patti'):
                data_dict.update({'kurto_half_sleeve_patti': vals.get('half_sleeve_patti')})
            if vals.get('petch'):
                data_dict.update({'kurto_petch': vals.get('petch')})
            if vals.get('petch1'):
                data_dict.update({'kurto_petch1': vals.get('petch1')})
            if vals.get('petch2'):
                data_dict.update({'kurto_petch2': vals.get('petch2')})
            if vals.get('half_sleeve1'):
                data_dict.update({'kurto_half_sleeve1': vals.get('half_sleeve1')})
            if vals.get('collar_kurto'):
                data_dict.update({'kurto_collar_kurto': vals.get('collar_kurto')})
            partner.write(data_dict)
        return super(TailorKurtoMap, self).write(vals)

    def button_done(self):
        for rec in self:
            rec.state = 'done'

    def button_ready(self):
        for rec in self:
            rec.state = 'ready'

    def button_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'
