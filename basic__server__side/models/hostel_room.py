from odoo import fields, models, api

class HostelRoom(models.Model):

    _name = 'hostel.room'
    _description = 'Information about Hostel Rooms'

    name = fields.Char(string='Hostel Room Name', required=True)
    room_no = fields.Char(string='Room Number', required=True)
    other_info = fields.Text(string='Other Information')
    description = fields.Html('Description')
    room_rate = fields.Float(string='Hostel Average Rating', digits=(14, 4))
    state = fields.Selection([('draft', 'Draft'), ('available', 'Available'), ('closed', 'Closed')], 'State', default='draft')

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'), ('available', 'closed'), ('closed', 'available')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                continue

    def make_available(self):
        self.change_state('available')

    def make_closed(self):
        self.change_state('closed')