import os
import re

# Папка, в которой будем искать .htm/.html файлы
root_dir = '.'  # <-- Укажи свою папку

# Путь к папке с svg-файлами, к которому нужно сделать относительную ссылку
target_path = os.path.normpath('bitrix/templates/aspro_max/images/svg')

# Регулярка для поиска любых xlink:href ссылок на целевой каталог
pattern = re.compile(r'''xlink:href=["']([^"']*bitrix/templates/aspro_max/images/svg/[^"']+)["']''')

for subdir, _, files in os.walk(root_dir):
    for filename in files:
        if filename.endswith(('.htm', '.html')):
            file_path = os.path.join(subdir, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Функция для замены каждой найденной ссылки
            def replace_link(match):
                original_href = match.group(1)
                # Абсолютный путь к текущему HTML-файлу
                html_dir = os.path.dirname(file_path)
                # Абсолютный путь к SVG-файлу (убираем префиксы ../ или /)
                cleaned_href = original_href.lstrip('/').lstrip('./')
                full_svg_path = os.path.normpath(os.path.join(root_dir, cleaned_href))

                # Путь до папки, где лежит SVG
                rel_svg_dir = os.path.dirname(full_svg_path)

                # Относительный путь от HTML-файла до целевого SVG-файла
                relative_path = os.path.relpath(full_svg_path, html_dir)
                # Приводим к POSIX-формату (с прямыми слэшами)
                relative_path = relative_path.replace(os.sep, '/')

                return f'xlink:href="{relative_path}"'

            new_content = pattern.sub(replace_link, content)

            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Updated: {file_path}')
