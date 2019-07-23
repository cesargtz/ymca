# -*- coding: utf-8 -*-

from odoo import models, fields, api

class partner_ymca(models.Model):
    _inherit = 'res.partner'

    packages = fields.Selection([
     ('i', 'Individual'),
     ('a', 'Aerobico'),
     ('e', 'Estudiante'),
     ('f', 'Familiar'),
     ('c', 'Cortersia'),
     ('an', 'Anual'),
     ('ss', 'Sin suscripcion')
    ], default='ss', required=True, string="Tipo de paquete")

    code = fields.Integer(compute="get_code", string="Codigo Checador",  readonly=False )
    no_casillero = fields.Integer(compute="get_locker", string="Numero de Casillero", readonly=False )
    last_month_pay = fields.Date(string="Ultimo Mes Pagado")
    casillero_disponible = fields.Date(string="Casillero Disponible Hasta")
    family_active = fields.Boolean(string="Activo Para Familiar", default=False, store=True, readonly=False)
    incomes = fields.One2many('account.voucher', 'id', 'Ingresos', compute="_compute_incomes")
    family = fields.One2many('res.partner', 'parent_id', 'Familiares', compute="_compute_family")

    def _compute_family(self):
        for record in self:
            if record.name:
                record.family = self.env['res.partner'].search([('parent_id', '=', record.id)])

    def _compute_incomes(self):
        for record in self:
            if record.name:
                record.incomes = self.env['account.voucher'].search([('partner_id','=', record.id),
                                                               ('state','=','posted'),], order="date desc")

    @api.multi
    @api.onchange('code')
    def _onchange_code(self):
        for line in self:
            self.env.cr.execute("SELECT id FROM res_partner WHERE name = '%s'" % (line.name))
            id = self.env.cr.fetchall()
            if len(id) == 1:
                if line.code == 0:
                    self.env.cr.execute("UPDATE partner_ymca_code set partner = Null WHERE partner = %d" % (id[0][0]))
                else:
                    self.env.cr.execute("SELECT partner, code FROM partner_ymca_code WHERE code = %d" % (line.code))
                    q = self.env.cr.fetchall()
                    if q:
                        if q[0][0] != id[0][0] and  q[0][0] != None:
                            self.code = 0
                            return {
                                'warning':{
                                    'title': "El codigo ya esta ocupado.",
                                    'message': "El codigo que estas tratando de usar ya se encuenta ocupado por otro usuario" },
                                }
                        else:
                            self.env.cr.execute("UPDATE partner_ymca_code set partner = %d WHERE code = %d" % (id[0][0], line.code))
                    else:
                        self.code = 0
                        return {
                            'warning':{
                                'title': "El codigo no existe",
                                'message': "El codigo que estas tratando de usar no existe en la base de datos. Favor de crearlo antes de asignarlo." },
                            }
            if len(id) > 1:
                return {
                    'warning':{
                        'title': "Usuario Duplicado",
                        'message': "Solo puedes tener un usuario con el mismo nombre, favor de corregir el problema." },
                    }
            if not len(id):
                if line.name:
                    self.code = 0
                    return {
                        'warning':{
                            'title': "Favor de guardar el usuario",
                            'message': "Guarda el usuario antes de asignarle su codigo. Gracias!" },
                        }

    @api.one
    def get_code(self):
        for rec in self:
            rec.code = self.env['partner_ymca_code'].search([('partner', '=', rec.id)]).code

    @api.one
    def get_locker(self):
        for rec in self:
            rec.no_casillero = self.env['partner_ymca_locker'].search([('partner', '=', rec.id)]).locker

    @api.onchange('packages')
    def delete_code(self):
        for rec in self:
            if rec.packages == 'ss':
                self.env.cr.execute("UPDATE partner_ymca_code set partner = Null WHERE partner = %d" % (self._origin.id))

    @api.multi
    @api.onchange('no_casillero')
    def _onchange_locker(self):
        for line in self:
            self.env.cr.execute("SELECT id FROM res_partner WHERE name = '%s'" % (line.name))
            id = self.env.cr.fetchall()
            if len(id) == 1:
                if line.no_casillero == 0:
                    self.env.cr.execute("UPDATE partner_ymca_locker set partner = Null WHERE partner = %d" % (id[0][0]))
                else:
                    self.env.cr.execute("SELECT partner, locker FROM partner_ymca_locker WHERE locker = %d" % (line.no_casillero))
                    q = self.env.cr.fetchall()
                    if q:
                        if q[0][0] != id[0][0] and  q[0][0] != None:
                            self.no_casillero = 0
                            return {
                                'warning':{
                                    'title': "Numero de casillero ocupado.",
                                    'message': "El numero de casillero que estas tratando de usar ya se encuentra ocupado por otro usuario" },
                                }
                        else:
                            self.env.cr.execute("UPDATE partner_ymca_locker set partner = %d WHERE locker = %d" % (id[0][0], line.no_casillero))
                    else:
                        self.no_casillero = 0
                        return {
                            'warning':{
                                'title': "El numero de casillero no existe",
                                'message': "El numero que estas tratando de usar no existe en la base de datos. Favor de crearlo antes de asignarlo." },
                            }
            if len(id) > 1:
                return {
                    'warning':{
                        'title': "Usuario Duplicado",
                        'message': "Solo puedes tener un usuario con el mismo nombre, favor de corregir el problema." },
                    }
            if not len(id):
                if line.name:
                    self.no_casillero = 0
                    return {
                        'warning':{
                            'title': "Favor de guardar el usuario",
                            'message': "Guarda el usuario antes de asignarle su codigo. Gracias!" },
                        }
