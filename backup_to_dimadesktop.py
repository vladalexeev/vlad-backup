
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
DIMA_BACKUP = '\\\\DIMADESKTOP\\vlad\\'


start_time = datetime.now()

lenovo_total_result = TotalCounter()
dimadesktop_total_result = TotalCounter()
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
        print('Synchronize with dimadesktop: impossible')
        r = foldersync2.sync(
            SITES_FOLDER+'impossible',
            DIMA_BACKUP+'Sites\\impossible',
            BACKUP_DATA_FOLDER+'dimadesktop-impossible.data.json'
        )
        dimadesktop_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print('Synchronize with dimadesktop: zkaluga.avhost.info')
        r = foldersync2.sync(
            SITES_FOLDER+'zkaluga.avhost.info',
            DIMA_BACKUP+'Sites\\zkaluga.avhost.info',
            BACKUP_DATA_FOLDER+'dimadesktop-zkaluga.avhost.info.data.json'
        )
        dimadesktop_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print('Synchronize with dimadesktop: ART_SORTED')
        r = foldersync2.sync(
            FROM_INET_FOLDER+'Important\\ART_SORTED',
            DIMA_BACKUP+'ART_SORTED',
            BACKUP_DATA_FOLDER+'dimadesktop-ART_SORTED.data.json'
        )
        dimadesktop_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print('Synchronize with dimadesktop: IMP_SORTED')
        r = foldersync2.sync(
            FROM_INET_FOLDER+'Important\\IMP_SORTED',
            DIMA_BACKUP+'IMP_SORTED',
            BACKUP_DATA_FOLDER+'dimadesktop-IMP_SORTED.data.json'
        )
        dimadesktop_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print('Synchronize with dimadesktop: unprocessed_images')
        r = foldersync2.sync(
            FROM_INET_FOLDER+'Important\\unprocessed_images',
            DIMA_BACKUP+'unprocessed_images',
            BACKUP_DATA_FOLDER+'dimadesktop-unprocessed_images.data.json'
        )
        dimadesktop_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print('Synchronize with dimadesktop: impossible-video')
        r = foldersync2.sync(
            FROM_INET_FOLDER+'impossible-video',
            DIMA_BACKUP+'impossible-video',
            BACKUP_DATA_FOLDER+'dimadesktop-impossible_video.data.json'
        )
        dimadesktop_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print('Synchronize with dimadesktop: Music-car')
        r = foldersync.sync(
            'C:\\VladWork\\Music-car',
            DIMA_BACKUP+'Music-car'
        )
        dimadesktop_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print('Synchronize with dimadesktop: grid-paint-backup')
        r = foldersync.sync(
            'C:\\VladWork\\grid-paint-backup',
            DIMA_BACKUP+'grid-paint-backup'
        )
        dimadesktop_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    print('')
    print('')
    print('==========')
    print('Total result of sync with dimadesktop:')
    dimadesktop_total_result.print()
    print('Finished! {}'.format(datetime.now() - start_time))


    try:
        print('--------')
        print('Synchronize with dimadesktop: Backup-Data')
        foldersync.sync(
            BACKUP_DATA_FOLDER,
            DIMA_BACKUP+'Backup-data'
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


