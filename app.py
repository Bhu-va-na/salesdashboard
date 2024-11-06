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

@app.route('/sales/<int:sale_id>', methods=['PUT'])
def update_sale(sale_id):
    data = request.get_json()
    return jsonify(sales_api.update_sale(sale_id, data))

@app.route('/sales/<int:sale_id>', methods=['DELETE'])
def delete_sale(sale_id):
    return jsonify(sales_api.delete_sale(sale_id))

@app.route('/sales/statistics', methods=['GET'])
def sales_statistics():
    return jsonify(sales_api.sales_statistics())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

