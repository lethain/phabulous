import unittest
from mock import patch, Mock
import phabulous


class TestPhabulous(unittest.TestCase):
    "Test Phabulous."
    def setUp(self):
        "Setup test."
        self.responses = Mock()
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
            'project.query.return_value.data': {
                'phid-1': {
                    'phid': 'phid-1',
                    'id': 'id-1',
                    'name': 'project 1',
                    'dateCreated': '1/2/3',
                    'slugs': 'slugs',
                    'dateModified': '2/3/4',
                },
            },
        })
        self.phab = phabulous.Phabulous(self.responses)

    def test_project(self):
        "Test the project object."
        project = self.phab.project(id="will")
        projects = self.phab.projects(ids=["will"])

        self.assertEquals(len(projects), 1)
        self.assertEquals(project.phid, projects[0].phid)
        self.assertEquals(project.phid, 'phid-1')
        self.assertEquals(project.id, 'id-1')

        self.assertTrue(project.tasks)
        self.assertTrue(project.members)

        for task in project.tasks:
            self.assertEquals(task.title, 'task')
            self.assertEquals(task.dependencies, [])

        for user in project.members:
            self.assertEquals(user.name, 'will')
            self.assertEquals(user.email, 'will@example.org')

    def test_user(self):
        "Test the user object."
        user = self.phab.user(username="will")
        self.assertEquals(user.name, 'will')
        self.assertEquals(user.email, 'will@example.org')
        self.assertTrue(user.tasks)
        for task in user.tasks:
            self.assertEquals(task.title, 'task')
            self.assertEquals(task.dependencies, [])


if __name__ == '__main__':
    unittest.main()
