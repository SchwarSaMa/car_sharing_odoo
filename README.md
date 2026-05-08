# Car Sharing Reservation Management

A specialized Odoo module designed to manage internal corporate car-sharing.

## 1. Description

This project implements a reservation system within Odoo. It extends the standard fleet management capabilities by adding a custom reservation layer. The core logic ensures that vehicles are never double-booked and that seat capacities are strictly respected, including the driver.

**Key Technical Features:**

* **Collision Detection:** Advanced domain filtering prevents overlapping time slots for the same vehicle.
* **Capacity Logic:** Real-time computation of available seats based on many-to-many passenger relationships.
* **Data Integrity:** Multi-layer Python constraints (`@api.constrains`) to prevent past-dated bookings or illogical time ranges.

## 2. Installation

To set up this module in your Odoo environment, follow these steps:

### Prerequisites
*   **Odoo Version:** Developed and tested for **Odoo 19.0**.
*   **Core Dependencies:** 
    *   **Fleet (`fleet`):** This module extends `fleet.vehicle` to manage car-specific data and seat synchronization.
    *   **Base (`res.users`):** Integrates with the standard Odoo user management for assigning Drivers and Passengers.

### Setup Steps
1.  **Clone the Repository**  
    Navigate to your Odoo custom addons folder and clone the repository:
    ```bash
    git clone https://github.com/SchwarSaMa/car_sharing_odoo.git
    ```

2.  **Server Configuration**  
    Make sure your Odoo configuration file (`odoo.conf`) includes the path to the directory where you cloned the repo:
    ```ini
    addons_path = /your/path/to/odoo/addons, /path/to/car_sharing_odoo
    ```

3.  **Module Activation**  
    *   Restart your Odoo service.
    *   Login to your Odoo instance as **Administrator**.
    *   Activate **Developer Mode** (Settings > Activate the developer mode).
    *   Navigate to **Apps** and click **"Update Apps List"** in the top menu.
    *   Search for "Car Sharing Reservation" and click **Activate**.

4.  **Initial Configuration**  
    Once installed, ensure you have at least one vehicle created in the **Fleet** app with the "Seats" field populated, as the reservation logic depends on this value.

## 3. Usage

Once installed, navigate to the **Car Sharing** menu:

* **Create a Reservation:** Select a vehicle, driver, and desired timeframe.
* **Validation:** If you select a timeframe that overlaps with an existing booking for the same car, the system will trigger a `ValidationError`.
* **Passenger Management:** Add passengers via the `Passenger` field. The system will automatically update the `Available Seats` field.
* **Safety Checks:** The system will block any attempt to save a reservation where the driver is also listed as a passenger or if the total headcount exceeds the vehicle's capacity.

## 4. Future Roadmap (Contributing)

While this is a portfolio project, the following features could be implemented:

* **Car Availability:** Dynamic filtering of available vehicles based on selected dates.
* **Access Rights:** Restrictions to prevent passengers from modifying other participants.
* **Trip Change Requests:** Voting system for passengers to propose and approve new departure times.
* **Driver Replacement:** License verification to identify eligible backup drivers for emergencies.
* **Calendar Integration:** Automatic synchronization of trips with passenger calendars.
* **Smart Notifications:** Automated email reminders and scheduled trip updates.

## 5. License

This project is licensed under the **LGPL-2.1 licence** - see the `LICENSE` file for details.