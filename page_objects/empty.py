# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By
from toolium.pageelements import PageElement
from toolium.pageobjects.page_object import PageObject


class EmptyPageObject(PageObject):

    a_page_element = None

    def init_page_elements(self):
        self.a_page_element = PageElement(By.ID, "page_element", wait=True)

    def get_element(self, element_name, text=""):

        switcher = {
            "a_page_element": self.a_page_element
        }

        el = switcher.get(element_name, None)

        if el is None:
            self.logger.error('Element "{}" is undefined'.format(element_name))
        else:
            return el
