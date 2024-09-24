# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "tailor.map"

    def action_preview_so(self):
        return {
            'target': 'new',
            'type': 'ir.actions.act_url',
            'url': '/report/pdf/joli_tailor.report_tailor_customer_receipt/%s' % self.id
        }