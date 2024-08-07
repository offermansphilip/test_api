from quart import Quart, jsonify, request, abort

app = Quart(__name__)

# Sample data
products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 499.99},
    {"id": 3, "name": "Tablet", "price": 299.99},
]

# Utility function to find a product by ID
def find_product(product_id):
    return next((product for product in products if product["id"] == product_id), None)

# Read all products
@app.route('/products', methods=['GET'])
async def get_products():
    return jsonify(products)

# Read a single product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
async def get_product(product_id):
    product = find_product(product_id)
    if product is None:
        abort(404, "Product not found")
    return jsonify(product)

# Create a new product
@app.route('/products', methods=['POST'])
async def create_product():
    data = await request.get_json()
    new_id = max(product["id"] for product in products) + 1
    new_product = {
        "id": new_id,
        "name": data["name"],
        "price": data["price"]
    }
    products.append(new_product)
    return jsonify(new_product), 201

# Update an existing product
@app.route('/products/<int:product_id>', methods=['PUT'])
async def update_product(product_id):
    product = find_product(product_id)
    if product is None:
        abort(404, "Product not found")

    data = await request.get_json()
    product["name"] = data.get("name", product["name"])
    product["price"] = data.get("price", product["price"])
    return jsonify(product)

# Delete a product
@app.route('/products/<int:product_id>', methods=['DELETE'])
async def delete_product(product_id):
    product = find_product(product_id)
    if product is None:
        abort(404, "Product not found")
    
    products.remove(product)
    return '', 204

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
