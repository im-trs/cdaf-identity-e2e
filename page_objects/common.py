# -*- coding: utf-8 -*-
import os
import time
from contextlib import contextmanager

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import \
    staleness_of
from selenium.webdriver.support.ui import WebDriverWait
from toolium.pageelements import PageElement, PageElements
from toolium.pageobjects.page_object import PageObject


def wait_for_seconds(value):
    value = float(value)
    time.sleep(value)


class CommonPageObject(PageObject):

    def open(self, page_name: str):
        """ Open URL in browser

        :param page_name: the name of the page to open
        :returns: this page object instance
        """
        page_name = page_name.strip().lower()
        switcher = {
            # URLs are defined in the properties.cfg
            page_name: self.config.get(page_name, 'url')
        }
        url = switcher.get(page_name, None)

        self.driver.get('{}'.format(url))

        self.logger.info("title = {}".format(self.driver.title))
        return self.driver.title

    def get_page(self, page_name: str):
        """ Return Page Object Storefront

       :returns: this page object instance
       """

        switcher = {
            # "home_page": HomePageObject,
            # "register_page": RegisterPageObject
        }
        page = switcher.get(page_name.strip().lower(), None)
        self.logger.info("title = {}".format(self.driver.title))
        return page

    def click_element(self, element_name: str, el: PageElement):
        self.logger.info("Attempting to click on the {}".format(element_name))
        self.utils.wait_until_element_clickable(el)
        self.click_page_element(el, element_name)
        return self

    def hover_element(self, element_name: str, el: PageElement):
        self.logger.info("Attempting to hover on the {}".format(element_name))
        self.utils.wait_until_element_visible(el)
        self.utils.focus_element(el)
        return self

    def scroll_to_page_element(self, element_name: str, el: PageElement):
        fast_scroll_elements = ['priced_shipping_method', 'payment_place_order', 'delivery_proceed_to_payment']
        self.logger.info("Attempting to scroll to the {}".format(element_name))
        self.utils.wait_until_element_visible(el)
        js_scroll = "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });"
        if element_name in fast_scroll_elements:
            js_scroll = "arguments[0].scrollIntoView({ behavior: 'instant', block: 'center', inline: 'center' });"
        self.utils.driver_wrapper.driver.execute_script(js_scroll, el.web_element)
        self.utils.wait_until_element_visible(el, 5)
        self.utils.wait_until_element_clickable(el, 5)
        return self

    def enter_text(self, element_name: str, el: PageElement, text: str):
        # add elements to this array if there should not be a tab pressed after text is entered
        no_tab_elements = ['search_text', 'quantity', 'payment_card_security_code']
        self.logger.info("Sending keys {} to {}".format(text, element_name))
        self.utils.wait_until_element_clickable(el).clear()

        if element_name == 'address_finder':
            os.system("echo %s| clip" % text.strip())
            os.system("echo %s| pbcopy" % text.strip())
            self.utils.wait_until_element_clickable(el).send_keys(Keys.SHIFT, Keys.INSERT)
        else:
            self.utils.wait_until_element_clickable(el).send_keys(text)

        if element_name not in no_tab_elements:
            self.utils.wait_until_element_clickable(el).send_keys(Keys.TAB)

        if element_name == 'delivery_postcode':
            self.utils.driver_wrapper.driver.execute_script("arguments[0].click();", el.web_element)
            self.wait_for_load_screen()
        return self

    def get_attribute_value(self, element_name: str, el: PageElement, attribute: str):
        self.logger.info(
            "Getting the value of attribute {} in element {}".format(attribute, element_name, attribute))
        value = self.utils.wait_until_element_visible(el).get_attribute(attribute)
        self.logger.info(
            "Value of attribute {} in element {} is {}".format(attribute, element_name, value))
        return value

    def element_is_displayed(self, element_name: str, el: PageElement):
        self.logger.info(
            "Checking if element {} is displayed".format(element_name))
        ret = self.utils.get_web_element(el).is_displayed()
        self.logger.info(
            "Element {} is displayed is {}".format(element_name, str(ret)))
        return ret

    def wait_until_element_is_displayed(self, element_name: str, el: PageElement):
        self.logger.info(
            "Checking if element {} is displayed".format(element_name))
        self.utils.wait_until_element_visible(el, 10)
        ret = self.utils.get_web_element(el).is_displayed()
        self.logger.info(
            "Element {} is displayed is {}".format(element_name, str(ret)))
        return ret

    def select_option(self, element_name: str, option: str, el: PageElement):
        self.logger.info("Selecting option {} from {}".format(option, element_name))
        option_xpath = "//option[. = '" + option + "' or @value = '" + option + "' or contains(text(), '" + option + "')]"
        # self.utils.wait_until_element_clickable(el).click()
        self.click_page_element(el, element_name)
        self.utils.get_web_element(el).find_element(By.XPATH, option_xpath).click()
        if element_name == 'basket_quantity' or element_name == 'delivery_country' or element_name == 'item_size_drop_down' or element_name == 'delivery_state':
            self.wait_for_load_screen()
        # self.utils.wait_until_element_clickable(el).click()
        self.click_page_element(el, element_name)

    def frame_switch_xpath(self, el: PageElement):
        self.logger.info("Switching frame")
        frame = self.driver.find_element_by_xpath(el.locator[1])
        self.driver.switch_to.frame(frame)

    def frame_switch_default(self):
        self.logger.info("Switching to default content")
        self.driver.switch_to.default_content()

    def switch_to_window(self, window_name='default'):
        lower_window_name = str(window_name).strip().lower()

        match lower_window_name:
            case 'default':
                self.driver.switch_to_window(self.driver.window_handles[0])
            case 'popup':
                self.driver.switch_to_window(self.driver.window_handles[1])
            case _:
                print(f'Window not found, the case may need to be added...')

    def get_find_tables(self, sub_content: str):
        tables = PageElements(By.TAG_NAME, 'table')
        for table in tables:
            attribute_value = str(self.utils.get_web_element(table).get_attribute('textContent')).strip().lower()
            self.logger.info("table text_content = {}".format(attribute_value))
            if sub_content.strip().lower() in attribute_value.strip().lower():
                return True
        return False

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.driver, timeout).until(
            staleness_of(old_page)
        )

    def click_wait_for_browser_transition(self, element_name: str, el: PageElement):
        with self.wait_for_page_load(timeout=10):
            self.click_element(element_name, el)

    def wait_element_text_wait_for_browser_transition(self, element_name: str, el: PageElement, text):
        with self.wait_for_page_load(timeout=10):
            self.wait_element_text(element_name, el, text)

    def wait_element(self, element_name: str, el: PageElement):
        self.logger.info("Checking if element {} is displayed".format(element_name))
        return self.utils.wait_until_element_visible(el)

    def wait_element_text(self, element_name: str, el: PageElement, text):
        self.logger.info(
            "Checking if element {} is displayed".format(element_name))
        el = self.utils.wait_until_element_contains_text(self.utils.get_web_element(el), text)
        if el is not None:
            self.logger.info("Successfully waited for the text value of element {} to contain {}".format(element_name,
                                                                                                         text))
            return True
        else:
            self.logger.info("Failed to waited for the text value of element {} to contain {}".format(element_name,
                                                                                                      text))

    def wait_for_query(self, jquery):
        pass

    def wait_for_load_screen(self):
        try:
            loading_screen = self.utils.driver_wrapper.driver.execute_script("return document.getElementsByClassName('local-progress')")
            self.utils.wait_until_element_visible(loading_screen, 3)
        except Exception:
            pass

        try:
            loading_screen = self.utils.driver_wrapper.driver.execute_script("return document.getElementsByClassName('local-progress')")
            self.utils.wait_until_element_not_visible(loading_screen, 4)
        except Exception:
            pass

    def click_page_element(self, el: PageElement, element_name: str):
        try:
            # Attempt to click the element
            self.utils.wait_until_element_clickable(el).click()
        except ElementClickInterceptedException:
            try:
                # If the click fails due to an intercept exception, use ActionChains to move the mouse to the element and click it
                actions = ActionChains(self.driver_wrapper.driver)
                actions.move_to_element(el.web_element).click().perform()
            except ElementClickInterceptedException:
                # If the click fails due to an intercept exception, use JavaScript to click the element
                self.utils.driver_wrapper.driver.execute_script("arguments[0].scrollIntoView();", el.web_element)
                self.utils.driver_wrapper.driver.execute_script("arguments[0].click();", el.web_element)
        return self





