import os
import shutil
import filecmp

remoteIP = "0"
remotePort = "2222"
remoteUser = "nathan."
remotePass = ""
remoteDir = "HOME/template-upload/"
localDir = "intake/"
outputDir = '/webapps////'


def sftp():
    command = f"echo 'get -R {remoteDir}* {localDir}' | sshpass -p '{remotePass}' sftp -oPort={remotePort} {remoteUser}@{remoteIP}"
    print(os.popen(command).read())

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def clearDirContents(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))


def moveFiles(intake_dir, output_dir):
    for root, dirs, files in os.walk(intake_dir):
        relative_path = os.path.relpath(root, intake_dir)
        target_dir = os.path.join(output_dir, relative_path)
        ensureDir(target_dir)  
        
        for file in files:
            src_file_path = os.path.join(root, file)
            dst_file_path = os.path.join(target_dir, file)
            
            if not os.path.exists(dst_file_path) or not filecmp.cmp(src_file_path, dst_file_path, shallow=False):
                shutil.copy2(src_file_path, dst_file_path)

sftp()
moveFiles(localDir, outputDir)
clearDirContents(localDir)
