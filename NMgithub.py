import sys
import os
from github import Github, Auth, InputGitTreeElement

def NMgithub(repo_name, branch, cred):
    auth = Auth.Token(cred)
    g = Github(auth=auth)
    repo = g.get_repo(repo_name)
    g_files = [str(c).replace('ContentFile(path="', '').replace('")', '') for c in repo.get_contents("")]
    l_files = list(os.listdir(os.getcwd()))
    l_files = [f for f in l_files if f[0] != '.']
    for f_name in l_files:
        print("Checking %s..." % (f_name))
        if f_name.endswith(".jpg") or f_name.endswith(".pcap"):
            with open(f_name, "rb") as f:
                l_content = bytes(bytearray(f.read()))
        else:
            with open(f_name, "r") as f:
                l_content = f.read()
        if f_name not in g_files:
            repo.create_file(f_name, "Creating file %s" %(f_name), l_content, branch=branch)
        else:
            g_content = repo.get_contents(f_name)
            if l_content != g_content:
                repo.update_file(g_content.path, "Made changes to %s" %(f_name), l_content, g_content.sha, branch=branch)
            else:
                print("Ignoring %s: no changes detected" % (f_name))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: NMgithub.py git_repo git_branch git_token")
    else:
        NMgithub(sys.argv[1], sys.argv[2], sys.argv[3])
