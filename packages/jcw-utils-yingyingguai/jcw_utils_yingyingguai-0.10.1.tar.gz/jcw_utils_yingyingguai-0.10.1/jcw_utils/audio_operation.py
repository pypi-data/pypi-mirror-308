from itertools import count
from mutagen.mp3 import MP3
import os

def extract_mp3_info(mp3_file_path):
    '''
    看MP3文件秒数用的
    '''
    try:
        audio = MP3(mp3_file_path)
        file_name = os.path.basename(mp3_file_path)
        file_size = os.path.getsize(mp3_file_path)
        play_length = audio.info.length

        print(f'name:{file_name},size:{file_size},audio length:{play_length}')

    except Exception as e:
        print(f"Error processing {mp3_file_path}: {e}")
# mp3_directory = r"E:\20241110清理手表录音"
# count=0
# for root, dirs, files in os.walk(mp3_directory):
#     for file in files:
#         if file.endswith(".mp3"):
#             count+=1
#             mp3_file_path = os.path.join(root, file)
#             extract_mp3_info(mp3_file_path)
# print(f'count{count}')
                