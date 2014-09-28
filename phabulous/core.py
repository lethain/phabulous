"""
Core implementation of Phabulous.
"""
from __future__ import absolute_import
from lazy import lazy
from phabricator import Phabricator


def first_or_none(values):
    "Return first value if list isn't empty or None."
    return values[0] if values else None


class Phabulous(object):
    "Shared base clas for Phabulous classes."
    def __init__(self, phabricator=None):
        "Initialize Phabulous object."
        self.phab = phabricator if phabricator else Phabricator()

    def _build(self, cls, resp):
        "Build responses."
        return [cls(x, phabricator=self.phab) for x in resp]

    def _pluralize(self, kwargs):
        "Pluralize keys."
        return {'%ss' % x:(y,) for x, y in kwargs.iteritems()}

    def projects(self, **kwargs):
        "Retrieve projects."
        if kwargs:
            data = self.phab.project.query(**kwargs).data.itervalues()
            return self._build(Project, data)
        return []

    def project(self, **kwargs):
        "Retrieve a project."
        return first_or_none(self.projects(**self._pluralize(kwargs)))

    def tasks(self, **kwargs):
        "Retrieve tasks."
        if kwargs:
            data = self.phab.maniphest.query(**kwargs).itervalues()
            return self._build(Task, data)
        return []

    def task(self, **kwargs):
        "Retrieve task."
        return first_or_none(self.tasks(**self._pluralize(kwargs)))

    def users(self, **kwargs):
        "Retrieve users."
        if kwargs:
            data = self.phab.user.query(**kwargs)
            return self._build(User, data)
        return []

    def user(self, **kwargs):
        "Retrieve user."
        return first_or_none(self.users(**self._pluralize(kwargs)))


class Task(Phabulous):
    "Wrapper around Maniphest task."
    def __init__(self, data, *args, **kwargs):
        "Initialize Task."
        super(Task, self).__init__(*args, **kwargs)
        self.data = data
        self.description = data['description']
        self.title = data['title']
        self.id = data['id']
        self.priority = data['priority']
        self.phid = data['phid']
        self.status = data['statusName']
        self.is_open = not self.data.get('isClosed')
        self.is_closed = not self.is_open
        self.auxiliary = data.get('auxiliary')

    @lazy
    def dependencies(self):
        "Retrieve dependent tasks."
        phids = self.data.get('dependsOnTaskPHIDs')
        if phids:
            return self.tasks(phids=phids)
        return []


    @lazy
    def owner(self):
        "Retrieve owner user for a task."
        return self.user(phid=self.data['ownerPHID'])

    @lazy
    def projects(self):
        "Retrieve projects for a task."
        phids = self.data.get('projectPHIDs')
        if phids:
            return super(Task, self).projects(phids=self.data.get('projectPHIDs'))
        else:
            return []

    def __repr__(self):
        return "Task(T%s: %s)" % (self.id, self.title[:100])


class User(Phabulous):
    "Wrapper around Phabricator user responses."
    def __init__(self, data, *args, **kwargs):
        "Initialize phab user from API response."
        super(User, self).__init__(*args, **kwargs)
        self.data = data
        self.name = data['userName']
        self.email = data['email']
        self.phid = data['phid']
        self.task_filters = {
            'ownerPHIDs': (self.phid,),
            'status': 'status-open',
        }

    @lazy
    def tasks(self):
        "Retrieve tasks from Phabricator API for user."
        return super(User, self).tasks(**self.task_filters)
    
    def __repr__(self):
        return "User(%s)" % (self.name,)


class Project(Phabulous):
    "A Phabricator project."
    def __init__(self, data, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.data = data
        self.phid = data['phid']
        self.id = data['id']
        self.name = data['name']
        self.date_created = data['dateCreated']
        self.slugs = data['slugs']
        self.date_modified = data['dateModified']
        self.task_filters = {
            'projectPHIDs': (self.phid,),
            'status': 'status-open',
        }

    @lazy
    def tasks(self):
        "Retrieve tasks from Phabricator API for user."
        return super(Project, self).tasks(**self.task_filters)

    @lazy
    def members(self):
        "Retrieve members."
        return self.users(phids=self.data.get('members'))
        
    def __repr__(self):
        return "Project(%s)" % self.name   

