import os

def rename_file(name, color, image_path):
    folder_path= "/Users/tharshini/Documents/Sort-ware-Solutions"
    new_folder_path="/Users/tharshini/Documents/Sort-ware-Solutions/Read_Cards"
    new_name=f"{name}_{color}.png"
    old_file = os.path.join(folder_path, image_path)
    new_file = os.path.join(new_folder_path, new_name)
    os.rename(old_file, new_file)
    
