# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import api, models, fields

class Accessory(models.Model):
    _inherit = ['mail.thread']
    _name = 'lgps.accessory'

    name = fields.Char(
        required=True,
        string="Internal Id",
    )

    serialnumber_id = fields.Many2one(
        comodel_name="stock.production.lot",
        required=True,
        string="Serial Number",
        index=True,
    )

    client_id = fields.Many2one(
        comodel_name="res.partner",
        required=True,
        string="Installed On",
        domain=[
            ('customer', '=', True),
            ('active', '=', True),
            ('is_company', '=', True)
        ],
        index=True,
    )

    gpsdevice_id = fields.Many2one(
        comodel_name="lgps.gpsdevice",
        ondelete="cascade",
        string="Installed On",
        index=True,
    )

    installation_date = fields.Date(
        default=fields.Date.today,
        string="Installation Date",
    )

    status = fields.Selection(
        selection=[
        ("Baja", "Baja"),
        ("Comodato", "Comodato"),
        ("Cortesía", "Cortesía"),
        ("Demo", "Demo"),
        ("Desinstalado", "Desinstalado"),
        ("Externo", "Externo"),
        ("Hibernado", "Hibernado"),
        ("Instalado", "Instalado"),
        ("Inventario", "Inventario"),
        ("Nuevo", "Nuevo"),
        ("Por Instalar", "Por Instalar"),
        ("Prestado", "Prestado"),
        ("Pruebas", "Pruebas"),
        ("Reemplazo", "Reemplazo"),
        ("Respaldo", "Respaldo"),
        ("Vendido", "Vendido")
        ],
        default="Inventario",
        string="Status",
    )

    product_id = fields.Many2one(
        comodel_name="product.product",
        required=True,
        string="Product Type",
        index=True
    )

    invoice_id = fields.Many2one(
        comodel_name="account.invoice",
        required=True,
        string="Invoice",
        index=True,
    )

    warranty_start_date = fields.Date(
        default=fields.Date.today,
        string="Warranty Start Date",
    )

    warranty_end_date = fields.Date(
        compute="_compute_end_warranty",
        string="Warranty End Date",
    )

    warranty_term = fields.Selection(
        selection=[
            ("12 meses", "12 meses"),
            ("18 meses", "18 meses"),
            ("24 meses", "24 meses"),
            ("36 meses", "36 meses")
        ],
        default="12 meses",
        string="Warranty Term",
    )

    @api.one
    @api.depends('warranty_term','warranty_start_date')
    def _compute_end_warranty(self):
        if not (self.warranty_term and self.warranty_start_date):
            self.warranty_end_date = None
        else:
            months = int(self.warranty_term[:2])
            years = months / 12
            days = int(round(years * 365, 0))
            start = fields.Date.from_string(self.warranty_start_date)
            duration = timedelta(days=days, seconds=0)
            self.warranty_end_date = start + duration

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Accessory, self).copy(default)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The accessory id must be unique"),
    ]
