def readTextLines(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            yield line

text_lines = readTextLines("python_poem.txt")

for i, line in enumerate(text_lines):
    if "beats" in line:
        print("Word beats found in line: ", i)
