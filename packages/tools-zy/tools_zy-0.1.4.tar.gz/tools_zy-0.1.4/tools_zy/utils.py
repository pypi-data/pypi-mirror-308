import shutil
import os
from tqdm import tqdm



def copy_files(org_folder, det_folder, names, format=".jpg"):
    if not os.path.exists(det_folder):
        os.makedirs(det_folder)
    for name in tqdm(names, desc=org_folder + '\n', ncols=80, unit=format):
        org_fullname = os.path.join(org_folder, name + format)
        det_fullname = os.path.join(det_folder, name + format)
        shutil.copy(org_fullname, det_fullname)

def move_files(org_folder, det_folder, names, format=".jpg"):
    if not os.path.exists(det_folder):
        os.makedirs(det_folder)
    for name in tqdm(names, desc=org_folder + '\n', ncols=80, unit=format):
        org_fullname = os.path.join(org_folder, name + format)
        det_fullname = os.path.join(det_folder, name + format)
        shutil.move(org_fullname, det_fullname)

