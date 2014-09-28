"""
Core implementation of Phabulous.
"""
from __future__ import absolute_import
from lazy import lazy
from phabricator import Phabricator


def first_or_none(values):
    "Return first value if list isn't empty or None."
    return values[0] if values else None


class PhabulousStart(object):
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

class Task(PhabulousStart):
    "Wrapper around Phab task response."
    def __init__(self, data, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
        self.data = data
        self.description = data['description']
        self.title = data['title']
        self.dependencies = data['dependsOnTaskPHIDs']
        self.id = data['id']
        self.priority = data['priority']
        self.phid = data['phid']
        self.status = data['statusName']
        self.is_open = not self.data.get('isClosed')
        self.is_closed = not self.is_open
        #self.category = data.get('auxiliary', {}).get('uber:maniphest_categroy', '').split('|') or None
        #self.owner_phid = data['ownerPHID']
        #owner = retrieve_users(phids=[self.owner_phid])
        #self.owner = owner.values()[0] if owner else None        
        #self.projects = dict(retrieve_projects(phids=data['projectPHIDs'])).values()
        
        """
        if 'std:maniphest:uber:estimate' in data:
            self.estimate = int(data['std:maniphest:uber:estimate'])
        else:
            self.estimate = 1
        """

    def __repr__(self):
        return "Task(T%s: %s)" % (self.id, self.title[:100])


class User(PhabulousStart):
    "Wrapper around Phabricator user responses."
    def __init__(self, data, *args, **kwargs):
        "Initialize phab user from API response."
        super(User, self).__init__(*args, **kwargs)
        self.data = data
        self.name = data['userName']
        self.phid = data['phid']
        self.task_filters = {
            'ownerPHIDs': (self.phid,),
            'status': 'status-open',
        }

    @lazy
    def tasks(self):
        "Retrieve tasks from Phabricator API for user."
        data = self.phab.maniphest.query(**self.task_filters).itervalues()
        return self._build(Task, data)
    
    def __repr__(self):
        return "User(%s)" % (self.name,)


class Project(PhabulousStart):
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

    @lazy
    def members(self):
        "Retrieve members."
        if 'members' in self.data and self.data['members']:
            data = self.phab.user.query(phids=self.data['members'])
            return self._build(User, data)
        return []
        
    def __repr__(self):
        return "Project(%s)" % self.name   


class Phabulous(PhabulousStart):
    "Core interface for interacting with Phabulous."
    def projects(self, **kwargs):
        "Retrieve projects."
        if kwargs:
            data = self.phab.project.query(**kwargs).data.itervalues()
            return self._build(Project, data)
        return {}

    def project(self, **kwargs):
        "Retrieve a project."
        return first_or_none(self.projects(**self._pluralize(kwargs)))

