# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
from io import StringIO, BytesIO
import logging
import json
import requests

class upc_generator(models.Model):
    _name = 'upc.generator'

    name = fields.Char(string='UPC code', size=11, required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True)
    line_ids = fields.One2many('upc.generator.lines', inverse_name='upc_id', string='UPC Generado')

    _defaults = {
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'account.account', context=c),
    }

    def generate_upc(self, cr, uid, ids, context=None):
        #        Now we need to do the UPC A check digit calculation.
        #        Add up the numbers in the odd positions left to right. Multiple the result by 3.
        #        Add up the numbers in the even positions. Now add the first subtotal to the second.
        #        The UPC barcode check digit is the single digit number makes the total a multiple of 10.'
        #        …….s…..t…….r……i…….n…..g
        #        ….0……1……2…..3……4……5
        #        ..-6….-5….-4….-3….-2….-1

        upc_ids = self.search(cr, uid, [], context=context)

        if not len(upc_ids):
            raise osv.except_osv(_('Error'), _('Please enter UPC Code in Configuration'))

        upc_data = self.browse(cr, uid, upc_ids[0], context=context)
        if not len(upc_data.name) == 11:
            raise osv.except_osv(_('Error'), _('UPC Code in Configuration should be of 11 digits'))

        checksum_digit = self.calc_checksum(upc_data.name)
        #        checkDigitSubtotal = int(upc_data.name[:-10]) + int(upc_data.name[2:-8]) + int(upc_data.name[4:-6]) + int(upc_data.name[6:-4]) + int(upc_data.name[8:-2]) + int(upc_data.name[10:])
        #
        #        checkDigitSubtotal = int(3 * int(checkDigitSubtotal)) + int(upc_data.name[1:-9]) + int(upc_data.name[3:-7]) + int(upc_data.name[5:-5]) + int(upc_data.name[7:-3]) + int(upc_data.name[9:-1])
        #
        #        checkDigitSubtotal = 300 - checkDigitSubtotal
        #
        #        string_convert_ckd = str(checkDigitSubtotal)
        #        checksum_digit = string_convert_ckd[len(string_convert_ckd)-1:]

        new_upc_code = int(upc_data.name) + 1
        if new_upc_code:
            self.write(cr, uid, upc_ids, {'name': new_upc_code})

        vals = {
            'name': str(upc_data.name),
            'check_digit': str(checksum_digit),
            'upc_id': upc_ids[0],
            'product_id': ids[0]
        }
        line_ids = self.pool.get('upc.generator.lines').search(cr, uid, [('product_id', '=', ids[0])])
        if len(line_ids):
            self.pool.get('upc.generator.lines').write(cr, uid, line_ids[0], vals)
        else:
            self.pool.get('upc.generator.lines').create(cr, uid, vals)

        return str(upc_data.name) + str(checksum_digit)

    def calc_checksum(self, s):
        even_sum = 0
        odd_sum = 0
        for x in range(0, len(s)):
            if x % 2 == 0:
                even_sum += int(s[x:x + 1])
            else:
                odd_sum += int(s[x:x + 1])

        result = (even_sum * 3) + odd_sum

        mod_val = result % 10
        if mod_val == 0:
            checksum_digit = 0
        else:
            checksum_digit = 10 - mod_val

        return checksum_digit


upc_generator()


class upc_generator_lines(osv.osv):
    _name = 'upc.generator.lines'

    _columns = {
        'name': fields.char('UPC 11 digit code', size=11, readonly=True),
        'check_digit': fields.char('UPC Version A check digit', size=1, readonly=True),
        'upc_id': fields.many2one('upc.generator', 'UPC code'),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
    }

    _order = 'id'


upc_generator_lines()

