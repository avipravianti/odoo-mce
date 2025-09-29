# Odoo XML-RPC Client API

A REST API service that interfaces with Odoo 17 through its XML-RPC API. This service provides a simple HTTP interface for managing Sales Orders in Odoo without requiring direct XML-RPC calls.

## Features

-   **Complete Sales Order Management**: Create, read, update, and delete sales orders
-   **Action Support**: Confirm, cancel, or reset sales orders to draft state
-   **REST API Interface**: Simple JSON-based HTTP endpoints
-   **Environment-based Configuration**: Easy configuration through environment variables
-   **Error Handling**: Clear error messages for debugging

## Requirements

-   Python 3.8+
-   Flask
-   requests
-   python-dotenv
-   Odoo 17 instance with XML-RPC enabled

## Installation

1. Clone the repository or download the files
2. Navigate to the client_app directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your Odoo connection by creating a `.env` file:

```
ODOO_URL=http://localhost:8095
ODOO_DB=odoo-db
ODOO_USERNAME=admin
ODOO_PASSWORD=your_password
```

5. Run the application:

```bash
python app.py
```

The server will start on port 5001 by default.

## API Endpoints

### Get Sales Orders

**GET** `/api/sale-orders`

Query parameters:

-   `domain`: Odoo domain filter (default: `[]`)
-   `fields`: Comma-separated list of fields to return
-   `offset`: Number of records to skip (pagination)
-   `limit`: Maximum number of records to return
-   `order`: Field to sort by (e.g., `name desc`)

Example:

```bash
curl "http://localhost:5001/api/sale-orders?limit=10&fields=name,partner_id,amount_total"
```

### Get Sales Order Details

**GET** `/api/sale-orders/<order_id>`

Query parameters:

-   `fields`: Comma-separated list of fields to return

Example:

```bash
curl "http://localhost:5001/api/sale-orders/42?fields=name,partner_id,order_line"
```

### Create Sales Order

**POST** `/api/sale-orders`

Body: JSON object with sales order fields

Example:

```bash
curl -X POST "http://localhost:5001/api/sale-orders" \
  -H "Content-Type: application/json" \
  -d '{
    "partner_id": 1,
    "date_order": "2025-09-29",
    "order_line": [
      [0, 0, {
        "product_id": 1,
        "product_uom_qty": 1,
        "price_unit": 100
      }]
    ]
  }'
```

### Update Sales Order

**PUT** `/api/sale-orders/<order_id>`

Body: JSON object with fields to update

Example:

```bash
curl -X PUT "http://localhost:5001/api/sale-orders/42" \
  -H "Content-Type: application/json" \
  -d '{
    "note": "Updated via API"
  }'
```

### Confirm Sales Order

**POST** `/api/sale-orders/<order_id>/confirm`

Example:

```bash
curl -X POST "http://localhost:5001/api/sale-orders/42/confirm"
```

### Cancel Sales Order

**POST** `/api/sale-orders/<order_id>/cancel`

Example:

```bash
curl -X POST "http://localhost:5001/api/sale-orders/42/cancel"
```

### Reset Sales Order to Draft

**POST** `/api/sale-orders/<order_id>/draft`

Example:

```bash
curl -X POST "http://localhost:5001/api/sale-orders/42/draft"
```

## Architecture

This service follows a simple two-layer architecture:

1. **REST API Layer** (`app.py`): Handles HTTP requests, parameter parsing, and response formatting
2. **Odoo Client Layer** (`odoo_client.py`): Manages XML-RPC communication with Odoo

## Security Considerations

This implementation is intended for development purposes. For production use, consider:

1. Adding authentication to the API endpoints
2. Implementing HTTPS
3. Adding rate limiting
4. Using a production WSGI server instead of Flask's built-in server
5. Implementing detailed logging and monitoring

## Troubleshooting

### Connection Issues

-   Verify the Odoo server is running and accessible
-   Check the URL, database name, username, and password in your `.env` file
-   Ensure XML-RPC is enabled in your Odoo instance

### Authentication Errors

-   Verify the credentials in your `.env` file
-   Check that the user has appropriate permissions in Odoo

### Operation Errors

-   For create/update operations, check the data format matches Odoo's expectations
-   For action operations (confirm/cancel), check the sale order's current state allows the action
