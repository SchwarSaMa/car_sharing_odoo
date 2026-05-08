from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api


class CarReservation(models.Model):
    _name = "car.reservation"
    _description = "Car Sharing Reservation"

    location_from = fields.Char(string="Startort", required=True)
    location_to = fields.Char(string="Zielort")
    departure_time = fields.Datetime(string="Departure", required=True)

    tot_seats = fields.Integer(
        string="Seats",
        related="vehicle_id.seats",
        readonly=True,
        store=True,
    )
    available_seats = fields.Integer(
        string="Available Seats",
        compute="_compute_available_seats",
        store=True,
    )

    vehicle_id = fields.Many2one("fleet.vehicle", string="Vehicle", required=True)
    driver_id = fields.Many2one("res.users", string="Driver", required=True)

    passenger_ids = fields.Many2many("res.users", string="Passengers")

    @api.constrains("departure_time")
    def _validate_departure_time(self):
        for record in self:
            if record.departure_time < fields.Datetime.now():
                raise ValidationError("Departure time cannot lie in the past.")

    @api.constrains("driver_id", "passenger_ids")
    def _check_driver_in_passenger(self):
        for record in self:
            if record.driver_id in record.passenger_ids:
                raise ValidationError(
                    f"Driver {record.driver_id.name} cannot be a passenger at the same time."
                )

    @api.constrains("vehicle_id", "passenger_ids", "tot_seats")
    def _check_vehicle_capacity(self):
        for record in self:
            if record.vehicle_id and record.vehicle_id.seats <= 0:
                raise ValidationError(
                    f"Add number of seats for the car: {record.vehicle_id.name} "
                )
            # passengers plus 1 driver
            tot_passengers = len(record.passenger_ids) + 1
            if tot_passengers > record.tot_seats:
                raise ValidationError(
                    f"The vehicle {record.vehicle_id.name} only has {record.tot_seats} seats. "
                    f"Including the driver all {tot_passengers} seats are occupied."
                )

    @api.depends("passenger_ids", "tot_seats", "driver_id")
    def _compute_available_seats(self):
        for record in self:
            tot_people = len(record.passenger_ids) + len(record.driver_id)
            record.available_seats = record.tot_seats - tot_people
