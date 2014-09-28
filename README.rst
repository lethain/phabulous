=========
phabulous
=========

Phabulous is an extremely simple wrapper around `python-phabricator <https://github.com/disqus/python-phabricator>`_,
with the aim of creating a simpler, more Pythonic interface. I was motivated
to put it together after copy-pasting the same set of classes across a dozen
iPython notebooks which were all playing with Phabricator data.

It is mostly focused oon reading and tabulating task data, it's not particularly
concerned about doing anything else.

Simplest example::

    from phabricator import Phabricator
    from phabulous import Phabulous

    # create a python-phabricator Phabricator object,
    # this uses your ~/.arcrc file
    phab = Phabulous(Phabricator())

    project = phab.project(id=481)
    for task in project.tasks():
        print task.title, task.owner.name


See on `Github <https://github.com/lethain/phabulous>`_, or on
`PyPi <http://pypi.python.org/pypi/phabulous/>`_.


Installation
============

The simplest way to install is via PyPi::

    pip install phabulous

If you want to develop extraction, then after installing `lxml`,
you can install from GitHub::

    git clone
    cd phabulous
    virtualenv env
    . ./env/bin/activate
    pip install -r requirements.txt
    pip install -e .

Then you can run the tests::

    python tests/tests.py

All of which should pass in a sane installation.


Examples
========

See more examples in `./examples`.
