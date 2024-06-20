from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class InheritHelpDesk(models.Model):
    _name = "stock.picking.aromitalia"
    _inherit = ['stock.picking']

    is_aromitalia = fields.Boolean(string="is_aromitalia", default=False)
    motivos = fields.Selection([
        ('motivo1', 'motivo1'),
        ('motivo2', 'motivo2'),
        ('motivo3', 'motivo3')
    ], string="Motivo")

    id_rel = fields.Integer(string="id relacionado")
    move_line_ids_arom = fields.One2many('stock.picking.aromitalia.lines', 'picking_id', 'Operations without package')

    # @api.depends('move_line_ids_arom')
    # def _cal_weight_mm(self):
    #     for picking in self:
    #         picking.weight = sum(move.weight for move in picking.move_line_ids_arom)

    # def _compute_shipping_weight_mm(self):
    #     for picking in self:
    #         # if shipping weight is not assigned => default to calculated product weight
    #         picking.shipping_weight = picking.weight_bulk + sum([pack.shipping_weight or pack.weight for pack in picking.package_ids])


    #weight_mm = fields.Float(compute='_cal_weight_mm', digits='Stock Weight', store=True, help="Total weight of the products in the picking.", compute_sudo=True)
    #shipping_weight_mm = fields.Float("Weight for Shipping", compute='_compute_shipping_weight_mm', help="Total weight of packages and products not in a package. Packages with no shipping weight specified will default to their products' total weight. This is the weight used to compute the cost of the shipping.")

    def _set_scheduled_date(self):
        print('nada')




class InheritHelpDeskLines(models.Model):
    _name = "stock.picking.aromitalia.lines"

    picking_id = fields.Many2one(
        'stock.picking.aromitalia', 'Transfer', auto_join=True,
        check_company=True,
        index=True,
        help='The stock operation where the packing has been made')
    product_id = fields.Many2one('product.product', 'Product', index=True,)
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure',related='product_id.uom_id', store=True)
    location_id = fields.Many2one(
        'stock.location', 'From', check_company=True, required=True, store=True, readonly=False)
    location_dest_id = fields.Many2one('stock.location', 'To', store=True, readonly=False)
    company_id = fields.Many2one('res.company', string='Company', readonly=True, required=True, index=True)
    reserved_uom_qty = fields.Float('Reserved', default=0.0, digits='Product Unit of Measure', required=True, copy=False)
    lot_id = fields.Many2one(
        'stock.lot', 'Lot/Serial Number',
        domain="[('product_id', '=', product_id), ('company_id', '=', company_id)]", check_company=True)
    package_id = fields.Many2one(
        'stock.quant.package', 'Source Package', ondelete='restrict',
        check_company=True,
        domain="[('location_id', '=', location_id)]")
    owner_id = fields.Many2one(
        'res.partner', 'From Owner',
        check_company=True,
        help="When validating the transfer, the products will be taken from this owner.")
    qty_done = fields.Float('Done', default=0.0, digits='Product Unit of Measure', copy=False)
    picking_origin = fields.Integer('id origin')
    backorder_id = fields.Integer('id back')

    @api.model_create_multi
    def create(self, vals):
        pickings = super(InheritHelpDeskLines, self).create(vals)
        print('vlas line arom',vals )
        return pickings


