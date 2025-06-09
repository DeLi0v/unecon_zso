import os
from bs4 import BeautifulSoup
import re

# Папка, где находятся .htm файлы
ROOT_DIR = "."

# Регулярное выражение для поиска нужных ссылок
INDEX_LINK_REGEX = re.compile(r"^\.\./(index-\d+\.htm(?:\?.*)?)$")


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    changed = False

    # Ищем все теги <a href="...">
    for a in soup.find_all("a", href=True):
        href = a["href"]
        match = INDEX_LINK_REGEX.match(href)
        if match:
            new_href = match.group(1)  # удаляем ../
            a["href"] = new_href
            changed = True
            print(f"  Обновлена ссылка в {filepath}: {href} → {new_href}")

    # Если были изменения, переписываем файл
    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(soup))
        return True

    return False


def main():
    updated_files = 0
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith(".htm") or file.endswith(".html"):
                fullpath = os.path.join(root, file)
                if process_file(fullpath):
                    updated_files += 1
    print(f"\nИтого обновлено файлов: {updated_files}")


if __name__ == "__main__":
    main()
