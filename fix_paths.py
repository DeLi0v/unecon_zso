import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse, urlsplit, urlunsplit
from pathlib import Path


def make_relative_path(from_path, to_path):
    """Вернуть относительный путь от from_path к to_path"""
    from_dir = os.path.dirname(from_path)
    rel_path = os.path.relpath(to_path, start=from_dir)
    return rel_path.replace("\\", "/")  # для веб лучше слеши


def process_file(filepath, site_root):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    changed = False

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()

        # Пропускаем якоря и почту
        if href.startswith("#") or href.startswith("mailto:"):
            continue

        # Пропускаем внешние ссылки (схема в url)
        parsed = urlparse(href)
        if parsed.scheme in ["http", "https", "ftp", "tel"]:
            continue

        # Абсолютные пути (начинающиеся с /) преобразуем относительно site_root
        if href.startswith("/"):
            abs_target = os.path.join(site_root, href.lstrip("/"))
        else:
            # Относительный путь — формируем абсолютный путь от current файла
            abs_target = os.path.normpath(os.path.join(os.path.dirname(filepath), href))

        # Проверяем, существует ли файл или папка
        if not os.path.exists(abs_target):
            # Если нет, просто игнорируем замену
            continue

        # Формируем правильный относительный путь от текущего файла до цели
        new_rel = make_relative_path(filepath, abs_target)

        if new_rel != href:
            a["href"] = new_rel
            changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Обновлен файл: {filepath}")


def main():
    site_root = os.path.abspath(".")  # корень сайта (укажите при необходимости)
    for root, dirs, files in os.walk(site_root):
        for file in files:
            if file.lower().endswith(".htm"):
                full_path = os.path.join(root, file)
                try:
                    process_file(full_path, site_root)
                except Exception as e:
                    print(f"Ошибка в файле {full_path}: {e}")
                    # Не прерывать выполнение


if __name__ == "__main__":
    main()
