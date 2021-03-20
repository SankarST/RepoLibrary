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

# moved to bookcopy
    rental_ids = fields.One2many('library.rental',related = 'copy_ids.rental_ids',  string='Rentals')
    author_names = fields.Char(compute = '_compute_author_names')

    copy_ids = fields.One2many('library.copy','book_id',string="Book Copies")
    copy_count = fields.Integer(compute = '_compute_copy_count')

    @api.depends('author_ids')
    def _compute_author_names(self):
        for r in self:
            if not r.author_ids:
                r.author_names = ""
            else:
#                r.author_names = r.mapped('author_ids.name')
                result = r.mapped('author_ids.name')
                r.author_names = ", ".join(result)

    @api.depends('copy_ids')
    def _compute_copy_count(self):
        for r in self:
#            if r.copy_ids:
            r.copy_count = len(r.copy_ids)
#            else :
#                r.copy_count = 1;

class BookCopy(models.Model):
    _name = 'library.copy'
    _description = 'Book Copy'
    _rec_name = 'reference'

    book_id = fields.Many2one('library.book', string="Book", required=True, ondelete="cascade", delegate=True)
    reference = fields.Char()

    rental_ids = fields.One2many('library.rental', 'copy_id', string='Rentals')
