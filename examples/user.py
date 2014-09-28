"""
Starting from a user.
"""
import phabulous


phab = phabulous.Phabulous()
user = phab.user(username='wlarson')
print "Name: \t%s" % user.name
print "Email: \t%s" % user.email
for task in user.tasks[:10]:
    print "\t%s" % task.title
    for project in task.projects:
        print "\t\t%s" % project.name
