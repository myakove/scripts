#! /usr/bin/python

import argparse
from jenkinsapi.jenkins import Jenkins as JenkinsAPI
from jenkins import Jenkins as JenkinsPython


user_input = argparse.ArgumentParser()
user_input.add_argument("--server", "-SRV", help="Jenkins server")
user_input.add_argument("--username", "-U", help="Username for Jenkins server")
user_input.add_argument("--password", "-P", help="Password got Jenkins server")
user_input.add_argument("--action", "-A", help="action to run on the job,"
                        "enable, disable, print (name) and build.")
user_input.add_argument("--search", "-S", help="search for job to apply the"
                        "action")
user_input.add_argument("--view", "-V", help="Jenkins view")
user_input.add_argument("--nview", "-NV", help="Nested Jenkins view")
option = user_input.parse_args()


JENKINS_URL = 'http://jenkins.qa.lab.tlv.redhat.com:8080'
JENKINS_USER = 'qe_automation'
JENKINS_PASSWD = '123456'

if not option.server:
    option.server = JENKINS_URL
if not option.username:
    option.username = JENKINS_USER
if not option.password:
    option.password = JENKINS_PASSWD

if not (option.action and
        option.view and
        option.nview):
    print "Server, search, action, view, nview must be specify"
    print user_input.format_usage()

else:
    j = JenkinsAPI(baseurl=option.server,
                   username=option.username,
                   password=option.password)
    jp = JenkinsPython(option.server,
                       option.username,
                       option.password)

    view = j.get_view(option.view)
    nested_view = view.get_nested_view_dict()
    view_url = nested_view.get(option.nview)
    view_by_url = j.get_view_by_url(view_url)
    jobs_dict = view_by_url.get_job_dict().keys()

    for job in jobs_dict:
        active_job = j.get_job(job)
        if option.search:
            if option.search in job:
                if option.action == "enable":
                    active_job.enable()
                    print job, "enabled"
                if option.action == "disable":
                    active_job.disable()
                    print job, "disabled"
                if option.action == "print":
                    print active_job.name
                if option.action == "build":
                    jp.build_job(active_job.name)
                    print active_job.name, "building"

        else:
            if option.action == "enable":
                active_job.enable()
                print job, "enabled"
            if option.action == "disable":
                active_job.disable()
                print job, "disabled"
            if option.action == "print":
                print active_job.name
            if option.action == "build":
                jp.build_job(active_job.name)
                print active_job.name, "building"










