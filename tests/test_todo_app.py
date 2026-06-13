import unittest

from app import create_app, db


class TodoAppTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "test-secret",
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page_requires_login(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_can_register_login_and_manage_tasks(self):
        register_response = self.client.post(
            "/register",
            data={"username": "alice", "password": "secret123"},
            follow_redirects=True,
        )
        self.assertEqual(register_response.status_code, 200)
        self.assertIn(b"Registration successful", register_response.data)

        login_response = self.client.post(
            "/login",
            data={"username": "alice", "password": "secret123"},
            follow_redirects=True,
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b"Todo App", login_response.data)

        add_response = self.client.post("/tasks/add", data={"title": "Study Flask"}, follow_redirects=True)
        self.assertEqual(add_response.status_code, 200)
        self.assertIn(b"Study Flask", add_response.data)

        with self.app.app_context():
            from app.models import Task, User

            user = User.query.filter_by(username="alice").first()
            task = Task.query.filter_by(user_id=user.id).first()
            self.assertIsNotNone(task)
            self.assertFalse(task.completed)

        toggle_response = self.client.post(f"/tasks/{task.id}/toggle", follow_redirects=True)
        self.assertEqual(toggle_response.status_code, 200)
        self.assertIn(b"Task updated", toggle_response.data)


if __name__ == "__main__":
    unittest.main()
