
import os
import shutil
from os import listdir
from os.path import isdir, isfile, join, exists, getmtime, getsize
from datetime import datetime
from file_util import str_file_size

class FolderSync:
    
    def __init__(self, src_folder, dst_folder, test=False):
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        self.test = test
        self.new_files = 0
        self.updated_files = 0
        self.deleted_files = 0
        self.new_folders = 0
        self.deleted_foldes = 0
        
    def run(self):
        start_time = datetime.now()
        self._run('')
        
        print('Work time = {}'.format(datetime.now() - start_time))
        if self.new_files == 0 and self.deleted_foldes == 0 and self.new_files == 0 and self.updated_files == 0 and self.deleted_files == 0:
            print('Nothing changed')
        else:
            print('New folders = {}'.format(self.new_folders))
            print('Deleted folders = {}'.format(self.deleted_foldes))
            print('New files = {}'.format(self.new_files))
            print('Updated files = {}'.format(self.updated_files))
            print('Deleted files = {}'.format(self.deleted_files)) 
        
    def _mkdir(self, dir_name):
        print('mkdir: {}'.format(dir_name))
        if not self.test:
            os.makedirs(join(self.dst_folder, dir_name))
        self.new_folders += 1
        
    def _copy_from_to(self, from_file, to_file):
        shutil.copy2(from_file, to_file)
    
    def _copy_file(self, file_name):
        print('copy: {} ({})'.format(file_name, str_file_size(join(self.src_folder, file_name))))
        if not self.test:
            self._copy_from_to(
                               join(self.src_folder, file_name), 
                               join(self.dst_folder, file_name)
                               )
        self.new_files += 1
        
    def _update_file(self, file_name):
        print('update: {} ({})'.format(file_name, str_file_size(join(self.src_folder, file_name))))
        if not self.test:
            self._copy_from_to(
                               join(self.src_folder, file_name), 
                               join(self.dst_folder, file_name)
                               )
        self.updated_files += 1
    
    def _rmdir(self, dir_name):
        abs_dst_folder = join(self.dst_folder, dir_name)
        dst_folder_content = [join(dir_name, f) for f in listdir(abs_dst_folder)]
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
    
    def _compare_files(self, file_name):
        abs_dst_file = join(self.dst_folder, file_name)
        if not exists(abs_dst_file):
            return False
        
        abs_src_file = join(self.src_folder, file_name)
        
        src_size = getsize(abs_src_file)
        dst_size = getsize(abs_dst_file)
        if src_size != dst_size:
            return False
        
        src_mtime = getmtime(abs_src_file)
        dst_mtime = getmtime(abs_dst_file)
        if abs(src_mtime - dst_mtime) > 0.01:
            return False
        
        return True
        
    def _distribute_files(self, src_list, dst_list):
        return (
                [f for f in src_list if f not in dst_list],
                [f for f in src_list if f in dst_list],
                [f for f in dst_list if f not in src_list]
                )
        
    def _listdir(self, abs_folder):
        if not exists(abs_folder):
            return []
        else:
            return listdir(abs_folder)
        
    
    def _run(self, folder_name):
        abs_src_folder = join(self.src_folder, folder_name)
        src_folder_content = [join(folder_name, f) for f in self._listdir(abs_src_folder)]
        src_dir_list = sorted([f for f in src_folder_content if isdir(join(self.src_folder, f))])
        src_file_list = sorted([f for f in src_folder_content if isfile(join(self.src_folder, f))])
        
        abs_dst_folder = join(self.dst_folder, folder_name)
        if not exists(abs_dst_folder):
            self._mkdir(folder_name)
        dst_folder_content = [join(folder_name, f) for f in self._listdir(abs_dst_folder)]
        dst_dir_list = sorted([f for f in dst_folder_content if isdir(join(self.dst_folder, f))])
        dst_file_list = sorted([f for f in dst_folder_content if isfile(join(self.dst_folder, f))])
        
        new_files, exist_files, removed_files = self._distribute_files(src_file_list, dst_file_list)
        for file_name in new_files:
            self._copy_file(file_name)
            
        for file_name in exist_files:
            if not self._compare_files(file_name):
                self._update_file(file_name)
                
        for file_name in removed_files:
            self._del_file(file_name)
        
        
        new_dirs, exist_dirs, removed_dirs = self._distribute_files(src_dir_list, dst_dir_list)
        update_dirs = sorted(new_dirs + exist_dirs)
        
        for dir_name in update_dirs:
            self._run(dir_name)
            
        for dir_name in removed_dirs:
            self._rmdir(dir_name)
            

def sync(src_folder, dst_folder, test=False):
    fs = FolderSync(src_folder, dst_folder, test)
    fs.run()
        
    