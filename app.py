"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from time import gmtime, strftime

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
        posts = Post.query.all()
        reversed_posts = posts[::-1][:5]
        user_list = []
        for post in reversed_posts:
            user_list.append(User.query.get_or_404(post.user_id))
        return render_template('home.html', posts=reversed_posts, user_list=user_list)

    @app.route('/users')
    def list_users():
        """Display all users"""
        users = User.query.all()
        return render_template('list.html', users=users)

    @app.route('/users/<int:user_id>')
    def user_profile(user_id):
        user = User.query.get_or_404(user_id)
        posts = Post.query.filter_by(user_id=user_id)
        return render_template('user_profile.html', user=user, posts=posts)

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
    def edit_user_edit(user_id):
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
    
    @app.route('/posts/<int:post_id>')
    def show_post(post_id):
        post = Post.query.get_or_404(post_id)
        user = User.query.get_or_404(post.user_id)
        return render_template('show_post.html', post=post, user=user)
    
    @app.route('/posts/<int:post_id>/edit', methods=["GET"])
    def edit_post_form(post_id):
        post = Post.query.get_or_404(post_id)
        return render_template('edit_post.html', post=post)

    @app.route('/posts/<int:post_id>/edit', methods=["POST"])
    def edit_post_edit(post_id):
        post = Post.query.get_or_404(post_id)

        post.title = request.form["title"]
        post.content = request.form["postContent"]
        db.session.add(post)
        db.session.commit()
        return redirect(f'/posts/{post.id}')
    
    @app.route('/users/<int:user_id>/posts/new', methods=["GET"])
    def new_post_form(user_id):
        user = User.query.get_or_404(user_id)
        tags = Tag.query.all()
        return render_template('new_post.html', user=user, tags=tags)

    @app.route('/users/<int:user_id>/posts/new', methods=["POST"])
    def new_post_post(user_id):
        tag_ids = [int(num) for num in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        new_post = Post(
        title=request.form['title'],
        content=request.form['postContent'],
        created_at = strftime("%Y-%m-%d %H:%M:%S", gmtime()),
        user_id = user_id,
        tags=tags)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/posts/{new_post.id}')
    
    @app.route('/posts/<int:post_id>/delete', methods=["POST"])
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        user = User.query.get_or_404(post.user_id)
        db.session.delete(post)
        db.session.commit()
        return redirect(f'/users/{user.id}')
    
    @app.route('/tags', methods=["GET"])
    def list_tags():
        tags = Tag.query.all()
        return render_template('list_tags.html', tags=tags)
    
    @app.route('/tags/<int:tag_id>', methods=["GET"])
    def show_tag(tag_id):
        tag = Tag.query.get_or_404(tag_id)
        return render_template('show_tag.html', tag=tag)

    @app.route('/tags/new', methods=["GET"])
    def new_tag():
        return render_template('create_tag.html')
    
    @app.route('/tags/new', methods=["POST"])
    def new_tag_post():
        new_tag = Tag(name=request.form["tagName"])
        db.session.add(new_tag)
        db.session.commit()

        return redirect(f'/tags/{new_tag.id}')
    
    @app.route('/tags/<int:tag_id>/edit', methods=["GET"])
    def edit_tag(tag_id):
        tag = Tag.query.get_or_404(tag_id)
        return render_template('edit_tag.html', tag=tag)
    
    @app.route('/tags/<int:tag_id>/edit', methods=["POST"])
    def edit_tag_post(tag_id):
        tag = Tag.query.get_or_404(tag_id)
        tag.name = request.form["tagName"]
        db.session.add(tag)
        db.session.commit()
        return redirect(f'/tags/{tag.id}')
        
    
    @app.route('/tags/<int:tag_id>/delete', methods=["POST"])
    def delete_tag(tag_id):
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        return redirect('/tags')


    return app
    
if __name__=='__main__':
    app = create_app('blogly')
    #connect_db(app)
    app.run(debug=True)