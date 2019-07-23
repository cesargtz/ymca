# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError

class partner_ymca_code(models.Model):
    _name = 'partner_ymca_code'

    name = fields.Char(compute="_compute_name", readonly=True)

    partner = fields.Many2one('res.partner', string="Usuario",
        domain=[('customer','=',True)])
    code = fields.Integer(string="Codigo")

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(code)',
         "El codigo debe ser unico"),

         ('unique_partner',
          'UNIQUE(partner)',
          "El usuario ya cuenta con codigo"),
    ]

    @api.depends('name')
    def _compute_name(self):
        self.name = self.code
