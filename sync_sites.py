import json

from foldersync2_sftp import sync_sftp

# TEST_SITE_LOCAL_PATH = 'C:\\temp\\test-site'
# TEST_SITE_REMOTE_PATH = '/var/www/test-site'
# TEST_SITE_SYNC_FILE = 'C:\\VladWork\\Backup-data\\firstvds-test-site-data.json'

IM_POSSIBLE_SITE_LOCAL_PATH = 'C:\\VladWork\\Sites\\impossible\\impossible'
IM_POSSIBLE_SITE_REMOTE_PATH = '/var/www/im-possible.info'
IM_POSSIBLE_SITE_SYNC_FILE = 'C:\\VladWork\\Backup-data\\firstvds-im-possible-data.json'

ZKALUGA_SITE_LOCAL_PATH = 'C:\\VladWork\\Sites\\zkaluga.avhost.info'
ZKALUGA_SITE_REMOTE_PATH = '/var/www/zkaluga.avhost.info'
ZKALUGA_SITE_SYNC_FILE = 'C:\\VladWork\\Backup-data\\firstvds-zkaluga-data.json'


TEST_SITE_CREDENTIALS = 'C:\\VladWork\\firstvds-im-possible-credentials.json'

with open(TEST_SITE_CREDENTIALS, 'r', encoding='utf-8') as f:
    remote_host_props = json.load(f)


print('Synchronize im-possible.info')

sync_sftp(
    IM_POSSIBLE_SITE_LOCAL_PATH,
    IM_POSSIBLE_SITE_REMOTE_PATH,
    [
        '.eclipse-web-kit',
        '.settings',
        '.vscode',
    ],
    IM_POSSIBLE_SITE_SYNC_FILE,
    remote_host_props['hostname'],
    remote_host_props['port'],
    remote_host_props['username'],
    remote_host_props['password']
)

print('')
print('')
print('Synchronize zkaluga.avhost.info')


sync_sftp(
    ZKALUGA_SITE_LOCAL_PATH,
    ZKALUGA_SITE_REMOTE_PATH,
    [
        '.eclipse-web-kit',
        '.settings',
        '.vscode',
    ],
    ZKALUGA_SITE_SYNC_FILE,
    remote_host_props['hostname'],
    remote_host_props['port'],
    remote_host_props['username'],
    remote_host_props['password']
)



