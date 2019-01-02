# -*- coding: utf-8 -*-

from odoo import api, models, fields

class Vehicle(models.Model):
    _inherit = ['mail.thread']
    _name = 'lgps.vehicle'

    name = fields.Char(
        required=True,
        string="Nick",
    )
    mark = fields.Char(
        string='Mark'
    )

    model = fields.Char(
        string='Model'
    )

    category = fields.Selection(
        selection=[
        ('Automovil', 'Automóvil'),
        ('Chasis', 'Chasis'),
        ('Caja Seca', 'Caja Seca'),
        ('Caja Refrigerada', 'Caja Refrigerada'),
        ('Camioneta', 'Camioneta'),
        ('Dolly', 'Dolly'),
        ('Lowboy', 'Lowboy'),
        ('Pipa', 'Pipa'),
        ('Plancha', 'Plancha'),
        ('Rabon', 'Rabon'),
        ('Remolque', 'Remolque'),
        ('Tanque', 'Tanque'),
        ('Torton', 'Torton'),
        ('Tracto', 'Tracto')
    ],
        default="Automovil",
        string="Category"
    )

    status = fields.Selection(
        selection=[
            ('Baja', 'Baja'),
            ('En Taller', 'En Taller'),
            ('En Servicio', 'En Servicio'),
            ('Fuera de Servicio', 'Fuera de Servicio')
        ],
        string="Status"
    )

    year = fields.Integer(
        string="Year",
    )

    color = fields.Char(
        string="Color"
    )

    plates = fields.Char(
        string="Plates"
    )

    observations = fields.Text(
        string="Observations"
    )

    client_id = fields.Many2one(
        comodel_name="res.partner",
        required=True,
        string="Owner",
        domain=[
            ('customer', '=', True),
            ('active', '=', True),
            ('is_company', '=', True)
        ],
        index=True,
    )

    gpsdevice_id = fields.Many2one(
        comodel_name="lgps.gpsdevice",
        string="Gps Installed",
        index=True,
    )

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

        return super(Vehicle, self).copy(default)
