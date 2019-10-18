from pos_microservice import app, bcrypt
from flask import request, jsonify, Blueprint
from flask_marshmallow import Marshmallow
from pos_microservice.pointOfSale.models import PointOfSale
from datetime import datetime
from key import key
import re

import requests
from ..decorators import require_appkey

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

# Init bluebripnt
pos = Blueprint('pos', __name__)

# Init marshmallow
ma = Marshmallow(pos)


# TestClass schema
class PointOfSaleSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('designation', 'localisation', 'address', 'email', 'phone_number')


# Init schema
pointOfSale_schema = PointOfSaleSchema()
pointsOfSale_schema = PointOfSaleSchema(many=True)


# Get all points of sale
@pos.route('/pointsOfSale', methods=['GET'])
@require_appkey
def get_points_of_Sale():
    all_point_of_sales = PointOfSale.query.all()
    result = pointsOfSale_schema.dump(all_point_of_sales)
    return jsonify(result.data)


# Get Single point of sale by designation
@pos.route('/pointOfSale/findByDesignation/<string:designation>', methods=['GET'])
@require_appkey
def get_point_of_sale_by_designation(designation):
    # Fetch point of sale
    # pos = PointOfSale.query.filter_by(designation=designation).first()
    des = ""
    print(designation)
    for item in designation.encode("cp1252").decode("utf8").split():
        des = des + item + " "
    print(des)
    pos = PointOfSale.query.filter({"designation": re.compile(r".*" + des[0:len(des) - 1] + ".*", re.IGNORECASE)}).all()
    if not pos:
        return jsonify({'msg': 'No point of sale found!'
                        })
    return pointsOfSale_schema.jsonify(pos)


# Get Single point of sale by address
@pos.route('/pointOfSale/findByAddress/<string:address>', methods=['GET'])
@require_appkey
def get_point_of_sale_by_address(address):
    # Fetch point of sale
    addr = ""
    # print(address.encode("latin1").decode("utf8"))
    for item in address.encode("cp1252").decode("utf8").split():
        addr = addr + item + " "
    pos = PointOfSale.query.filter({"address": re.compile(r".*" + addr[0:len(addr) - 1] + ".*", re.IGNORECASE)}).all()
    if not pos:
        return jsonify({'msg': 'No point of sale found!'
                        })
    return pointsOfSale_schema.jsonify(pos)


# Get Single point of sale by a precise localisation
@pos.route('/pointOfSale/findByLocalisation/<string:localisation>', methods=['GET'])
@require_appkey
def get_point_of_sale_by_localisation(localisation):
    # Fetch point of sale
    pos = PointOfSale.query.filter_by(localisation=localisation).first()
    if not pos:
        return jsonify({'msg': 'No point of sale found!'
                        })
    return pointOfSale_schema.jsonify(pos)


# add a point of sale
@pos.route("/addPointOfSale", methods=['POST'])
@require_appkey
def add_point_of_Sale():
    designation = request.json['designation']
    localisation = request.json['localisation']
    address = request.json['address']
    email = request.json['email']
    phone_number = request.json['phone_number']
    # Fetch pos
    pos = PointOfSale.query.filter_by(designation=designation, localisation=localisation, address=address).first()

    if pos is None:
        now = datetime.now()  # current date and time
        timeStamp = now.strftime("%m/%d/%Y, %H:%M:%S")
        x = timeStamp + request.json['designation']
        idPointOfSale = bcrypt.generate_password_hash(x).decode('utf-8')
        designation = request.json['designation']
        localisation = request.json['localisation']
        address = request.json['address']
        email = request.json['email']
        phone_number = request.json['phone_number']

        new_pos = PointOfSale(idPointOfSale=idPointOfSale, designation=designation, localisation=localisation,
                              address=address, email=email, phone_number=phone_number)
        new_pos.save()
        return jsonify({
            'msg': 'New pos successfully created !',
            'isCreated': True})

    else:
        return jsonify({
            'msg': 'you already registred that pos !',
            'isCreated': False
        })


