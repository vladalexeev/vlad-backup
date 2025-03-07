
import os

def roll_file_stack(base_name, stack_size=5):
    last_file = base_name.format('-'+str(stack_size))
    if os.path.exists(last_file):
        os.remove(last_file)
        
    for index in reversed(range(1, stack_size)):
        cur_file = base_name.format('-'+str(index))
        next_file = base_name.format('-'+str(index+1))
        if os.path.exists(cur_file):
            os.rename(cur_file, next_file)
            
    first_file = base_name.format('')
    if os.path.exists(first_file):
        os.rename(first_file, base_name.format('-1'))
        
def long_file_name(abs_file_name):
    if abs_file_name.startswith('\\\\'):
        return '\\\\?\\UNC\\'+abs_file_name[2:]
    else:
        return '\\\\?\\'+abs_file_name
    
def str_file_size(file_path):
    full_size = os.path.getsize(file_path)
    return str_size(full_size)
    
def str_size(size):
    size_kb = float(size) / 1024
    if size_kb < 1024:
        return '{:.1f} KB'.format(size_kb)
    else:
        size_mb = size_kb / 1024
        return '{:.1f} MB'.format(size_mb)
    
    
if __name__ == '__main__':
    print(str_size(200))
    print(str_size(2000))
    print(str_size(20000))
    print(str_size(2000000))