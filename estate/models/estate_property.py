from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property"

    name = fields.Char("Title", required=True)
    description = fields.Text("Descirption")
    postcode = fields.Char()
    date_availability = fields.Date(required=True)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer(required=True)
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
