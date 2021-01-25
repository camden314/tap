from __future__ import print_function
import os
import shutil
import requests
import io
from tqdm import tqdm
import colorama
import zipfile
import time
import glob
from pathlib import Path
from distutils.spawn import find_executable
from pyunpack import Archive

colorama.init()

def clearscreen():
	os.system("cls")

def runit():
	os.environ["PATH"] += os.pathsep + str(Path.home())

	if find_executable('ffmpeg') is None:
		url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z" #big file test
		# Streaming, so we can iterate over the response.
		response = requests.get(url, stream=True)
		total_size_in_bytes= int(response.headers.get('content-length', 0))
		print(total_size_in_bytes)
		block_size = 1024 #1 Kibibyte
		progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc='Downloading \u001b[32;1mffmpeg\u001b[0m', colour='green')
		file = io.BytesIO()
		file_dat = b""
		for data in response.iter_content(block_size):
			progress_bar.update(len(data))
			file.write(data)
			#file_dat += data
		file.seek(0)
		progress_bar.close()
		if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
			print("\u001b[31mERROR, something went wrong\u001b[0m")
			exit()

		print("Pouring \u001b[32;1mffmpeg\u001b[0m...")

		save_location = Path.home()/"ff.7z"
		with open(save_location,'wb') as tmp:
			tmp.write(file.read())

		Archive(str(save_location)).extractall(Path.home())

		exec_path = Path.home()/"ffmpeg-4.3.1-2021-01-01-full_build"/"bin"
		os.rename(exec_path/"ffmpeg.exe", Path.home()/"ffmpeg.exe")
		os.rename(exec_path/"ffplay.exe", Path.home()/"ffplay.exe")

		# cleanup
		shutil.rmtree(Path.home()/"ffmpeg-4.3.1-2021-01-01-full_build")
		os.remove(save_location)
	try:
		os.makedirs(str(Path.home() / 'Desktop' / 'holds'))
	except OSError:
		pass
	try:
		str(Path.home() / 'Desktop' / 'holds' / '*.wav')
		os.makedirs(str(Path.home() / 'Desktop' / 'releases'))
	except OSError:
		pass

	if len(glob.glob(str(Path.home() / 'Desktop' / 'holds' / '*.wav'))) == 0 or len(glob.glob(str(Path.home() / 'Desktop' / 'releases' / '*.wav'))) == 0:
		print("\u001b[31;1m[Error]\u001b[0m No clicks found. Put your recorded clicks into the holds/releases folder on your desktop")
		print("Exiting")
		exit()
	if len(glob.glob(str(Path.home() / 'Desktop' / 'holds' / 's*.wav'))) == 0:
		print("\u001b[31;1m[Warning]\u001b[0m No soft clicks found. Tap will still work, but will not be as realistic. Add soft clicks by putting an 's' in front of the file name in the holds folder")
	import clk
	clk.main()
if __name__ == '__main__':
	runit()