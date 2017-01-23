# Azure Storage Account
AZURE_ACCOUNT_NAME = "dbbackupbksys"
AZURE_ACCOUNT_KEY  = 'CkD5/KNWSF/BV4sM0XcnyrfBgPmZXjQW4i/FR4l2wX2Mn/PMZtZ/5u9D2wP6JUpXHDyJUwDtaiAECnuOYBPmfw=='
AZURE_CONTAINER = 'fullbkup'
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

DBBACKUP_STORAGE = DEFAULT_FILE_STORAGE
DBBACKUP_STORAGE_OPTIONS = {
    'container': AZURE_ACCOUNT_NAME,
    'account_name': AZURE_ACCOUNT_NAME,
    'account_key': AZURE_ACCOUNT_KEY,
}