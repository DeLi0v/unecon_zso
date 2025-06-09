import os
from bs4 import BeautifulSoup
from pathlib import Path
import re

# Путь к корню сайта
site_root = Path("/путь/к/папке/с/вашими/страницами")

# Старая и новая разметка header (строки с вашим html)
old_header_start = '<header id="header">'
old_header_end = """
</svg></i><a href="tel:88003508983" rel="nofollow">8-800-350-89-83</a>
                    </div>
                    <!-- /noindex -->
                  </div>
                </div>
              </div>
            </div>
          </div>
          """

new_header_html = """
<header id="header">
        <div class="header-wrapper header-v7">
          <div class="logo_and_menu-row header__top-part">
            <div class="maxwidth-theme logo-row">
              <div class="header__top-inner">
                <a href="index.htm" style="display: flex;
                    align-items: center;
                    text-decoration: none;">
                  <div class="logo-block floated header__top-item">
                    <div class="line-block line-block--16">
                      <div class="logo line-block__item no-shrinked">
                        <img alt="ЗСОмаркет" data-src="upload/CMax/7de/a5zzzr7oxd95dux98mdxu5xoycjlquue.png"
                          src="upload/CMax/7de/a5zzzr7oxd95dux98mdxu5xoycjlquue.png" title="ЗСОмаркет" />
                      </div>
                    </div>
                  </div>
                  <div class="header__top-item">
                    <div class="float_wrapper">
                      <div class="hidden-sm hidden-xs">
                        <div class="top-description addr">
                          Медицинские товары от производителя
                        </div>
                      </div>
                    </div>
                  </div>
                </a>
                <div class="header__top-item flex1 fix-block">
                  <div class="search_wrap">
                    <div class="search-block inner-table-block">
                      <div class="search-wrapper">
                        <div id="title-search_fixed">
                          <form action="/catalog/" class="search">
                            <div class="search-input-div">
                              <input autocomplete="off" class="search-input" style="z-index: 1;"
                                id="title-search-input_fixed" maxlength="50" name="q" placeholder="ПОИСК" size="20"
                                type="text" value="" />
                            </div>
                            <div class="search-button-div" style="z-index: 2;">
                              <button class="btn btn-search" name="s" type="submit" value="Найти">
                                <i aria-hidden="true" class="svg search2 inline"><svg height="17" width="17">
                                    <use
                                      xlink:href="bitrix/templates/aspro_max/images/svg/header_icons_srite.svg#search">
                                    </use>
                                  </svg></i>
                              </button>
                              <span class="close-block inline-search-hide"><i aria-hidden="true"
                                  class="svg inline svg-inline-search svg-close close-icons colored_theme_hover"><svg
                                    height="16" viewbox="0 0 16 16" width="16" xmlns="http://www.w3.org/2000/svg">
                                    <path class="cccls-1"
                                      d="M334.411,138l6.3,6.3a1,1,0,0,1,0,1.414,0.992,0.992,0,0,1-1.408,0l-6.3-6.306-6.3,6.306a1,1,0,0,1-1.409-1.414l6.3-6.3-6.293-6.3a1,1,0,0,1,1.409-1.414l6.3,6.3,6.3-6.3A1,1,0,0,1,340.7,131.7Z"
                                      data-name="Rounded Rectangle 114 copy 3" transform="translate(-325 -130)"></path>
                                  </svg></i></span>
                            </div>
                          </form>
                        </div>
                      </div>
                      <script>
                        var jsControl = new JCTitleSearch4({
                          //'WAIT_IMAGE': '/bitrix/themes/.default/images/wait.gif',
                          AJAX_PAGE: "/",
                          CONTAINER_ID: "title-search_fixed",
                          INPUT_ID: "title-search-input_fixed",
                          INPUT_ID_TMP: "title-search-input_fixed",
                          MIN_QUERY_LEN: 2,
                        });
                      </script>
                    </div>
                  </div>
                </div>
                <div class="phone-block icons">
                  <div class="inline-block">
                    <!-- noindex -->
                    <div class="phone with_dropdown">
                      <i aria-hidden="true" class="svg svg-inline-phone inline"><svg height="13" width="5">
                          <use xlink:href="bitrix/templates/aspro_max/images/svg/header_icons_srite.svg#phone_black">
                          </use>
                        </svg></i><a href="tel:88003508983" rel="nofollow">8-800-350-89-83</a>
                    </div>
                    <!-- /noindex -->
                  </div>
                </div>
                <div class="line-block line-block--40 line-block--40-1200">
                  <div class="right-icons wb line-block__item header__top-item">
                    <div class="line-block line-block--40 line-block--40-1200">
                      <!--'start_frame_cache_header-basket-with-compare-block1'-->
                      <!-- noindex -->
                      <div class="wrap_icon wrap_basket baskets line-block__item top_basket">
                        <a class="basket-link basket big" href="basket/index.htm" rel="nofollow" title="Корзина пуста">
                          <span class="js-basket-block">
                            <i aria-hidden="true" class="svg basket big inline"><svg height="16" width="19">
                                <use xlink:href="bitrix/templates/aspro_max/images/svg/header_icons_srite.svg#basket">
                                </use>
                              </svg></i>
                            <span class="title dark_link">Корзина</span>
                            <span class="count">0</span>
                          </span>
                        </a>
                        <span class="basket_hover_block loading_block loading_block_content"></span>
                      </div>
                      <!-- /noindex -->
                      <!--'end_frame_cache_header-basket-with-compare-block1'-->
                    </div>
                  </div>
                  <div class="line-block__item no-shrinked">
                    <div class="show-fixed top-ctrl">
                      <div class="personal_wrap">
                        <div class="wrap_icon inner-table-block person">
                          <!--'start_frame_cache_header-auth-block2'-->
                          <!-- noindex -->
                          <div class="auth_wr_inner">
                            <a class="personal-link dark-color" href="auth/index.htm" rel="nofollow"
                              title="Мой кабинет"><i aria-hidden="true" class="svg svg-inline-cabinet big inline"><svg
                                  height="18" width="18">
                                  <use xlink:href="bitrix/templates/aspro_max/images/svg/header_icons_srite.svg#user">
                                  </use>
                                </svg></i><span class="wrap"><span class="name">Войти</span></span></a>
                          </div>
                          <!-- /noindex -->
                          <!--'end_frame_cache_header-auth-block2'-->
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
"""


