import json
import os
from os.path import exists, join, isdir, isfile, getsize, getmtime
from datetime import datetime

import paramiko

from file_util import long_file_name, str_file_size

FILES = 'files'
FOLDERS = 'folders'

FILE_SIZE = 'size'
FILE_TIME = 'time'

class FolderSync2_SFTP:
    
    def __init__(
            self,
            src_folder: str,
            dst_folder: str,
            sync_file: str,
            hostname: str,
            port: int,
            username: str,
            password: str,
            test=False):
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        self.sync_file = sync_file
        self.current_sync = None
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.test = test
        self.new_files = 0
        self.updated_files = 0
        self.deleted_files = 0
        self.new_folders = 0
        self.deleted_foldes = 0
        self.ssh = None
        self.sftp = None
        
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

        self.current_sync = {
            FILES: {},
            FOLDERS: []}

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Подключаемся к серверу
        self.ssh.connect(self.hostname, port=self.port, username=self.username, password=self.password)

        # Создаем SFTP сессию
        self.sftp = self.ssh.open_sftp()
        
        self._run_copy_and_update_files('')
        self._run_delete_files()
        self._run_delete_folders()

        self.sftp.close()
        self.ssh.close()

        with open(self.sync_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_sync, f)
        
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
            
            if file_name in self.prev_sync[FILES]:
                prev_attr = self.prev_sync[FILES][file_name]
                if prev_attr[FILE_SIZE] != file_size or prev_attr[FILE_TIME] != file_time:
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
            abs_path = join(self.dst_folder, dir_name).replace('\\', '/')
            if not exists(abs_path):
                try:
                    self.sftp.stat(abs_path)
                except FileNotFoundError:
                    self.sftp.mkdir(abs_path)
        self.new_folders += 1
        
    def _copy_from_to(self, from_file, to_file):
        self.sftp.put(from_file, to_file.replace('\\', '/'))
    
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
            self.sftp.rmdir(join(self.dst_folder, dir_name).replace('\\', '/'))
        self.deleted_foldes += 1
    
    def _del_file(self, file_name):
        print('del: {}'.format(file_name))
        if not self.test:
            full_file_name = join(self.dst_folder, file_name).replace('\\', '/')
            self.sftp.remove(full_file_name)
        self.deleted_files += 1
        
            
def sync_sftp(src_folder, dst_folder, sync_file, hostname, port, username, password, test=False):
    fs = FolderSync2_SFTP(src_folder, dst_folder, sync_file, hostname, port, username, password, test)
    fs.run()
        
    
    