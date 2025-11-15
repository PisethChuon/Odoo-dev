# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _, _logger


class HostelRoom(models.Model):
    _name = 'hostel.room'
    _description = "Information about hostel Room"

    # Additional fields specific to basic_server_side
    name = fields.Char(string="Hostel Name", required=True)
    room_no = fields.Char(string="Room Number", required=True)
    allocation_date = fields.Date(string="Allocation Date")
    other_info = fields.Text("Other Information",
                             help="Enter more information")
    description = fields.Html('Description')
    room_rating = fields.Float('Hostel Average Rating', digits=(14, 4))
    member_ids = fields.Many2one('hostel.room.member', string='Members')
    category_id = fields.Many2one('hostel.room.category', string='Category')
    cost_price = fields.Float('Room Cost Price')
    previous_room_id = fields.Many2one('hostel.room', string='Previous Room')
    state = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('closed', 'Closed')],
        'State', default="draft")
    remarks = fields.Text('Remarks')

    @api.model
    def create(self, values):
        if not self.user_has_groups('local-addons.group_hostel_manager'):
            values.get('remarks')
            if values.get('remarks'):
                raise UserError(
                    'You are not allowed to set remarks field.'
                )
        return super(HostelRoom, self).create(values)

    def write(self, values):
        if not self.user_has_groups('local-addons.group_hostel_manager'):
            if values.get('remarks'):
                raise UserError(
                    'You are not allowed to modify remarks field.'
                )
        return super(HostelRoom, self).write(values)

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

    #  Makes room records display more informatively by showing who lives in each room
    def name_get(self):
        result = []
        for room in self:
            members = room.member_ids.mapped('name')
            name = '%s (%s)' % (room.name, ', '.join(members))
            result.append((room.id, name))
        return result

    # Makes it easier to find rooms by allowing searches across room names
    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None):
        domain = domain or []

        if name:
            name_domain = [
                '|', '|',
                ('name', operator, name),
                ('room_no', operator, name),
                ('member_ids.name', operator, name)
            ]
            domain = name_domain + domain

        # Search and return IDs
        return self._search(domain, limit=limit, order=order)

    def log_all_room_members(self):
        hostel_room_obj = self.env['hostel.room.member']  # This is an empty recordset of model 'hostel.room.member'
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

    # Method to filter rooms with multiple members
    def filter_members(self):
        all_rooms = self.search([])
        filtered_rooms = self.rooms_with_multiple_members(all_rooms)
        _logger.info('Filtered Rooms found: %s', filtered_rooms)

    @api.model
    def rooms_with_multiple_members(self, all_rooms):
        return all_rooms.filtered(lambda b: len(b.member_ids) > 1)

    # Method to map room members' names
    def mapped_rooms(self):
        all_rooms = self.search([])
        room_authors = self.get_member_names(all_rooms)
        _logger.info('Mapped Rooms found: %s', room_authors)

    @api.model
    def get_member_names(self, all_rooms):
        return all_rooms.mapped('member_ids.name')

    # Method to sort rooms by rating
    def sort_room(self):
        all_rooms = self.search([])
        rooms_sorted = self.sort_rooms_rating(all_rooms)
        _logger.info('Sorted Rooms found: %s', all_rooms)
        _logger.info('Sorted Rooms Rating: %s', rooms_sorted)

    # Api method to sort rooms by rating
    @api.model
    def sort_rooms_rating(self, all_rooms):
        return all_rooms.sorted(key='room_rating')

    def grouped_data(self):
        data = self._get_average_cost()
        _logger.info('Average Cost: %s', data)

    @api.model
    def _get_average_cost(self):
        grouped_result = self.read_group(
            ['cost_price', '!=', False],  # Domain
            ['category_id', 'cost_price:avg'],  # Fields to read
            ['category_id']  # Group by
        )
        return grouped_result


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
