
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
    