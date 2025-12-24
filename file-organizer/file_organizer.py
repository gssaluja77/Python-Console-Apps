# File Organizer Script

import os, shutil
from pathlib import Path

folders = {
    "Images": [
        ".jpeg",
        ".jpg",
        ".tiff",
        ".gif",
        ".bmp",
        ".png",
        ".bpg",
        ".svg",
        ".heif",
        ".psd",
        ".ico",
        ".webp",
    ],
    "Audio": [
        ".aac",
        ".aa",
        ".aac",
        ".dvf",
        ".m4a",
        ".m4b",
        ".m4p",
        ".mp3",
        ".msv",
        ".ogg",
        ".oga",
        ".raw",
        ".vox",
        ".wav",
        ".wma",
    ],
    "Videos": [
        ".avi",
        ".flv",
        ".wmv",
        ".mov",
        ".mp4",
        ".webm",
        ".vob",
        ".mng",
        ".qt",
        ".mpg",
        ".mpeg",
        ".3gp",
    ],
    "Archives": [
        ".a",
        ".ar",
        ".cpio",
        ".iso",
        ".tar",
        ".gz",
        ".rz",
        ".7z",
        ".dmg",
        ".rar",
        ".xar",
        ".zip",
    ],
    "PDF Files": [".pdf"],
    "Applications": [".exe", ".app", ".apk", ".ipa"],
    "Documents": [".pages", ".doc", ".docx", ".docm", ".dot"],
    "Spreadsheets": [".numbers", ".xls", ".xlsx", ".xlsm"],
    "Text Files": [".txt", ".in", ".out", ".md"],
    "Python Files": [".py", ".pyw", ".ipynb", ".pyc"],
    "Java Files": [".class", ".java"],
    "C/C++ Files": [".c", ".cpp"],
    "JSON Files": [".json"],
    "Presentations": [".key", ".ppt", ".pptm", ".pptx"],
    "Shortcuts": [".lnk"],
}


extensions = {}
for folder, ext_list in folders.items():
    for ext in ext_list:
        extensions[ext] = folder

file_path = Path(__file__).resolve()
pwd = file_path.parent
all_files = os.listdir(pwd)

for file in all_files:
    if file.startswith("."):
        continue
    if os.path.isfile(os.path.join(pwd, file)):
        ext = os.path.splitext(file)[1]
        if ext in extensions:
            if not os.path.exists(os.path.join(pwd, extensions[ext])):
                os.mkdir(os.path.join(pwd, extensions[ext]))
                shutil.move(os.path.join(pwd, file), os.path.join(pwd, extensions[ext]))
            else:
                shutil.move(os.path.join(pwd, file), os.path.join(pwd, extensions[ext]))
        else:
            if not os.path.exists(os.path.join(pwd, "Misc")):
                os.mkdir(os.path.join(pwd, "Misc"))
                shutil.move(os.path.join(pwd, file), os.path.join(pwd, "Misc"))
            else:
                shutil.move(os.path.join(pwd, file), os.path.join(pwd, "Misc"))
