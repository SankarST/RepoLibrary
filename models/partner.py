# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Partner(models.Model):

    _inherit = 'res.partner'

    is_author = fields.Boolean(string="Is an Author", default=False)
    is_publisher = fields.Boolean(string="Is a Publisher", default=False)
    customer = fields.Boolean(string="Is Customer",default=True)

    current_rental_ids = fields.One2many('library.rental', 'customer_id', string='Current Rentals', domain=[('state', '=', 'rented')])
    old_rental_ids = fields.One2many('library.rental', 'customer_id', string='Old Rentals', domain=[('state', '=', 'returned')])
    lost_rental_ids = fields.One2many('library.rental', 'customer_id', string='Lost Rentals', domain=[('state', '=', 'lost')])


    rental_ids = fields.One2many('library.rental', 'customer_id', string='Rentals')
    book_ids = fields.Many2many('product.product',string='Books') 
    books_published = fields.One2many('product.product', 'publisher_id',string='Books Published')

    birthdate = fields.Date()
    nationality_id = fields.Many2one('res.country',ondelete='set null', string="Nationality", index=True)


    qty_lost_book = fields.Integer(string='Number of book copies lost', compute="_get_lost_books_qty")

    def _get_lost_books_qty(self):
        for rec in self:
            rec.qty_lost_book = len(rec.lost_rental_ids)


#    _name = 'library.partner'
#    _description = 'Partner'

#    name = fields.Char()
#    email = fields.Char()
#    address = fields.Text()
#    partner_type = fields.Selection([('customer', 'Customer'), ('author', 'Author')], default="customer")

#    rental_ids = fields.One2many('library.rental', 'customer_id', string='Rentals')
#     book_ids = fields.Many2many('library.book',string='Books') 
