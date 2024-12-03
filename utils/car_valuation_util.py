import csv
import os
import random
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CarValuationUtil:
    @staticmethod
    def read_input_file(input_file, minimum_mileage, maximum_mileage):
        """
        Reads the input file, extracts vehicle registration numbers,
        and assigns a random mileage to each.

        :param input_file: Path to the input file containing registration numbers
        :return: Dictionary with registration numbers as keys and random mileage as values
        """
        with open(input_file, 'r') as file:
            content = file.read()

        # Adjust regex to handle space-separated registrations like 'AD58 VNF'
        registrations = [reg.replace(" ", "") for reg in re.findall(r'[A-Z0-9]{2,}\s?[A-Z0-9]{3}', content)]

        # Assign random mileage to each registration
        registration_data = {reg: random.randint(minimum_mileage, maximum_mileage) for reg in registrations}

        return registration_data
