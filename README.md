# Odoo

[![Build Status](https://runbot.odoo.com/runbot/badge/flat/1/master.svg)](https://runbot.odoo.com/runbot)
[![Documentation](https://img.shields.io/badge/master-docs-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/documentation/17.0)
[![Help](https://img.shields.io/badge/master-help-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/forum/help-1)
[![Nightly Builds](https://img.shields.io/badge/master-nightly-875A7B.svg?style=flat&colorA=8F8F8F)](https://nightly.odoo.com/)

Odoo is a suite of web based open source business apps.

This repository contains two custom solutions built on Odoo 17:

1. **ap_invoice_request**: An Odoo module for external invoice requests
2. **client_app**: A standalone REST API service using Odoo's XML-RPC API

## 1. External Invoice Request Module (ap_invoice_request)

The External Invoice Request module provides a secure way for customers to request invoices for their sales orders without requiring an Odoo login.

### Key Features

-   **External Web Access**: Customers can access their uninvoiced sales orders through a unique URL
-   **Token-based Security**: Optional tokens provide secure access for specific customers
-   **Intuitive Interface**: User-friendly web interface for selecting orders for invoicing
-   **Admin Approval**: Backend workflow for reviewing and approving invoice requests
-   **PDF Downloads**: Automatic PDF for approved invoices

### Installation

1. Install the module from the Apps menu or via command line:
    ```bash
    python odoo-bin -c odoo.conf -d your_database -i ap_invoice_request
    ```

### Usage

**For Customers:**

-   Access `/sale-orders/to-invoice` to see all uninvoiced orders
-   Access `/external/sale-invoice/<token>` for customer-specific orders
-   Select an order and submit an invoice request
-   Download the PDF once approved

**For Administrators:**

-   Navigate to Accounting → Invoice Requests
-   Review and approve/reject pending requests
-   Access the external form via the "View External Form" button

## 2. XML-RPC Client API (client_app)

A standalone REST API service that interfaces with Odoo through its XML-RPC API, providing a simpler interface for managing Sales Orders.

### Key Features

-   **Complete Sales Order Management**: Create, read, update sales orders
-   **Action Support**: Confirm, cancel, reset sales orders to draft
-   **REST API Interface**: Simple JSON-based HTTP endpoints

### Installation

1. Navigate to the client_app directory
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Configure Odoo connection in `.env` file
4. Run the application:
    ```bash
    python app.py
    ```

### API Endpoints

-   **GET** `/api/sale-orders`: List sales orders
-   **GET** `/api/sale-orders/<id>`: Get a specific sales order
-   **POST** `/api/sale-orders`: Create a new sales order
-   **PUT** `/api/sale-orders/<id>`: Update a sales order
-   **POST** `/api/sale-orders/<id>/confirm`: Confirm a sales order
-   **POST** `/api/sale-orders/<id>/cancel`: Cancel a sales order
-   **POST** `/api/sale-orders/<id>/draft`: Reset a sales order to draft

More detailed documentation is available in each component's respective README file.

Odoo Apps can be used as stand-alone applications, but they also integrate seamlessly so you get
a full-featured [Open Source ERP](https://www.odoo.com) when you install several Apps.

## Getting started with Odoo

For a standard installation please follow the [Setup instructions](https://www.odoo.com/documentation/17.0/administration/install/install.html)
from the documentation.

To learn the software, we recommend the [Odoo eLearning](https://www.odoo.com/slides),
or [Scale-up, the business game](https://www.odoo.com/page/scale-up-business-game).
Developers can start with [the developer tutorials](https://www.odoo.com/documentation/17.0/developer/howtos.html).

## Security

If you believe you have found a security issue, check our [Responsible Disclosure page](https://www.odoo.com/security-report)
for details and get in touch with us via email.
