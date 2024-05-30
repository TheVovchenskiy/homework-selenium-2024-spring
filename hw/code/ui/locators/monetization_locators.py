from selenium.webdriver.common.by import By

class MonetizationPageLocators:
    TOP = (By.XPATH, '//*[contains(@class, "PartnerContent_top__")]')

    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, '//*[contains(@class, "PartnerContent_headerButton__")]')
    HELP_BUTTON = (By.XPATH, '//*[contains(@class, "PartnerContent_headerButtonSecondary__")]')

    FOR_SITES_BUTTON = (By.XPATH, '//button[contains(text(), "Для сайтов")]')
    FOR_APPLICATIONS_BUTTON = (By.XPATH, '//button[contains(text(), "Для приложений")]')

    BANNER_ITEM = (By.XPATH, '//*[@src="https://r.mradx.net/cms/D5/219C16.svg"]')
    INSTREAM_ITEM = (By.XPATH, '//*[@src="https://r.mradx.net/cms/93/626CF5.svg"]')
    ADAPTIVE_BLOCK_ITEM = (By.XPATH, '//*[@src="https://r.mradx.net/cms/49/C5EF6A.svg"]')
    INPAGE_ITEM = (By.XPATH, '//*[@src="https://r.mradx.net/cms/93/626CF5.svg"]')
    FULLSCREEN_ITEM = (By.XPATH, '//*[@src="https://r.mradx.net/cms/5F/70FCED.svg"]')
    STICKY_BANNER_ITEM = (By.XPATH, '//*[@src="https://r.mradx.net/cms/92/F817FC.svg"]')
    FOR_SITE_ITEMS = [BANNER_ITEM, INSTREAM_ITEM, ADAPTIVE_BLOCK_ITEM, INPAGE_ITEM, FULLSCREEN_ITEM, STICKY_BANNER_ITEM]


    MOBILE_BANNER_ITEM = (By.XPATH, '//*[@src="https://r.mradx.net/cms/A8/6A359F.svg"]')
    NATIVE_FORMAT_ITEM = (By.XPATH, '//*[@src="https://r.mradx.net/cms/F8/D78B3C.svg"]')
    MOBILE_FULLSCREEN_ITEM = (By.XPATH, '//*[@src="https://r.mradx.net/cms/A1/1D1E28.svg"]')
    VIDEO_FOR_REWARD_ITEM = (By.XPATH, '//*[@src="https://r.mradx.net/cms/88/C08D6E.svg"]')
    FOR_APPLICATIONS_ITEMS = [MOBILE_BANNER_ITEM, NATIVE_FORMAT_ITEM, MOBILE_FULLSCREEN_ITEM, VIDEO_FOR_REWARD_ITEM]

    PERSONAL_ACCOUNT_BUTTON_2 = (By.XPATH, '//*[contains(@class, "CallToAction_button__")]')

    NAME_INPUT = (By.XPATH, '//*[@id="name"]')
    EMAIL_INPUT = (By.XPATH, '//*[@id="email"]')
    COMPANY_INPUT = (By.XPATH, '//*[@id="company"]')
    POSITION_INPUT = (By.XPATH, '//*[@id="position"]')
    COMMENT_INPUT = (By.XPATH, '//*[@id="comment"]')

    SEND_FEEDBACK_BUTTON = (By.XPATH, '//*[contains(@class, "Form_button__")]')

    SUCCESS_FORM = (By.XPATH, '//*[contains(@class, "Form_success__")]')