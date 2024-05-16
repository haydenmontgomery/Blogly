"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

def create_app(database_name, testing=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{database_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = "abc123"
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    if testing:
        app.config["WTF_CSRF_ENABLED"] = False

    debug = DebugToolbarExtension(app)
    app.app_context().push()
    connect_db(app)
    db.create_all()

    @app.route('/')
    def to_list():
        return redirect('/users')

    @app.route('/users')
    def list_users():
        """Display all users"""
        users = User.query.all()
        return render_template('list.html', users=users)

    @app.route('/users/<int:user_id>')
    def user_profile(user_id):
        user = User.query.get_or_404(user_id)
        return render_template('user_profile.html', user=user)

    @app.route('/users/new', methods=["GET"])
    def new_user():
        return render_template('create_user.html')

    @app.route('/users/new', methods=["POST"])
    def create_user():
        new_user = User(
        first_name=request.form['firstName'],
        last_name=request.form['lastName'],
        image_url=request.form['imageURL'] or None)
            
        db.session.add(new_user)
        db.session.commit()

        return redirect('/users')

    @app.route('/users/<int:user_id>/edit', methods=["GET"])
    def edit_user(user_id):
        user = User.query.get_or_404(user_id)
        return render_template('edit_user.html', user=user)

    @app.route('/users/<int:user_id>/edit', methods=["POST"])
    def edit_user_post(user_id):
        edited_user = User.query.get_or_404(user_id)
        """     if request.form["firstName"] != 1 or request.form["lastName"] != 1 or request.form["imageURL"] != 1:
            return redirect(f'/{user_id}')
        else: """
        edited_user.first_name = request.form["firstName"]
        edited_user.last_name = request.form["lastName"]
        edited_user.image_url = request.form["imageURL"]

        
        db.session.add(edited_user)
        db.session.commit()
        return redirect('/users')

    @app.route('/users/<int:user_id>/delete', methods=["POST"])
    def delete_user(user_id):
        user_to_delete = User.query.get_or_404(user_id)
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/users')
    
    return app
    
if __name__=='__main__':
    app = create_app('blogly')
    #connect_db(app)
    app.run(debug=True)