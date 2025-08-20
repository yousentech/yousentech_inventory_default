from odoo import models, api,fields, _

class purchase_order(models.Model):
    _inherit = "purchase.order"

    picking_type_domain = fields.Char(
        string="Picking Type Domain",
        compute="_compute_picking_type_warehouse_domain",
        store=False)

    @api.depends('partner_id', 'company_id')
    def _compute_picking_type_warehouse_domain(self):
        for order in self:
            domain = []
            # Get user's inventory config for current company
            config = self.env['res.user.inventory.config'].search([
                ('user_id', '=', self.env.user.id),('company_id', '=', order.company_id.id),('operation_type', '=', 'incoming')], limit=1)
            
            # Priority 1: Use user's default warehouse from config
            if config and config.default_warehouse_id:
                domain = [
                    ('warehouse_id', '=', config.default_warehouse_id.id),
                    ('code', '=', 'incoming')]
            # Priority 2: Fall back to company default
            elif order.company_id.default_warehouse_id:
                domain = [
                    ('warehouse_id', '=', order.company_id.default_warehouse_id.id),
                    ('code', '=', 'incoming')]
            
            order.picking_type_domain = domain
            

    def _get_picking_type(self, company_id):
        picking_type = super(purchase_order, self)._get_picking_type(company_id)
        
        # First check if there's a user-specific configuration
        user_config = self.env['res.user.inventory.config'].search([
            ('user_id', '=', self.env.user.id),('company_id', '=', company_id),('operation_type', '=', 'incoming')], limit=1)
        
        if user_config and user_config.picking_type_id:
            # Use the picking type from user's inventory config if it matches the operation type
            picking_type = user_config.picking_type_id.id
        elif self.env.company.purchase_picking_type_id:
            # Company's default if no user-specific setting
            picking_type = self.env.company.purchase_picking_type_id.id
        
        return picking_type

    def _prepare_picking(self):
        res = super(purchase_order, self)._prepare_picking()
        
        # Get user configuration for current company
        user_config = self.env['res.user.inventory.config'].search([
            ('user_id', '=', self.env.user.id),('company_id', '=', self.company_id.id),('operation_type', '=', 'incoming')], limit=1)
        
        # Priority 1: Use picking type from user config if operation type is incoming
        if user_config and user_config.picking_type_id and user_config.operation_type == 'incoming':
            res["picking_type_id"] = user_config.picking_type_id.id
        # Priority 2: Use company default
        elif self.env.company.purchase_picking_type_id:
            res["picking_type_id"] = self.env.company.purchase_picking_type_id.id
        
        return res
    
            
            
    