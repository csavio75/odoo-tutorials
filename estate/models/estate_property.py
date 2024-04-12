# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property"
    _order = "id desc"
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)",
         "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)",
         "The offer price must be positive"),
    ]

    # Default value for date availability

    def _default_date_availability(self):
        return fields.Date.today()

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

    # Special
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean("Active", default=True)

    # Relational fields
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property type")
    user_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", readonly=True, copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")

    # Computed
    total_area = fields.Integer(
        "Total Area (sqm)",
        compute="_compute_total_area",
        help="Total area computed by summing the living area and the garden area",
    )
    best_price = fields.Float(
        "Best Offer", compute="_compute_best_price", help="Best offer received")

    # ---------------------------------------- Compute methods ------------------------------------

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped(
                "price")) if prop.offer_ids else 0.0

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.selling_price, precision_rounding=0.01)
                and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # ------------------------------------------ CRUD Methods -------------------------------------

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Only new and canceled properties can be deleted.")

    # ---------------------------------------- Action Methods -------------------------------------

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})
