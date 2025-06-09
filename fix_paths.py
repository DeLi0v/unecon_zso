import os
import re
from bs4 import BeautifulSoup

SITE_DIR = "."  # корень сайта с файлами


def make_relative_path(from_path, to_path):
    from_dir = os.path.dirname(from_path)
    rel_path = os.path.relpath(to_path, start=from_dir)
    return rel_path.replace("\\", "/")


def update_nav_links_in_file(file_path, site_root_abs):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")

    navs = soup.find_all(
        "nav"
    )  # Можно изменить на soup.select('.nav') если навигация по классу
    if not navs:
        return False

    changed = False
    for nav in navs:
        links = nav.find_all("a", href=True)
        for a in links:
            href = a["href"].strip()
            # Если ссылка абсолютная (http:// или https://), пропускаем
            if (
                href.startswith("http://")
                or href.startswith("https://")
                or href.startswith("#")
                or href.startswith("mailto:")
            ):
                continue
            # Если ссылка абсолютная от корня сайта (начинается с /), то её нужно поправить на относительный путь
            if href.startswith("/"):
                abs_target = os.path.join(site_root_abs, href.lstrip("/"))
            else:
                # относительная ссылка, считаем абсолютный путь от текущ файла
                abs_target = os.path.normpath(
                    os.path.join(os.path.dirname(file_path), href)
                )

            # Теперь надо вычислить правильный относительный путь от текущего файла до abs_target
            new_rel = make_relative_path(file_path, abs_target)
            if new_rel != href:
                a["href"] = new_rel
                changed = True

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print(f"Обновлены ссылки навигации в файле: {file_path}")
    return changed


def main():
    # Абсолютный путь к корню сайта
    site_root_abs = os.path.abspath(SITE_DIR)
    for root, dirs, files in os.walk(SITE_DIR):
        for file in files:
            if file.endswith((".html", ".htm", ".php")):
                full_path = os.path.abspath(os.path.join(root, file))
                update_nav_links_in_file(full_path, site_root_abs)


if __name__ == "__main__":
    main()
