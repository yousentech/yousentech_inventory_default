from odoo import models, fields, _,api

class res_company(models.Model):
    _inherit = 'res.company'
    
    allowed_warehouse_ids = fields.Many2many('stock.warehouse', string='Allowed Warehouses',domain="[('company_id','in',self.env.user.company_ids)]")
    # domain feild
    domain_allowed_warehouse_ids = fields.Char("domain_stock_allowed_ids",compute="_get_domain_allowed_warehouse_ids")
   
    def _get_domain_allowed_warehouse_ids(self):
        for record in self:  
            record.domain_allowed_warehouse_ids = [("company_id", "in", self.env.user.company_ids.ids)]

    default_warehouse_id = fields.Many2one('stock.warehouse', string='Default Warehouse')
    # domain feild
    domain_default_warehouse_id = fields.Char("domain_default_warehouse_id",compute="_get_domain_default_warehouse_id")
   
    @api.depends('allowed_warehouse_ids')
    def _get_domain_default_warehouse_id(self):
        for record in self: 
            record.domain_default_warehouse_id = [("id", "in", record.allowed_warehouse_ids.ids)]
            
    sale_picking_type_id = fields.Many2one('stock.picking.type', string='Place Of Sale', domain=[('code', '=', ['outgoing'])])
    # domain feild
    domain_picking_type_id= fields.Char("domain_picking_type_id",compute="_compute_picking_type_domain")
    
    @api.depends('default_warehouse_id')
    def _compute_picking_type_domain(self):
        for record in self:  
            record.domain_picking_type_id = [('warehouse_id', '=', record.default_warehouse_id.id),('code','=','outgoing')]
            
    purchase_picking_type_id = fields.Many2one("stock.picking.type", string="Where to buy",domain=[('code','=','incoming')])
    purchase_picking_type_domain= fields.Char("purchase_picking_type_domain",compute="_compute_branch_picking_type_domain")
    
    @api.depends('default_warehouse_id')
    def _compute_branch_picking_type_domain(self):
        self.purchase_picking_type_domain = [('warehouse_id', '=', self.default_warehouse_id.id),('code','=','incoming')]
        
        
    default_product_type = fields.Selection(
        selection=[('consu', 'Consumable'), ('service', 'Service'), ('product', 'Storable Product')],
        string='Default Product Type',
        help='This type will be used as default when creating new products'
    )
  
    # internal_picking_type_id = fields.Many2one('stock.picking.type', string='Internal Operation Type',domain=[('code','=','internal')])
    # # domain feild
    # domain_internal_picking_type_id= fields.Char("domain_internal_picking_type_id",compute="_compute_internal_picking_type_domain")
    
    # @api.depends('default_warehouse_id')
    # def _compute_internal_picking_type_domain(self):
    #     for record in self:  
    #         record.domain_internal_picking_type_id = [('warehouse_id', '=', record.default_warehouse_id.id),('code','=','internal')]       
            
