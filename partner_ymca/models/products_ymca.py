# -*- coding: utf-8 -*-

from odoo import models, fields, api

class partner_ymca(models.Model):
    _inherit = 'product.template'

    packages = fields.Selection([
     ('i', 'Individual'),
     ('a', 'Aerobico'),
     ('e', 'Estudiante'),
     ('f', 'Familiar'),
    ], string="Paquete al que pertenece")


    _sql_constraints = [
        ('name_unique',
         'UNIQUE(packages)',
         "El paquete ya esta asignado a otro producto"),
    ]
