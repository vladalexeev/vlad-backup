
from os import listdir
from os.path import isdir, isfile, join, exists, getctime, getmtime, getsize

class FolderSync:
    
    def __init__(self, src_folder, dst_folder):
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        
    def run(self):
        self._run('')
        
    def _mkdir(self, dir_name):
        print('mkdir {}'.format(dir_name))
        pass
    
    def _copy_file(self, file_name):
        pass
    
    def _rmdir(self, dir_name):
        pass
    
    def _del_file(self, file_name):
        pass
    
    def _compare_files(self, file_name):
        abs_dst_file = join(self.dst_folder, file_name)
        if not exists(abs_dst_file):
            return False
        
        abs_src_file = join(self.src_folder, file_name)
        
        src_size = getsize(abs_src_file)
        dst_size = getsize(abs_dst_file)
        if src_size <> dst_size:
            return False
        
        src_ctime = getctime(abs_src_file)
        dst_ctime = getctime(abs_dst_file)
        if src_ctime <> dst_ctime:
            return False
        
        src_mtime = getmtime(abs_src_file)
        dst_mtime = getmtime(abs_dst_file)
        if src_mtime <> dst_mtime:
            return False
        
        return True
        
        
    
    def _run(self, folder_name):
        abs_src_folder = join(self.src_folder, folder_name)
        src_folder_content = [join(folder_name, f) for f in listdir(abs_src_folder)]
        src_dir_list = sorted([f for f in src_folder_content if isdir(join(self.src_folder, f))])
        src_file_list = sorted([f for f in src_folder_content if isfile(join(self.src_folder, f))])
        
        abs_dst_folder = join(self.dst_folder, folder_name)
        if not exists(abs_dst_folder):
            self._mkdir(folder_name)
        dst_folder_content = [join(folder_name, f) for f in listdir(abs_dst_folder)]
        dst_dir_list = sorted([f for f in dst_folder_content if isdir(join(self.dst_folder, f))])
        dst_file_list = sorted([f for f in dst_folder_content if isfile(join(self.dst_folder, f))])
        
        for dir_name in src_dir_list:
            print('{}'.format(dir_name))
            self._run(dir_name)
            

def sync(src_folder, dst_folder):
    fs = FolderSync(src_folder, dst_folder)
    fs.run()
        
    