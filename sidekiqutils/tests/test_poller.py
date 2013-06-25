"""
This module contains tests for the class poller.SidekiqPoller.

author:  Isaac Johnston
date  :  June 19, 2013

"""
import os
import unittest

from sidekiqutils import SidekiqPoller

WORKERS = [
    {'worker' : u'doc-1:22684-24032220:default',
     'id'     : u'worker_0',
     'class'  : u'ImageConversion',
     'queue'  : u'low',
     'started': '2013-06-19T16:08:32',
     'args'   : [
         'https://s3.amazonaws.com/caplinked-r3-dev-nonprod/assets/' \
         'original/28690-02.06%20Employee%20Handbook_Sample.pdf?' \
         'AWSAccessKeyId=AKIAJAKMAJ6RLROMGC4Q&Expires=1372288112&' \
         'Signature=VqPr7s52GA6wVhKNxrcS8l4vUrQ%3D',
         '28690',
         '02.06 Employee Handbook_Sample.pdf',
         'https://staging.caplinked.com',
         'caplinked-conversion2-dev']},
    {'worker': u'doc-1:22684-18389520:default',
     'id': u'worker_38',
     'class': u'ImageConversion',
     'queue': u'low',
     'started': '2013-06-19T16:10:11',
     'args': [
         'https://s3.amazonaws.com/caplinked-r3-dev-nonprod/assets/' \
         'original/28714-pg_0036.pdf?AWSAccessKeyId=' \
         'AKIAJAKMAJ6RLROMGC4Q&Expires=1372288188&Signature=' \
         'QjxyCxmBGq24ulQqwgFzlQr4pCw%3D',
         '28714',
         'pg_0036.pdf',
         'https://staging.caplinked.com',
         'caplinked-conversion2-dev']}
]


class SidekiqPollerTestCase(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        poller = SidekiqPoller(
            'http://doc-test.caplinked.com/sidekiq/',
            'me',
            'secret'
        )
        self.poller = poller

    def tearDown(self):
        pass

    def test_dump_and_load_workers(self):
        """
        Verify SidekiqPoller.dump_workers() writes a sequence of workers to
        disk and SidekiqPoller.load_workers() reads the same sequence from disk.

        """
        poller = self.poller
        dumpfile = 'sidekiqutils/tests/sidekiq.dbm'
        # Test when there are workers in the list.
        expected = [
            (w['worker'], w['started'], w['args'][1]) for w in WORKERS
        ]
        poller.dump_workers(dumpfile, WORKERS)
        try:
            self.assertEqual(expected, poller.load_workers(dumpfile))
        finally:
            os.unlink(dumpfile)

        # Test when there are no workers in the list.
        poller.dump_workers(dumpfile, [])
        try:
            self.assertEqual([], poller.load_workers(dumpfile))
        finally:
            os.unlink(dumpfile)

    def test_get_workers(self):
        """
        Verify SidekiqPoller.get_workers() returns a list of dicts for each
        active worker or an empty list if there are no active workers.

        """
        poller = self.poller

        # Test when there are workers.
        workers_fd = open('sidekiqutils/tests/htmlfiles/workers.html')
        try:
            poller.opener.open = lambda url: workers_fd
            workers = poller.get_workers()
        finally:
            workers_fd.close()
        # Check the number of workers.
        self.assertEqual(39, len(workers))
        # Check the values of the first and last workers.
        self.assertEqual(WORKERS[0], workers[0])
        self.assertEqual(WORKERS[-1], workers[-1])

        # Test when there are no workers.
        workers_fd = open('sidekiqutils/tests/htmlfiles/no-workers.html')
        try:
            poller.opener.open = lambda url: workers_fd
            self.assertEqual([], poller.get_workers())
        finally:
            workers_fd.close()


if __name__ == '__main__':
    unittest.main()
