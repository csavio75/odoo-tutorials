# -*- coding: utf-8 -*-

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property"
    _order = "id desc"

    # Default value for date availability

    def _default_date_availability(self):
        return fields.Date.context_today(self)

    # Basic types
    name = fields.Char("Title", required=True)
    description = fields.Text("Descirption")
    postcode = fields.Char()
    date_availability = fields.Date("Available from",
                                    required=True, default=lambda self: self._default_date_availability(), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(required=True, default=1)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Integer()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ])

    # Relational fields
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property type")
    user_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user)
