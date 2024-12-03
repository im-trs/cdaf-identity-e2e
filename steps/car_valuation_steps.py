import csv
import random
import re
from difflib import SequenceMatcher

from behave import given, when, then

from steps.common_ui_steps import __enter_text_check_value
from steps.mapping import get_element


def is_similar(expected, actual, threshold=0.8):
    """
    Checks if two strings are similar based on a given threshold.

    :param expected: The expected string.
    :param actual: The actual string.
    :param threshold: A float value representing similarity (0 to 1).
    :return: Boolean indicating if the strings are similar enough.
    """
    return SequenceMatcher(None, expected, actual).ratio() >= threshold


@given('the system reads the input file "{input_file}" with mileage range {minimum_mileage} to {maximum_mileage}')
def step_read_input_file_with_mileage_range(context, input_file, minimum_mileage, maximum_mileage):
    """
    Reads the input file, extracts registration numbers, and assigns random mileage within the specified range.

    :param context: Behave context object
    :param input_file: Path to the input file
    :param minimum_mileage: Minimum mileage value (string with quotes)
    :param maximum_mileage: Maximum mileage value (string with quotes)
    """
    try:
        # Strip quotes and convert mileage strings to integers
        min_mileage = int(minimum_mileage.strip('"').replace(",", ""))
        max_mileage = int(maximum_mileage.strip('"').replace(",", ""))

        # Read the input file and assign random mileage
        context.input_data = read_input_file(input_file, min_mileage, max_mileage)
        context.registration_numbers = list(context.input_data.keys())
        print(f"Input data with mileage range loaded: {context.input_data}")
        print(f"Registration numbers: {context.registration_numbers}")
    except Exception as e:
        raise AssertionError(f"Error reading input file or assigning mileage: {e}")


@then('for each registration in the input file:')
def step_for_each_registration(context):
    """
    Iterates through each registration number and executes steps for each one.

    :param context: Behave context object
    """
    if not hasattr(context, "registration_numbers") or not context.registration_numbers:
        raise ValueError("No registration numbers found in context. Ensure input file is read correctly.")

    for registration in context.registration_numbers:
        context.current_registration = registration.strip()
        print(f"Processing registration: {context.current_registration}")

        try:
            context.execute_steps(f"""
                Given the "confused_page" page is open with title "Confused.com"
                When on page "confused_page" the user clicks the "cookies"
                And on page "confused_page" the user clicks the "hero_product_car_insurance"
                And on page "confused_page" the user enters the registration number into the "registration-number-input" field
                And on page "confused_page" the user clicks the "find-vehicle-btn"
                Then on page "confused_page" verify no errors are displayed for "error-summary__heading"
                And on page "confused_page" waiting for element "registration-lookup-summary-title" text to contain "Make and model"
                When on page "confused_page" the user scrapes the car details in "car_details"
                Then the system should compare fetched details with expected "input/car_output.txt"
            """)
        except Exception as e:
            mismatch = f"Error processing registration '{context.current_registration}': {e}"
            context.mismatches.append(mismatch)
            print(mismatch)


@when('on page "{page_name}" the user enters the registration number into the "{element_name}" field')
def step_enter_registration_number(context, page_name, element_name):
    """
    Enters the current registration number into the specified field.

    :param context: Behave context object
    :param page_name: The variable representing the page name
    :param element_name: The field element to enter the registration number
    """
    try:
        registration_plate = context.current_registration
        print(f'On page "{page_name}", entering registration number "{registration_plate}" into "{element_name}".')
        __enter_text_check_value(page_name, registration_plate, element_name)
    except Exception as e:
        print(f"Error entering registration number: {e}")
        raise


@when('on page "{page_name}" the user scrapes the car details in "{element_name}"')
def step_scrape_car_details(context, page_name, element_name):
    """
    Scrapes car details from the specified HTML element on the page.

    :param context: Behave context object
    :param page_name: Name of the page being interacted with
    :param element_name: Identifier for the HTML element containing the car details (class name)
    """
    try:
        car_details_panel = get_element(page_name, element_name)

        vehicle_details = {}
        for line in car_details_panel.text.splitlines():
            if ": " in line:
                key, value = line.split(": ", 1)
                vehicle_details[key.strip()] = value.strip()

        registration = vehicle_details.pop("Registration", None)
        if not registration:
            raise ValueError("Registration not found in the scraped details.")

        context.fetched_details = {registration: vehicle_details}
        print(f"Scraped vehicle details: {context.fetched_details}")
    except Exception as e:
        print(f"Error scraping car details from element {element_name}: {e}")
        raise


@then('the system should compare fetched details with expected "{output_file}"')
def step_compare_fetched_details_with_output_file(context, output_file):
    """
    Compares the fetched details with the expected output from the given file.

    :param context: Behave context object
    :param output_file: Path to the output file containing expected details
    """
    try:
        if not hasattr(context, "fetched_details") or not context.fetched_details:
            raise ValueError("No fetched details available in context.")

        # Load expected details from the file
        expected_details = {}
        with open(output_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                reg_number = row["VARIANT_REG"]
                expected_details[reg_number] = {
                    "Manufacturer": row["MAKE"],
                    "Model": row["MODEL"],
                    "Year": row["YEAR"],
                }

        # Compare fetched and expected details
        for reg_number, fetched_detail in context.fetched_details.items():
            expected_detail = expected_details.get(reg_number)
            if not expected_detail:
                # Log a mismatch for a missing registration
                mismatch = f"No expected data found for registration: {reg_number}"
                context.mismatches.append(mismatch)
                continue

            for key, expected_value in expected_detail.items():
                fetched_value = fetched_detail.get(key)
                if key == "Model" and not is_similar(expected_value, fetched_value):
                    mismatch = (
                        f"Mismatch for {reg_number} - {key}: "
                        f"Expected '{expected_value}', Found '{fetched_value}'"
                    )
                    context.mismatches.append(mismatch)
                elif fetched_value != expected_value:
                    mismatch = (
                        f"Mismatch for {reg_number} - {key}: "
                        f"Expected '{expected_value}', Found '{fetched_value}'"
                    )
                    context.mismatches.append(mismatch)

        # Handle registrations in the expected file but not fetched
        for reg_number in expected_details:
            if reg_number not in context.fetched_details:
                mismatch = f"Registration '{reg_number}' not found in fetched details."
                context.mismatches.append(mismatch)

    except Exception as e:
        print(f"Error comparing fetched details with expected output: {e}")
        raise


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
