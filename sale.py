# -*- encoding: utf-8 -*-
##############################################################################
#
#    cbk_crm_information: CRM Information Tab
#    Copyright (c) 2013 Codeback Software S.L. (http://codeback.es)    
#    @author: Miguel García <miguel@codeback.es>
#    @author: Javier Fuentes <javier@codeback.es>
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from datetime import datetime, timedelta  

import pdb

class sale_order_line(osv.osv):

    _name = "sale.order.line"
    _inherit = "sale.order.line"
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, context=None):

        result_prod = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag, context=context)

        if product:
            product_mod = self.pool.get('product.product')
            partner_mod = self.pool.get('res.partner')

            if partner_id:
                lang = partner_mod.browse(cr, uid, partner_id).lang            
            context_partner = {'lang': lang, 'partner_id': partner_id}

            product_obj = product_mod.browse(cr, uid, product, context=context_partner)

            if product_obj.parent_prod_id:
                parent_id = product_obj.parent_prod_id.id
                result_parent = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, parent_id, qty=qty,
                    uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
                    lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging,
                    fiscal_position=fiscal_position, flag=flag, context=flag)

                if result_prod['value'].get('price_unit') and result_parent['value'].get('price_unit'):
                    result_prod['value']['price_unit'] = result_parent['value']['price_unit']
                if result_prod['value'].get('purchase_price') and result_parent['value'].get('purchase_price'):
                    result_prod['value']['purchase_price'] = result_parent['value']['purchase_price']

        return result_prod

