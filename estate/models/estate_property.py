from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Real estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(required=True)
    excepted_price = fields.Float(required=True)
    selling_price = fields.Float(required=True)
    bedrooms = fields.Integer(required=True)
    living_area = fields.Integer(required=True)
    facade = fields.Integer()
    garade = fields.Integer()
    garden = fields.Boolean()
    garden_orientation = fields.Selection(string="Garden orientation", selection=[(
        'north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
