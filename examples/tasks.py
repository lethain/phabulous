"""
Look through some tasks.
"""
import phabulous
phab = phabulous.Phabulous()
project = phab.project(id=481)
for task in project.tasks[:25]:
    deps = ",".join([x.title for x in task.dependencies])
    print "[%s] %s:\t%s Dependencies: %s" % (task.is_open, task.owner.name, task.title, deps)
