

from flask import Flask, request, abort
from mock_data import catalog
import json
import random

# new instance of Flask class
app = Flask("__name__")

me = {
            "name": "Eric",
            "last": "Moore",
            "age:": 35,
            "hobbies":[],
            "address":{
                "street": "Evergreen",
                "number": 42,
                "city": "SpringField"

                }
    }


@app.route("/", methods=['GET'])
def home():
    return "Hello from Python"


@app.route("/test")
def any_name():
    return "I'm a test function"


@app.route("/about")
def my_name():
    return (me["name"] + " " + me["last"])


# *******************************************************************************
# ********************************** API ENDPOINTS ******************************
# *******************************************************************************

@app.route("/api/catalog")
def get_catalog():
    # TODO:read the catalog from a database

    return json.dumps(catalog)

@app.route("/api/catalog", methods=["post"])
def save_product():
    product = request.get_json()
    print (product)


    #  data validations
    # product has to be 5 c
    # if no title then return error
    if not 'title' in product or len(product["title"]) < 5:
        return abort(400, "Title is required, and should be at least 5 chars long")

    # should be a price
    if not 'price' in product:
        return abort(400, "Price is required")

    # if price is not float and not an int, error
    if not isinstance(product["price"], float) and not isinstance(product["price"], int):
        return abort(400, "Price should be a valid number")
        


    # price should be greater than 0
    if product["price"] <= 0:
        return abort(400, "Price should be greater than 0")

    
    #assign a unique _id
    product["_id"] = random.randint(1000, 100000)

    #save the product in catalog
    catalog.append(product)

    return json.dumps(product)



@app.route("/api/cheapest")
def get_cheapest():
    # find the chepest product on the catalog list
    # 1 - travel the list (catalog) for loop
    # 2 - print the price on the consol

    cheap = catalog[0]
    for product in catalog:
        if product["price"] < cheap["price"]:
            cheap = product

    #return it as json
    return json.dumps(cheap)



@app.route("/api/product/<id>")
def get_product(id):
    # find the product whos _id is equal to id
    for product in catalog:
        if product["_id"] == id:
            return json.dumps(product)
            
    #return it as json
    return "NOT FOUND"



#end point to retrieve all products by category
@app.route("/api/catalog/<category>")
def get_by_category(category):
    result=[]
    category = category.lower()
    for product in catalog:
        if product["category"].lower() == category:
            result.append(product)
        
    return json.dumps(result)


@app.route("/api/categories")
def get_categories():
    result=[]
    for product in catalog:
        cat = product["category"]

        if cat not in result:
            result.append(cat)
        
    return json.dumps(result)
    

# start the server
app.run(debug=True)