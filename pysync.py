import os
import shutil
import filecmp


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def moveFiles(intake_dir, output_dir):
    for root, dirs, files in os.walk(intake_dir):
        relative_path = os.path.relpath(root, intake_dir)
        target_dir = os.path.join(output_dir, relative_path)
        ensure_dir(target_dir)  
        
        for file in files:
            src_file_path = os.path.join(root, file)
            dst_file_path = os.path.join(target_dir, file)
            
            if not os.path.exists(dst_file_path) or not filecmp.cmp(src_file_path, dst_file_path, shallow=False):
                shutil.copy2(src_file_path, dst_file_path)
                print(f"Copied {src_file_path} to {dst_file_path}")

intakePath = 'intakeTestDir'
outputPath = '/'
moveFiles(intakePath, outputPath)
