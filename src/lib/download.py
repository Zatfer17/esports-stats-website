import gdown

def download_data(url, folder, quiet=False):
    gdown.download_folder(url, quiet=quiet, use_cookies=False, output=folder)