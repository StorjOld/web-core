#!/usr/bin/env python
#
# Daemon to upload files on record
# to multiple cloud hosting websites.
#

import time
import settings
import cloudmanager
import metachains_dtc

def make_cloudmanager():
    return cloudmanager.CloudManager(
        settings.DATABASE,
        settings.STORAGE_PATH,
        settings.STORAGE_SIZE)

def make_coin():
    return metachains_dtc.Datacoin(
        settings.DATACOIN_URL,
        settings.DATACOIN_USERNAME,
        settings.DATACOIN_PASSWORD)


if __name__ == "__main__":
    cm = make_cloudmanager()

    while True:
       cm.cloud_sync()
       time.sleep(settings.CLOUDSYNC_WAIT)
