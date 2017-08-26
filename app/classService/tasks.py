from app import cel

@cel.task
def extract_quiz_task(filename):
    print(filename)
    import zipfile
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(filename[:-4])
    zip_ref.close()
    import os
    os.remove(filename)
