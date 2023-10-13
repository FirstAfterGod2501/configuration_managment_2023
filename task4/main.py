import subprocess


def execute_task(task):
    if task[0] == "service":
        for subtask in task[1:]:
            if subtask[0] == "compileOptions":
                compile_options = subtask[1:]
            elif subtask[0] == "compiler":
                compiler = subtask[1]
            elif subtask[0] == "add":
                source_files = subtask[1:]

    compile_command = [compiler] + compile_options + source_files
    subprocess.run(compile_command)

for task in input_data:
    execute_task(task)















































































# Пример входных данных
input_data = [
    ["service",
     ["compileOptions", "-O3", "-std=c++20"],
     ["compiler", "gcc"],
     ["add", ["source", "main.cpp"]]
     ]
]
