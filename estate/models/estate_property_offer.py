# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offers"

    validity = fields.Integer("Validity (days)", required=True, default=7)
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True)
    price = fields.Float(required=True)
    state = fields.Selection(
        string="Decision",
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        default=False
    )
    property_id = fields.Many2one("estate.property", string="Property")
    date_deadline = fields.Date("Deadline", compute="_compute_deadline")

    # computed method

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    # ------------------------------------------ CRUD Methods -------------------------------------

    @api.model
    def create(self, vals):
        if vals.get("property_id") and vals.get("price"):
            prop = self.env["estate.property"].browse(vals["property_id"])
            # We check if the offer is higher than the existing offers
            if prop.offer_ids:
                max_offer = max(prop.mapped("offer_ids.price"))
                if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError(
                        f"The offer must be higher than {max_offer:.2f}")
            prop.state = "offer_received"
        return super().create(vals)

    # ---------------------------------------- Action Methods -------------------------------------

    def action_accept(self):
        if "accepted" in self.mapped("property_id.offer_ids.state"):
            raise UserError("An offer as already been accepted.")
        self.write(
            {
                "state": "accepted",
            }
        )
        return self.mapped("property_id").write(
            {
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )

    def action_refuse(self):
        return self.write(
            {
                "state": "refused",
            }
        )