def is_relative_url(url):
    if not url:
        return False
    # Относительные, если не начинаются с http://, https://, / (корень), mailto:, tel:, # и др.
    return not re.match(r"^(?:https?:|mailto:|tel:|/|#)", url)


def fix_relative_url(base_path: Path, url: str) -> str:
    # base_path — путь к html-файлу
    # url — относительный путь из header
    # Нужно преобразовать url так, чтобы он был правильным относительно base_path
    target_path = (site_root / url).resolve()
    try:
        # получить относительный путь от base_path.parent к target_path
        relative_path = os.path.relpath(target_path, base_path.parent)
        return relative_path.replace("\\", "/")  # на всякий случай заменить \ на /
    except Exception:
        return url  # если что-то не так — вернуть как есть


for html_file in site_root.rglob("*.htm*"):  # найти все .htm и .html
    print(f"Обрабатываю: {html_file}")
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Заменяем старый header новым — для надёжности можно через BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    old_header = soup.find("header", {"id": "header"})
    if not old_header:
        print(f"header не найден в {html_file}")
        continue

    # Вставляем новый header как BeautifulSoup-объект
    new_header_soup = BeautifulSoup(new_header_html, "html.parser").find(
        "header", {"id": "header"}
    )
    if not new_header_soup:
        print("Ошибка: новый header не найден в html строке")
        break

    # Исправляем относительные ссылки в новом header-е
    for tag in new_header_soup.find_all(src=True):
        url = tag["src"]
        if is_relative_url(url):
            tag["src"] = fix_relative_url(html_file, url)

    for tag in new_header_soup.find_all(href=True):
        url = tag["href"]
        if is_relative_url(url):
            tag["href"] = fix_relative_url(html_file, url)

    # Тоже для data-src и других атрибутов, если нужно
    for tag in new_header_soup.find_all(attrs={"data-src": True}):
        url = tag["data-src"]
        if is_relative_url(url):
            tag["data-src"] = fix_relative_url(html_file, url)

    # Заменяем старый header на новый
    old_header.replace_with(new_header_soup)

    # Записываем обратно
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

print("Готово!")
