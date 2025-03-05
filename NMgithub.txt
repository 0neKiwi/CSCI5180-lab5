import sys
import os
from github import Github, Auth, InputGitTreeElement

auth = Auth.Token(sys.argv[1])
g = Github(auth=auth)

repo = g.get_repo("0neKiwi/CSCI5180-lab5")
contents = repo.get_contents("")
files = []
local = ["json.txt"]#list(os.listdir(os.getcwd()))
for c in contents:
    f = str(c).replace('ContentFile(path="','').replace('")', '')
    files.append(f)

for l in local:
    with open(l, "r") as f:
        content = "\n".join(f.readlines())

    if l not in files:
        repo.create_file(l, "Create file", content, branch="master")
    else:
        contents = repo.get_contents("json.txt")
        if content != contents:
            repo.update_file(contents.path, "made changes", content, contents.sha, branch="master")
        else:
            print("Ignoring %s" % (l))
