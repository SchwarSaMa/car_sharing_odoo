{
    "name": "Car Sharing Reservation",
    "version": "1.0",
    "summary": "Administration of car reservations",
    "description": """
        This module can:
        - make reservations for cars in the fleet
        - adds passengers and a driver to a reservation
        - checks the cars capacity if it has number of seats
    """,
    "category": "Services",
    "author": "Maximilian",
    "depends": [
        "base",
        "fleet",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/reservation_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
