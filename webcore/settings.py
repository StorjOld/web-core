
# Cloud manager settings
PROJECT_ROOT          = '.'

DATABASE_PATH         = 'postgres://storj:so-secret@localhost/storj'
STORAGE_PATH          = PROJECT_ROOT + '/uploads'
STORAGE_SIZE          = 20*(2**20)  # 20 MiB
STORAGE_FILE          = 5*(2**20)   # 5 MiB

# Datacoin settings

DATACOIN_OVERRIDE     = None # override with callable to bypass Datacoin
DATACOIN_URL          = "http://127.0.0.1:11777"
DATACOIN_USERNAME     = "datacoinrpc"
DATACOIN_PASSWORD     = "secretish-password"

# cloud synchronization daemon settings
CLOUDSYNC_WAIT        = 30 # in seconds

# Transfer limit settings

TRANSFER_MAX_INCOMING = 0 # in bytes
TRANSFER_MAX_OUTGOING = 0 # in bytes

# Accounts API

ACCOUNTS_API_ENABLED  = False
ACCOUNTS_API_BASE_URL = "http://node.storj.io/accounts"
ACCOUNTS_API_KEY      = "secret-key"

try:
    from local_settings import *
except ImportError:
    pass

