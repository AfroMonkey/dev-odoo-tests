# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, models, fields, _
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
        ("drop", "Drop"),
        ("comodato", _("Comodato")),
        ("courtesy", _("Courtesy")),
        ("demo", _("Demo")),
        ("uninstalled", _("Uninstalled")),
        ("external", _("External")),
        ("hibernate", _("Hibernate")),
        ("installed", _("Installed")),
        ("inventory", _("Inventory")),
        ("new", _("New")),
        ("ready", _("Ready to Install")),
        ("borrowed", _("Borrowed")),
        ("tests", _("Tests")),
        ("replacement", _("Replacement")),
        ("backup", _("Backup")),
        ("Sold", _("Sold"))
        ],
        default="inventory",
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
            ("12", _("12 months")),
            ("18", _("18 months")),
            ("24", _("24 months")),
            ("36", _("36 months"))
        ],
        default="12",
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
        help="Time without reporting in platforms expressed in hours",
    )

    accessory_ids = fields.One2many(
        comodel_name="lgps.accessory",
        inverse_name="gpsdevice_id",
        string="Accessories"
    )

    state = fields.Selection([
        ('crear', _('Crear')),
        ('asignar', _('Asignar')),
        ('programar', _('Programar')),
        ('pruebas', _('Programar')),
        ('instalado', _('Instalado')),
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
            #duration = timedelta(months=months)
            duration = timedelta(days=days)
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
        self.message_post(body="instalado")

        #list = self.env['lgps.cellchip'].search([
#            ('status', '=' , 'Suspendida')
#        ], limit=1)
        # limit=1 devuelve una referencia al modelo
        # limit > 1 devuelve una lista de referencias

        #self.cellchip_id.name = "01928172"
        self.write({
            'state': 'instalado',
        })

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The gps device id must be unique"),
    ]
