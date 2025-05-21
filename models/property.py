from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    ref = fields.Char(readonly=True,default="New")
    name = fields.Char(required=True,default="New",translate=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char()
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute="_compute_diff",store=1)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ],default="north")

    state = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('sold','Sold'),
        ('closed','Closed'),
    ], default='draft')
    
    owner_id = fields.Many2one('owner')
    owner_phone = fields.Char(related='owner_id.phone' ,readonly=0)
    owner_address = fields.Char(related='owner_id.address',readonly=0)
    tag_ids = fields.Many2many('tag')
    active = fields.Boolean(default=1)
    create_time = fields.Datetime(default=fields.Datetime.now())
    next_time = fields.Datetime(compute='_compute_next_time')

    _sql_constraints = [
        ('unique_name','unique("name")','This name is exist!')
    ]

    line_ids = fields.One2many('property.line','property_id')

    @api.depends('expected_price','selling_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price 
    
    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False



    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            if rec.expected_price < 0 :
                return{
                    'warning' : {
                        'title' : 'Warning',
                        'message' : 'negative value.',
                        'type': 'notification'
                        }
                }

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0 :
                raise ValidationError('Please add valid number of bedrooms!')
            

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state,'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state,'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state,'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state,'closed')
            rec.state = 'closed'  


    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True

    @api.model
    def create(self,vals):
        res = super(Property,self).create(vals)
        if res.ref == "New":
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res
    
    def create_history_record(self,old_state,new_state,reason = ""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id' : rec.env.uid,
                'property_id':rec.id,
                'old_state':old_state,
                'new_state':new_state,
                'reason':reason or "",
                'line_ids':[(0,0,{'description' : line.description, 'area': line.area }) for line in rec.line_ids],
            })

    def action_open_change_state_wizerd(self):
        action = self.env['ir.actions.actions']._for_xml_id('real_estate.change_state_wizerd_action')
        action['context'] = {'default_property_id':self.id}
        return action
    
    def action(self):
        print(self.env['property'].search(['|',('name','=','property1'),('postcode','!=','24445')]))

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('real_estate.owner_action')
        view_id = self.env.ref('real_estate.owner_view_form')
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id.id,'form']]
        return action

class PropertyLine(models.Model):
    _name = 'property.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')