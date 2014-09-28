"""
Look through some tasks.
"""
import phabulous
phab = phabulous.Phabulous()
project = phab.project(id=481)
for task in project.tasks[:5]:
    print "[%s] %s:\t%s" % (task.is_open, task.owner.name, task.title)
