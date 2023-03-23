import os


def load_all_files(self):
    yaml_files = []
    for dir_name, dirs, files in os.walk(self):
        for file in files:
            if file.endswith('.yaml'):
                yaml_files.append(os.path.join(dir_name, file))
    return yaml_files
    print(yaml_files)

    # for i in yaml_files:
    #     print(i)
    #     return i

#
# for i in load_all_files("C:\\Users\\CCJ\\Desktop\\Taichi-main\\configuration"):
#
#     print(i)
