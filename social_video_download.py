import shutil
from urllib.parse import urlparse
import time
import instaloader
import sys
import os
from TikTokApi import TikTokApi
import instaloader
from instaloader import Post
import argparse


DIR_PATH = os.getcwd()
source_folder = os.path.dirname(str(os.path.abspath(sys.argv[0])))

instegram_user_name = "" # your email
instegram_password = '' # your password

def create_folder(out_folder, folder_name):
    out_path = os.path.join(out_folder, folder_name)
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    return out_path


def error_log(error,source_url=""):
    log_path = DIR_PATH+"/log/error.txt"
    with open(log_path, 'a') as outfile:
        outfile.write(source_url+"-"+error)
        outfile.write('\n')


def tiktok_download_function(video_url, downloaded_file_path):
    try:
        with TikTokApi() as api:
            vd = api.video(
                url=video_url).bytes()

            with open(downloaded_file_path, 'wb') as output:
                output.write(vd)
    except Exception as e:
        error_log(error=str(e))


def instegram_download_video(video_url, downloaded_file_path):
    try:
        L = instaloader.Instaloader()
        L.login(instegram_user_name, instegram_password)
        path = urlparse(video_url).path
        short_code = path.split("/")[2]
        print(short_code)
        post = Post.from_shortcode(L.context, short_code)
        L.download_post(post, "temp")
        downloaded_files = os.listdir("temp")
        for fil in downloaded_files:
            d_file_path = "temp/" + str(fil)
            if str(fil).__contains__(".mp4"):
                d_file_path = "temp/" + str(fil)
                shutil.copy(d_file_path, downloaded_file_path)
                break
        shutil.rmtree('temp')
    except Exception as e:
        error_log(error=str(e))


log_folder_path = create_folder(source_folder, "log")
#url = sys.argv[1]
#file_path =sys.argv[2]

parser = argparse.ArgumentParser()
parser.add_argument('-u', help='URL')
parser.add_argument('-o', help='Output')
args = parser.parse_args()
url = args.u
file_path = args.o
try:

    if str(url).__contains__("tiktok"):
        tiktok_download_function(url, file_path)

    elif str(url).__contains__("instagram"):
        instegram_download_video(url, file_path)

    else:
        error_log("Unknown url")
except Exception as e:
    error_log(error=str(e))
