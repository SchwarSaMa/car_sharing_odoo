from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo import api


class CarReservation(models.Model):
    _name = "car.reservation"
    _description = "Car Sharing Reservation"

    location_from = fields.Char(string="Startort", required=True)
    location_to = fields.Char(string="Zielort")
    departure_time = fields.Datetime(string="Departure Date", required=True)
    return_date = fields.Datetime(string="Return Date", required=True)

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

    @api.constrains("departure_time", "return_date")
    def _validate_return_date(self):
        for record in self:
            if record.return_date <= record.departure_time:
                raise ValidationError(
                    "The car's return date cannot lie before the departure time"
                )

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

    @api.constrains("departure_time", "return_date", "vehicle_id")
    def _prevent_double_reservation(self):
        for record in self:
            if record.departure_time and record.return_date:
                domain = [
                    ("vehicle_id", "=", record.vehicle_id.id),
                    ("id", "!=", record.id),
                    ("return_date", ">", record.departure_time),
                    ("departure_time", "<", record.return_date),
                ]
                search_results = self.env["car.reservation"].search(domain)

                if search_results:
                    raise ValidationError(
                        f"This car {record.vehicle_id.name} is already reserved:\n"
                        f"from {search_results[0].departure_time} until {search_results[0].return_date}\n"
                    )

    @api.depends("passenger_ids", "tot_seats", "driver_id")
    def _compute_available_seats(self):
        for record in self:
            tot_people = len(record.passenger_ids) + 1
            record.available_seats = record.tot_seats - tot_people
