from pos_microservice import db


# class Author(db.Document):
#     name = db.StringField()

class PointOfSale(db.Document):
    idPointOfSale = db.StringField(max_length=200)
    designation = db.StringField()
    # localisation = db.DocumentField(Author)
    localisation = db.StringField()
    address = db.StringField(max_length=500)
    email = db.StringField(max_length=200)
    phone_number = db.StringField(max_length=20)

    def __str__(self):
        return self.designation + self.localisation + self.address + self.phone_number + self.email

