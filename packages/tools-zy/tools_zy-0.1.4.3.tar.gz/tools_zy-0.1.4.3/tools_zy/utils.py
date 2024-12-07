import shutil
import os
from tqdm import tqdm


def operate_files(org_folder, det_folder, names=None, format=".jpg", op='copy', recursion=False):
    """
    copy or move files from org_folder to det_folder.
    if names is not None, file name is (name + format), and recursion will be ignored.
    org_folder: original folder
    det_folder: destination folder
    names: file names to be operated
    format: file format
    op: 'copy' or 'move'
    recursion: whether to operate files in subfolders
    """
    def opt_file_(org_file, det_file, op):
        if op == 'copy':
            shutil.copy(org_file, det_file)
        elif op == 'move':
            shutil.move(org_file, det_file)

    if not os.path.exists(det_folder):
        os.makedirs(det_folder)
    if names is not None: 
        # 指定文件夹下文件名
        for name in tqdm(names, desc=org_folder + '\n', ncols=80, unit=format):
            org_fullname = os.path.join(org_folder, name + format)
            det_fullname = os.path.join(det_folder, name + format)
            opt_file_(org_fullname, det_fullname, op)
    elif recursion:
        # 只指定文件后缀，但是要求递归操作
        for root, dirs, files in os.walk(org_folder):
            names = [f for f in files if f.endswith(format)]
            for name in tqdm(names, desc=root + '\n', ncols=80, unit=format):
                org_fullname = os.path.join(root, name + format)
                det_fullname = os.path.join(det_folder, name + format)
                opt_file_(org_fullname, det_fullname, op)
    else:
        # 只指定文件后缀，不递归操作
        names = [f for f in os.listdir(org_folder) if f.endswith(format)]
        for name in tqdm(names, desc=org_folder + '\n', ncols=80, unit=format):
            org_fullname = os.path.join(org_folder, name + format)
            det_fullname = os.path.join(det_folder, name + format)
            opt_file_(org_fullname, det_fullname, op)


def copy_files(org_folder, det_folder, names=None, format=".jpg", recursion=False):
    operate_files(org_folder, det_folder, names, format, recursion, op='copy')

def move_files(org_folder, det_folder, names=None, format=".jpg", recursion=False):
    operate_files(org_folder, det_folder, names, format, recursion, op='move')

