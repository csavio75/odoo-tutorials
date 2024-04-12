# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"

    name = fields.Char(required=True)
    color = fields.Integer("Color index", default=1)
