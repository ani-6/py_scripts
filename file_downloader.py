import os,sys
import requests
import werkzeug
from tqdm import tqdm


def download_ckpt(url:str, directory, filename:str="", overwrite:bool=False, chunk_size:int=1) -> None:
    """
    try auto detect file name if left empty
    option to overwrite if file already existed
    chunk_size in MBytes
    """
    HEADERS = {"User-Agent": "my gist code"}  # some sites block if u dont have at least user agent
    with requests.get(url, headers=HEADERS, stream=True) as resp:

        # get file name
        if filename == "":
            MISSING_FILENAME = "missing_name"
            if content_disposition := resp.headers.get("Content-Disposition"):
                param, options = werkzeug.http.parse_options_header(content_disposition)
                if param == "attachment":
                    filename = options.get("filename", MISSING_FILENAME)
                else:
                    filename = MISSING_FILENAME
            else:
                filename = os.path.basename(url)
                fileext = os.path.splitext(filename)[-1]
                if fileext == "":
                    filename = MISSING_FILENAME

        # download file
        full_filename = directory + '/' + filename
        if overwrite or not os.path.exists(full_filename):
            TOTAL_SIZE = int(resp.headers.get("Content-Length", 0))
            CHUNK_SIZE = chunk_size * 10**6
            with (
              open(full_filename, mode="wb") as file,
              tqdm(total=TOTAL_SIZE, desc=f"download {filename}", unit="B", unit_scale=True) as bar
            ):
                for data in resp.iter_content(chunk_size=CHUNK_SIZE):
                    size = file.write(data)
                    bar.update(size)
def create_dir(path):
    isExist = os.path.exists(path)
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(path)
       print("Directory is created!")

if __name__ == "__main__":
    download_to_directory = 'files'
    url_to_download = ''
    create_dir(download_to_directory)
    if len(sys.argv) >= 2:
        url = sys.argv[1]
    else:
        url = url_to_download
    try:
        download_ckpt(url,download_to_directory)
    except PermissionError:
        print("Please provide write permission to folder - ",download_to_directory)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
    except:
        print("Something else went wrong")