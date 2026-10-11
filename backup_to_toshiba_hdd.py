
# import sys
# import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)

import traceback

import foldersync
import foldersync2
from datetime import datetime

from calc_util import TotalCounter

SITES_FOLDER = 'C:\\VladWork\\Sites\\'
FROM_INET_FOLDER = 'C:\\VladWork\\From_Inet\\'
BACKUP_DATA_FOLDER = 'C:\\VladWork\\Backup-data\\'

ONE_DRIVE_BACKUP = 'C:\\Users\\vlada\\OneDrive\\Backup\\'
TARGET_BACKUP = 'D:\\Backup\\'
TARGET_TITLE = 'HDD'
TARGET_BACKUP_FILE_PREFIX = 'toshiba-hdd'


start_time = datetime.now()

total_result = TotalCounter()
error_count = 0


try:

    print('Synchronize with OneDrive: impossible')
    foldersync.sync(
        SITES_FOLDER+'impossible',
        ONE_DRIVE_BACKUP+'impossible'
    )

    print('--------')
    print('Synchronize with OneDrive: zkaluga.avhost.info')
    foldersync.sync(
        SITES_FOLDER+'zkaluga.avhost.info',
        ONE_DRIVE_BACKUP+'zkaluga.avhost.info'
    )






    try:
        print('--------')
        print(f'Synchronize with {TARGET_TITLE}: impossible')
        r = foldersync2.sync(
            SITES_FOLDER +'impossible',
            TARGET_BACKUP + 'Sites\\impossible',
            BACKUP_DATA_FOLDER + TARGET_BACKUP_FILE_PREFIX + '-impossible.data.json'
        )
        total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print(f'Synchronize with {TARGET_TITLE}: zkaluga.avhost.info')
        r = foldersync2.sync(
            SITES_FOLDER +'zkaluga.avhost.info',
            TARGET_BACKUP + 'Sites\\zkaluga.avhost.info',
            BACKUP_DATA_FOLDER + TARGET_BACKUP_FILE_PREFIX + '-zkaluga.avhost.info.data.json'
        )
        total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print(f'Synchronize with {TARGET_TITLE}: ART_SORTED')
        r = foldersync2.sync(
            FROM_INET_FOLDER +'Important\\ART_SORTED',
            TARGET_BACKUP + 'ART_SORTED',
            BACKUP_DATA_FOLDER + TARGET_BACKUP_FILE_PREFIX + '-ART_SORTED.data.json'
        )
        total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print(f'Synchronize with {TARGET_TITLE}: IMP_SORTED')
        r = foldersync2.sync(
            FROM_INET_FOLDER +'Important\\IMP_SORTED',
            TARGET_BACKUP + 'IMP_SORTED',
            BACKUP_DATA_FOLDER +TARGET_BACKUP_FILE_PREFIX + '-IMP_SORTED.data.json'
        )
        total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print(f'Synchronize with {TARGET_TITLE}: unprocessed_images')
        r = foldersync2.sync(
            FROM_INET_FOLDER +'Important\\unprocessed_images',
            TARGET_BACKUP + 'unprocessed_images',
            BACKUP_DATA_FOLDER + TARGET_BACKUP_FILE_PREFIX + '-unprocessed_images.data.json'
        )
        total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print(f'Synchronize with {TARGET_TITLE}: impossible-video')
        r = foldersync2.sync(
            FROM_INET_FOLDER +'impossible-video',
            TARGET_BACKUP + 'impossible-video',
            BACKUP_DATA_FOLDER + TARGET_BACKUP_FILE_PREFIX + '-impossible_video.data.json'
        )
        total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print(f'Synchronize with {TARGET_TITLE}: Music-car')
        r = foldersync.sync(
            'C:\\VladWork\\Music-car',
            TARGET_BACKUP + 'Music-car'
        )
        total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print(f'Synchronize with {TARGET_TITLE}: grid-paint-backup')
        r = foldersync.sync(
            'C:\\VladWork\\grid-paint-backup',
            TARGET_BACKUP + 'grid-paint-backup'
        )
        total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    print('')
    print('')
    print('==========')
    print(f'Total result of sync with {TARGET_TITLE}:')
    total_result.print()
    print('Finished! {}'.format(datetime.now() - start_time))


    try:
        print('--------')
        print(f'Synchronize with {TARGET_TITLE}: Backup-Data')
        foldersync.sync(
            BACKUP_DATA_FOLDER,
            TARGET_BACKUP + 'Backup-data'
        )
    except:
        traceback.print_exc()
        error_count += 1


    print('=================')
    print(f'Total errors {error_count}')


    input("Press Enter to continue...")
except Exception as e:
    traceback.print_exc()
    input("Press Enter to continue...")


