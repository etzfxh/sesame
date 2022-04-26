#!/usr/bin/env python3

from collections import defaultdict
from pathlib import Path
import subprocess
import sys

BROWSER = 'firefox'
EDITOR = 'subl'
FILEMANAGER = 'pcmanfm'

APP_TO_EXT = {
    BROWSER: ['.htm', '.html', '.mp3', '.mp4'],
    'evince': ['.pdf'],
    'localc': ['.csv', '.ods', '.xls', '.xlsx'],
    'loimpress': ['.ppt', '.pptx'],
    'lowriter': ['.doc', '.docx', '.odf'],
    'lyx': ['.lyx'],
    'ristretto': ['.jpg', '.jpeg', '.png', '.svg', '.tif', '.tiff'],
#    'vlc': ['.mp3', '.mp4'],   # won't work when called from i3wm
    'yEd': ['.graphml'],
}

EXT_TO_APP = {
    ext: app
    for app, exts in APP_TO_EXT.items()
    for ext in exts}

OPTIONS = defaultdict(list)
OPTIONS[BROWSER] = ['-new-window']
OPTIONS[EDITOR] = ['-n']        # new window
OPTIONS[FILEMANAGER] = ['-n']   # new window

def sesame():
    '''
    Open the first command line argument, which may be a path or a url, with
    the appropriate application, using appropriate options:

    - Local directories are opened with the FILEMANAGER.
    - Local files are opened depending on their file name extension:
        - If the extension is in EXT_TO_APP, the respective app is used.
        - Otherwise, the EDITOR is used.
    - In all other cases, the BROWSER is used.
    '''
    path_or_url = sys.argv[1]
    maybe_path = Path(path_or_url).expanduser()
    if maybe_path.is_dir():
        app = FILEMANAGER
    elif maybe_path.is_file():
        try:
            app = EXT_TO_APP[maybe_path.suffix.lower()]
        except KeyError:
            app = EDITOR
    else:
        app = BROWSER
    command = [app] + OPTIONS[app] + [path_or_url]
    subprocess.run(command)

if __name__ == '__main__':
    sesame()
