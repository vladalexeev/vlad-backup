import foldersync
import file_util

import shutil
from datetime import datetime


SITES_FOLDER = 'D:\\VladWork\\Sites\\'
FROM_INET_FOLDER = 'D:\\From_Inet\\'

ONE_DRIVE_BACKUP = 'D:\\VladWork\\OneDrive\\Backup\\'
LENOVO_BACKUP = '\\\\LENOVO-PC\\Vlad\\Backup\\'


start_time = datetime.now()

print('Synchronize with OneDrive: impossible')
foldersync.sync(SITES_FOLDER+'impossible', 
                ONE_DRIVE_BACKUP+'impossible')

print('Synchronize with OneDrive: zkaluga.avhost.info')
foldersync.sync(SITES_FOLDER+'zkaluga.avhost.info', 
                ONE_DRIVE_BACKUP+'zkaluga.avhost.info')

print('Synchronize with Lenovo: IMP_SORTED')
foldersync.sync(FROM_INET_FOLDER+'Important\\IMP_SORTED', 
                LENOVO_BACKUP+'IMP_SORTED')

print('Archive: impossible')
file_util.roll_file_stack(SITES_FOLDER+'impossible{}.zip', 5)
shutil.make_archive(
    SITES_FOLDER+'impossible', 
    'zip', SITES_FOLDER,
    'impossible')

print('Archive: unprocessed images')
file_util.roll_file_stack(FROM_INET_FOLDER+'Important\\unprocessed_images{}.zip', 2)
shutil.make_archive(
    FROM_INET_FOLDER+'Important\\unprocessed_images', 
    'zip', FROM_INET_FOLDER+'Important\\',
    'unprocessed_images')


print('Copy to Lenovo: impossible.zip')
file_util.roll_file_stack(LENOVO_BACKUP+'impossible{}.zip', 5)
shutil.copy2(SITES_FOLDER+'impossible.zip', LENOVO_BACKUP+'impossible.zip')


print('Copy to Lenovo: unprocessed_images.zip')
file_util.roll_file_stack(LENOVO_BACKUP+'unprocessed_images{}.zip', 2)
shutil.copy2(FROM_INET_FOLDER+'Important\\unprocessed_images.zip', LENOVO_BACKUP+'unprocessed_images.zip')


print('')
print('Finished! {}'.format(datetime.now() - start_time))