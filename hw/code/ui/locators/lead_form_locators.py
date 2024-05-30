from selenium.webdriver.common.by import By

from ui.locators.base_locators import Locator, locator_xpath_parent


class LeadFormLocators:
    CREATE_BUTTON = (By.XPATH, '//*[@test-id="create-leadform-button"]')

    LEAD_FORM_LIST_ITEM = (By.XPATH, '//div[@data-entityid]')

    def LEAD_FORM_ITEM_NAME(name: str) -> Locator:
        return (By.XPATH, f'//button[text()="{name}"]')
    
    def LEAD_FORM_ITEM_DELETE_BUTTON(name: str) -> Locator:
        return (By.XPATH, f'//button[text()="{name}"]/..//button[span/text()="Удалить"]')
    
    def LEAD_FORM_ITEM_EDIT_BUTTON(name: str) -> Locator:
        return (By.XPATH, f'//button[text()="{name}"]/..//button[span/text()="Редактировать"]')
    
    DELETE_LEAD_FORM_BUTTON = (By.XPATH, '//button[span/span/text()="Удалить"]')
    CANCEL_DELETE_LEAD_FORM_BUTTON = (By.XPATH, '//button[span/span/text()="Отменить"]')

    MODAL = (By.XPATH, '//div[contains(@class, "ModalRoot_componentWrapper")]')

    SUBMIT_BUTTON = (By.XPATH, '//*[@data-testid="submit"]')
    CANCEL_BUTTON = (By.XPATH, '//*[@data-testid="cancel"]')

    ERROR_MESSAGE = (By.XPATH, './/span[@role="alert"]')

    def PREVIEW_TAG(tag: str, text: str) -> Locator:
        return (By.XPATH, f'//{tag}[text()="{text}"]')

    # First step
    LID_FORM_NAME_INPUT = (By.XPATH, '//input[@placeholder="Название лид-формы"]')
    LID_FORM_NAME_BLOCK = (By.XPATH, '//input[@placeholder="Название лид-формы"]/../..')
    
    ADD_LOGO_BUTTON = (By.XPATH, '//*[@data-testid="set-global-image"]')
    ADD_LOGO_BLOCK = (By.XPATH, '//*[@data-testid="set-global-image"]/..')

    MEDIA_HEADER = (By.XPATH, '//h2[text()="Медиатека"]')
    FILE_INPUT = (By.XPATH, '//input[@type="file"]')

    FILE_ERROR_BANNER = (By.XPATH, '//div[contains(@class, "ErrorBanner_container")]')
    FAILED_TO_LOAD_FILES_ERROR = (By.XPATH, '//div[text()="Не удалось загрузить файлы"]')
    LOGO_ITEM = (By.XPATH, '//div[contains(@class, "ImageItems_imageItem")]')

    LOGO_PREVIEW = (By.XPATH, '//*[contains(@class, "Preview_activeLogoWrap")]')
    LOGO_RIGHT_PREVIEW = (By.XPATH, '//img[@alt="Название компании"]')
    CHANGE_LOGO_BUTTON = (By.XPATH, '//*[@data-testid="change-image"]')
    CROP_LOGO_BUTTON = (By.XPATH, '//*[@data-testid="crop-image"]')

    COMPANY_NAME_INPUT = (By.XPATH, '//input[@placeholder="Название компании"]')
    COMPANY_NAME_BLOCK = (By.XPATH, '//input[@placeholder="Название компании"]/../..')

    # Compact
    COMPACT_LABEL = (By.XPATH, '//input[@value="compact"]/..')
    HEADER_TEXT_INPUT = (By.XPATH, '//input[@placeholder="Текст заголовка"]')
    HEADER_TEXT_BLOCK = (By.XPATH, '//input[@placeholder="Текст заголовка"]/../..')
    SHORT_DESCRIPTION_INPUT = (By.XPATH, '//input[@placeholder="Краткое описание опроса"]')
    SHORT_DESCRIPTION_BLOCK = (By.XPATH, '//input[@placeholder="Краткое описание опроса"]/../..')

    # Long text
    LONG_TEXT_LABEL = (By.XPATH, '//input[@value="long_text"]/..')
    LONG_DESCRIPTION_INPUT = (By.XPATH, '//textarea[@placeholder="Расскажите о вашем опросе или предложении"]')
    LONG_DESCRIPTION_BLOCK = (By.XPATH, '//textarea[@placeholder="Расскажите о вашем опросе или предложении"]/../..')

    # Award
    AWARD_LABEL = (By.XPATH, '//input[@value="award"]/..')

    DISCOUNT_RADIOBUTTON = (By.XPATH, '//input[@value="discount"]')
    DISCOUNT_BUTTON = (By.XPATH, '//input[@value="discount"]/..')

    DISCOUNT_VALUE_BLOCK = (By.XPATH, '//h5[text()="Размер скидки"]/..')
    DISCOUNT_VALUE_INPUT = (By.XPATH, '//h5[text()="Размер скидки"]/../div/span/input')

    MONEY_DISCOUNT_BUTTON = (By.XPATH, '//input[@value="money"]/..')
    MONEY_DISCOUNT_INPUT = (By.XPATH, '//input[@value="money"]')
    PERCENT_DISCOUNT_BUTTON = (By.XPATH, '//input[@value="percent"]/..')
    PERCENT_DISCOUNT_INPUT = (By.XPATH, '//input[@value="percent"]')

    BONUS_RADIOBUTTON = (By.XPATH, '//input[@value="bonus"]')
    BONUS_BUTTON = (By.XPATH, '//input[@value="bonus"]/..')
    BONUS_VALUE_INPUT = (By.XPATH, '//input[@placeholder="Бонус"]')
    BONUS_VALUE_BLOCK = (By.XPATH, '//input[@placeholder="Бонус"]/../..')

    ACTIVE_COLOR = (By.XPATH, '//div[contains(@class, "GradientSelector_roundActive")]')
    STYLE_RED = (By.XPATH, '//*[@data-id="0"]')

    SET_MAIN_IMAGE_BUTTON = (By.XPATH, '//*[@data-testid="set-main-image"]')

    # Second step
    ADD_QUESTION_BUTTON = (By.XPATH, '//span[contains(text(), "Добавить вопрос")]/../..')

    def QUESTIONS_CONTAINER(question_num: int) -> Locator:
        return (By.XPATH, f'//div[contains(text(), "Вопрос № {question_num}")]/../../..')
    
    def REMOVE_QUESTION_BUTTON(question_num: int) -> Locator:
        return (By.XPATH, f'//div[div/text()="Вопрос № {question_num}"]/div/button[@aria-label="Remove"]')
    
    def QUESTIONS_ERROR_ICON(question_num: int) -> Locator:
        return (By.XPATH, f'//div[contains(text(), "Вопрос № {question_num}")]/div[contains(@class, "Question_errorIconWrap")]')

    QUESTION_TEXT = (By.XPATH, '//textarea[@placeholder="Напишите вопрос"]')
    QUESTION_TYPE_BUTTON = (By.XPATH, '//div[contains(text(), "Выбор одного ответа")]')

    QUESTION_TYPE_FLOATING_TOOLTIP = (By.XPATH, '//div[contains(@id, "floating-ui-") and @role="tooltip"]')
    ONE_ANSWER_BUTTON = (By.XPATH, '//span[contains(text(), "Выбор одного ответа")]/../../..')
    MULTIPLE_ANSWER_BUTTON = (By.XPATH, '//span[contains(text(), "Выбор нескольких ответов")]/../../..')
    FREE_FORM_ANSWER_BUTTON = (By.XPATH, '//span[contains(text(), "Ответ в произвольной форме")]/../../..')

    ANSWER_INPUT = (By.XPATH, '//input[@placeholder="Введите ответ"]')
    ANSWER_REMOVE = (By.XPATH, '//div[@class="Answer_answer__t-JwF"]/button[@aria-label="Remove"]')

    ADD_ANSWER_BUTTON = (By.XPATH, '//button[span/span/text()="Добавить ответ"]')
    ANSWER_HINT_BUTTON = (By.XPATH, '//div[@class="Hint_hintTrigger__ixYRu"]/button')
    ANSWER_HINT_TOOLTIP = (By.XPATH, '//div[contains(@class, "Tooltip_tooltipContainer__P1b-O") and div[@role="list"]]')
    ANSWER_HINT_ITEM = (By.CLASS_NAME, 'vkuiCell')

    CONTACT_INFO_CONTAINER = (By.XPATH, '//div[h4/text()="Контактная информация"]/div/div[@data-rbd-droppable-id="droppable"]')
    ADD_CONTACT_INFO_BUTTON = (By.XPATH, '//button[contains(@class, "Questions_addContactFieldsBtn")]')

    FIRST_NAME_DELETE_BUTTON = (By.XPATH, '//button[@data-id="first_name" and @aria-label="Delete"]')
    LAST_NAME_DELETE_BUTTON = (By.XPATH, '//button[@data-id="last_name" and @aria-label="Delete"]')
    EMAIL_DELETE_BUTTON = (By.XPATH, '//button[@data-id="email" and @aria-label="Delete"]')
    PHONE_DELETE_BUTTON = (By.XPATH, '//button[@data-id="phone" and @aria-label="Delete"]')
    SOCIAL_MEDIA_PROFILE_DELETE_BUTTON = (By.XPATH, '//button[@data-id="social_media_profile" and @aria-label="Delete"]')
    AGE_DELETE_BUTTON = (By.XPATH, '//button[@data-id="age" and @aria-label="Delete"]')
    BIRTH_DATE_DELETE_BUTTON = (By.XPATH, '//button[@data-id="birth_date" and @aria-label="Delete"]')
    COUNTRY_DELETE_BUTTON = (By.XPATH, '//button[@data-id="country" and @aria-label="Delete"]')
    CITY_DELETE_BUTTON = (By.XPATH, '//button[@data-id="city" and @aria-label="Delete"]')

    CONTACT_INFO_MODAL = (By.XPATH, '//div[contains(@id, "_modal_") and @aria-labelledby]')

    FIRST_NAME_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and @value="first_name"]')
    LAST_NAME_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and @value="last_name"]')
    EMAIL_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and @value="email"]')
    PHONE_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and @value="phone"]')
    SOCIAL_MEDIA_PROFILE_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and @value="social_media_profile"]')
    AGE_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and @value="age"]')
    BIRTH_DATE_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and @value="birth_date"]')
    COUNTRY_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and @value="country"]')
    CITY_CHECKBOX = (By.XPATH, '//input[@type="checkbox" and @value="city"]')

    FIRST_NAME_BUTTON = (By.XPATH, '//input[@type="checkbox" and @value="first_name"]/..')
    LAST_NAME_BUTTON = (By.XPATH, '//input[@type="checkbox" and @value="last_name"]/..')
    EMAIL_BUTTON = (By.XPATH, '//input[@type="checkbox" and @value="email"]/..')
    PHONE_BUTTON = (By.XPATH, '//input[@type="checkbox" and @value="phone"]/..')
    SOCIAL_MEDIA_PROFILE_BUTTON = (By.XPATH, '//input[@type="checkbox" and @value="social_media_profile"]/..')
    AGE_BUTTON = (By.XPATH, '//input[@type="checkbox" and @value="age"]/..')
    BIRTH_DATE_BUTTON = (By.XPATH, '//input[@type="checkbox" and @value="birth_date"]/..')
    COUNTRY_BUTTON = (By.XPATH, '//input[@type="checkbox" and @value="country"]/..')
    CITY_BUTTON = (By.XPATH, '//input[@type="checkbox" and @value="city"]/..')

    SUBMIT_ADD_CONTACT_INFO_BUTTON = (By.XPATH, '//button[span/span/text()="Добавить"]')

    ERROR_BANNER = (By.XPATH, '//p[text()="Минимальное количество полей: 1"]')

    # Third step
    HEADER_BLOCK = (By.XPATH, '//h5[text()="Заголовок"]/..')
    HEADER_INPUT = (By.XPATH, '//h5[text()="Заголовок"]/../span/input')
    DESCRIPTION_BLOCK = (By.XPATH, '//h5[text()="Описание"]/..')
    DESCRIPTION_INPUT = (By.XPATH, '//h5[text()="Описание"]/../span/input')

    ADD_SITE_BUTTON = (By.XPATH, '//div[@role="button" and @data-testid="add-site-btn"]')
    SITE_BLOCK = (By.XPATH, '//div[@placeholder="Введите ссылку на сайт"]')
    SITE_INPUT = (By.XPATH, '//div[@placeholder="Введите ссылку на сайт"]/span/input')

    ADD_PHONE_BUTTON = (By.XPATH, '//div[@role="button" and @data-testid="add-phone-btn"]')
    PHONE_INPUT = (By.XPATH, '//input[@placeholder="+7......"]')
    PHONE_BLOCK = (By.XPATH, '//input[@placeholder="+7......"]/../..')

    ADD_PROMO_CODE_BUTTON = (By.XPATH, '//div[@role="button" and @data-testid="add-promo-code-btn"]')
    PROMO_CODE_INPUT = (By.XPATH, '//input[@placeholder="Введите промокод"]')
    PROMO_CODE_BLOCK = (By.XPATH, '//input[@placeholder="Введите промокод"]/../..')

    # Fourth step
    NOTIFY_EMAIL_CHECKBOX = (By.XPATH, '//span[text()="Уведомлять о новых заявках по email"]/../../../input[@type="checkbox"]')
    NOTIFY_EMAIL_BUTTON = (By.XPATH, '//span[text()="Уведомлять о новых заявках по email"]/../../../input[@type="checkbox"]/..')
    EMAILS_INPUT = (By.XPATH, '//input[@placeholder="email@example.com"]')
    EMAILS_BLOCK = (By.XPATH, '//input[@placeholder="email@example.com"]/../..')

    NOTIFY_MESSENGER_CHECKBOX = (By.XPATH, '//span[text()="Уведомлять о новых заявках в VK Messenger"]/../../../input[@type="checkbox"]')
    NOTIFY_MESSENGER_BUTTON = (By.XPATH, '//span[text()="Уведомлять о новых заявках в VK Messenger"]/../../../input[@type="checkbox"]/..')

    NAME_INPUT = (By.XPATH, '//input[@placeholder="Введите фамилию, имя и отчество"]')
    NAME_BLOCK = (By.XPATH, '//input[@placeholder="Введите фамилию, имя и отчество"]/../..')

    ADDRESS_INPUT = (By.XPATH, '//input[@placeholder="Введите адрес"]')
    ADDRESS_BLOCK = (By.XPATH, '//input[@placeholder="Введите адрес"]/../..')

    EMAIL_INPUT = (By.XPATH, '//input[@placeholder="Введите email"]')
    EMAIL_BLOCK = (By.XPATH, '//input[@placeholder="Введите email"]/../..')

    INN_INPUT = (By.XPATH, '//input[@placeholder="Введите ИНН"]')
    INN_BLOCK = (By.XPATH, '//input[@placeholder="Введите ИНН"]/../..')
