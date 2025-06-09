import os
from pathlib import Path
from bs4 import BeautifulSoup

# Корневая папка сайта, откуда считаем абсолютные пути
SITE_ROOT = Path(r"D:\on deskort\Ден\ВУЗ\Помощь\ВКР Елюкина").resolve()

# CSS-селектор для навигационной панели — подкорректируйте, если надо
NAV_SELECTOR = ".menu-row"


def fix_nav_links(file_path: Path, site_root: Path, nav_selector: str):
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Не удалось прочитать файл {file_path}: {e}")
        return

    soup = BeautifulSoup(content, "html.parser")

    nav = soup.select_one(nav_selector)
    if not nav:
        print(
            f"Навигационная панель с селектором '{nav_selector}' не найдена в {file_path}"
        )
        return

    # Путь папки, где лежит текущий файл
    current_dir = file_path.parent

    # Обрабатываем все ссылки внутри навигации
    links = nav.find_all("a", href=True)
    for link in links:
        href = link["href"].strip()
        if (
            not href
            or href.startswith("#")
            or href.startswith("mailto:")
            or href.startswith("tel:")
        ):
            continue  # пропускаем якоря и почту/телефон

        # Определим абсолютный путь целевой страницы относительно корня сайта
        target_path = (current_dir / href).resolve()

        # Проверяем, что целевой путь в пределах сайта, иначе не меняем
        try:
            target_path.relative_to(site_root)
        except ValueError:
            # Вне сайта, возможно абсолютная ссылка или внешняя - пропускаем
            continue

        # Считаем относительный путь от current_dir до target_path
        rel_path = os.path.relpath(target_path, current_dir)

        # Заменяем ссылку на обновлённый относительный путь с нормализацией
        rel_path = rel_path.replace("\\", "/")  # для URL всегда слэши

        link["href"] = rel_path

    # Записываем обратно в файл
    try:
        file_path.write_text(str(soup), encoding="utf-8")
        print(f"Обновлены ссылки в {file_path}")
    except Exception as e:
        print(f"Не удалось записать файл {file_path}: {e}")


def main():
    for root, dirs, files in os.walk(SITE_ROOT):
        for file in files:
            if file.lower().endswith(".htm"):  # только .htm файлы
                full_path = Path(root) / file
                try:
                    fix_nav_links(full_path, SITE_ROOT, NAV_SELECTOR)
                except Exception as e:
                    print(f"Ошибка при обработке {full_path}: {e}")


if __name__ == "__main__":
    main()
