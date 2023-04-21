from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model
from flask import flash


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

# ============= CREATE =============
    @classmethod
    def create_one( cls, data ):
        query  = """
        INSERT INTO recipes (name, description, instructions, date, under_30, user_id)
        VALUES (%(name)s, %(description)s , %(instructions)s, %(date)s, %(under_30)s, %(user_id)s);
        """
        return connectToMySQL( DATABASE ).query_db( query, data )


# ============= READ ALL =============
    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM recipes
        JOIN users
        ON users.id = recipes.user_id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        list_of_all_recipes = []
        for row in results:
            this_recipe = cls(row)
            user_data = {
                **row,
                'id' : row['users.id'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            this_user = user_model.User(user_data)
            this_recipe.maker = this_user
            list_of_all_recipes.append(this_recipe)
        return list_of_all_recipes


    # ============= READ ONE =============
    @classmethod
    def get_by_id(cls, id):
        # prepara the data dict for the query method
        data = {
            'id' : id
        }
        query = """
        SELECT * FROM recipes
        JOIN users
        ON users.id = recipes.user_id
        WHERE recipes.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if results:
            # create the party
            this_recipe = cls(results[0])
            # create the user for the party
            row = results[0]
            user_data = {
                **row,
                'id' : row['users.id'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
            this_user = user_model.User(user_data)
            this_recipe.maker = this_user
            return this_recipe
        

    # ============= UPDATE =============
    @classmethod
    def update(cls, data):
        query ="""
        UPDATE recipes
        SET
            name = %(name)s,
            description = %(description)s,
            instructions = %(instructions)s,
            date = %(date)s,
            under_30 = %(under_30)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    

    # ============= DELETE =============
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s
        """
        return connectToMySQL(DATABASE).query_db(query, data)


    # ============= VALIDATOR =============
    @staticmethod
    def validate(form_data):
        is_valid = True

        if len(form_data['name']) < 3:
            is_valid = False
            flash('Name must be at least 3 characters long')
        
        if len(form_data['description']) < 3:
            is_valid = False
            flash('Description must be at least 3 characters long')

        if len(form_data['instructions']) < 3:
            is_valid = False
            flash('Instructions must be at least 3 characters long')

        if len(form_data['date']) < 1:
            is_valid = False
            flash('date is required')
        
        if 'under_30' not in form_data:
            is_valid = False
            flash('Under 30 is required')

        return is_valid