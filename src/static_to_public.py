import os
import shutil


def main():
    # print(__file__)
    path_to_static = __file__.removesuffix("src/static_to_public.py") + "static"
    # print(path_to_static)
    path_to_public = __file__.removesuffix("src/static_to_public.py") + "public"
    # static_files = os.listdir(path_to_static)
    # print(os.listdir(path_to_static))
    # print(path_to_public)
    shutil.rmtree(path_to_public)
    # print(path_to_public)
    os.mkdir(path_to_public)
    copy_static_to_public(path_to_static, path_to_public)

def copy_static_to_public(src_path, dest_path, log = [], depth = 0):
    files = os.listdir(src_path)
    for file in files:
        if os.path.isfile(os.path.join(src_path, file)):
            # print(f"file {file}")
            shutil.copy(os.path.join(src_path, file), dest_path)
            message = f"Added {file} from {src_path} to {dest_path}"
            log.append(message)
        else:
            # print(f"not file {file}")
            depth += 1
            os.mkdir(os.path.join(dest_path, file))
            copy_static_to_public(os.path.join(src_path, file), os.path.join(dest_path, file), log, depth)
            depth -= 1
    
    # if depth == 0:
    #     print(log)

    



if __name__ == "__main__":
    main()

