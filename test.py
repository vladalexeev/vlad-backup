# -*- coding: utf-8 -*-
import foldersync
import foldersync2
import file_util

import shutil
import os

# foldersync.sync('D:\\VladWork\\Sites\\impossible', 
#                 'D:\\VladWork\\OneDrive\\Backup\\impossible',
#                 test=True)

# foldersync.sync('D:\\From_Inet\\Important\\IMP_SORTED',
#                 '\\\\LENOVO-PC\\Vlad\\Backup\\IMP_SORTED',
#                 test=True)

# file_util.roll_file_stack('D:\\VladWork\\Sites\\zkaluga-test{}.zip', 5)
# 
# shutil.make_archive(
#     'D:\\VladWork\\Sites\\zkaluga-test\\', 
#     'zip',
#     'D:\\VladWork\\Sites',
#     'zkaluga.avhost.info')


foldersync2.sync('c:\\Temp\\test\\zkaluga.avhost.info',
                 'c:\\Temp\\test\\backup',
                 'c:\\Temp\\test\\sync.prop',
                 False)


print('Finished!')