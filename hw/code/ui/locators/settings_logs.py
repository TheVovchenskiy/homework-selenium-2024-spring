from selenium.webdriver.common.by import By


class SettingsLogsPageLocators:
    TAB_ITEM = (By.ID, 'tab-settings.logs')

    FILTER_BUTTON = (By.XPATH, '//*[@data-testid="filter-button"]')

    @staticmethod
    def filter_section_button(text: str):
        return (By.XPATH, f'//button[span[span[span[contains(text(), "{text}")]]]]')

    FILTER_MODAL = (By.XPATH, '//div[@data-popper-reference-hidden and @data-popper-escaped and @data-popper-placement and @data-popper-interactive]')

    SEARCH_FILTER_INPUT = (By.XPATH, './/input[@type="search"]')

    OBJECT_TYPE_BUTTON = filter_section_button('Тип объекта')
    WHAT_CHANGED_BUTTON = filter_section_button('Что изменилось')
    CHANGE_AUTHOR_BUTTON = filter_section_button('Автор изменения')

    CHECKBOX = (By.XPATH, '//input[@type="checkbox"]')
    CHECKBOX_BUTTON = (By.XPATH, CHECKBOX[1] + '/../..')

    @staticmethod
    def modal_button(text: str):
        return (By.XPATH, f'//button[span[span[contains(text(), "{text}")]]]')

    SELECT_ALL_BUTTON = modal_button('Выбрать все')
    RESET_BUTTON = modal_button('Сбросить')
    RESET_ALL_BUTTON = modal_button('Сбросить все')

    SAVE_BUTTON = modal_button('Применить')
    CANCEL_BUTTON = modal_button('Отмена')
    
