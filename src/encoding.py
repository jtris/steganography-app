import os


def encode_file_by_appending(file_path: str, data: bytes, save_path: str) -> str:
    with open(file_path, 'rb') as f:
        image_contents = f.read()

    if os.path.isfile(save_path):
        os.remove(save_path)

    with open(save_path, 'ab') as f:
        f.write(image_contents+data)
