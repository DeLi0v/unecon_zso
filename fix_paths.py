import os
from bs4 import BeautifulSoup

# Путь к корню сайта с .htm файлами
ROOT_DIR = '.'

# Селектор блока с ссылками
BLOCK_CLASS = 'bottom-icons-panel'

def calc_depth(filepath):
    # Определим уровень вложенности файла относительно корня
    # Корень = 0, например, /index.htm -> 0, /catalog/index.htm -> 1, /auth/index.htm -> 1, /auth/subdir/page.htm -> 2
    rel_path = os.path.relpath(filepath, ROOT_DIR)
    # Разделяем путь по /
    parts = rel_path.split(os.sep)
    # Если файл в корне, depth = 0, иначе количество папок перед файлом
    return len(parts) - 1

def normalize_href(href):
    # Очистим href от лишних элементов (./, ../), вернем упрощенный путь
    # Например: ../index.htm -> index.htm, ./catalog/index.htm -> catalog/index.htm
    return os.path.normpath(href).replace('\\', '/')

def adjust_link(href, depth):
    # Относительный путь до корня сайта из текущей папки
    up_path = '../' * depth

    # Уберем возможные ./ и ../ из href (нормализуем)
    normalized_href = normalize_href(href)

    # Если ссылка начинается с '/' — считаем это корнем сайта и превращаем в относительную ссылку
    if normalized_href.startswith('/'):
        normalized_href = normalized_href[1:]

    # Теперь вернем ссылку, учитывая уровень вложенности
    # Например, для depth=2 и href='catalog/index.htm' будет '../../catalog/index.htm'
    # Если href уже идет с '../', уберем их и добавим свои
    href_parts = normalized_href.split('/')
    while href_parts and href_parts[0] == '..':
        href_parts.pop(0)
    final_href = up_path + '/'.join(href_parts)
    # Уберем двойные слэши, если есть
    final_href = final_href.replace('//', '/')
    # Если final_href пустой, поставим './'
    if final_href == '':
        final_href = ''
    return final_href

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    depth = calc_depth(filepath)

    block = soup.find('div', class_=BLOCK_CLASS)
    if not block:
        return False

    links = block.find_all('a', href=True)
    changed = False
    for a in links:
        old_href = a['href']
        new_href = adjust_link(old_href, depth)
        if old_href != new_href:
            a['href'] = new_href
            changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
    return changed

def main():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith('.htm') or file.endswith('.html'):
                fullpath = os.path.join(root, file)
                if process_file(fullpath):
                    print(f'Обновлен файл: {fullpath}')
                    count += 1
    print(f'Обновлено файлов: {count}')

if __name__ == '__main__':
    main()
