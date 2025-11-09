from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    active = fields.Boolean('Active', default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active

class HostelRoom(models.Model):
    _name = "hostel.room"
    _description = "Hostel Room Information"
    _inherit = ['base.archive']
    _rec_name = "room_no"

    @api.depends("student_per_room", "student_ids")
    def _compute_check_availability(self):
        """Method to check room availability"""
        for rec in self:
            student_count = len(rec.student_ids) if rec.student_ids else 0
            rec.availability = rec.student_per_room - student_count

    name = fields.Char(string="Room Name", required=True)
    room_no = fields.Char("Room No.", required=True)
    floor_no = fields.Integer("Floor No.", default=1, help="Floor Number")
    currency_id = fields.Many2one('res.currency', string='Currency')
    rent_amount = fields.Monetary('Rent Amount',
                                  help="Enter rent amount per month")  # optional attribute: currency_field='currency_id' incase currency field have another name then 'currency_id'
    hostel_id = fields.Many2one("hostel.hostel", "hostel", help="Name of hostel")
    student_ids = fields.One2many("hostel.student", "room_id",
                                  string="Students", help="Enter students")
    hostel_amenities_ids = fields.Many2many("hostel.amenities",
                                            string="Amenities", domain="[('active', '=', True)]",
                                            help="Select hostel room amenities")
    student_per_room = fields.Integer("Student Per Room", required=True,
                                      help="Students allocated per room")
    availability = fields.Float(compute="_compute_check_availability",
                                store=True, string="Availability", help="Room availability in hostel")

    _sql_constraints = [
        ("room_no_unique", "unique(room_no)", "Room number must be unique!")]

    def write(self, vals):
        """Override write to recompute student hostel_id when room hostel_id changes"""
        result = super(HostelRoom, self).write(vals)
        if 'hostel_id' in vals and self.student_ids:
            # Trigger recomputation of hostel_id on all students in this room
            self.student_ids._compute_hostel_id()
        return result

    @api.constrains("rent_amount")
    def _check_rent_amount(self):
        """Constraint on negative rent amount"""
        if self.rent_amount < 0:
            raise ValidationError(_("Rent Amount Per Month should not be a negative value!"))
