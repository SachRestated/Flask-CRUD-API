from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, name):
        # connection, cursor = cls.open_connection()

        # query = "SELECT * FROM items WHERE name = ?"
        # result = cursor.execute(query, (name, ))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     return cls(*row)
        # return None
        return ItemModel.query.filter_by(name=name).first() # SELECT * FROM items where name = name LIMIT 1

    # @classmethod
    # def open_connection(cls):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #     return connection, cursor

    def save_to_db(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO {table} VALUES(?, ?)".format(table=ItemModel.TABLE_NAME)
        # cursor.execute(query, (self.name, self.price))

        # connection.commit()
        # connection.close()
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # def update(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()

    #     query = "UPDATE items SET price=? WHERE name=?"
    #     cursor.execute(query, (self.price, self.name))
    #     # self.name, self.price self.name self.name

    #     connection.commit()
    #     connection.close()
