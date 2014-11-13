#
# Daemon to synchronize all parts:
# - send local storage to cloud hosting websites
# - fetch metadata from blockchain
# - send new local metadata to blockchain

import time
import settings
import cloudmanager
import metachains

def make_cloudmanager():
    return cloudmanager.CloudManager(
        settings.DATABASE_PATH,
        settings.STORAGE_PATH,
        settings.STORAGE_SIZE)

def make_coin():
    return metachains.Florincoin(
        settings.FLORINCOIN_URL,
        settings.FLORINCOIN_USERNAME,
        settings.FLORINCOIN_PASSWORD)

def make_sync(coin, cloud):
    return metachains.Synchronizer(
        coin,
        cloud)


if __name__ == "__main__":
    coin  = make_coin()
    cloud = make_cloudmanager()
    sync  = make_sync(coin, cloud)

    while True:
        sync.scan_blockchain()
        sync.scan_database()
        cloud.cloud_sync()

        time.sleep(settings.CLOUDSYNC_WAIT)
