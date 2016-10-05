
from os import listdir
from os.path import isdir, isfile, join

class FolderSync:
    
    def __init__(self, src_folder, dst_folder):
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        
    def run(self):
        self._run('')
    
    def _run(self, folder_name):
        src_folder_content = listdir(join(self.src_folder, folder_name))
        src_dir_list = sorted([f for f in src_folder_content if isdir(join(self.src_folder, folder_name, f))])
        src_file_list = sorted([f for f in src_folder_content if isfile(join(self.src_folder, folder_name, f))])
        
        for dir_name in src_dir_list:
            rel_dir_name = join(folder_name, dir_name) 
            print('{}'.format(rel_dir_name))
            self._run(rel_dir_name)
            

def sync(src_folder, dst_folder):
    fs = FolderSync(src_folder, dst_folder)
    fs.run()
        
    