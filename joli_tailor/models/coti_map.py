# -*- encoding: UTF-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TailorCotiMap(models.Model):
    _name = 'tailor.coti.map'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Tailor Coti'
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
    pet = fields.Char(string="Pet")
    cuff = fields.Char(string="Cuff")
    seat = fields.Char(string="Seat")
    half_sleeve = fields.Char()
    half_sleeve_patti = fields.Selection([
        ('Simple', 'Simple'),
        ('Patti', 'Patti')], string="Sleeve Patti", copy=False)
    petch = fields.Char(string="Petch")
    petch1 = fields.Char()
    petch2 = fields.Char()
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
    charge = fields.Float(string="Charge", required=True, related="tailor_map_id.coti_charge")
    fancy_button = fields.Float(string="Fancy Button")
    tailor_charge = fields.Float(string="Tailor Charge")
    map_require = fields.Boolean(related='tailor_map_id.map_require', string="Map Require")
    half_sleeve1 = fields.Char()
    collar_coti = fields.Char()
    is_deliver = fields.Boolean()
    coti_qty = fields.Integer(string="Quantity", readonly=True, tracking=True, related="tailor_map_id.coti_qty")

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
        res = super(TailorCotiMap, self).default_get(field_list)
        partner = self.env['res.partner'].search([('id','=',res.get('partner_id'))])
        res.update({
            'length': partner.coti_length,
            'shoulder': partner.coti_shoulder,
            'sleeve_length': partner.coti_sleeve_length,
            'sleeve_length1': partner.coti_sleeve_length1,
            'sleeve_length2': partner.coti_sleeve_length2,
            'chest': partner.coti_chest,
            'pet': partner.coti_pet,
            'cuff': partner.coti_cuff,
            'seat': partner.coti_seat,
            'open_shirt': partner.coti_open_shirt,
            'collar': partner.coti_collar,
            'pocket': partner.coti_pocket,
            'shoulder_type': partner.coti_shoulder_type,
            'patti': partner.coti_patti,
            'bombay_patti': partner.coti_bombay_patti,
            'note': partner.coti_note,
            'fancy_button': partner.coti_fancy_button,
            'design_no': partner.coti_design_no,
            'half_sleeve': partner.coti_half_sleeve,
            'half_sleeve_patti': partner.coti_half_sleeve_patti,
            'petch': partner.coti_petch,
            'petch1': partner.coti_petch1,
            'petch2': partner.coti_petch2,
            'half_sleeve1': partner.coti_half_sleeve1,
            'collar_coti': partner.coti_collar_coti,
        })
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'tailor.coti.map') or _('New')
            partner = self.env['res.partner'].search([('id','=', vals['partner_id'])])
            data_dict = {}
            if vals.get('length'):
                data_dict.update({'coti_length': vals.get('length')})
            if vals.get('shoulder'):
                data_dict.update({'coti_shoulder': vals.get('shoulder')})
            if vals.get('sleeve_length'):
                data_dict.update({'coti_sleeve_length': vals.get('sleeve_length')})
            if vals.get('sleeve_length1'):
                data_dict.update({'coti_sleeve_length1': vals.get('sleeve_length1')})
            if vals.get('sleeve_length2'):
                data_dict.update({'coti_sleeve_length2': vals.get('sleeve_length2')})
            if vals.get('chest'):
                data_dict.update({'coti_chest': vals.get('chest')})
            if vals.get('pet'):
                data_dict.update({'coti_pet': vals.get('pet')})
            if vals.get('cuff'):
                data_dict.update({'coti_cuff': vals.get('cuff')})
            if vals.get('seat'):
                data_dict.update({'coti_seat': vals.get('seat')})
            if vals.get('open_shirt'):
                data_dict.update({'coti_open_shirt': vals.get('open_shirt')})
            if vals.get('collar'):
                data_dict.update({'coti_collar': vals.get('collar')})
            if vals.get('pocket'):
                data_dict.update({'coti_pocket': vals.get('pocket')})
            if vals.get('shoulder_type'):
                data_dict.update({'coti_shoulder_type': vals.get('shoulder_type')})
            if vals.get('patti'):
                data_dict.update({'coti_patti': vals.get('patti')})
            if vals.get('bombay_patti'):
                data_dict.update({'coti_bombay_patti': vals.get('bombay_patti')})
            if vals.get('note'):
                data_dict.update({'coti_note': vals.get('note')})
            if vals.get('fancy_button'):
                data_dict.update({'coti_fancy_button': vals.get('fancy_button')})
            if vals.get('design_no'):
                data_dict.update({'coti_design_no': vals.get('design_no')})
            if vals.get('half_sleeve'):
                data_dict.update({'coti_half_sleeve': vals.get('half_sleeve')})
            if vals.get('half_sleeve_patti'):
                data_dict.update({'coti_half_sleeve_patti': vals.get('half_sleeve_patti')})
            if vals.get('petch'):
                data_dict.update({'coti_petch': vals.get('petch')})
            if vals.get('petch1'):
                data_dict.update({'coti_petch1': vals.get('petch1')})
            if vals.get('petch2'):
                data_dict.update({'coti_petch2': vals.get('petch2')})
            if vals.get('half_sleeve1'):
                data_dict.update({'coti_half_sleeve1': vals.get('half_sleeve1')})
            if vals.get('collar_coti'):
                data_dict.update({'coti_collar_coti': vals.get('collar_coti')})
            partner.write(data_dict)
        return super(TailorCotiMap, self).create(vals_list)

    def write(self, vals):
        for res in self:
            partner = self.env['res.partner'].search([('id','=',res.partner_id.id)])
            data_dict = {}
            if vals.get('length'):
                data_dict.update({'coti_length': vals.get('length')})
            if vals.get('shoulder'):
                data_dict.update({'coti_shoulder': vals.get('shoulder')})
            if vals.get('sleeve_length'):
                data_dict.update({'coti_sleeve_length': vals.get('sleeve_length')})
            if vals.get('sleeve_length1'):
                data_dict.update({'coti_sleeve_length1': vals.get('sleeve_length1')})
            if vals.get('sleeve_length2'):
                data_dict.update({'coti_sleeve_length2': vals.get('sleeve_length2')})
            if vals.get('chest'):
                data_dict.update({'coti_chest': vals.get('chest')})
            if vals.get('pet'):
                data_dict.update({'coti_pet': vals.get('pet')})
            if vals.get('cuff'):
                data_dict.update({'coti_cuff': vals.get('cuff')})
            if vals.get('seat'):
                data_dict.update({'coti_seat': vals.get('seat')})
            if vals.get('open_shirt'):
                data_dict.update({'coti_open_shirt': vals.get('open_shirt')})
            if vals.get('collar'):
                data_dict.update({'coti_collar': vals.get('collar')})
            if vals.get('pocket'):
                data_dict.update({'coti_pocket': vals.get('pocket')})
            if vals.get('shoulder_type'):
                data_dict.update({'coti_shoulder_type': vals.get('shoulder_type')})
            if vals.get('patti'):
                data_dict.update({'coti_patti': vals.get('patti')})
            if vals.get('bombay_patti'):
                data_dict.update({'coti_bombay_patti': vals.get('bombay_patti')})
            if vals.get('note'):
                data_dict.update({'coti_note': vals.get('note')})
            if vals.get('fancy_button'):
                data_dict.update({'coti_fancy_button': vals.get('fancy_button')})
            if vals.get('design_no'):
                data_dict.update({'coti_design_no': vals.get('design_no')})
            if vals.get('half_sleeve'):
                data_dict.update({'coti_half_sleeve': vals.get('half_sleeve')})
            if vals.get('half_sleeve_patti'):
                data_dict.update({'coti_half_sleeve_patti': vals.get('half_sleeve_patti')})
            if vals.get('petch'):
                data_dict.update({'coti_petch': vals.get('petch')})
            if vals.get('petch1'):
                data_dict.update({'coti_petch1': vals.get('petch1')})
            if vals.get('petch2'):
                data_dict.update({'coti_petch2': vals.get('petch2')})
            if vals.get('half_sleeve1'):
                data_dict.update({'coti_half_sleeve1': vals.get('half_sleeve1')})
            if vals.get('collar_coti'):
                data_dict.update({'coti_collar_coti': vals.get('collar_coti')})
            partner.write(data_dict)
        return super(TailorCotiMap, self).write(vals)

    def button_done(self):
        for rec in self:
            rec.state = 'done'

    def button_ready(self):
        for rec in self:
            rec.state = 'ready'

    def button_set_to_draft(self):
        for rec in self:
            rec.state = 'draft'
