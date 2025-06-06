import os
import re

ROOT_DIR = './'  # Корневая директория сайта (относительно неё считаем уровни)

# Исправленное регулярное выражение (добавлена недостающая закрывающая кавычка)
pattern = re.compile(r'''(?P<attr>href)=["'](?P<path>/?(?:\.\./)*([^"']+\.htm)[^"']*)["']''')

def get_relative_prefix(filepath):
    """Возвращает относительный префикс (../) в зависимости от глубины вложенности файла"""
    rel_path = os.path.relpath(filepath, ROOT_DIR)
    depth = len(rel_path.split(os.sep)) - 1
    return '../' * depth if depth > 0 else './'

def make_relative_path(link_path, filepath):
    """Преобразует путь в ссылке в относительный"""
    if link_path.startswith('#'):
        return link_path  # Якорные ссылки не трогаем

    # Если ссылка уже относительная (содержит ../)
    if link_path.startswith('../'):
        return link_path

    rel_prefix = get_relative_prefix(filepath)
    
    # Если ссылка абсолютная (начинается с /)
    if link_path.startswith('/'):
        return rel_prefix + link_path.lstrip('/')
    
    # Если ссылка уже относительная (без / в начале)
    if '/' in link_path:
        return rel_prefix + link_path
    else:
        return rel_prefix + link_path if rel_prefix != './' else link_path

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace(match):
        attr = match.group('attr')
        old_path = match.group('path')
        new_path = make_relative_path(old_path, filepath)
        return f'{attr}="{new_path}"'

    new_content = pattern.sub(replace, content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✔ Обновлено: {filepath}")
    else:
        print(f"— Без изменений: {filepath}")

# Рекурсивный обход всех .htm файлов
for dirpath, _, filenames in os.walk(ROOT_DIR):
    for filename in filenames:
        if filename.endswith('.htm'):
            filepath = os.path.join(dirpath, filename)
            process_file(filepath)