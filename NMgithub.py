from github import Github, Auth, InputGitTreeElement

auth = Auth.Token(sys.argv[1])
g = Github(auth=auth)

repo = g.get_repo("0neKiwi/CSCI5180-lab5")
contents = repo.get_contents("")
files = []
for c in contents:
    f = str(c).replace('ContentFile(path="','').replace('")', '')
    files.append(f)

with open("json.txt", "r") as f:
    content = "\n".join(f.readlines())

if "json.txt" not in files:
    repo.create_file("json.txt", "Create json.txt", content, branch="master")
else:
    contents = repo.get_contents("OneKiwi/CSCI5180-lab5/json.txt")
    if content != contents:
        repo.update_file(contents.path, "made changes", content, contents.sha, branch="master")

