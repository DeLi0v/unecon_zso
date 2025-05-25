import os
import re

# Корень сайта — здесь нужно указать абсолютный путь к корневой папке сайта на диске
ROOT_DIR = os.path.abspath('.')  # если скрипт запускается из корня сайта

def get_relative_upload_path(file_path):
    # Вычисляем относительный путь от директории файла до корня
    file_dir = os.path.dirname(os.path.abspath(file_path))
    relative_path = os.path.relpath(ROOT_DIR, file_dir)
    if relative_path == '.':
        # Если файл в корне, просто upload/...
        return 'upload'
    else:
        # Иначе, например ../../upload
        return os.path.join(relative_path, 'upload').replace('\\', '/')

def replace_upload_paths_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    relative_upload_path = get_relative_upload_path(file_path)

    # Паттерн для src, href, data-src, data-bg
    attr_pattern = re.compile(r'(src|href|data-src|data-bg)=["\']/upload/([^"\']+)["\']')

    def attr_replacer(match):
        attr = match.group(1)
        path_rest = match.group(2)
        return f'{attr}="{relative_upload_path}/{path_rest}"'

    content = attr_pattern.sub(attr_replacer, content)

    # Паттерн для url("/upload/...")
    url_pattern = re.compile(r'url\(["\']/upload/([^"\']+)["\']\)')

    def url_replacer(match):
        path_rest = match.group(1)
        return f'url("{relative_upload_path}/{path_rest}")'

    content = url_pattern.sub(url_replacer, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Обработан файл: {file_path}')

def process_all_htm_files(start_dir):
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.lower().endswith('.htm'):
                full_path = os.path.join(root, file)
                replace_upload_paths_in_file(full_path)

if __name__ == '__main__':
    process_all_htm_files(ROOT_DIR)
