from playwright.sync_api import expect

# TEST OTEVŘENÍ KONKRÉTNÍ HTTPS
def test_page_load(browser):
    page=browser.new_page()
    page.goto("https://www.knihy.cz/")
    page_logo=page.locator("#header > div.web__header > div > header > div.header__logo > a")
    expect (page).to_have_url("https://www.knihy.cz/")
    page.close()

# TEST ODSOUHLASIT COOKIES
def test_approve_cookies(page):
    page.goto("https://www.knihy.cz/")
    cookie_yes_button=page.locator("body > div.box-cookies.js-cookies-consent-bar.hidden-print > div > div.box-cookies__action > a.js-cookies-consent-button.btn.btn--small.box-cookies__action__btn.box-cookies__action__btn--accept.btn--primary")
    expect(cookie_yes_button).to_be_visible(timeout=5000)
    cookie_yes_button.click()
    expect(cookie_yes_button).not_to_be_visible(timeout=5000)

# TEST VYHLEDÁNÍ NÁZVU KNIHY ZAPSANÉHO BEZ DIAKRITIKY
def test_find_book_name(page):
    page.goto("https://www.knihy.cz/")
    search_input=page.locator("#js-search-autocomplete-input")
    search_input.fill("zatmeni")
    search_input.press("Enter")
    search_result=page.locator(".list-products-page__item__title__tag.js-list-products-item-title")
 
    assert search_result.count() > 0
    results_list = search_result.all()
    for result in results_list:
        text=result.inner_text().lower()
        # předpoklad, že text obsahuje slovo zatmění s diakritikou
        assert("zatmění") in text

# TEST OTEVŘENÍ PAGE KNIHY(vyhledání knihy s názvem Zatmění, POTVRDIT image knihy od autora Jo Nesbo)
def test_open_book_page(page):
    page.goto("https://www.knihy.cz/")
    search_input=page.locator("#js-search-autocomplete-input")
    search_input.fill("zatmeni")
    search_input.press("Enter")
    search_result=page.locator(".list-products-page__item__title__tag")

    assert search_result.count() > 0
    results_list = search_result.all()
    for result in results_list:
        if "Jo Nesbo" in results_list:
            search_result.click()
            assert search_result.to_have_url("https://www.knihy.cz/zatmeni-2/")

# TEST KNIHA JE PŘIDANÁ DO KOŠÍKU
def test_add_to_cart(page):
    page.goto("https://www.knihy.cz/zatmeni-2/")

    add_to_cart_button=page.locator("body > div.web__in > div:nth-child(2) > div > div > div > div:nth-child(2) > div.js-box-detail.box-detail > div.box-detail__info > div.js-product-detail-main-add-to-cart-wrapper.box-detail-add.box-detail__info__add > div.box-detail-add__row.box-detail-add__row--prices > div > div.box-detail-add__action > form > button")
    add_to_cart_button.click()

    pop_up_window_added_to_cart=page.locator("#js-window")
    expect(pop_up_window_added_to_cart).to_be_visible

    go_to_cart=page.locator("#js-window > div.js-window-content.window-popup__in > a")
    go_to_cart.click()
    expect(page).to_have_url("https://www.knihy.cz/kosik/")

# TEST FINÁLNÍ CENA KNIHY ODPOVÍDÁ ÚDAJI NA PAGE KNIHY I V KOŠÍKU
def test_book_price(page):
    page.goto("https://www.knihy.cz/zatmeni-2/")
    final_price="367"

    book_price_bookpage=page.locator("body > div.web__in > div:nth-child(2) > div > div > div > div:nth-child(2) > div.js-box-detail.box-detail > div.box-detail__info > div.js-product-detail-main-add-to-cart-wrapper.box-detail-add.box-detail__info__add > div.box-detail-add__row.box-detail-add__row--prices > div > div.box-detail-add__prices__item.box-detail-add__prices__item--main")
    book_price_bookpage.wait_for(state="visible", timeout=15000)
    actual_price = book_price_bookpage.inner_text()
    print(f"Price on book page: {actual_price}")
    expect(book_price_bookpage).to_contain_text(final_price, timeout=5000)
    
    add_to_cart_button=page.locator("body > div.web__in > div:nth-child(2) > div > div > div > div:nth-child(2) > div.js-box-detail.box-detail > div.box-detail__info > div.js-product-detail-main-add-to-cart-wrapper.box-detail-add.box-detail__info__add > div.box-detail-add__row.box-detail-add__row--prices > div > div.box-detail-add__action > form > button")
    add_to_cart_button.click()

    pop_up_window_added_to_cart=page.locator("#js-window")
    expect(pop_up_window_added_to_cart).to_be_visible(timeout=10000)

    go_to_cart=page.locator("#js-window > div.js-window-content.window-popup__in > a")
    go_to_cart.click()
    
    book_price_cart=page.locator("body > div.web__in.web__in--order-process > div:nth-child(2) > div > div > div > form > table > tbody > tr > td.table-cart__cell.table-cart__cell--price.js-cart-item-total-price")
    book_price_cart.wait_for(state="visible", timeout=15000)
    actual_price_cart = book_price_cart.inner_text()
    print(f"Price in cart: {actual_price_cart}")
    expect(book_price_cart).to_contain_text(final_price, timeout=10000)

# TEST ZOBRAZENÍ POLE PRO VYPLNĚNÍ SLEVOVÉHO VOUCHERU
def test_open_voucher_window(page):
    page.goto("https://www.knihy.cz/zatmeni-2/")

    add_to_cart_button=page.locator("body > div.web__in > div:nth-child(2) > div > div > div > div:nth-child(2) > div.js-box-detail.box-detail > div.box-detail__info > div.js-product-detail-main-add-to-cart-wrapper.box-detail-add.box-detail__info__add > div.box-detail-add__row.box-detail-add__row--prices > div > div.box-detail-add__action > form > button")
    add_to_cart_button.click()

    pop_up_window_added_to_cart=page.locator("#js-window")
    expect(pop_up_window_added_to_cart).to_be_visible(timeout=5000)

    go_to_cart=page.locator("#js-window > div.js-window-content.window-popup__in > a")
    go_to_cart.click()
    expect(page).to_have_url("https://www.knihy.cz/kosik/", timeout=10000)

    discout_checkbox=page.locator("#js-promo-code-box > label > input")
    discount_input_field=page.locator("#js-promo-code-box-input > input")
    expect(discount_input_field).not_to_be_visible(timeout=5000)

    discout_checkbox.click()
    expect(discount_input_field).to_be_visible(timeout=5000)

# TEST ROZBALENÍ OKNA S HODNOCENÍM E-SHOPU OD HEUREKY
def test_overeno_zakazniky(page):
    page.goto("https://www.knihy.cz/")
    overeno_element=page.locator("#heurekaTableft")
    overeno_element.hover()

    popup_heureka=page.locator("#hw-87kwowifjjowiklsadh666left")
    expect(popup_heureka).to_be_visible(timeout=5000)