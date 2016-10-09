
import pickle
import os
import shutil
from os.path import exists, join, isdir, isfile, getsize, getmtime
from datetime import datetime

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
        self.deleted_foldes = 0
        
    def run(self):
        start_time = datetime.now()
        
        if not exists(self.dst_folder):
            os.makedirs(self.dst_folder)
        
        if exists(self.sync_file):
            self.prev_sync = pickle.load(open(self.sync_file, 'rb'))
        else:
            self.prev_sync = {
                FILES: {},
                FOLDERS: []}
        self.current_sync = {
            FILES: {},
            FOLDERS: []}    
        
        self._run_copy_and_update_files('')
        self._run_delete_files()
        self._run_delete_folders()
        
        pickle.dump(self.current_sync, open(self.sync_file, 'wb'), 2)
        
        print('Work time = {}'.format(datetime.now() - start_time))
        if self.new_files == 0 and self.deleted_foldes == 0 and self.new_files == 0 and self.updated_files == 0 and self.deleted_files == 0:
            print('Nothing changed')
        else:
            print('New folders = {}'.format(self.new_folders))
            print('Deleted folders = {}'.format(self.deleted_foldes))
            print('New files = {}'.format(self.new_files))
            print('Updated files = {}'.format(self.updated_files))
            print('Deleted files = {}'.format(self.deleted_files)) 
        
        
    def _run_copy_and_update_files(self, folder_name):
        abs_src_folder = join(self.src_folder, folder_name)
        src_folder_content = [join(folder_name, f) for f in self._listdir(abs_src_folder)]
        src_dir_list = sorted([f for f in src_folder_content if isdir(join(self.src_folder, f))])
        src_file_list = sorted([f for f in src_folder_content if isfile(join(self.src_folder, f))])
        
        if folder_name <> '' and folder_name not in self.prev_sync[FOLDERS]:
            self._mkdir(folder_name)
        
        for file_name in src_file_list:
            abs_file_name = join(self.src_folder, file_name)
            file_size = getsize(abs_file_name)
            file_time = getmtime(abs_file_name)
            self.current_sync[FILES][file_name] = {
                FILE_SIZE: file_size,
                FILE_TIME: file_time
                }
            
            if file_name in self.prev_sync[FILES]:
                prev_attr = self.prev_sync[FILES][file_name]
                if prev_attr[FILE_SIZE] <> file_size or prev_attr[FILE_TIME] <> file_time:
                    self._update_file(file_name)
            else:
                self._copy_file(file_name)
                
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
            os.makedirs(join(self.dst_folder, dir_name))
        self.new_folders += 1
        
    def _copy_from_to(self, from_file, to_file):
        shutil.copy2(from_file, to_file)
    
    def _copy_file(self, file_name):
        print('copy: {}'.format(file_name))
        if not self.test:
            self._copy_from_to(
                               join(self.src_folder, file_name), 
                               join(self.dst_folder, file_name)
                               )
        self.new_files += 1
        
    def _update_file(self, file_name):
        print('update: {}'.format(file_name))
        if not self.test:
            self._copy_from_to(
                               join(self.src_folder, file_name), 
                               join(self.dst_folder, file_name)
                               )
        self.updated_files += 1
    
    def _rmdir(self, dir_name):
        abs_dst_folder = join(self.dst_folder, dir_name)
        dst_folder_content = [join(dir_name, f) for f in os.listdir(abs_dst_folder)]
        dir_list = sorted([f for f in dst_folder_content if isdir(join(self.dst_folder, f))])
        file_list = sorted([f for f in dst_folder_content if isfile(join(self.dst_folder, f))])
        
        for file_name in file_list:
            self._del_file(file_name)
            
        for subdir in dir_list:
            self._rmdir(subdir) 
        
        print('rmdir: {}'.format(dir_name))
        if not self.test:
            os.rmdir(join(self.dst_folder, dir_name))
        self.deleted_foldes += 1
    
    def _del_file(self, file_name):
        print('del: {}'.format(file_name))
        if not self.test:
            os.remove(join(self.dst_folder, file_name))
        self.deleted_files += 1
        
            
def sync(src_folder, dst_folder, sync_file, test=False):
    fs = FolderSync2(src_folder, dst_folder, sync_file, test)
    fs.run()
        
    
    