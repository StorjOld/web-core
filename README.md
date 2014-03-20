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


Retrieve incoming transfer byte count, for the current month and for all time:

    GET /api/bandwidth/usage
    Parameters: None

    Normal result:
    {
      "current": { "incoming": 192746, "outgoing": 547291 },
      "total":   { "incoming": 792431, "outgoing": 953218 }
    }


Retrieve monthly transfer limits, in bytes:

    GET /api/bandwidth/limits
    Parameters: None

    Normal result:
    { "incoming": 1048576, "outgoing": 2097152 }


Retrieve storage usage, in bytes:

    GET /api/storage/usage
    Parameters: None

    Normal result:
    { "usage": 5909746 }


Retrieve storage capacity, in bytes:

    GET /api/storage/capacity
    Parameters: None

    Normal result:
    { "capacity": 67108864 }


Retrieve datacoin balance, in DTC:

    GET /api/dtc/balance
    Parameters: None

    Normal result:
    { "balance": 1.05 }


Retrieve datacoin address:

    GET /api/dtc/address
    Parameters: None

    Normal result:
    { "address": "DPhb7Pe1Ur6nWzLYBC1SeV8xAGCrYGMLVn" }


Retrieve synchronization status:

    GET /api/sync/status
    Parameters: None

    Normal result:
    {
      "blockchain_queue": [
        {
          "datetime": "1395271678",
          "filehash": "ed641794a34b43bbaf90a95b7f308e0fea4a91d36ae5837dfe94ca47b36245fb",
          "filename": "ed64179_dbz_4.jpg",
          "filesize": 109780,
          "uploads": [
            {
              "host_name": "euroshare_eu",
              "url": "http://euroshare.eu/file/15828782/ed64179-dbz-4.jpg"
            },
            {
              "host_name": "rghost",
              "url": "http://rghost.net/53193939"
            },
            {
              "error": true,
              "host_name": "zalil_ru"
            }
          ]
        }
      ],
      "cloud_queue": [
        {
          "filehash": "069c2733ac4a608ef6acc70386378e0974ba0e045c3a0e684a9ed3b0fe2c68ae",
          "filename": "069c273_78bandnames.jpg",
          "filesize": 500228
        }
      ]
    }
