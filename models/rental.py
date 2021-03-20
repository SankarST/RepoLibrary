# -*- coding: utf-8 -*-
from datetime import timedelta,datetime
from odoo import fields, models,api

class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'


    customer_id = fields.Many2one('library.partner', string='Customer',
        domain=[('partner_type','=','customer')] )

    book_id = fields.Many2one('library.book', string='Book' ,related="copy_id.book_id",readonly=True)
    copy_id = fields.Many2one('library.copy', string="Book Copy")

    rental_date = fields.Date()
    return_date = fields.Date(required=True)

    customer_address = fields.Text(related='customer_id.address')
    customer_email = fields.Char(related='customer_id.email')

    book_authors = fields.Many2many(related='book_id.author_ids')
    book_edition_date = fields.Date(related='book_id.edition_date')
    book_publisher = fields.Many2one(related='book_id.publisher_id')
    book_author_names = fields.Char(compute = '_compute_book_author_names',string="Authors")


    late_return = fields.Boolean(string = "Is Late" ,default="False" , compute="_compute_late_return" , store=True)

    actual_return_date = fields.Date()

    comments = fields.Text(string="Comments");

    @api.depends('book_id',"copy_id")
    def name_get(self):
        result = []
        for r in self:
            name = 'Rental - ' + str(r.id) + ' '  +  r.copy_id.name
           # name = 'Rental - ' + str(r.id) 
            result.append((r.id, name))
        return result

    @api.depends('return_date','actual_return_date')
    def _compute_late_return(self):
        late_return_flag =  False
        for r in self:
            if not r.actual_return_date:
                if r.return_date :
                    #temp_return_date = r.return_date
                    if (r.return_date <= fields.Date.today()):
                        late_return_flag = True
            else:
                # actual_return_date = r.actual_return_date
                # return_date = r.return_date
                if (r.actual_return_date > r.return_date):
                    late_return_flag =  True
            r.late_return = late_return_flag


    @api.depends('book_authors')
    def _compute_book_author_names(self):
        for r in self:
            if not r.book_authors:
                r.book_author_names = ""
            else:
#                r.author_names = r.mapped('author_ids.name')
                result = r.mapped('book_authors.name')
                r.book_author_names = ", ".join(result)



#datetime.strptime(time_str, '%H::%M::%S').time()



#start_day = datetime.strptime(line.actual_return_date,
#                                              DEFAULT_SERVER_DATETIME_FORMAT)
#                end_day = datetime.strptime(line.date_return,
#                                            DEFAULT_SERVER_DATETIME_FORMAT)
#                if start_day > end_day:
#                    diff = rd(start_day.date(), end_day.date())


#    @api.depends('seats', 'attendee_ids')
#    def _compute_taken_seats(self):
#        for session in self:
#            if not session.seats:
#                session.taken_seats = 0.0
#            else:
#                session.taken_seats = 100.0 * len(session.attendee_ids) / session.seats
