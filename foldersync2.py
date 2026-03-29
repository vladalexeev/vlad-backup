import json
import os
import shutil
from copy import deepcopy
from os.path import exists, join, isdir, isfile, getsize, getmtime
from datetime import datetime
from file_util import long_file_name, str_file_size, file_size, str_size, str_size_ex

FILES = 'files'
FOLDERS = 'folders'

FILE_SIZE = 'size'
FILE_TIME = 'time'

class FolderSync2:
    
    def __init__(self, src_folder, dst_folder, sync_file, test=False):
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        self.sync_file = sync_file
        self.test = test
        self.new_files = 0
        self.updated_files = 0
        self.deleted_files = 0
        self.new_folders = 0
        self.deleted_folders = 0
        self.new_file_size = 0
        self.updated_file_size = 0
        self.deleted_file_size = 0
        self.prev_sync = None
        self.temp_current_sync = None
        self.current_sync = None
        self.last_temp_current_sync_saved = 0
        
    def run(self):
        start_time = datetime.now()
        
        if not exists(self.dst_folder):
            os.makedirs(self.dst_folder)
        
        if exists(self.sync_file):
            with open(self.sync_file, 'r', encoding='utf-8') as f:
                self.prev_sync = json.load(f)
        else:
            self.prev_sync = {
                FILES: {},
                FOLDERS: []}
        self.temp_current_sync = deepcopy(self.prev_sync)
        self.current_sync = {
            FILES: {},
            FOLDERS: []}    
        
        self._run_copy_and_update_files('')
        self._run_delete_files()
        self._run_delete_folders()

        with open(self.sync_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_sync, f)
        
        print('Work time = {}'.format(datetime.now() - start_time))
        if self.new_files == 0 and self.deleted_folders == 0 and self.new_files == 0 and self.updated_files == 0 and self.deleted_files == 0:
            print('Nothing changed')
        else:
            print(f'New folders = {self.new_folders}')
            print(f'Deleted folders = {self.deleted_folders}')
            print(f'New files = {self.new_files} ({str_size_ex(self.new_file_size)})')
            print(f'Updated files = {self.updated_files} ({str_size_ex(self.updated_file_size)})')
            print(f'Deleted files = {self.deleted_files} ({str_size_ex(self.deleted_file_size)})')
        
        
    def _run_copy_and_update_files(self, folder_name):
        abs_src_folder = join(self.src_folder, folder_name)
        src_folder_content = [join(folder_name, f) for f in self._listdir(abs_src_folder)]
        src_dir_list = sorted([f for f in src_folder_content if isdir(join(self.src_folder, f))])
        src_file_list = sorted([f for f in src_folder_content if isfile(join(self.src_folder, f))])
        
        if folder_name != '' and folder_name not in self.prev_sync[FOLDERS]:
            self._mkdir(folder_name)
        
        for file_name in src_file_list:
            abs_file_name = join(self.src_folder, file_name)
            file_size = getsize(abs_file_name)
            file_time = getmtime(abs_file_name)
            self.current_sync[FILES][file_name] = {
                FILE_SIZE: file_size,
                FILE_TIME: file_time
            }
            self.temp_current_sync[FILES][file_name] = {
                FILE_SIZE: file_size,
                FILE_TIME: file_time
            }
            
            if file_name in self.prev_sync[FILES]:
                prev_attr = self.prev_sync[FILES][file_name]
                if prev_attr[FILE_SIZE] != file_size or prev_attr[FILE_TIME] != file_time:
                    self._update_file(file_name)
            else:
                self._copy_file(file_name)

            total_files_changed = self.new_files + self.updated_files
            if total_files_changed - self.last_temp_current_sync_saved == 1000:
                print('>>>>>>>>>>>>=============-----------=============<<<<<<<<<<<')
                print('')
                with open(self.sync_file, 'w', encoding='utf-8') as f:
                    json.dump(self.temp_current_sync, f)
                self.last_temp_current_sync_saved = total_files_changed

        for dir_name in src_dir_list:
            self.current_sync[FOLDERS].append(dir_name)
            self._run_copy_and_update_files(dir_name)
            
    def _listdir(self, abs_folder):
        if not exists(abs_folder):
            return []
        else:
            return os.listdir(abs_folder)
            
    def _run_delete_files(self):
        for file_name in self.prev_sync[FILES]:
            if file_name not in self.current_sync[FILES]:
                self._del_file(file_name)
            
    def _run_delete_folders(self):
        for dir_name in self.prev_sync[FOLDERS]:
            if dir_name not in self.current_sync[FOLDERS]:
                self._rmdir(dir_name)
            
        
    def _mkdir(self, dir_name):
        print('mkdir: {}'.format(dir_name))
        if not self.test:
            abs_path = join(self.dst_folder, dir_name)
            if not exists(abs_path):
                os.makedirs(abs_path)
        self.new_folders += 1
        
    def _copy_from_to(self, from_file, to_file):
#         from_file = '\\\\?\\'+from_file
#         to_file = '\\\\?\UNC\\'+to_file[2:]
            
        shutil.copy2(long_file_name(from_file), 
                     long_file_name(to_file))
    
    def _copy_file(self, file_name):
        src_file_path = join(self.src_folder, file_name)
        dst_file_path = join(self.dst_folder, file_name)
        print('copy: {} ({})'.format(file_name, str_file_size(src_file_path)))
        if not self.test:
            self._copy_from_to(src_file_path, dst_file_path)
        self.new_file_size += file_size(src_file_path)
        self.new_files += 1
        
    def _update_file(self, file_name):
        src_file_path = join(self.src_folder, file_name)
        dst_file_path = join(self.dst_folder, file_name)

        print('update: {} ({})'.format(file_name, str_file_size(src_file_path)))
        self.updated_file_size += file_size(src_file_path) - file_size(dst_file_path)
        if not self.test:
            self._copy_from_to(src_file_path, dst_file_path)
        self.updated_files += 1
    
    def _rmdir(self, dir_name):
        abs_dst_folder = join(self.dst_folder, dir_name)
        if not os.path.exists(abs_dst_folder):
            return
        
        dst_folder_content = [join(dir_name, f) for f in os.listdir(abs_dst_folder)]
        dir_list = sorted([f for f in dst_folder_content if isdir(join(self.dst_folder, f))])
        file_list = sorted([f for f in dst_folder_content if isfile(join(self.dst_folder, f))])
        
        for file_name in file_list:
            self._del_file(file_name)
            
        for subdir in dir_list:
            self._rmdir(subdir) 
        
        print('rmdir: {}'.format(dir_name))
        if not self.test:
            shutil.rmtree(join(self.dst_folder, dir_name))
        self.deleted_folders += 1
    
    def _del_file(self, file_name):
        print('del: {}'.format(file_name))
        full_file_name = join(self.dst_folder, file_name)
        if os.path.isfile(full_file_name):
            self.deleted_file_size -= file_size(full_file_name)
        if not self.test:
            if os.path.isfile(full_file_name):
                os.remove(full_file_name)
        self.deleted_files += 1
        
            
def sync(src_folder, dst_folder, sync_file, test=False):
    fs = FolderSync2(src_folder, dst_folder, sync_file, test)
    fs.run()
    return fs
        
    
    