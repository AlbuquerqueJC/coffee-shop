import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


def shortRecipe(recipe):
    try:
        short_recipe={}
        for r in recipe:
            if r == 'color' or r == 'parts':
                short_recipe[r] = recipe[r]
    finally:
        return short_recipe


'''
Drink
a persistent drink entity, extends the base SQLAlchemy Model
'''


class Drink(db.Model):
    # Auto incrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string,
    # 'parts':integer}]
    recipe = Column(String(180), nullable=False)

    '''
    short()
        short form representation of the Drink model
    '''

    def short(self):
        print("JSON Recipe:")
        print(json.loads(self.recipe))
        '''
        for r in json.loads(self.recipe):
            if r == 'color' or r == 'parts':
                short_recipe[r] = json.loads(self.recipe)[r]
        '''
        '''
        short_recipe = [{'color': r['color'], 'parts': r['parts']} for r in
                        json.loads(self.recipe)]
        '''
        short_recipe = shortRecipe(json.loads(self.recipe))
        print("Short Recipe:")
        print(short_recipe)

        return {
            'id'    : self.id,
            'title' : self.title,
            'recipe': short_recipe
        }

    '''
    long()
        long form representation of the Drink model
    '''

    def long(self):
        return {
            'id'    : self.id,
            'title' : self.title,
            'recipe': json.loads(self.recipe)
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''

    def insert(self):
        print(self)
        try:
            db.session.add(self)
            db.session.commit()
        except():
            print("Unable to add drink")
            db.session.rollback()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except():
            print("Unable to delete drink")
            db.session.rollback()


    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''

    def update(self):
        try:
            db.session.update(self)
            db.session.commit()
        except Exception as e:
            print({e})
            db.session.rollback()
        finally:
            db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
