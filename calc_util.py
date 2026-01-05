from file_util import str_size_ex


class TotalCounter:
    def __init__(self):
        self.new_files = 0
        self.updated_files = 0
        self.deleted_files = 0
        self.new_folders = 0
        self.deleted_folders = 0
        self.new_file_size = 0
        self.updated_file_size = 0
        self.deleted_file_size = 0

    def add_sync_result(self, result):
        self.new_files += result.new_files
        self.updated_files += result.updated_files
        self.deleted_files += result.deleted_files
        self.new_folders += result.new_folders
        self.deleted_folders += result.deleted_folders
        self.new_file_size += result.new_file_size
        self.updated_file_size += result.updated_file_size
        self.deleted_file_size += result.deleted_file_size

    def print(self):
        print(f'New folders = {self.new_folders}')
        print(f'Deleted folders = {self.deleted_folders}')
        print(f'New files = {self.new_files} ({str_size_ex(self.new_file_size)})')
        print(f'Updated files = {self.updated_files} ({str_size_ex(self.updated_file_size)})')
        print(f'Deleted files = {self.deleted_files} ({str_size_ex(self.deleted_file_size)})')
