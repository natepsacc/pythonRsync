import os
import shutil
import filecmp
import paramiko



def scp():
    try:
        # Connect to the server
        client.connect(remoteIP, port=remotePort, username=remoteUser, password=remotePass)
        
        # Create an SFTP session over the existing connection
        sftp = client.open_sftp()
        
        # List files in the remote directory
        files = sftp.listdir(remoteDir)
        
        # Download each file in the remote directory
        for file in files:
            remoteFilePath = remoteDir + file
            localFilePath = localDir + file
            
            # Adjust the path if necessary, based on how the server exposes the file system
            sftp.get(remoteFilePath, localFilePath)
            print(f"Downloaded {file}")
        
        # Close the SFTP session and SSH connection
        sftp.close()
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
    # Executing the command
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
