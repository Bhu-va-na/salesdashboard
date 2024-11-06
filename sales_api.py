class SalesAPI:
    def __init__(self):
        self.sales = [
            {"id": 1, "item": "Laptop", "price": 1500, "quantity": 1, "customer": "John Doe", "date_of_sale": "2024-10-01", "category": "Electronics", "salesperson": "Alice"},
            {"id": 2, "item": "Phone", "price": 2000, "quantity": 1, "customer": "Jane Smith", "date_of_sale": "2024-10-02", "category": "Electronics", "salesperson": "Bob"},
            {"id": 3, "item": "Headphones", "price": 250, "quantity": 2, "customer": "David Lee", "date_of_sale": "2024-10-03", "category": "Accessories", "salesperson": "Alice"},
            {"id": 4, "item": "Monitor", "price": 350, "quantity": 1, "customer": "Sara Kim", "date_of_sale": "2024-10-04", "category": "Electronics", "salesperson": "Charlie"},
            {"id": 5, "item": "Keyboard", "price": 100, "quantity": 3, "customer": "Mike Jones", "date_of_sale": "2024-10-05", "category": "Accessories", "salesperson": "Alice"}
        ]
    
    def total_sales(self):
        return sum(sale['price'] * sale['quantity'] for sale in self.sales)
    
    def total_transactions(self):
        return len(self.sales)
    
    def average_sale(self):
        return self.total_sales() / self.total_transactions() if self.total_transactions() > 0 else 0

    def total_quantity(self):
        return sum(sale['quantity'] for sale in self.sales)

    def best_selling(self):
        if not self.sales:
            return None
        sales_by_item = {}
        for sale in self.sales:
            if sale['item'] in sales_by_item:
                sales_by_item[sale['item']] += sale['quantity']
            else:
                sales_by_item[sale['item']] = sale['quantity']
        best_item = max(sales_by_item, key=sales_by_item.get)
        return best_item

    def get_sales(self):
        return self.sales

    def validate_sale_data(data):
        required_fields = ["item", "price", "quantity", "customer", "date_of_sale", "category", "salesperson"]
        for field in required_fields:
            if field not in data:
                return f"Missing required field: {field}"
        return None

    def add_sale(self, data):
        validation_error = self.validate_sale_data(data)
        if validation_error:
            return {"message": validation_error}, 400
    
        try:
            new_id = max(sale['id'] for sale in self.sales) + 1 if self.sales else 1
            new_sale = {**data, "id": new_id}
            self.sales.append(new_sale)
            return {"message": "Sale added successfully!", "sale": new_sale}, 201
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500


    def update_sale(self, sale_id, data):
        for sale in self.sales:
            if sale['id'] == sale_id:
                sale.update(data)
                return {"message": "Sale updated successfully!", "sale": sale}
        return {"message": "Sale not found!"}, 404
    
    def delete_sale(self, sale_id):
        for sale in self.sales:
            if sale['id'] == sale_id:
                self.sales.remove(sale)
                return {"message": "Sale deleted successfully!"}
        return {"message": "Sale not found!"}, 404
    
    def sales_statistics(self):
        return {
            "total_sales": self.total_sales(),
            "total_transactions": self.total_transactions(),
            "average_sale": self.average_sale(),
            "total_quantity": self.total_quantity(),
            "best_selling": self.best_selling()
        }
