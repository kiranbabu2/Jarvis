import github

token = "my gitHub token"
g = github.Github('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')
new_repo = g.get_user().get_repo('Jarvis')

new_repo.create_file("new_file1.txt", "init commit", "file_content ------ ")