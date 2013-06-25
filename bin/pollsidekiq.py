#!/usr/bin/python
"""
Use this script to poll the Sidekiq web server for info. about workers.

If the list of active workers is the same as the last time the script was run,
a toaster notification will be displayed.

Usage:
    pollsidekiq.py [-v] <username> <password> <environment>

    -v          -- print the active workers to std out. 
    username    -- usename to access the web server.
    password    -- password.
    environment -- environment.  valid options are st or pr for staging or prod.

Example:
    pollsidekiq.py -v myname mypass pr

author:  Isaac Johnston
date  :  June 20, 2013

"""
import os
import shlex
import sys
import tempfile
import time
from subprocess import Popen

from sidekiqutils import SidekiqPoller

USAGE = '\nUsage:  %s [-v] <username> <password> <environment>\n' % __file__


def do_it():
    # Get command-line arguments.
    try:
        verbose_flag, username, password, env = sys.argv[1:]
        verbose = True
    except ValueError:
        try:
            username, password, env = sys.argv[1:]
            verbose = False
        except:
            sys.exit(USAGE)
    except:
        sys.exit(USAGE)
    base_url = {
        'st': 'http://doc-test.caplinked.com/sidekiq/',
        'pr': 'http://doc-1.caplinked.com/sidekiq/'
    }[env]
    
    # Poll the server.
    poller = SidekiqPoller(username, password, base_url)
    workers = poller.get_workers()

    # Print the status of workers.
    if verbose:
        print "\nNumber of workers: ", len(workers)
        for worker in workers:
            print "-" * 40
            print "ID      : ", worker['id']
            print "Worker  : ", worker['worker']
            print "Started : ", worker['started']
            print "Queue   : ", worker['queue']
            print "Filename: ", worker['args'][2]
            print "Asset ID: ", worker['args'][1]
        print

    # Check to see if all of the same workers from last time are running.
    dumpfile = os.path.join(tempfile.gettempdir(), env + '-sidekiq.dbm')
    try:
        lastmodified = time.ctime(os.path.getmtime(dumpfile))
        loaded = poller.load_workers(dumpfile)
    except OSError:
        loaded = []
    if workers:
        dumped = poller.dump_workers(dumpfile, workers)
        try:
            assert set(dumped).intersection(loaded) != set(loaded)
        except AssertionError:
            summary = "Workers on %s haven't changed since the script was " \
                "last run on %s" % (env.upper(), lastmodified)
            cmd = 'notify-send "{}"'.format(summary)
            p = Popen(shlex.split(cmd))
            if verbose:
                print summary, "\n"


if __name__ == '__main__':
    do_it()
