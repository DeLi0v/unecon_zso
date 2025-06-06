import os
import re

ROOT_DIR = os.path.abspath('./')
LOGO_REL_PATH = 'upload/CMax/7de/a5zzzr7oxd95dux98mdxu5xoycjlquue.png'  # путь к логотипу от корня сайта

# Шаблон для <a href="index.htm" ...>
pattern_href = re.compile(r'<a\s+([^>]*?)href=["\']index\.htm["\']', flags=re.IGNORECASE)

# Шаблоны для логотипа
pattern_src = re.compile(r'src=["\']upload/CMax/[^"\']+["\']', flags=re.IGNORECASE)
pattern_data_src = re.compile(r'data-src=["\']upload/CMax/[^"\']+["\']', flags=re.IGNORECASE)

def make_relative(from_file, to_path):
    from_dir = os.path.dirname(os.path.abspath(from_file))
    to_abs = os.path.normpath(os.path.join(ROOT_DIR, to_path))
    return os.path.relpath(to_abs, from_dir).replace('\\', '/')

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # Заменяем href="index.htm"
    def repl_href(match):
        nonlocal changed
        new_href = make_relative(filepath, 'index.htm')
        changed = True
        print(f"{filepath}: href=\"index.htm\" → href=\"{new_href}\"")
        return f'<a {match.group(1)}href="{new_href}"'

    content = pattern_href.sub(repl_href, content)

    # Заменяем src="upload/..."
    def repl_src(match):
        nonlocal changed
        new_path = make_relative(filepath, LOGO_REL_PATH)
        changed = True
        print(f"{filepath}: src → {new_path}")
        return f'src="{new_path}"'

    content = pattern_src.sub(repl_src, content)

    # Заменяем data-src="upload/..."
    def repl_data_src(match):
        nonlocal changed
        new_path = make_relative(filepath, LOGO_REL_PATH)
        changed = True
        print(f"{filepath}: data-src → {new_path}")
        return f'data-src="{new_path}"'

    content = pattern_data_src.sub(repl_data_src, content)

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✔ Обновлён: {filepath}")
    else:
        print(f"— Без изменений: {filepath}")

# Обход всех .htm и .html файлов
for dirpath, _, filenames in os.walk(ROOT_DIR):
    for filename in filenames:
        if filename.lower().endswith(('.htm', '.html')):
            fullpath = os.path.join(dirpath, filename)
            process_file(fullpath)
