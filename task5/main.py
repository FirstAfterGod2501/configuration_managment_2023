import os
import sys
import subprocess

def get_files_and_folders(path):
    files = []
    folders = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            files.append(item)
        elif os.path.isdir(item_path):
            folders.append(item)
    return files, folders

def get_commits():
    commits = []
    git_dir = os.path.join(os.getcwd(), '.git')
    refs_dir = os.path.join(git_dir, 'refs', 'heads')
    for branch in os.listdir(refs_dir):
        branch_path = os.path.join(refs_dir, branch)
        with open(branch_path, 'r') as f:
            commit = f.read().strip()
            commits.append(commit)
    return commits

def get_changed_files(commit):
    files = []
    git_dir = os.path.join(os.getcwd(), '.git')
    commit_dir = os.path.join(git_dir, 'objects', commit[:2])
    commit_file = os.path.join(commit_dir, commit[2:])
    if(not os.path.exists(commit_file)):
        return files
    with open(commit_file, 'rb') as f:
        content = f.read()
        decompressed_content = subprocess.check_output(['git', 'cat-file', '-p', commit])
        for line in decompressed_content.splitlines():
            if line.startswith(b'blob'):
                file_path = line.split(b'\t', 1)[1].decode()
                files.append(file_path)
    return files

def generate_dot_code():
    dot_code = 'digraph G {\n'
    commits = get_commits()
    for i, commit in enumerate(commits):
        dot_code += f'  commit{i}->"{commit}"\n'
        if i > 0:
            previous_commit = commits[i-1]
            changed_files = get_changed_files(commit)
            for file in changed_files:
                dot_code += f'  "{previous_commit}" -> "{commit}" [label="{file}"];\n'
    dot_code += '}'
    return dot_code

def save_dot_code(dot_code, file_path):
    with open(file_path, 'w') as f:
        f.write(dot_code)

def run():
    if len(sys.argv) != 2:
        print('Usage: python git_visualizer.py <output_file>')
        return
    output_file = sys.argv[1]
    dot_code = generate_dot_code()
    save_dot_code(dot_code, output_file)
    print(f'Dot code saved to {output_file}')

if __name__ == '__main__':
    run()
