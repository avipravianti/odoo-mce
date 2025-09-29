# client_app/app.py
from flask import Flask, request, jsonify
from odoo_client import OdooClient
import os

app = Flask(__name__)
odoo_client = OdooClient()


@app.route('/api/sale-orders', methods=['GET'])
def get_sale_orders():
    """Get list of sale orders"""
    try:
        # Parse query parameters
        domain = request.args.get('domain', '[]')
        fields = request.args.get('fields', None)
        if fields:
            fields = fields.split(',')
        offset = request.args.get('offset', 0, type=int)
        limit = request.args.get('limit', None, type=int)
        order = request.args.get('order', None)

        # Make XML-RPC call to Odoo
        results = odoo_client.get_sale_orders(
            eval(domain), fields, offset, limit, order
        )
        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/sale-orders/<int:order_id>', methods=['GET'])
def get_sale_order(order_id):
    """Get a specific sale order"""
    try:
        fields = request.args.get('fields', None)
        if fields:
            fields = fields.split(',')

        result = odoo_client.get_sale_order(order_id, fields)
        if result:
            return jsonify({"success": True, "data": result})
        return jsonify({"success": False, "error": "Order not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/sale-orders', methods=['POST'])
def create_sale_order():
    """Create a new sale order"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        order_id = odoo_client.create_sale_order(data)
        return jsonify({"success": True, "data": {"id": order_id}}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/sale-orders/<int:order_id>', methods=['PUT'])
def update_sale_order(order_id):
    """Update an existing sale order"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        result = odoo_client.update_sale_order(order_id, data)
        return jsonify({"success": True, "data": {"updated": result}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/sale-orders/<int:order_id>/confirm', methods=['POST'])
def confirm_sale_order(order_id):
    """Confirm a sale order"""
    try:
        result = odoo_client.confirm_sale_order(order_id)
        return jsonify({"success": True, "data": {"confirmed": result}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/sale-orders/<int:order_id>/cancel', methods=['POST'])
def cancel_sale_order(order_id):
    """Cancel a sale order"""
    try:
        result = odoo_client.cancel_sale_order(order_id)
        return jsonify({"success": True, "data": {"cancelled": result}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route('/api/sale-orders/<int:order_id>/draft', methods=['POST'])
def reset_sale_order_to_draft(order_id):
    """Reset a sale order to draft state"""
    try:
        result = odoo_client.reset_sale_order_to_draft(order_id)
        return jsonify({"success": True, "data": {"reset_to_draft": result}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