# Delete a point of sale

@pos.route('/pointOfSale/<string:idPointOfSale>', methods=['DELETE'])
@require_appkey
def delete_point_of_sale(idPointOfSale):
    # Fetch pos
    pos = PointOfSale.query.filter_by(idPointOfSale=idPointOfSale).first()
    if not pos:
        return jsonify({'msg': 'No point of sale found!',
                        'isDeleted': False})

    pos.remove()
    return jsonify({'msg': 'Point of sale successfully deleted!',
                    'isDeleted': True,
                    })


# Update a point of sale

@pos.route('/pointOfSale/<string:idPointOfSale>', methods=['PUT'])
@require_appkey
def update_point_of_sale(idPointOfSale):
    # Fetch list
    pos = PointOfSale.query.filter_by(idPointOfSale=idPointOfSale).first()
    if not pos:
        return jsonify({'msg': 'No point of sale found!',
                        'isUpdated': False
                        })

    designation = request.json['designation']
    localisation = request.json['localisation']
    address = request.json['address']
    email = request.json['email']
    phone_number = request.json['phone_number']

    pos.designation = designation
    pos.localisation = localisation
    pos.address = address
    pos.email = email
    pos.phone_number = phone_number

    pos.save()

    return jsonify({'msg': 'Point of sale successfully updated!',
                    'isUpdated': True,
                    'Designation': pos.designation,
                    'Localisation': pos.localisation,
                    'Address': pos.address,
                    'Email': pos.email,
                    'Phone Number': pos.phone_number})


# key is the key of the API Google maps
# the attribute type of the API represent the nature or the type of thing that you look for
# It's passed by default as 'grocery_or_supermarket' because our goal is find markets(points of sale)
# We set a 500 as radius that's mean it the search of a location will give as all markets with the same location
# and in the radius of 500 and then it will give us some markets out of that radius for better choice.
# exp of url : https://maps.googleapis.com/maps/api/place/textsearch/json?query=123+main+street&location=42.3675294,-71.186966&radius=10000&key=YOUR_API_KEY

# url google maps places pour comprendre l'utilité de chaque donné ; https://developers.google.com/places/web-service/search

@pos.route("/getPointOfSale/<string:location>")
@require_appkey
def get_places_by_location(location):
    search_payload = {"key": key, "type": "grocery_or_supermarket", "radius": 500, "location": location}
    search_req = requests.get(search_url, params=search_payload)
    search_json = search_req.json()
    msg = ""
    for item in search_json["results"]:
        loc = str(item["geometry"]["location"]["lat"]) + "," + str(item["geometry"]["location"]["lng"])
        pos = PointOfSale.query.filter_by(localisation=loc).first()
        if pos is None:
            designation = item["name"]
            localisation = loc
            if "formatted_address" in item:
                address = item["formatted_address"]
            else:
                address = "Unnamed Road"
            phone_number = "Unknown phone number"
            email = "Unknown email"
            now = datetime.now()  # current date and time
            timeStamp = now.strftime("%m/%d/%Y, %H:%M:%S")
            x = timeStamp + designation
            idPointOfSale = bcrypt.generate_password_hash(x).decode('utf-8')
            new_pos = PointOfSale(idPointOfSale=idPointOfSale, designation=designation, localisation=localisation,
                                  address=address, email=email, phone_number=phone_number)
            new_pos.save()
            msg = "You added a new point of sale : " + designation
            print(msg)
        else:
            print("Point of sale already exist")
    return search_json

    # place_id = search_json["results"][1]["place_id"]
    #
    # details_payload = {"key": key, "placeid": place_id}
    # details_resp = requests.get(details_url, params=details_payload)
    # details_json = details_resp.json()
    #
    # url = details_json["result"]["url"]
    #
    #
    # return jsonify({'result': url})
