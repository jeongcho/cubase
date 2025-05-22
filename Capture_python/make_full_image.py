import os

def create_image_list_file(directory, height):
    files = os.listdir(directory)
    png_files = [file for file in files if file.lower().endswith('.png')]
    png_files.sort()
    # content = '\n'.join(f'<img src="{file}" height="{height}">' for file in png_files)
    content = '\n'.join(f'![img]({file})' for file in png_files)
    # content = ' '.join(f'<img src="{file}" height="{height}">' for file in png_files)
    # content = ' '.join(f'![img]({file})' for file in png_files)
    text_file = "image_list.md"
    text_file_path = os.path.join(directory, text_file)
    with open(text_file_path, 'w') as file:
        file.write(content)
    return text_file_path

directory = os.getcwd()
height = 100
text_file_created = create_image_list_file(directory, height)


