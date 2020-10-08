import youtube_dl
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui 
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class download_info:
    url = ''
    percentance_str = ''
    percentance_int = 0

def my_hook(d):
    if d['status'] == 'downloading':
        download_info.percentance_str = d['_percent_str']
        download_info.percentance_str = download_info.percentance_str.replace('%','')
        download_info.percentance_int = int(float(download_info.percentance_str))
        p_bar.setValue(download_info.percentance_int)
    if d['status'] == 'finished':
        #print('Done downloading, now converting ...')
        percent_label.setText('Download completed.')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'progress_hooks': [my_hook],
}

boldFont=QtGui.QFont()
boldFont.setBold(True)

app = QApplication([])
app.setStyle('Fusion')
window = QWidget()
window.setWindowTitle('PYoutube Downloader')
window.setGeometry(1000, 600, 500, 270)
layout = QVBoxLayout()

url_label = QLabel('Youtube Link:')
url_label.setFont(boldFont)
url_label.setFont(QFont('Arial',17))
layout.addWidget(url_label)

url_textbox = QLineEdit()
url_textbox.setPlaceholderText("Enter url...")
url_textbox.setFont(QFont('Arial',15))
url_textbox.resize(40,80)
layout.addWidget(url_textbox)

blank_label = QLabel('')
layout.addWidget(blank_label)
layout.addWidget(blank_label)

download_button = QPushButton('Download (.mp3)')
download_button.setGeometry(20,20,300,180)
download_button.setStyleSheet('background-color : lightblue')
download_button.setFont(QFont('Arial',15))
layout.addWidget(download_button)

p_bar = QProgressBar()
p_bar.setGeometry(20,20,300,180)
p_bar.setFont(QFont('Arial',15))
layout.addWidget(p_bar)
p_bar.setValue(0)

percent_label = QLabel('Ready to download...')
percent_label.setFont(QFont('Arial',13))
layout.addWidget(percent_label)

trackname_label = QLabel('')
trackname_label.setFont(QFont('Arial',12))
layout.addWidget(trackname_label)

def download(url_args):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(
            url_args,
            download=True # False if we want only to extract the info
        )
        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result
        flag = True
        counter = 1
        track_name = video['title'] + '-' + video['id'] + '.mp3'
        track_name_renamed = video['title']
        dot_mp3 = '.mp3'
        try:
            os.rename(track_name, track_name_renamed + dot_mp3)
            trackname_label.setText(track_name_renamed + dot_mp3)
        except:
            while flag:
                final_name = track_name_renamed + '(' + str(counter) + ')' + dot_mp3
                try:
                    os.rename(track_name, final_name)
                    flag = False
                except:
                    counter+=1
                trackname_label.setText(final_name)

def on_button_clicked():
    download_info.url = url_textbox.text()
    url_textbox.setText('')
    percent_label.setText('Please wait...')
    trackname_label.setText('')
    download(download_info.url)

window.setLayout(layout)
download_button.clicked.connect(on_button_clicked)
window.show()
app.exec_()
#print(video) #video info
