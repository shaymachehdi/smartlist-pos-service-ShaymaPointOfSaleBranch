from pos_microservice import app,db
from pos_microservice.pointOfSale.models import PointOfSale
# class Author(db.Document):
#     name = db.StringField()
#
# class Book(db.Document):
#     title = db.StringField()
#     author = db.DocumentField(Author)
#     year = db.IntField()
#
# mark_pilgrim = Author(name='Shayma Chehdi')
# mark_pilgrim.save()

# @app.route('/')
# def todo():
#
#     _items = db.tododb.find()
#     items = [item for item in _items]
#
#     return render_template('todo.html', items=items)
#
#
# @app.route('/new', methods=['POST'])
# def new():
#     item_doc2 = {
#         'name': request.form['name'],
#         'description': request.form['description'],
# 	'rien': 54
#     }
#     db.tododb.insert(item_doc2)
#     return redirect(url_for('todo'))
# pos = PointOfSale(idPointOfSale="testbbbb", designation='test',localisation="{'lat':7.3,'long':9.6}",address="gfggf", email="test@gmail.com",phone_number="25995310")
# pos.save()
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
