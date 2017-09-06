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

@cel.task
def delete_quiz_resource(path):
    import shutil
    shutil.rmtree(path)

@cel.task
def delete_resource(filename):
    import os
    os.remove(filename)
