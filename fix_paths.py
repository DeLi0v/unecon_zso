import os
import re

ROOT_DIR = os.path.abspath('./')  # корень сайта

pattern = re.compile(
    r'''(?P<attr>href|src|data-src)=["'](?P<path>(?!https?:|mailto:|tel:|#|data:)([^"']+?\.(?:htm|html|png|jpg|jpeg|gif|svg)))["']''',
    flags=re.IGNORECASE
)

def resolve_relative_to_source(source_file, target_path):
    """
    Пересчитывает путь от файла source_file до target_path
    даже если target_path уже был относительным
    """
    source_abs = os.path.abspath(source_file)
    source_dir = os.path.dirname(source_abs)

    # Абсолютный путь до целевого ресурса
    if target_path.startswith('/'):
        target_abs = os.path.normpath(os.path.join(ROOT_DIR, target_path.lstrip('/')))
    else:
        target_abs = os.path.normpath(os.path.join(source_dir, target_path))

    # Пересчитываем путь от текущего файла
    rel_path = os.path.relpath(target_abs, start=source_dir)
    return rel_path.replace('\\', '/')

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def repl(match):
        attr = match.group('attr')
        old_path = match.group('path')
        new_path = resolve_relative_to_source(filepath, old_path)
        print(f"{filepath}: {attr} — {old_path} → {new_path}")
        return f'{attr}="{new_path}"'

    new_content = pattern.sub(repl, content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✔ Обновлён: {filepath}")
    else:
        print(f"— Без изменений: {filepath}")

# Обход всех HTML-файлов
for dirpath, _, filenames in os.walk(ROOT_DIR):
    for filename in filenames:
        if filename.lower().endswith(('.htm', '.html')):
            fullpath = os.path.join(dirpath, filename)
            process_file(fullpath)
