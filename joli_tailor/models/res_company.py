# -*- encoding: UTF-8 -*-


from odoo import models, fields, api
from odoo.osv import expression


class ResCompany(models.Model):
    _inherit = 'res.company'

    shirt_charge = fields.Float()
    pent_charge = fields.Float()
    pair_pent_charge = fields.Float()
    pair_shirt_charge = fields.Float()
    kurto_charge = fields.Float()
    pathani_charge = fields.Float()
    lengho_charge = fields.Float()
    chorni_charge = fields.Float()
    greep_charge = fields.Float()
    coti_charge = fields.Float()
    blazer_charge = fields.Float()
    chirel_pocket_charge = fields.Float()
    fancy_button_charge = fields.Float()
