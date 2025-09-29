# External Invoice Request Module

## Overview

The External Invoice Request module provides a simple, secure way for customers to request invoices for their sales orders without requiring an Odoo login. It creates a streamlined workflow for both customers and accounting teams.

![Invoice Request Flow](https://img.shields.io/badge/status-stable-brightgreen.svg)

## Features

-   **External Web Access**: Customers can access their uninvoiced sales orders through a unique URL
-   **Token-based Security**: Optional tokens provide secure access for specific customers
-   **Intuitive Interface**: User-friendly web interface for selecting orders for invoicing
-   **Admin Approval**: Backend workflow for reviewing and approving invoice requests
-   **PDF Downloads**: Automatic PDF generation for approved invoices
-   **Sales Order Integration**: Direct integration with Odoo Sales module

## Technical Overview

### Models

-   **invoice.request**: Stores invoice request records with fields for partner_id, sale_id, invoice_id, status, etc.

### Views

-   **Invoice Request Form**: Admin interface for reviewing and processing invoice requests
-   **Invoice Request List**: Overview of all invoice requests with filtering options
-   **External Invoice Form**: Public-facing form for customers to request invoices

### Controllers

-   **External Invoice Controller**: Handles public URL endpoints for accessing and submitting invoice requests
-   **PDF Download Controller**: Securely serves invoice PDFs to authorized users

## Installation

1. Place the module in your Odoo addons directory
2. Update your Odoo configuration to include the module directory in the addons path
3. Restart your Odoo server
4. Install the module from the Apps menu or via command line:
    ```bash
    python odoo-bin -c <config_file> -d <database> -i ap_invoice_request
    ```

## Dependencies

-   base
-   sale
-   account
-   website

## Configuration

After installation, you can access the Invoice Requests menu under Accounting → Invoice Requests.

### Security Settings

Access rights to the module are managed through standard Odoo groups:

-   `account.group_account_manager`: Full access to manage invoice requests
-   `account.group_account_invoice`: Can view and approve invoice requests
-   `base.group_user`: Can view invoice requests

## Usage

### For Customers

1. **Accessing the System**:

    - General access: `/sale-orders/to-invoice`
    - Customer-specific access: `/external/sale-invoice/<token>`

2. **Requesting Invoices**:

    - Select a sales order from the list
    - Click "Request Invoice" to submit the request
    - A confirmation message will be displayed

3. **Downloading Invoices**:
    - After approval, return to the same URL
    - Click "Download Invoice PDF" to get the invoice

### For Accounting Teams

1. **Managing Requests**:

    - Navigate to Accounting → Invoice Requests → Invoice Requests
    - Review pending requests in the list view
    - Open a request to see details

2. **Processing Requests**:

    - Click "Approve and Create Invoice" to generate and post the invoice
    - Click "Reject" to decline the request
    - Use the smart button to view the generated invoice

3. **Customer Access**:
    - Click "View External Form" to see what the customer sees
    - Generate tokens for specific partners via the "get_partner_token" method

## API

For developers, the module offers several API endpoints:

-   `GET /sale-orders/to-invoice`: Lists all sales orders with "to invoice" status
-   `GET /external/sale-invoice/<token>`: Shows invoice request form for specific customer
-   `POST /external/sale-invoice/submit`: Handles invoice request submission
-   `GET /external/sale-invoice/download/<invoice_id>`: Downloads invoice PDF

## Customization

### Adding Fields to Invoice Request

1. Extend the `invoice.request` model in a custom module:

    ```python
    class InvoiceRequestCustom(models.Model):
        _inherit = 'invoice.request'

        custom_field = fields.Char('Custom Field')
    ```

2. Modify the views by inheritance to display the new fields

### Changing Approval Workflow

The `approve_request` method in the `invoice.request` model can be overridden to implement custom approval workflows.

## Troubleshooting

### Common Issues

-   **No Sales Orders Displayed**: Check that sales orders have invoice_status = 'to invoice'
-   **PDF Download Error**: Ensure the invoice is fully posted and accessible to public users
-   **Token Invalid**: Tokens are unique; generate a new one if needed

### Debug Mode

Enable debug mode in Odoo to see additional information when troubleshooting issues.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under LGPL-3 - see the LICENSE file for details.
