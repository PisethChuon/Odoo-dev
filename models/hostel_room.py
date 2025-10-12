from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.tools.populate import compute


class HostelRoom(models.Model):

    _name = "hostel.room"
    _description = "Hostel Room Information"
    _rec_name = "room_no"

    name = fields.Char(string="Room Name", required=True)
    room_no = fields.Char("Room No.", required=True)
    floor_no = fields.Integer("Floor No.", default=1, help="Floor Number")
    currency_id = fields.Many2one('res.currency', string="Currency")
    rent_amount = fields.Monetary('Rent Amount', help="Enter rent amount per month")
    student_ids = fields.One2many("hostel.student", "room_id", string="Students", help="Enter students")
    student_per_room = fields.Integer("Student per Room",requests=True, default=1, help="Student allocated per Room")
    availability = fields.Float(compute="_compute_availability", string="Availability", help="Room availability in hostel")

    _sql_constraints = [("room_no_unique", "unique(room_no)", "Room number must be unique!")]

    @api.constrains('rent_amount')
    def _check_rent_amount(self):
        """Constraint on negative rent amount"""
        if self.rent_amount < 0:
            raise ValidationError("Rent amount must be positive")

    @api.depends('student_per_room', 'student_per_room')
    def _compute_check_availability(self):
        """Method to check room availability"""
        for rec in self:
            rec.availability = rec.student_per_room - len(rec.student_ids.ids)
