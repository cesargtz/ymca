# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError

class partner_ymca_locker(models.Model):
    _name = 'partner_ymca_locker'

    partner = fields.Many2one('res.partner', string="Usuario",
        domain=[('customer','=',True)])
    locker = fields.Integer(string="Codigo de Casillero")

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(locker)',
         "El numero de casillero debe ser unico."),

         ('unique_partner',
          'UNIQUE(partner)',
          "El usuario ya cuenta con numero de casillero."),
    ]
