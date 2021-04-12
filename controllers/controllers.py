# -*- coding: utf-8 -*-
import logging

from odoo import http

_logger = logging.getLogger(__name__)


class Library(http.Controller):
#     @http.route('/library/library/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"





    @http.route('/rent_webform', type="http", auth="public", website=True)
    def rent_webform(self, **kw):

        bookcopy_rec = http.request.env['library.copy'].sudo().search([])
        logging.info("Book info -----------------------%s " ,bookcopy_rec)
        logging.warning(bookcopy_rec)
        #login_user_rec=http.request.env.user
 #       logging.info( login_user_rec.partner_id)

#
#        login_partner_rec  = http.request.env['res.partner'].search([
#            ('id', '=', login_user_rec.partner_id.id)
#        ], limit=1)

#        logging.info("login_partner......", login_partner_rec)


#        return http.request.render('library.create_rent', {'login_user_rec':login_user_rec,
#		'bookcopy_rec': bookcopy_rec,
#                'login_partner_rec':login_partner_rec})
        return http.request.render('library.create_rent', {'bookcopy_rec': bookcopy_rec})





    @http.route('/create/webrent', type="http", auth="public", website=True)
    def create_webrent(self, **kw):
        logging.warning("Execution Uid .................%s " , http.request.uid)  
#        logging.warning(http.request.env.context.get(uid)) not working 
        logging.info("Env.uer %s " , http.request.env.user)
#        login_user_rec=http.request.env.user
#        logging.info("login_user...... %s", login_user_rec)

#        logging.info(http.request.env.user.login)


        print("Data Received.....", kw)
        logging.info("In Create Web Rent")
        logging.info(kw)
        login_user_rec=http.request.env.user
        logging.info("login_user......", login_user_rec)


        login_partner_rec  = http.request.env['res.partner'].search([
				('id', '=', login_user_rec.partner_id.id)
			       ], limit=1)

        logging.info("login_partner......", login_partner_rec)
        
        kw['customer_id'] = login_partner_rec.id
        logging.info("Print kw")
        logging.info(kw)
        rental_rec = http.request.env['library.rental'].sudo().create(kw)
        logging.info("rental_rec :  %s " , rental_rec)
        return http.request.render("library.rent_thanks", {'rental_rec':rental_rec})



    @http.route('/library/library/', auth='public' , website=True)
    def index(self, **kw):
        BookCopy = http.request.env['library.copy']
        return http.request.render('library.index', {
            'bookcopy': BookCopy.sudo().search([])
        })

    @http.route('/library/books/', auth='public' , website=True)
    def books(self, **kw):
        Books = http.request.env['product.product']
        return http.request.render('library.books', {
            'books': Books.search([])
        })

   

#     @http.route('/academy/academy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('academy.listing', {
#             'root': '/academy/academy',
#             'objects': http.request.env['academy.academy'].search([]),
#         })

#     @http.route('/academy/academy/objects/<model("academy.academy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('academy.object', {
#             'object': obj
#         })
