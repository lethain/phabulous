=========
phabulous
=========

Phabulous is an extremely simple wrapper around `python-phabricator <https://github.com/disqus/python-phabricator>`_,
with the aim of supporting writing more concise, and perhaps more predictable
code interacting with Phabricator's Conduit APIs.

I'm mostly using it to support writing iPython Notebooks which explore teams'
work loads and project planning, so it really only supports read operations
at this point.

Simplest example::

    from phabulous import Phabulous

    project = Phabulous().project(id=481)
    for task in project.tasks():
        print task.title, task.owner.name


See on `Github <https://github.com/lethain/phabulous>`_, or on
`PyPi <http://pypi.python.org/pypi/phabulous/>`_.


Installation
============

The simplest way to install is via PyPi::

    pip install phabulous

If you want to develop extraction, you can install from GitHub::

    git clone git@github.com:lethain/phabulous.git
    # or
    git clone https://github.com/lethain/phabulous.git
    cd phabulous
    virtualenv env
    . ./env/bin/activate
    pip install -r requirements.txt
    pip install -e .

Then you can run the tests::

    python tests/tests.py

All of which should pass in a sane installation.


Usage
=====

You should be able to explore from any starting object across
the graph of Phabricator stuff. Let's look at some examples.

Note that authentication is handled by the underlying ``python-phabricator``
library, which by default uses your ``~/.arcrc`` files.

First, let's start with a project::

    import phabulous
    phab = phabulous.Phabulous()
    project = phab.project(id=481)
    for task in project.tasks[:5]:
        print "[%s] %s:\t%s" % (task.is_open, task.owner.name, task.title)

But maybe you want to start with a user instead::

    import phabulous
    user = phabulous.Phabulous().user(username='wlarson')
    print "Name: \t%s" % user.name
    print "Email: \t%s" % user.email
    for task in user.tasks[:10]:
        deps = ",".join([x.title for x in task.dependencies])
        print "\t%s" % task.title
        print "\tDependencies: %s" % deps
        for project in task.projects:
            print "\t\t%s" % project.name

See more examples in ``./examples``.
