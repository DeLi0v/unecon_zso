import os
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import unquote

ROOT_DIR = "."  # корневая папка с html-файлами


def resolve_path(base_file, href):
    """Абсолютный путь к ресурсу по ссылке относительно текущего HTML-файла"""
    href_clean = href.split("?")[0].split("#")[0]
    return (base_file.parent / href_clean).resolve()


def file_exists(path):
    return path.is_file()


def is_in_logo_or_breadcrumbs(tag):
    """Проверяет, находится ли ссылка внутри логотипа или хлебных крошек"""
    for parent in tag.parents:
        if parent.has_attr("class"):
            cls = parent["class"]
            if "logo" in cls or "breadcrumbs__link" in cls:
                return True
    return False


def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    changed = False

    for a in soup.find_all("a", href=True):
        if is_in_logo_or_breadcrumbs(a):
            continue

        href = unquote(a["href"])

        if href.startswith(("http://", "https://", "//", "#", "mailto:", "tel:")):
            continue

        original_path = resolve_path(file_path, href)

        if not file_exists(original_path):
            cleaned_href = href.lstrip("../").lstrip("/")
            local_path = file_path.parent / cleaned_href

            if file_exists(local_path):
                print(
                    f"[+] {file_path.relative_to(ROOT_DIR)}: исправлена ссылка {href} → {cleaned_href}"
                )
                a["href"] = cleaned_href
                changed = True

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        return True
    return False


def main():
    fixed_count = 0
    for root, _, files in os.walk(ROOT_DIR):
        for name in files:
            if name.endswith((".htm", ".html")):
                path = Path(root) / name
                if process_file(path):
                    fixed_count += 1
    print(f"\n✅ Готово. Исправлено файлов: {fixed_count}")


if __name__ == "__main__":
    main()
