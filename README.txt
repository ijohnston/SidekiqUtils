============
sidekiqutils
============

sidekiqutils provides a wrapper around the Sidekiq web interface.  You might
find it useful for polling the status of workers.  Typical usage often looks
like this::

    #!/usr/bin/python
    from sidekiqutils import SidekiqPoller

    poller = SidekiqPoller('myname', 'mypass', 'myserverurl')
    workers = poller.get_workers()
    w = workers[0]
    worker, worker_id, started = w['worker'], w['id'], w['started']
    dumped = poller.dump_workers('/path/to/file.dbm', workers)
    worker, started, asset_id = dumped[0]
    loaded = poller.load_workers('/path/to/file.dbm')
    worker, started, asset_id = loaded[0]


Intallation
===========
1. Extract the archive.
2. Change into the project directory created in step 1.
3. Run setup command (may need admin privileges):  python setup.py install


Contributors
============
Isaac Johnston
