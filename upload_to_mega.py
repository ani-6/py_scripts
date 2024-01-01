from mega import Mega
import os
import sys

email = ''
password = ''
directory = 'files'
folder_to_upload = 'uploads'

def login_to_mega(email,password):
    try:
        print('Trying to login in your account')
        mega = Mega()
        m = mega.login(email, password)
        print('Login successfull')
        return m
    except:
        print('Bad login!')
        sys.exit(0)

def get_all_files_to_upload():
    try:
        dir_list = os.listdir('imgs')
        return dir_list
    except Exception as error:
        print('Error: ',error)

def upload_files(list,m):
    if len(list)==0:
        print('No files to upload')
        sys.exit(0)
    try:
        folder = m.find(folder_to_upload)
        print("Uploading files...")
        for f in list:
            upload_file = directory + '/' + f
            file = m.upload(upload_file, folder[0])
            print(f,' successfully uploaded')
        return "All files uploaded sucessfully" 
    except Exception as error:
        print('Error: ',error)


if __name__ == "__main__":
    try:
        m = login_to_mega(email,password)
        list = get_all_files_to_upload()
        result = upload_files(list,m)
        print(result)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
    except:
        print("Something else went wrong")