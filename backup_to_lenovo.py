

import traceback

import foldersync
import foldersync2
from datetime import datetime

from calc_util import TotalCounter

SITES_FOLDER = 'C:\\VladWork\\Sites\\'
FROM_INET_FOLDER = 'C:\\VladWork\\From_Inet\\'
BACKUP_DATA_FOLDER = 'C:\\VladWork\\Backup-data\\'

ONE_DRIVE_BACKUP = 'C:\\Users\\vlada\\OneDrive\\Backup\\'
LENOVO_BACKUP = '\\\\LENOVO-PC\\Vlad\\Backup\\'


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
        print('Synchronize with Lenovo: impossible')
        r = foldersync2.sync(
            SITES_FOLDER+'impossible',
            LENOVO_BACKUP+'Sites\\impossible',
            BACKUP_DATA_FOLDER+'lenovopc-impossible.data.json'
        )
        lenovo_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1

    try:
        print('--------')
        print('Synchronize with Lenovo: zkaluga.avhost.info')
        r = foldersync2.sync(
            SITES_FOLDER+'zkaluga.avhost.info',
            LENOVO_BACKUP+'Sites\\zkaluga.avhost.info',
            BACKUP_DATA_FOLDER+'lenovopc-zkaluga.avhost.info.data.json'
        )
        lenovo_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1

    try:
        print('--------')
        print('Synchronize with Lenovo: ART_SORTED')
        r = foldersync2.sync(
            FROM_INET_FOLDER+'Important\\ART_SORTED',
            LENOVO_BACKUP+'ART_SORTED',
            BACKUP_DATA_FOLDER+'lenovopc-ART_SORTED.data.json'
        )
        lenovo_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1

    try:
        print('--------')
        print('Synchronize with Lenovo: IMP_SORTED')
        r = foldersync2.sync(
            FROM_INET_FOLDER+'Important\\IMP_SORTED',
            LENOVO_BACKUP+'IMP_SORTED',
            BACKUP_DATA_FOLDER+'lenovopc-IMP_SORTED.data.json'
        )
        lenovo_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print('Synchronize with Lenovo: unprocessed_images')
        r = foldersync2.sync(
            FROM_INET_FOLDER+'Important\\unprocessed_images',
            LENOVO_BACKUP+'unprocessed_images',
            BACKUP_DATA_FOLDER+'lenovopc-unprocessed_images.data.json'
        )
        lenovo_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print('Synchronize with Lenovo: impossible-video')
        r = foldersync2.sync(
            FROM_INET_FOLDER+'impossible-video',
            LENOVO_BACKUP+'impossible-video',
            BACKUP_DATA_FOLDER+'lenovopc-impossible_video.data.json'
        )
        lenovo_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1

    try:
        print('--------')
        print('Synchronize with Lenovo: Music-car')
        r = foldersync.sync(
            'C:\\VladWork\\Music-car',
            LENOVO_BACKUP+'Music-car'
        )
        lenovo_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1


    try:
        print('--------')
        print('Synchronize with Lenovo: grid-paint-backup')
        r = foldersync.sync(
            'C:\\VladWork\\grid-paint-backup',
            LENOVO_BACKUP+'grid-paint-backup'
        )
        lenovo_total_result.add_sync_result(r)
    except:
        traceback.print_exc()
        error_count += 1



    print('')
    print('')
    print('==========')
    print('Total result of sync with Lenovo:')
    lenovo_total_result.print()
    print('Finished! {}'.format(datetime.now() - start_time))







    try:
        print('--------')
        print('Synchronize with Lenovo: Backup-Data')
        foldersync.sync(
            BACKUP_DATA_FOLDER,
            LENOVO_BACKUP+'Backup-data'
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


