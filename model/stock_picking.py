from odoo import models,api, fields, _

class stock_picking(models.Model):
    _inherit = "stock.picking"

    
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
                ('user_id', '=', self.env.user.id),('company_id', '=', order.company_id.id),('operation_type', '=', 'internal')], limit=1)
            
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