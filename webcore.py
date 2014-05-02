import settings
import cloudmanager
import metachains_dtc
import token_manager

class Receipt(object):
    def __init__(self, token, bytecount):
        self.token     = token
        self.bytecount = bytecount

class WebCore(object):
    def __init__(self):
        self.cloud = cloudmanager.CloudManager(
            settings.DATABASE_PATH,
            settings.STORAGE_PATH,
            settings.STORAGE_SIZE)

        self.tokens = token_manager.TokenManager(
            settings.DATABASE_PATH)

        self.coin = metachains_dtc.Datacoin(
            settings.DATACOIN_URL,
            settings.DATACOIN_USERNAME,
            settings.DATACOIN_PASSWORD)

    def charge_upload(self, token, file_path):
        bytecount = os.path.getsize(file_path)

        if self.tokens.consume(token, bytecount * 4):
            return Receipt(token, bytecount * 4)
        else:
            return None

    def charge_download(self, token, filehash):
        info = self.cloud.info(filehash)

        if info is None:
            return None

        bytecount = info['size']
        if not self.cloud.on_cache(filehash):
            bytecount *= 2

        if self.tokens.consume(token, bytecount):
            return Receipt(token, bytecount)
        else:
            return None

    def refund(self, receipt):
        self.tokens.deposit(receipt.token, receipt.bytecount)


