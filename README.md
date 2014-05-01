web-core
========

web-core, a filehost web app, that allows anyone to upload files via a API.
Files are hashed and uploaded to public file hosting. Using the hashes a node
can look up the information of where that file was stored using the
[Datacoin](http://datacoin.info/) blockchain. This makes a file uploaded to
BitCumulus accessible through any node in the network.

- Coded in [Python](http://python.org/) and [Flask](http://flask.pocoo.org/), a Python microframework for web.
- Must be run on a Linux based web server, [Debian](http://www.debian.org/) distro recommended.

#### Web interface

If you wish to use this in a browser, take a look at
[BitCumulus](https://github.com/Storj/BitCumulus). It is a web interface,
composed of only html, css and javascript, powered by the web-core API.


#### Scope

This project depends on several other projects:

- [plowshare-wrapper](https://github.com/Storj/plowshare-wrapper) provides a
  python interface to upload and download files from popular file hosting
  sites. It is a python wrapper of the plowshare tool.

- [cloudmanager](https://github.com/Storj/cloud-manager) contains most of the
  file handling logic. It keeps track of all the uploaded files, keeps track of
  the files present in local cache, and handles database serialization.

- [metachains-dtc](https://github.com/Storj/metachains-dtc) is a wrapper for
  the Datacoin client, using json RPC. It also contains a synchronization class,
  which allows one to synchronize data from and to the blockchain.

This project puts everything together and makes it accessible through a web
application. It uses `cloudmanager` to manage all uploads/downloads, and
`metachains-dtc` to enable synchronization of the hosted content information
between nodes running BitCumulus.


#### Synchronization note

Keep in mind that the `upload` command spends datacoins, so be careful when
using it.


## Installation

Check [INSTALL.md](INSTALL.md) for installation instructions.


## API documentation

Upload a file to the cloud manager:

    POST /api/upload
    Parameters:
    - file


Download a file from the cloud manager identified by the given file hash:

    GET /api/download/<filehash>
    Parameters:
    - filehash


Retrieve information regarding a given file hash:

    GET /api/find/<filehash>
    Parameters:
    - filehash

    Error results:
    { "error": "File not found" }

    Normal Result:
    {
      "datetime": "1395268813",
      "filehash": "cda2bb0f57d172b4901ee71f64f067335023c30e9eea2b7bc9d02ced942b3a29",
      "filename": "cda2bb0_zenziC_-_Biomechanical.mp3",
      "filesize": 3546893,
      "uploads": [
        {
          "host_name": "multiupload",
          "url": "http://multiupload.nl/K69M8BRFYR"
        },
        {
          "host_name": "euroshare_eu",
          "url": "http://euroshare.eu/file/15828724/cda2bb0-zenzic-biomechanical.mp3"
        },
        {
          "error": true,
          "host_name": "zalil_ru"
        }
      ],
      "version": "0.2"
    }

Retrieve node information, including storage, transfer limits, synchronization
status, datacoin information. All sizes are in bytes.

    GET /api/status
    Parameters: None

    Normal result:
        {
            "bandwidth": {
                "total": {
                    "incoming": 792431,
                    "outgoing": 953218
                    },
                "current": {
                    "incoming": 192746,
                    "outgoing": 547291
                    },
                "limits": {
                    "incoming": 1048576,
                    "outgoing": 2097152
                    }
                },

            "storage": {
                "capacity":      67108864,
                "used":          5909746,
                "max_file_size": 1048576
                },

            "sync": {
                "blockchain_queue": {
                    "count": 73,
                    "size":  912834
                },
                "cloud_queue": {
                    "count": 12,
                    "size":  6572
                },

            "datacoin": {
                "balance": 1.05,
                "address": "DPhb7Pe1Ur6nWzLYBC1SeV8xAGCrYGMLVn"
                }
        }
