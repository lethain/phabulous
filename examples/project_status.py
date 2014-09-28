"""
Inspect the status of a given project.
"""
import phabulous


phab = phabulous.Phabulous()

project = phab.project(id=481)

# print out soem stuff
print "%s\b" % project
for attr in ('name', 'date_created', 'phid', 'id'):
    print "%s: %s" % (attr.capitalize(), getattr(project, attr))

print "members:"
for user in project.members:
    print "\t%s" % user.name

