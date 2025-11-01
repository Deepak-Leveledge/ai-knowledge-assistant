import os 

UPLOAD_FOLDER = "uploads"

def save_upload_file(file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open ( file_path, "wb") as f:
        f.write(file.file.read())
        
    return file_path