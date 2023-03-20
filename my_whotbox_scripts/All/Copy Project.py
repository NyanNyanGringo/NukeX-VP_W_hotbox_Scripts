import os
import shutil
import re

def lastCopyPlusOne(nk_last_copy):
    separate = nk_last_copy.split('_COPY_')
    number_plus_one = str(int((separate[-1]).replace('.nk', '')) + 1).zfill(3)
    
    return str(separate[0] + '_COPY_' + str(number_plus_one) + '.nk')

root = nuke.root().name()
if root == 'Root':
    nuke.message('Please save prj first')
else:
    root_parts = os.path.split(root)
    root_name = root_parts[1]
    root_path = root_parts[0]
    
    nk_files = []
    for file in os.listdir(root_path):
        print('wrok with ' + file)
        if os.path.isfile(os.path.join(root_path, file)):
            if file.endswith(".nk"):
                nk_files.append(file)
    print(f'got nk_files: {nk_files}')
    
    nk_copies = []
    for nk_file in nk_files:
        if '_COPY_' in nk_file:
            nk_copies.append(nk_file)
    print(f'got nk_copies: {nk_copies}')
    
    if len(nk_copies) > 0:
        nk_copies = sorted(nk_copies)
        nk_last_copy = nk_copies[-1]
        shutil.copy(root, os.path.join(root_path, lastCopyPlusOne(nk_last_copy)))
        nuke.message('Copied with filename ' + str(lastCopyPlusOne(nk_last_copy)))
    else:
        shutil.copy(root, os.path.join(root_path, root_name.replace('.nk', '')+'_COPY_001.nk'))
        nuke.message('Copied with filename ' + str(root_name.replace('.nk', '')+'_COPY_001.nk'))
