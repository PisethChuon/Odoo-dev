# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _, _logger


class HostelRoom(models.Model):

    _name = 'hostel.room'
    _description = "Information about hostel Room"

    name = fields.Char(string="Hostel Room Name", required=True)
    room_no = fields.Char(string="Room Number", required=True)
    other_info = fields.Text("Other Information",
        help="Enter more information")
    description = fields.Html('Description')
    room_rating = fields.Float('Hostel Average Rating', digits=(14, 4))
    state = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('closed', 'Closed')],
        'State', default="draft")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'closed'),
                   ('closed', 'draft')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                message = _('Moving from %s to %s is not allowed') % (room.state, new_state)
                raise UserError(message)
    # Method to change state to 'draft'
    def make_available(self):
        self.change_state('available')
    # Method to change state to 'closed'
    def make_closed(self):
        self.change_state('closed')

    def log_all_room_members(self):
        hostel_room_obj = self.env['hostel.room.member']    # This is an empty recordset of model 'hostel.room.member'
        all_members = hostel_room_obj.search([])
        print('all_members', all_members)
        return True
    # Method to create categories with child categories
    def create_categories(self):
        categ1 = {
            'name': 'Single Room',
            'description': 'Single Room Category'
        }
        categ2 = {
            'name': 'Double Room',
            'description': 'Double Room Category',
        }
        parent_category_val = {
            'name': 'Deluxe Room',
            'description': 'Deluxe Room Category',
            'child_ids': [(0, 0, categ1), (0, 0, categ2)]
        }
        record = self.env['hostel.room.category'].create(parent_category_val)
        return True

    # Method to update room number
    def update_room_no(self):
        self.ensure_one()
        self.room_no = 'RM002'

    def find_room(self):
        domain = [
            '|',
                '&', ('name', 'ilike', 'Room Name'),
                     ('category_id.name', '=', 'Category Name'),
                '&', ('name', 'ilike', 'Another Room Name'),
                     ('category_id.name', '=', 'Another Category Name')
        ]
        rooms = self.search(domain)
        _logger.info('Room found: %s', rooms)
        return True

    def filter_members(self):
        all_rooms = self.search([])
        filtered_rooms = self.rooms_with_multiple_members(all_rooms)
        _logger.info('Filtered Rooms found: %s', filtered_rooms)

    @api.model
    def rooms_with_multiple_members(self, all_rooms):
        return all_rooms.filtered(lambda b: len(b.member_ids) > 1)



class HostelRoomNumber(models.Model):
    _name = 'hostel.room.member'
    # Use delegation inheritance so each hostel.room.member delegates to a res.partner record
    _inherits = {'res.partner': 'partner_id'}
    _description = "Hostel Room Number Inherited from res.partner"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of Birth')