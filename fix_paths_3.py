import os
from bs4 import BeautifulSoup

ROOT_DIR = "."  # Директория с HTML-файлами


def is_exception(a_tag):
    """Проверяет, нужно ли исключить ссылку из замены"""
    # Исключение по классу
    if "breadcrumbs__link" in a_tag.get("class", []):
        return True

    # Исключение — если находится внутри логотипа
    parent = a_tag
    for _ in range(4):  # Проверим до 4 уровней вверх
        parent = parent.parent
        if parent and "class" in parent.attrs:
            classes = parent.get("class", [])
            if any(cls in ["logo", "logo-block"] for cls in classes):
                return True
    return False


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    changed = False

    for a in soup.find_all("a", href=True):
        if a["href"] == "../index.htm" and not is_exception(a):
            print(f'  Обновлена ссылка в {filepath}: {a["href"]} → index.htm')
            a["href"] = "index.htm"
            changed = True

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
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    updated_files += 1
    print(f"\nГотово. Изменено файлов: {updated_files}")


if __name__ == "__main__":
    main()
