from flask import Flask, render_template, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from sales_api import SalesAPI

app = Flask(__name__)

# Swagger UI Configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Sales Dashboard"})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Sales API endpoint integration
sales_api = SalesAPI()

@app.route('/')
def home():
    sales_stats = sales_api.sales_statistics()
    return render_template('index.html', 
                           total_sales=sales_stats['total_sales'], 
                           total_transactions=sales_stats['total_transactions'], 
                           average_sale=sales_stats['average_sale'],
                           total_quantity=sales_stats['total_quantity'],
                           best_selling=sales_stats['best_selling'],
                           sales=sales_api.get_sales())

@app.route('/sales', methods=['GET'])
def get_sales():
    return jsonify(sales_api.get_sales())

@app.route('/sales', methods=['POST'])
def add_sale():
    data = request.get_json()
    return jsonify(sales_api.add_sale(data))

@app.route('/sales', methods=['PUT'])
def update_sale():
    data = request.get_json()

    # Check if the sale_id is provided in the request body
    sale_id = data.get('id')
    if not sale_id:
        return jsonify({"message": "Sale ID is required"}), 400

    # Check if sale exists with the provided ID
    sale = next((sale for sale in sales_api.sales if sale['id'] == sale_id), None)
    if not sale:
        return jsonify({"message": "Sale not found!"}), 404

    # Validate that the required fields are in the request data
    required_fields = ["item", "price", "quantity", "customer", "date_of_sale", "category", "salesperson"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"Missing required field: {field}"}), 400

    # Validate data types or ranges (example for price and quantity)
    if not isinstance(data.get('price'), (int, float)) or data.get('price') <= 0:
        return jsonify({"message": "Price must be a positive number"}), 400
    
    if not isinstance(data.get('quantity'), int) or data.get('quantity') <= 0:
        return jsonify({"message": "Quantity must be a positive integer"}), 400

    # Update the sale with the new data
    sale.update(data)
    
    return jsonify({"message": "Sale updated successfully!", "sale": sale})

@app.route('/sales', methods=['DELETE'])
def delete_sale():
    data = request.get_json()
    sale_id = data.get('id')
    
    if not sale_id:
        return jsonify({"message": "Sale ID is required"}), 400
    
    return jsonify(sales_api.delete_sale(sale_id))

@app.route('/sales/statistics', methods=['GET'])
def sales_statistics():
    return jsonify(sales_api.sales_statistics())

if __name__ == "__main__":
    app.run(debug=True)
