
# import sys
# import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)

import foldersync
import foldersync2
from datetime import datetime


SITES_FOLDER = 'C:\\VladWork\\Sites\\'
FROM_INET_FOLDER = 'C:\\VladWork\\From_Inet\\'
BACKUP_DATA_FOLDER = 'C:\\VladWork\\Backup-data\\'

ONE_DRIVE_BACKUP = 'C:\\Users\\vlada\\OneDrive\\Backup\\'
LENOVO_BACKUP = '\\\\LENOVO-PC\\Vlad\\Backup\\'


start_time = datetime.now()

try:

    print('Synchronize with OneDrive: impossible')
    foldersync.sync(SITES_FOLDER+'impossible',
                    ONE_DRIVE_BACKUP+'impossible')

    print('--------')
    print('Synchronize with OneDrive: zkaluga.avhost.info')
    foldersync.sync(SITES_FOLDER+'zkaluga.avhost.info',
                    ONE_DRIVE_BACKUP+'zkaluga.avhost.info')

    print('--------')
    print('Synchronize with Lenovo: impossible')
    foldersync2.sync(SITES_FOLDER+'impossible',
                     LENOVO_BACKUP+'Sites\\impossible',
                     BACKUP_DATA_FOLDER+'impossible.data')

    print('--------')
    print('Synchronize with Lenovo: zkaluga.avhost.info')
    foldersync2.sync(SITES_FOLDER+'zkaluga.avhost.info',
                     LENOVO_BACKUP+'Sites\\zkaluga.avhost.info',
                     BACKUP_DATA_FOLDER+'zkaluga.avhost.info.data')

    print('--------')
    print('Synchronize with Lenovo: ART_SORTED')
    foldersync2.sync(FROM_INET_FOLDER+'Important\\ART_SORTED',
                     LENOVO_BACKUP+'ART_SORTED',
                     BACKUP_DATA_FOLDER+'ART_SORTED.data')

    print('--------')
    print('Synchronize with Lenovo: IMP_SORTED')
    foldersync2.sync(FROM_INET_FOLDER+'Important\\IMP_SORTED',
                     LENOVO_BACKUP+'IMP_SORTED',
                     BACKUP_DATA_FOLDER+'IMP_SORTED.data')

    print('--------')
    print('Synchronize with Lenovo: unprocessed_images')
    foldersync2.sync(FROM_INET_FOLDER+'Important\\unprocessed_images',
                     LENOVO_BACKUP+'unprocessed_images',
                     BACKUP_DATA_FOLDER+'unprocessed_images.data')

    print('--------')
    print('Synchronize with Lenovo: impossible-video')
    foldersync2.sync(FROM_INET_FOLDER+'impossible-video',
                     LENOVO_BACKUP+'impossible-video',
                     BACKUP_DATA_FOLDER+'impossible_video.data')

    print('--------')
    print('Synchronize with Lenovo: Music-car')
    foldersync.sync('C:\\VladWork\\Music-car',
                    LENOVO_BACKUP+'Music-car')

    print('--------')
    print('Synchronize with Lenovo: Backup-Data')
    foldersync.sync(BACKUP_DATA_FOLDER,
                    LENOVO_BACKUP+'Backup-data')

    print('')
    print('Finished! {}'.format(datetime.now() - start_time))

    input("Press Enter to continue...")
except Exception as e:
    import traceback
    traceback.print_exc()
    input("Press Enter to continue...")


