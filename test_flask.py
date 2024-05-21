from unittest import TestCase

from app import create_app
from models import connect_db, db, User, Post, Tag, PostTag
app = create_app('test_blogly', testing=True)
#connect_db(app)
#app.app_context().push()
# Use test database and don't clutter tests with SQL
""" app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.app_context().push()
"""
db.drop_all()
db.create_all() 


class PetViewsTestCase(TestCase):
    """Tests for site"""

    def setUp(self):
        """Add sample user, post, tag, posttag connection."""

        User.query.delete()
        Post.query.delete()
        Tag.query.delete()
        PostTag.query.delete()
        user = User(first_name="TestFirstName", last_name="TestLastName", image_url="TestURL")
        db.session.add(user)
        db.session.commit()
        post = Post(title="Test Title", content="Test content", user_id=user.id)
        db.session.add(post)
        db.session.commit()
        tag = Tag(name="Test Tag")
        db.session.add(tag)
        db.session.commit()
        postTag = PostTag(post_id=post.id,tag_id=tag.id)
        db.session.add(postTag)
        db.session.commit()
        self.user_id = user.id
        self.user = user
        self.post_id = post.id
        self.post = post
        self.tag = tag
        self.tag_id = tag.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_user(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName TestLastName', html)
            self.assertIn('Test Title', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"firstName": "TestFirstName2", "lastName": "TestLastName2", "imageURL": "TestURL2"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestFirstName2", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotEqual('TestFirstName', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstName TestLastName', html)
            self.assertIn('Test content', html)
            self.assertIn('Test Tag', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "Test2", "postContent": "Test content2", "tags": self.tag_id}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2", html)
            self.assertIn('Test Tag', html)

    def test_edit_post(self):
        with app.test_client() as client:
            d = {"title": "TestEdit", "postContent": "Test edit", "tags": self.tag_id}
            resp = client.post(f"/posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotEqual("Test content", html)
            self.assertIn('Test Tag', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotEqual('Test Title', html)

    def test_list_tags(self):
        with app.test_client() as client:
            resp = client.get("/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Tag', html)

    def test_add_tag(self):
        with app.test_client() as client:
            d = {"tagName": "Test Tag2"}
            resp = client.post(f"/tags/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Tag2', html)

    def test_show_tag(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Tag', html)

    def test_edit_tag(self):
        with app.test_client() as client:
            d = {"tagName": "Test Edit Tag"}
            resp = client.post(f"/tags/{self.tag_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotEqual('Test Tag', html)

    def test_delete_tag(self):
        with app.test_client() as client:
            resp = client.post(f"/tags/{self.tag_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotEqual('Test Tag', html)