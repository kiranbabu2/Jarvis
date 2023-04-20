import github as gt

g = gt.Github('XXXXXXXXXXXXXXXXXXXXX')
repo = g.get_user().get_repo('Jarvis')

def get_csv_contents(file_path):
    with open(file_path, mode ='r') as file:
        data = file.read()
    return data

def get_image_contents(file_path):
    with open(file_path, "rb") as image:
        f = image.read()
        image_data = bytearray(f)
    return bytes(image_data)

def save_file(repo, data,git_path, commit_message):
    try:
        contents = repo.get_contents(git_path, ref="main")
        repo.update_file(contents.path,commit_message, data, contents.sha, branch="main")
    except:
        repo.create_file(git_path, commit_message,data)
    return
