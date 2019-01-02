# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, models, fields
import math
import logging
_logger = logging.getLogger(__name__)

class GpsDevice(models.Model):
    _inherit = ['mail.thread']
    _name = 'lgps.gpsdevice'

    name = fields.Char(
        required=True,
        string="Dispositivo GPS",
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

    nick = fields.Char(
        string="Nick",
    )

    serialnumber_id = fields.Many2one(
        comodel_name="stock.production.lot",
        required=True,
        string="Serial Number",
        index=True,
    )

    imei = fields.Char(
        string="IMEI",
    )

    idf = fields.Char(
        string="IDF",
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

    platform = fields.Selection(
        selection=[
        ("Cybermapa", "Cybermapa"),
        ("Gurtam", "Gurtam"),
        ("Novit", "Novit"),
        ("Mapaloc", "Mapaloc"),
        ("Position Logic", "Position Logic"),
        ("Sosgps", "Sosgps"),
        ("Utrax", "Utrax")
        ],
        string="Platform",
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

    fuel = fields.Boolean(
        default=False,
        string="Fuel",
    )

    speaker = fields.Boolean(
        default=False,
        string="Speaker",
    )

    anti_jammer_blocker = fields.Boolean(
        default=False,
        string="Anti Jammer Blocker",
    )

    smart_blocker = fields.Boolean(
        default=False,
        string="Smart Blocker",
    )

    blocker = fields.Boolean(
        default=False,
        string="Blocker",
    )

    scanner = fields.Boolean(
        default=False,
        string="Scanner",
    )

    load_drivers = fields.Boolean(
        default=False,
        string="Load Drivers",
    )

    solar_panel = fields.Boolean(
        default=False,
        string="Solar Panel",
    )

    temperature = fields.Boolean(
        default=False,
        string="Temperature",
    )

    ibutton = fields.Boolean(
        default=False,
        string="iButton",
    )

    microphone = fields.Boolean(
        default=False,
        string="Microphone",
    )

    sheet = fields.Boolean(
        default=False,
        string="Sheet",
    )

    opening_sensor = fields.Boolean(
        default=False,
        string="Opening Sensor",
    )

    datetime_gps = fields.Datetime(
        string="DateTime GPS",
    )

    datetime_server = fields.Datetime(
        string="DateTime Server",
    )

    last_position = fields.Char(
        string="Last Position",
    )

    cellchip_id = fields.Many2one(
        comodel_name="lgps.cellchip",
        required=True,
        string="Cellchip Number",
    )

    last_report = fields.Integer(
        string="Last Report",
        compute="_compute_last_report",
        store=True,
    )

    state = fields.Selection([
        ('crear', 'Crear'),
        ('asignar', 'Asignar'),
        ('programar', 'Programar'),
        ('pruebas', 'Programar'),
        ('instalado', 'Instalado'),
    ], default='crear')

    @api.one
    @api.depends('datetime_gps')
    def _compute_last_report(self):
        if not self.datetime_gps:
            self.last_report = None
        else:
            start_dt = fields.Datetime.from_string(self.datetime_gps)
            today_dt = fields.Datetime.from_string(fields.Datetime.now())
            difference = today_dt - start_dt
            time_difference_in_hours = difference.total_seconds() / 3600
            self.last_report = math.ceil(time_difference_in_hours)

    @api.one
    @api.depends('warranty_term','warranty_start_date')
    def _compute_end_warranty(self):
        if not (self.warranty_term and self.warranty_start_date):
            self.warranty_end_date = None
        else:
            #_logger.info(self.warranty_term)
            months = int(self.warranty_term[:2])
            #_logger.info(months)
            years = months / 12
            #_logger.info(years)
            days = int(round(years * 365, 0))
            #_logger.info(days)
            start = fields.Date.from_string(self.warranty_start_date)
            duration = timedelta(days=days, seconds=0)
            #_logger.info(duration)
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

        return super(GpsDevice, self).copy(default)

    @api.one
    def crear_progressbar(self):
        self.message_post(body="crear")
        self.write({
            'state': 'crear',
        })

    # This function is triggered when the user clicks on the button 'Set to started'
    @api.one
    def asignar_progressbar(self):
        self.message_post(body="asignar")
        self.write({
            'state': 'asignar'
        })

    # This function is triggered when the user clicks on the button 'In progress'
    @api.one
    def programar_progressbar(self):
        self.message_post(body="programar")
        self.write({
            'state': 'programar'
        })

    # This function is triggered when the user clicks on the button 'Done'
    @api.one
    def pruebas_progressbar(self):
        self.message_post(body="pruebas")
        self.write({
            'state': 'pruebas',
        })

    # This function is triggered when the user clicks on the button 'Done'
    @api.one
    def instalado_progressbar(self):
        self.log_note(self, "instalado")
        self.write({
            'state': 'instalado',
        })

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The gps device id must be unique"),
    ]
