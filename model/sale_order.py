from odoo import models,api, fields, _

class sale_order(models.Model):
    _inherit = "sale.order"
    
    domain_allowed_warehouse_ids = fields.Char(compute="_get_domain_allowed_warehouse_ids",store=False)

    @api.depends('company_id')
    def _get_domain_allowed_warehouse_ids(self):
        for record in self:
            domain = []
            # Get user's inventory config for current company
            config = self.env['res.user.inventory.config'].search([
                ('user_id', '=', self.env.user.id),('company_id', '=', record.company_id.id),('operation_type', '=', 'outgoing')], limit=1)
            
            if config and config.allowed_warehouse_ids:
                domain = [("id", "in", config.allowed_warehouse_ids.ids)]
            elif self.env.company.allowed_warehouse_ids:
                domain = [("id", "in", self.env.company.allowed_warehouse_ids.ids)]
            
            record.domain_allowed_warehouse_ids = domain


    @api.onchange("company_id", "partner_id")
    def _default_warehouse(self):
        for rec in self:
            # Find user's inventory config for the selected company
            config = self.env['res.user.inventory.config'].search([
                ('user_id', '=', self.env.user.id),('company_id', '=', rec.company_id.id),('operation_type', '=', 'outgoing')], limit=1)
            
            # Set warehouse based on:
            # 1. User's default warehouse in config
            # 2. Company's default warehouse
            if config and config.default_warehouse_id:
                if config.default_warehouse_id.company_id == rec.company_id:
                    rec.write({"warehouse_id": config.default_warehouse_id.id})

            elif rec.company_id.default_warehouse_id:
                if rec.company_id.default_warehouse_id.company_id == rec.company_id:
                    rec.write({"warehouse_id": rec.company_id.default_warehouse_id.id})
