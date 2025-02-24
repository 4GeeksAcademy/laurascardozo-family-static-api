"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member(
    {"first_name":"Jhon", "age": 33, "lucky_numbers":[7,13,22]}
)
jackson_family.add_member(
    {"first_name":"Jane", "age": 33, "lucky_numbers":[10,14,3]}
)
jackson_family.add_member(
    {"first_name":"Jimmy", "age": 5, "lucky_numbers":[1]}
)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    print("somos los miembros", members)
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
                
        return jsonify({"error": "Miembro no encontrado"}), 400
    
    except Exception as error:
         return jsonify({"error": str(error)}), 500
    
@app.route('/member', methods=['POST'])
def add_new_member():
    try:
        body = request.get_json()
        first_name = body.get("first_name", None)
        age = body.get("age", None)
        lucky_numbers = body.get("lucky_numbers", None)
        
        if first_name is None:
            return jsonify({"error": "El nombre es requerido"}), 400
        if age is None:
            return jsonify({"error": "El age es requerido"}), 400
        if lucky_numbers is None:
            return jsonify({"error": "El Lucky number es requerido"}), 400
        

        jackson_family.add_member(body)

        return jsonify(body), 200
    
    except Exception as error:
         return jsonify({"error": str(error)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])        
def delete_member(member_id):
    try:
        is_deleted = jackson_family.delete_member(member_id)
        if is_deleted["done"]:
            return jsonify(is_deleted), 200
        else:
            return jsonify({"error": "Miembro no encontrado"}), 400
    except Exception as error:
         return jsonify({"error": str(error)}), 500
    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
