# api - API(интерфэйс програмирования приложения), набор определённых правил и инструментов , которые позволяют приложения взаимодействовать с друг другом

# HTTP , SSH , TCP/IP

from flask import Flask , jsonify , request

from main import *

app = Flask(__name__)

@app.route("/get_items/" , methods = ['GET'])
def get_items():
    items = get_item()
    return jsonify({'data':items})

@app.route("/" , methods = ['GET'])
def hello():
    return "<h1>Hello World</h1>"

@app.route("/create_item/", methods= ['POST'])
def create_item_rq():
    data = request.get_json()
    item = ItemPydantic(
        name = data.get('title', 'no name'),
        description = data.get('description', 'no desc'),
        price = data.get('price', 0)
    )
    create_item(item)
    return jsonify({'message': 'created sucsessfuly'}) 
@app.route("/retrieve_item/<int:item_id>/", methods= ['GET'])
def get_one_item(item_id):
    item = retrieve_item(item_id)
    if not item:
        return jsonify({'message': 'not found'})
    return jsonify({'data':item})

@app.route("/update_item/<int:item_id>/", methods= ['PUT'])
def update_item_fk(item_id):
    try:
        data = request.get_json()
        update_item(item_id, data)
        return 'Update Successfully'
    except:
        return "Data was a uncoorrect"
    
@app.route("/delete_item/<int:item_id>/", methods= ['DELETE'])
def delete_item_fk(item_id):
    try:
        delete_item(item_id)
        return f'this item whith {item_id} was delete'
    except:
        return 'no such ID exist'


app.run(host='localhost', port=8000)