from odoo import models,_,fields ,api
class product_template(models.Model):
    _inherit = 'product.template'
    
    @api.model
    def default_get(self, fields_list):
        defaults = super(product_template, self).default_get(fields_list)
        
        # Get default values in order: User -> Company -> Odoo default
        user_type = self.env.user.default_product_type
        company_type = self.env.company.default_product_type
        
        if user_type:
            defaults['detailed_type'] = user_type
        elif company_type:
            defaults['detailed_type'] = company_type
        # Note : If no value is set, Odoo's default will be used
        
        return defaults