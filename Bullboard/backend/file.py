def read_file(filename):
    with open(filename, "rb") as file:
        return file.read()


def read_file_as_list(filename):
    lines = []
    with open(filename, "r") as file:
        for line in file.readlines():
            lines.append(line)
    return lines