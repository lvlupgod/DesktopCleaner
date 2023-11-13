import os
import re
import shutil
import zipfile

while True:
    def remove_duplicates(directory):
        for root, dirs, files in os.walk(directory):
            filedict = {}
            for filename in files:
                filepath = os.path.join(root, filename)

                # Check if file is a duplicate
                match = re.search(r'^(.*?)\((\d+)\)(\.[^.]*)?$', filename)
                if match:
                    name = match.group(1)
                    number = int(match.group(2))
                    ext = match.group(3) or ''

                    # Add file to dictionary with name as key and number as value
                    if name not in filedict:
                        filedict[name] = [(number, filepath, ext)]
                    else:
                        filedict[name].append((number, filepath, ext))

            # Rename files in each group
            for name in filedict:
                files = filedict[name]
                files.sort(key=lambda x: x[0])
                print(files)
                latest = files[-1][1]
                ext = files[-1][2]

                for number, filepath, _ in files[:-1]:
                    print(f"Deleted duplicate file: {filepath}")
                    os.remove(filepath)

                os.rename(latest, os.path.join(root, f"{name}{ext}"))
                print(f"Renamed {latest} to {name}{ext}")


    downloads_dir = os.path.expanduser("~/Downloads")

    # Create a dictionary of file types and their corresponding folders
    file_types = {
        "Image": [".jpg", ".jpeg", ".png", ".gif", ".tiff", ".bmp", ".eps"],
        "Code": [".ipynb", ".py", ".js", ".html", ".css", ".php", ".cpp", ".h", ".java"],
        "Document": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx"],
        "Audio": [".mp3", ".wav", ".aac", ".ogg"],
        "Video": [".mp4", ".avi", ".mov", ".flv", ".wmv", ".mpeg"],
        "Photoshop": [".psd"],
    }

    # Create the folders for each file type
    for folder_name in file_types.keys():
        folder_path = os.path.join(downloads_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Iterate over the files in the Downloads folder
    for filename in os.listdir(downloads_dir):
        filepath = os.path.join(downloads_dir, filename)

        # Unzip .zip files and delete the .zip file
        if filename.endswith(".zip"):
            # Check if the file has already been unzipped
            unzip_dir = os.path.join(downloads_dir, filename[:-4])
            if not os.path.exists(unzip_dir):
                # Unzip the file
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(downloads_dir)
            # Delete the .zip file
            os.remove(filepath)
            print(f"Unzipped and removed {filename}")

        # Delete .torrent files
        elif filename.endswith(".torrent"):
            os.remove(filepath)
            print(f"Removed {filename}")

        # Move .srt files to the .subtitle folder inside the Video folder
        elif filename.endswith(".srt"):
            dest_folder = os.path.join(downloads_dir, "Video", ".subtitle")
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            shutil.move(filepath, os.path.join(dest_folder, filename))
            print(f"Moved {filename} to {dest_folder}")

        # Move the file to the appropriate folder based on its extension
        else:
            for folder_name, extensions in file_types.items():
                if any(filename.endswith(ext) for ext in extensions):
                    dest_folder = os.path.join(downloads_dir, folder_name)
                    shutil.move(filepath, os.path.join(dest_folder, filename))
                    print(f"Moved {filename} to {dest_folder}")
                    break

    remove_duplicates(os.path.expanduser("~/Downloads"))
#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
