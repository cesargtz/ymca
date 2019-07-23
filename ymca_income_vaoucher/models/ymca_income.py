# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ymca_income_vaoucher(models.Model):
    _inherit = 'account.voucher'

    packages = fields.Selection([
     ('i', 'Individual'),
     ('a', 'Aerobico'),
     ('e', 'Estudiante'),
     ('f', 'Familiar'),
     ('c', 'Cortersia'),
     ('sv', 'Visita'),
     ('va', 'Vapor'),
     ('an', 'Anual'),
     ('ss', 'Sin suscripcion'),
    ], required=True, string="Tipo de paquete")

    code_clock = fields.Integer(string="Codigo Checador", store=True)
    last_month_pay = fields.Date(string="Ultimo Pago", store=True)

    tiene_casillero = fields.Boolean(string="Casillero", default=False)
    no_casillero = fields.Integer(string="No de Casillero", store=True)
    valido_hasta = fields.Date(string="Valido hasta")

    incomes = fields.One2many('account.voucher', 'partner_id', 'Ingresos', compute="_compute_incomes", readonly=False, store=True)
    family = fields.One2many('res.partner', 'id', 'Familiares', compute="_compute_family", readonly=False, store=True)
    # codes_family = fields.One2many('partner_ymca_code', 'partner', 'Codigos Familiares', store=True, readonly=False)

    # def

    def _compute_family(self):
        if self.partner_id:
            self.family = self.env['res.partner'].search([('parent_id', '=', self.partner_id.id)])

    def _compute_incomes(self):
        if self.partner_id:
            self.incomes = self.env['account.voucher'].search([('partner_id','=', self.partner_id.id),
                                                               ('state','=','posted'),], order="date desc")
                                                               #  ('date','<=', self.date)


    # overwrite function
    @api.multi
    def proforma_voucher(self):
        last_voucher = self.env['account.voucher'].search([('partner_id','=', self.partner_id.id),('state','=','draft')], order="id desc", limit=1)
        self.calculate_last_paid(last_voucher, True)
        self.partner_id.casillero_disponible = self.valido_hasta
        family = self.env['res.partner'].search([('parent_id', '=', self.partner_id.id),('family_active', '=', True)])
        for line in family:
            if self.last_month_pay < self.date:
                line.last_month_pay = self.date
            else:
                line.last_month_pay = self.last_month_pay
        if self.tiene_casillero == False:
            self.partner_id.casillero_disponible = None
            # self.env.cr.execute("UPDATE partner_ymca_locker set partner = Null WHERE partner = %d" % (self.partner_id.id))
            # self.partner_id.no_casillero = 0
        return super(ymca_income_vaoucher, self).proforma_voucher()


    # @api.model
    # def create(self, vals):
    #     vals.update({'last_month_pay': self.env['account.voucher'].search([('partner_id','=', self.partner_id.id),
    #                                                                        ('state','=','posted')],
    #                                                                         order="date desc", limit=1).date})
    #     print(vals.get('last_month_pay'))
    #     return super(ymca_income_vaoucher, self).create(vals)

    @api.onchange('partner_id')
    def _compute_packages(self):
        for inv in self:
            if inv.partner_id:
                inv.packages = inv.partner_id.packages
                inv.code_clock = self.env['partner_ymca_code'].search([('partner.id', '=', inv.partner_id.id)]).code
                inv.no_casillero =  self.env['partner_ymca_locker'].search([('partner.id', '=', inv.partner_id.id)]).locker
                # Ultimo Pago
                last_voucher = self.env['account.voucher'].search([('partner_id','=', inv.partner_id.id),('state','=','posted')], order="id desc", limit=1)
                self.calculate_last_paid(last_voucher, False)
                print(last_voucher.number)
                inv.tiene_casillero = last_voucher.tiene_casillero
                inv.valido_hasta = last_voucher.valido_hasta
                # incomes
                inv.incomes = self.env['account.voucher'].search([('partner_id','=', inv.partner_id.id),('state','=','posted')], order="date desc")
                inv.family = self.env['res.partner'].search([('parent_id', '=', inv.partner_id.id)])

    # @api.onchange('no_casillero')
    # def _onchange_casillero(self):
    #     if self.partner_id:
    #         self.env.cr.execute("UPDATE partner_ymca_locker set locker = %d WHERE id = %d" % (self.no_casillero, self.partner_id.id))

    @api.onchange('code_clock')
    def _onchange_code_clock(self):
        for line in self:
            if line.partner_id:
                if line.code_clock == 0:
                    self.env.cr.execute("UPDATE partner_ymca_code set partner = Null WHERE partner = %d" % (line.partner_id.id))
                else:
                    self.env.cr.execute("SELECT partner, code FROM partner_ymca_code WHERE code = %d" % (line.code_clock))
                    q = self.env.cr.fetchall()
                    if q:
                        if q[0][0] != line.partner_id.id and  q[0][0] != None:
                            return {
                                'warning':{
                                    'title': "El codigo ya esta ocupado.",
                                    'message': "El codigo que estas tratando de usar ya se encuenta ocupado por otro usuario" },
                                }
                        else:
                            self.env.cr.execute("UPDATE partner_ymca_code set partner = %d WHERE code = %d" % (line.partner_id.id, line.code_clock))
                    else:
                        return {
                            'warning':{
                                'title': "El codigo no existe",
                                'message': "El codigo que estas tratando de usar no existe en la base de datos. Favor de crearlo antes de asignarlo." },
                            }

    def calculate_last_paid(self, last_voucher, save):
        if save:
            if self.last_month_pay < self.date:
                self.partner_id.last_month_pay = self.date
            else:
                self.partner_id.last_month_pay = self.last_month_pay
        else:
            if last_voucher:
                if last_voucher.last_month_pay > last_voucher.date:
                    self.last_month_pay = last_voucher.last_month_pay
                else:
                    self.last_month_pay = last_voucher.date
            else:
                self.last_month_pay = self.date



    @api.onchange('no_casillero')
    def _onchange_code_locker(self):
        for line in self:
            if line.partner_id:
                if line.no_casillero == 0:
                    self.env.cr.execute("UPDATE partner_ymca_locker set partner = Null WHERE partner = %d" % (line.partner_id.id))
                else:
                    self.env.cr.execute("SELECT partner, locker FROM partner_ymca_locker WHERE locker = %d" % (line.no_casillero))
                    q = self.env.cr.fetchall()
                    if q:
                        if q[0][0] != line.partner_id.id and  q[0][0] != None:
                            return {
                                'warning':{
                                    'title': "Numero de casillero ocupado.",
                                    'message': "El numero que estas tratando de usar ya se encuenta ocupado por otro usuario" },
                                }
                        else:
                            self.env.cr.execute("UPDATE partner_ymca_locker set partner = %d WHERE locker = %d" % (line.partner_id.id, line.no_casillero))
                    else:
                        return {
                            'warning':{
                                'title': "Numero de casillero no existe",
                                'message': "El  numero de casillero que estas tratando de usar no existe. Favor de crearlo antes de asignarlo." },
                            }
