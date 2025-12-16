from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class res_user_inventory_config(models.Model):
    _name = 'res.user.inventory.config'
    _description = 'Inventory User Config'

    company_id = fields.Many2one('res.company', string='Company')
    user_id = fields.Many2one('res.users',string='Users')
    
    # Allowed warehouses
    allowed_warehouse_ids = fields.Many2many(
        'stock.warehouse', string='Allowed Warehouses',domain="[('company_id','=',company_id)]")
    
    # Default warehouse
    default_warehouse_id = fields.Many2one(
        'stock.warehouse', string='Default Warehouse',domain="[('id', 'in', allowed_warehouse_ids)]")
    
    # Operation type based on default warehouse
    operation_type = fields.Selection([
        ('incoming', 'Purchases'),
        ('outgoing', 'Sales'),
        ('internal', 'Internal'),
    ], string='Operation Type')
    
    picking_type_id = fields.Many2one('stock.picking.type', string='Place Of sale/purchase')
    domain_picking_type_id = fields.Char("domain_picking_type_id",compute="_compute_domain_picking_types")

    @api.depends('operation_type', 'default_warehouse_id')
    def _compute_domain_picking_types(self):
        for record in self:
            if not record.operation_type and not record.default_warehouse_id:
                record.domain_picking_type_id = []
                continue
            domain = [('warehouse_id', '=', record.default_warehouse_id.id),('company_id','=',record.company_id.id)]
            if record.operation_type == 'incoming':
                domain.append(('code','=','incoming'))
            elif record.operation_type == 'outgoing':
                domain.append(('code','=','outgoing'))
            elif record.operation_type == 'internal':
                domain.append(('code','=','internal'))
            
            record.domain_picking_type_id = domain
            
    domain_company_id = fields.Char("domain_company_id",compute="compute_company_id_domain")
 
    @api.depends("user_id")
    def compute_company_id_domain(self):
      for rec in self :  
        rec.domain_company_id = [("id", "in", rec.user_id.company_ids.ids)]
        
    
    @api.onchange('operation_type','company_id')
    def _onchangeOperationType(self):
        for rec in self:
            rec.allowed_warehouse_ids = False
            rec.default_warehouse_id = False
            rec.picking_type_id = False
            
    @api.constrains('company_id', 'operation_type')
    def _check_company_operation_type_unique(self):
        for record in self:
            if record.company_id and record.operation_type:
                existing_records = self.search([
                    ('company_id', '=', record.company_id.id),
                    ('operation_type', '=', record.operation_type),
                    ('id', '!=', record.id),('user_id','=',  self.env.uid)
                ])
                if existing_records:
                    raise ValidationError(
                        _("A record with company '%s' and operation type '%s' already exists!") % 
                        (record.company_id.name, record.operation_type)
                    )
                    