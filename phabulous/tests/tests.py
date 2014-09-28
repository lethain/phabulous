import unittest
from mock import patch, Mock
import phabulous


class TestPhabulous(unittest.TestCase):
    "Test Phabulous."
    def setUp(self):
        "Setup test."
        self.responses = Mock()
        self.phab = phabulous.Phabulous(self.responses)

    def test_user(self):
        "Test the user object."
        self.responses.configure_mock(**{
            'user.query.return_value': [{
                'phid': '1',
                'userName': 'will',
                'email': 'will@example.org',
            }],
            'maniphest.query.return_value': {
                'task-phid': {
                    'id': '2',
                    'priority': 3,
                    'statusName': 'status-open',
                    'phid': '2',
                    'title': 'task',
                    'description': 'desc',

                    },
            },

        })
        user = self.phab.user(username="will")
        self.assertEquals(user.name, 'will')
        self.assertEquals(user.email, 'will@example.org')
        self.assertTrue(user.tasks)
        for task in user.tasks:
            self.assertEquals(task.title, 'task')
            self.assertEquals(task.dependencies, [])


if __name__ == '__main__':
    unittest.main()
