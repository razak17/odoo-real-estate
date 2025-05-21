### Real Estate Management Module for Odoo

A custom **Odoo** module designed for real estate management.

## Features

- **Property Management**Create, view, update, and manage property details easily.
- **Property Sales Tracking**Track and manage property sales and sales orders.
- **Owner & Partner Management**Associate properties with owners and manage partner relationships.
- **Property History**Keep detailed logs of property history and status changes.
- **Tag System**Tag properties to enable quick categorization and search.

## Project Structure

```plaintext
real_estate/
├── controllers/    # REST API Controllers
├── data/           # Static data files (e.g., sequences)
├── i18n/           # Translation files
├── models/         # Business logic (Python models)
├── reports/        # QWeb XML Reports
├── security/       # Access control and security rules
├── static/         # Static files (images, JS, CSS)
├── tests/          # Unit tests
├── views/          # XML views and menus
└── wizard/         # Wizard logic and views
```

## Installation

1. Clone this repository into your Odoo custom addons path:

```shellscript
git clone https://github.com/razak17/real-estate.git
```

2. Restart the Odoo server:

```shellscript
./odoo-bin -d your-database -u real_estate
```

3. Activate Developer Mode in Odoo UI.
4. Install the Real Estate module from the Apps menu.

## 🛠️ Requirements

- Odoo 18
- Python 3.10+
- PostgreSQL

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
