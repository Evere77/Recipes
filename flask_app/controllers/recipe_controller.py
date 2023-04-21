from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User
from flask import flash


# ============= CREATE PAGE - RENDER =============
@app.route('/recipe/new')
def new_recipe():
    return render_template('recipe_new.html')


# ============= CREATE METHOD - ACTION =============
@app.route('/recipe/create', methods=['POST'])
def create_recipe():
    if not Recipe.validate(request.form):
        return redirect('/recipe/new')
    
    # alt way - create the dict for the create
    # party_data = {
    #     **request.form,
    #     'user_id' : session['user_id']
    # }
    # Recipe.create_one(party_data)
    # we have a hidden input in the form
    #for a user_id


    Recipe.create_one(request.form)

    return redirect('/recipes')


# ============= READ ONE - RENDER =============
@app.route('/recipes/<int:id>')
def show_one(id):
    this_recipe = Recipe.get_by_id(id)
    return render_template('recipe_show.html', this_recipe=this_recipe)


# ============= EDIT RENDER PAGE ==============
@app.route('/recipes/edit/<int:id>')
def edit_page(id):
    this_recipe = Recipe.get_by_id(id)
    return render_template('recipe_edit.html', this_recipe=this_recipe)


# ============= UPDATE METHOD - ACTION =============
@app.route('/recipes/update', methods=['POST'])
def update_method():
    if not Recipe.validate(request.form):
        return redirect('/recipes')

    Recipe.update(request.form)
    return redirect('/recipes')


# ============= DELETE ACTION=============
@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete({'id' : id})
    return redirect('/recipes')