from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class InheritStockPicking(models.Model):
    _inherit = 'stock.picking'

    motivos = fields.Selection([
        ('motivo1', 'motivo1'),
        ('motivo2', 'motivo2'),
        ('motivo3', 'motivo3')
    ], string="Motivo")
    is_aromitalia = fields.Boolean(string="is_aromitalia", default=False)
    is_parcial = fields.Boolean(string="parciales")
    state = fields.Selection(selection_add=[('por entregar', 'Por entregar')])

    def change_state(self):
        self.update({
            'state': 'por entregar'
        })

    def _create_backorder(self):
        mm_backs = super(InheritStockPicking, self)._create_backorder()
        for backmm in mm_backs:
            current_p = self.env['stock.picking.aromitalia'].create({
                'name': backmm.name,
                'is_parcial': True,
                'is_aromitalia': True,
                'origin': backmm.origin,
                'note': backmm.note,
                'move_type': backmm.move_type,
                'priority': backmm.priority,
                'date': backmm.date,
                'location_id': backmm.location_id.id,
                'location_dest_id': backmm.location_dest_id.id,
                'picking_type_id': backmm.picking_type_id.id,
                'partner_id': backmm.partner_id.id,
                'user_id': backmm.user_id.id,
                'owner_id': backmm.owner_id.id,
                'is_locked': backmm.is_locked,
                'immediate_transfer': backmm.immediate_transfer,
                'motivos': backmm.motivos,
                'carrier_price': backmm.carrier_price,
                'carrier_id': backmm.carrier_id.id,
                'l10n_mx_edi_customs_no': backmm.l10n_mx_edi_customs_no,
                'state': 'assigned',
                'scheduled_date': backmm.scheduled_date,

            })
            if backmm.move_line_ids:
                for line in backmm.move_line_ids:
                    line_n = self.env['stock.picking.aromitalia.lines'].create({
                        'picking_id': current_p.id,
                        'picking_origin': line.picking_id.id,
                        'product_id': line.product_id.id,
                        'product_uom_id': line.product_uom_id.id,
                        'location_id': line.location_id.id,
                        'location_dest_id': line.location_dest_id.id,
                        'company_id': line.company_id.id,
                        'reserved_uom_qty': line.reserved_uom_qty,
                        'lot_id': line.lot_id.id,
                        'package_id': line.package_id.id,
                        'owner_id': line.owner_id.id,
                        'qty_done': line.qty_done,
                    })


        return mm_backs

    @api.model_create_multi
    def create(self, vals):
        pickings = super(InheritStockPicking, self).create(vals)
        for picking in pickings:
            print('pickings---------------------------------------------------------')
            if picking.backorder_id:
                if picking.is_aromitalia == False:
                    print('pickings se crea aarom---------------------------------------------------')
            elif picking.origin:
                print('pickings id_rel seg', picking.id)
                if picking.origin[0] == 'S':
                    if picking.is_aromitalia == False:
                        print('pickings se crea aarom2---------------------------------------------------')
                        current_p = self.env['stock.picking.aromitalia'].create({
                            'id_rel': picking.id,
                            'name': picking.name,
                            'is_aromitalia': True,
                            'origin': picking.origin,
                            'note': picking.note,
                            'move_type': picking.move_type,
                            'priority': picking.priority,
                            'date': picking.date,
                            'location_id': picking.location_id.id,
                            'location_dest_id': picking.location_dest_id.id,
                            'picking_type_id': picking.picking_type_id.id,
                            'partner_id': picking.partner_id.id,
                            'user_id': picking.user_id.id,
                            'owner_id': picking.owner_id.id,
                            'is_locked': picking.is_locked,
                            'immediate_transfer': picking.immediate_transfer,
                            'motivos': picking.motivos,
                            'carrier_price': picking.carrier_price,
                            'carrier_id': picking.carrier_id.id,
                            'l10n_mx_edi_customs_no': picking.l10n_mx_edi_customs_no,
                            'state': 'assigned',
                            'scheduled_date': picking.scheduled_date,
                        })
        return pickings

class InheritStockPickingine(models.Model):
    _inherit = 'stock.move.line'

    @api.model_create_multi
    def create(self, vals):
        lines = super(InheritStockPickingine, self).create(vals)
        for line in lines:
            print('lines foooor----------------------------------------', vals)
            if line.picking_id:
                bus = self.env['stock.picking.aromitalia'].search([('id_rel', '=', line.picking_id.id)], order='id ASC')
                print('linlen', len(line.picking_id.move_line_ids_without_package))
                print('buslen', len(bus.move_line_ids_arom))
                if bus:
                    if len(line.picking_id.move_line_ids_without_package) == (len(bus.move_line_ids_arom) +1):
                        line_n = self.env['stock.picking.aromitalia.lines'].create({
                            'picking_origin': line.picking_id.id,
                            #'backorder_id': line.backorder_id.id,
                            'product_id': line.product_id.id,
                            'product_uom_id': line.product_uom_id.id,
                            'location_id': line.location_id.id,
                            'location_dest_id': line.location_dest_id.id,
                            'company_id': line.company_id.id,
                            'reserved_uom_qty': line.reserved_uom_qty,
                            'lot_id': line.lot_id.id,
                            'package_id': line.package_id.id,
                            'owner_id': line.owner_id.id,
                            'qty_done': line.qty_done,

                        })

                        print('lines bus', bus)
                        if bus:
                            for busl in bus:
                                if not busl.move_line_ids_arom:
                                    line_n.update({
                                        'picking_id': busl.id
                                    })
                                else:
                                    if busl.move_line_ids_arom[0].picking_id.id == busl.id:
                                        line_n.update({
                                            'picking_id': busl.id
                                        })

        print('lines foooor----------------------------------------f')
        return lines
#

    def write(self, vals):
        stpick = super(InheritStockPickingine, self).write(vals)
        print('write vals', vals)
        print('write self', self)
        print('write stpick', stpick)

        return stpick