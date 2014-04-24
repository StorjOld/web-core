Installation
============

#### Dependencies

To use this, you must install the [plowshare command line
tool](https://code.google.com/p/plowshare/). Make sure that both plowup and
plowdown are in your PATH before continuing.

If you're running Debian, you can install it using the following commands:

    wget https://plowshare.googlecode.com/files/plowshare4_1~git20140112.7ad41c8-1_all.deb
    sudo dpkg -i plowshare4_1~git20140112.7ad41c8-1_all.deb
    sudo apt-get -f install


This project has a pip compatible requirements.txt. You can use virtualenv to
manage dependencies:

    cd BitCumulus
    virtualenv .env                  # create a virtual environment for this project
    source .env/bin/activate         # activate it
    pip install -r requirements.txt  # install dependencies

Afterwards, you need to set up a cloudmanager database:

    python -mcloudmanager.setup_db database/files.db


#### Configuration settings

web-core manages a database, a local storage cache, and a blockchain. These
can be configured correctly by setting a few parameters in `local_settings.py`:

    DATABASE_PATH           # Database path.

    DATACOIN_URL            # URL to the server RPC endpoint.
    DATACOIN_USERNAME       # RPC username.
    DATACOIN_PASSWORD       # RPC password.

    STORAGE_PATH            # Path to the local cache storage.
    STORAGE_SIZE            # Maximum capacity of the local storage (bytes).
    STORAGE_FILE            # Maximum file size allowed (bytes).

    TRANSFER_MAX_INCOMING   # Maximum incoming bandwidth allowed (bytes).
    TRANSFER_MAX_OUTGOING   # Maximum outgoing bandwidth allowed (bytes).

    CLOUDSYNC_WAIT          # Synchronization polling interval (seconds).


You must at least specify the blockchain server password.
Check the [settings.py](settings.py) for the default values.


#### Web application setup

To test the installation, use the following command:

    python index.py

BitCumulus will be running on http://localhost:5000. You can use `gunicorn` to
run multiple workers. Check the
[BitCumulus](https://github.com/Storj/BitCumulus) project if you wish to use
this with a web browser interface.


#### Synchronization setup

To enable cloud hosting synchronization and blockchain synchronization, you
must configure an extra daemon. This daemon periodically checks for the following:

- uploaded files, which are to be sent to multiple cloud hosting websites;
- json data in the blockchain, which are to be added to the database;
- files sent to cloud hosting websites, which are to be added to the blockchain.

The daemon makes use of the same settings as the web server, so you only need
to configure it once. There is only one additional parameter that you may
configure. By default, the scripts checks for updates every 30 seconds, but you
can override this in `local_settings.py`.

Using upstart, supervisord, or some other tool of your choice, set up a daemon
that runs the
[cloudsync.py](https://github.com/Storj/web-core/blob/master/cloudsync.py)
script.
