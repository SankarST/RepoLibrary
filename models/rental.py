# -*- coding: utf-8 -*-
from datetime import timedelta,datetime
from odoo import fields, models,api

class Rentals(models.Model):
    _name = 'library.rental'
    _description = 'Book rental'


    customer_id = fields.Many2one('res.partner', string='Customer' ,
        domain=[('customer','=',True)])
       # domain=['&', ('is_author','!=',True),('is_publisher','!=' , True)] )

    copy_id = fields.Many2one('library.copy', string="Book Copy")
    book_id = fields.Many2one('product.product', string='Book' ,related="copy_id.book_id",readonly=True,required=True)
    state = fields.Selection([('draft', 'Draft'), ('rented', 'Rented'), ('returned', 'Returned'), ('lost', 'Lost')], default="draft")


    rental_date = fields.Date(required=True)
    return_date = fields.Date(required=True)


    customer_address = fields.Text(compute='_compute_customer_address')
    customer_email = fields.Char(related='customer_id.email')


    book_authors = fields.Many2many(related='copy_id.author_ids')
    book_edition_date = fields.Date(related='copy_id.edition_date')
    book_publisher = fields.Many2one(related='copy_id.publisher_id')
    book_author_names = fields.Char(compute = '_compute_book_author_names',string="Authors")


    late_return = fields.Boolean(string = "Is Late" ,default="False" , compute="_compute_late_return" , store=True)

    actual_return_date = fields.Date()

    comments = fields.Text(string="Comments");


    def action_confirm(self):
        for rec in self:
            rec.state = 'rented'
            rec.copy_id.book_state = 'rented'
            rec.add_fee('time')

    def add_fee(self, type):
        for rec in self:
            if type == 'time':
                price_id = self.env.ref('library.price_rent')
                delta_dates = fields.Date.from_string(rec.return_date) - fields.Date.from_string(rec.rental_date)
                amount = delta_dates.days * price_id.price / price_id.duration
            elif type == 'loss':
                price_id = self.env.ref('library.price_loss')
                amount = price_id.price
            else:
                return

            self.env['library.payment'].create({
                'customer_id': rec.customer_id.id,
                'date':        rec.rental_date,
                'amount':      - amount,
            })

    def action_return(self):
        for rec in self:
            rec.state = 'returned'
            rec.copy_id.book_state = 'available'

    def action_lost(self):
        for rec in self:
            rec.state = 'lost'
            rec.copy_id.book_state = 'lost'
            rec.copy_id.active = False
            rec.add_fee('loss')

    @api.model
    def _cron_check_date(self):
        late_rentals = self.search([('state', '=', 'rented'), ('return_date', '<', fields.Date.today())])
        template_id = self.env.ref('library.mail_template_book_return')
        for rec in late_rentals:
            mail_id = template_id.send_mail(rec.id)


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


    @api.depends('customer_id')
    def _compute_customer_address(self):
        self.customer_address = self.customer_id.address_get()
#        for r in self:
#            addr =  r.customer_id.address_get()
#            self.customer_address = "Test" + addr.street

#    @api.depends('customer_address')
#    def _compute_address_id(self):
#        addr_id = self.customer_address['contact']
#        address_id = addr_id
'''
    @api.depends('addr_id')
    def _compute_addr(self) 
      	for rec in self:
            addr = [rec.addr_id.street, rec.addr_id.street2,
                rec.addr_id.city,
                   rec.addr_id.zip]
            self.addresscustomer_address = ', '.join(filter(bool, addr))

'''


#get('contact', False)
#        address_val  = self.customer_id.address_get()
#        self.customer_address = address_val.street2
#        address_val  = self.customer_id.address_get(self._cr, self.uid, [self.customer_id.id], ['contact'])['contact']
#        self.customer_address = address_val

#      	for rec in self:
#            addr = [rec.customer_id.street, rec.customer_id.street2,
#                rec.customer_id.city,
#                   rec.customer_id.zip]
#            self.customer_address = ', '.join(filter(bool, addr))



