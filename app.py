"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route("/")
def redirect_list_users():
    """Redirects to list_users. Fix later"""

    return redirect('/users')

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """show the post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title'] or None
    post.content = request.form['content'] or None
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect('/')

@app.route("/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    Post.query.filter(Post.id == post_id).delete()

    db.session.commit()
    return redirect('/')   

@app.route('/users')
def list_users():
    """List users and show link to add user form"""

    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/new')
def new_user_form():
    """show new user form"""

    return render_template("user_form.html")

@app.route('/users/new', methods=["POST"])
def add_user():
    """Add user and redirect to list."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show info on a single user"""

    user = User.query.get_or_404(user_id)
    return render_template('detail.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """show user edit form with preloaded data"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """show the new post form"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):

    title = request.form['title'] or None
    content = request.form['content'] or None
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):

    User.query.filter(User.id == user_id).delete()

    db.session.commit()
    return redirect('/users')

@app.route('/tags')
def show_tags():
    """ show all tags"""

    tags = Tag.query.all()
    
    return render_template('tags.html', tags=tags)

@app.route('/tags/new')
def show_tag_form():

    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def add_tag():
    """add a tag"""
    name = request.form['name'] or None
    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Sow details about tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag.html', tag=tag)
    

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag(tag_id):
    """show the edit form for tags"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """edit tag"""

    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form['name'] or None

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """delete the tag"""

    Tag.query.filter_by(id=tag_id).delete()

    db.session.commit()

    return redirect('/tags')

