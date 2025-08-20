from odoo import models, fields,_
class res_user(models.Model):
    _inherit = 'res.users'
  
    inventory_config_ids = fields.One2many(
        'res.user.inventory.config','user_id',
        string='Inventory Defaults'
    ) 
    
    default_product_type = fields.Selection(
        selection=[('consu', 'Consumable'), ('service', 'Service'), ('product', 'Storable Product')],
        string='Default Product Type',
        help='This type will be used as default when creating new products'
    )
    
  
        
            
   

