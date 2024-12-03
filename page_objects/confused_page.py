# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from toolium.pageelements import Button, InputText, Text, Link
from toolium.pageobjects.page_object import PageObject


class ConfusedPage(PageObject):

    def init_page_elements(self):
        pass

    def get_element(self, element_name, text=""):
        switcher = {
            "cookies": Button(By.ID, "button-save-all", wait=True),
            "hero_product_car_insurance": InputText(By.CSS_SELECTOR, 'a[data-ga-click-label="hero-product-Car-insurance-Primary-GAQ"]', wait=True),
            "registration-number-input": InputText(By.ID, "registration-number-input", wait=True),
            "find-vehicle-btn": Button(By.ID, "find-vehicle-btn", wait=True),
            "registration-lookup-summary-title": Link(By.ID, "registration-lookup-summary-title", wait=True),
            "car_details": Text(By.XPATH, "//div[@class='panel']", wait=True),
            "error-summary__heading": Text(By.CSS_SELECTOR, "h3[class='error-summary__heading']", wait=True),
        }

        el = switcher.get(element_name, None)

        if el is None:
            self.logger.error('Element "{}" is undefined'.format(element_name))
        else:
            return el
