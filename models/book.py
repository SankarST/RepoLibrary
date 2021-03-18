# -*- coding: utf-8 -*-
from odoo import fields, models, api


class Books(models.Model):
    _name = 'library.book'
    _description = 'Book'

    name = fields.Char(string='Title')

    author_ids = fields.Many2many("library.partner", string="Authors") 
#        domain=[('partner_type','=','author')] )
    edition_date = fields.Date()
    isbn = fields.Char(string='ISBN')
    publisher_id = fields.Many2one('library.publisher', string='Publisher')

    rental_ids = fields.One2many('library.rental', 'book_id', string='Rentals')
    
    author_names = fields.Char(compute = '_compute_author_names')

    @api.depends('author_ids')
    def _compute_author_names(self):
        for r in self:
            if not r.author_ids:
                r.author_names = ""
            else:
#                r.author_names = r.mapped('author_ids.name')
                result = r.mapped('author_ids.name')
                r.author_names = ", ".join(result)

