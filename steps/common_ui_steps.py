import csv
import os
import re
from datetime import date, datetime

import allure
from asserts import *
from behave import *
from retry import retry
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from page_objects.common import CommonPageObject, wait_for_seconds
from steps.mapping import get_element, get_page_object


class CommonStepsException(Exception):
    pass


@step('the "{page_name}" page is open')
def step_impl(context, page_name=""):
    try:
        context.current_page = CommonPageObject()
        context.current_page.open(page_name)
    except Exception as expt:
        print(f"Thrown exception on {page_name}: {expt}")
        raise


@step('the "{page_name}" page is open with title "{expected_title}"')
def step_impl(context, page_name="", expected_title=""):
    try:
        print(f'the "{page_name}" page is open with title "{expected_title}"')
        context.current_page = CommonPageObject()
        actual_title = context.current_page.open(page_name).strip().lower()
        expected_title = expected_title.strip().lower()
        check = actual_title == expected_title or (actual_title.find(expected_title) >= 0)
        assert_true(check, msg_fmt="expected title '{}' is not equal to the actual title '{}'".format(expected_title,
                                                                                                      actual_title))
    except Exception as expt:
        print(f"Thrown exception on {page_name}, expected_title '{expected_title}': {expt}")
        raise


@step('on page "{page_name}" the user hovers the "{element_name}"')
def step_impl(context, page_name="", element_name=""):
    try:
        print(f'on page "{page_name}" the user hovers the "{element_name}"')
        el = get_element(page_name, element_name)
        CommonPageObject().hover_element(element_name, el)
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step('on page "{page_name}" the user clicks the "{element_name}"')
def step_impl(context, page_name="", element_name=""):
    if element_name == 'cookies':
        try:
            el = get_element(page_name, element_name)
            CommonPageObject().hover_element(element_name, el).click_element(element_name, el)
        except Exception:
            print(f"Cookies button not found on page '{page_name}'. Skipping step.")
    else:
        try:
            scroll_to_elements = ['priced_shipping_method', 'add_to_basket_button', 'payment_place_order',
                                  'payment_view_all_saved_cards', 'proceed_with_card', 'delivery_proceed_to_payment',
                                  'enter_address_manually']
            print(f'on page "{page_name}" the user clicks the "{element_name}"')
            el = get_element(page_name, element_name)
            if element_name in scroll_to_elements:
                if element_name == 'priced_shipping_method':
                    CommonPageObject().wait_for_load_screen()
                CommonPageObject().scroll_to_page_element(element_name, el)
                CommonPageObject().driver.implicitly_wait(2)
                CommonPageObject().wait_until_element_is_displayed(element_name, el)
                CommonPageObject().click_element(element_name, el)
            else:
                CommonPageObject().hover_element(element_name, el).click_element(element_name, el)
        except Exception as expt:
            print(f"Thrown exception on {page_name}.{element_name}: {expt}")
            raise


@step('on page "{page_name}" the user switch on the JavaScript popup and click on the confirmation')
def step_impl(context, page_name=""):
    try:
        print(f'on page "{page_name}" the user switch on the JavaScript popup and click on the confirmation')
        alert = CommonPageObject().driver.switch_to.alert
        alert.accept()
    except Exception as expt:
        print(f"Thrown exception on {page_name}.JavaScriptPopup: {expt}")
        raise


@step('on page "{page_name}" the user clicks the element "{element_name}" if displayed')
def step_impl(context, page_name="", element_name=""):
    try:
        print(f'on page "{page_name}" the user clicks the element "{element_name}" if displayed')
        el = get_element(page_name, element_name)
        CommonPageObject().driver.implicitly_wait(3)
        element_displayed = CommonPageObject().element_is_displayed(element_name, el)
        if element_displayed:
            CommonPageObject().click_element(element_name, el)
    except NoSuchElementException:
        CommonPageObject().utils.set_implicitly_wait()
        pass


@step('on page "{page_name}" the user clicks the element "{element_name}" within frame "{element_frame}"')
def step_impl(context, page_name="", element_name="", element_frame=""):
    try:
        print(f'on page "{page_name}" the user clicks the element "{element_name}" within frame "{element_frame}"')
        if element_name == 'paypal_button':
            wait_for_seconds(3)
        el_frame = get_element(page_name, element_frame)
        CommonPageObject().frame_switch_xpath(el_frame)
        el = get_element(page_name, element_name)
        CommonPageObject().scroll_to_page_element(element_name, el).hover_element(element_name, el).click_element(element_name, el)
        CommonPageObject().frame_switch_default()
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step('on page "{page_name}" the user clicks on the "{element_name}" with the text "{text}"')
def step_impl(context, page_name="", element_name="", text=""):
    try:
        print(f'on page "{page_name}" the user clicks the "{element_name}" with text "{text}"')
        if page_name == 'p2p_goods_in' and (text == "<transfer_order_name>" or text == "transfer_order_name"):
            text = context.transfer_order_name
        el = get_element(page_name, element_name, text)
        if element_name == 'address_finder_option':
            CommonPageObject().scroll_to_page_element(element_name, el)
            CommonPageObject().utils.set_implicitly_wait()
            CommonPageObject().utils.wait_until_element_clickable(el, 5)
        CommonPageObject().hover_element(element_name, el).click_element(element_name, el)
        if element_name == ('address_finder_option' and 'delivery_method'):
            CommonPageObject().wait_for_load_screen()
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step(
    'on page "{page_name}" the user enters "{text}" into the "{element_name}" field to search for an element and clicks the the "{element_found}"')
@retry(AssertionError, tries=30, delay=1)
def step_impl(context, page_name="", text="", element_name="", element_found=""):
    nested_step_one = f'When on page "{page_name}" the user enters text "{context.example_table_dict["SALES_ORDER_NUMBER"]}" into the "{element_name}" field'
    nested_step_two = f'When on page "{page_name}" the user clicks the "{element_found}"'

    CommonPageObject().driver_wrapper.driver.refresh()
    print(nested_step_one)
    context.execute_steps(nested_step_one)

    print(nested_step_two)
    context.execute_steps(nested_step_two)


@step('on page "{page_name}" the user enters text "{text}" into the "{element_name}" field')
def step_impl(context, page_name="", text="", element_name=""):
    try:
        print(f'on page "{page_name}" the user enters text "{text}" into the "{element_name}" field')
        if page_name == 'customer_login' and (text == "<employee_email>" or text == "employee_email"):
            text = CustomerLoginPageObject().get_credentials(text)
        elif page_name == 'customer_login' and (text == "<employee_password>" or text == "employee_password"):
            text = CustomerLoginPageObject().get_password(text)
        elif page_name == 'p2p_goods_in' and (text == "<transfer_order_name>" or text == "transfer_order_name"):
            text = context.transfer_order_name

        __enter_text_check_value(page_name, text, element_name)
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step('on page "{page_name}" the user enters credentials "{text}" into the "{element_name}" field')
def step_impl(context, page_name="", text="", element_name=""):
    try:
        print(f'on page "{page_name}" the user enters credentials "{text}" into the "{element_name}" field')
        page_object = get_page_object(page_name)
        credentials = page_object.get_credentials(context, text)
        if credentials is not None:
            text = credentials
        __enter_text_check_value(page_name, text, element_name)
    except Exception:
        raise CommonStepsException(
            f'on page "{page_name}" the user enters credentials "{text}" into the "{element_name}" field UNSUCCESSFUL')


@step(
    'on page "{page_name}" the user enters text "{text}" into the "{element_name}" field of context "{element_context}" with added date/time stamp')
def step_impl(context, page_name="", text="", element_name="", element_context=""):
    try:
        print(
            f'on page "{page_name}" the user enters text "{text}" into the "{element_name}" field of context "{element_context}" with added date/time stamp')
        dt_string = datetime.now().strftime("%d%m%Y%H%M%S")

        match element_context.strip().lower():
            case 'email':
                text_plus_date_time = text.replace("@", "+{}@".format(dt_string))
                __enter_text_check_value(page_name, text_plus_date_time, element_name)

                for item in context.test_data:
                    if item['TC'] == context.data['TEST_CASE_ID']:
                        item[f'customer_email'] = text_plus_date_time

                print(f"The text entered was {text_plus_date_time}")
            case _:
                text_plus_date_time = str(text + "-{}".format(dt_string))
                __enter_text_check_value(page_name, text_plus_date_time, element_name)

                for item in context.test_data:
                    if item['TC'] == context.data['TEST_CASE_ID']:
                        item[f'{element_name}'] = text_plus_date_time

                print(f"The text entered was {text_plus_date_time}")
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step(
    'on page "{page_name}" the user enters text "{text}" into the "{element_name}" field within frame "{element_frame}"')
def step_impl(context, page_name="", text="", element_name="", element_frame=""):
    try:
        print(
            f'on page "{page_name}" the user enters text "{text}" into the "{element_name}" field within frame "{element_frame}"')
        el_frame = get_element(page_name, element_frame)
        CommonPageObject().frame_switch_xpath(el_frame)
        __enter_text_check_value(page_name, text, element_name)
        CommonPageObject().frame_switch_default()
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step(
    'on page "{page_name}" the user enters text "{text}" into the "{element_name}" field with parent text "{parent_text}" within frame "{element_frame}"')
def step_impl(context, page_name="", text="", element_name="", parent_text="", element_frame=""):
    try:
        print(
            f'on page "{page_name}" the user enters text "{text}" into the "{element_name}" field with parent text "{parent_text}" within frame "{element_frame}"')
        el_frame = get_element(page_name, element_frame, parent_text)
        CommonPageObject().frame_switch_xpath(el_frame)
        __enter_text_check_value(page_name, text, element_name)
        CommonPageObject().frame_switch_default()
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step('on page "{page_name}" the element "{element_name}" is displayed')
def step_impl(context, page_name="", element_name=""):
    try:
        print(f'on page "{page_name}" the element "{element_name}" is displayed')
        el = get_element(page_name, element_name)
        is_displayed = CommonPageObject().wait_until_element_is_displayed(element_name, el)
        assert_boolean_true(is_displayed,
                            msg_fmt="In page {} element '{}' on page is not displayed".format(page_name, element_name))
        print(f"\t page {page_name} element '{element_name}' on page is displayed")
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step('on page "{page_name}" the attribute "{attribute_name}" of element "{element_name}" is "{attribute_value}"')
def step_impl(context, page_name="", attribute_name="", element_name="", attribute_value=""):
    try:
        print(
            f'on page "{page_name}" the attribute "{attribute_name}" of element "{element_name}" is "{attribute_value}"')
        el = get_element(page_name, element_name)
        actual_attribute_value = CommonPageObject().get_attribute_value(element_name, el,
                                                                        attribute_name).lower().strip()
        expected_value = attribute_value.lower().strip()
        assert_equal(str(actual_attribute_value), str(expected_value),
                     msg_fmt="expected value '{}' is not equal to the actual value '{}'".format(expected_value,
                                                                                                actual_attribute_value))
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step('on page "{page_name}" the user selects option "{option}" from the "{element_name}" field')
def step_impl(context, page_name="", option="", element_name=""):
    try:
        print(f'on page "{page_name}" the user selects option "{option}" from the "{element_name}" field')
        el = get_element(page_name, element_name)
        context.current_page.select_option(element_name, option, el)
        # if element_name == 'delivery_country':
        #     CommonPageObject().wait_for_load_screen()
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step('on page "{page_name}" the user selects product item option "{option}" from the "{element_name}" field')
def step_impl(context, page_name="", option="", element_name=""):
    try:
        product_item_option = context.product_item[f'{option}']
        print(f'on page "{page_name}" the user selects option "{option}" from the "{element_name}" field')
        el = get_element(page_name, element_name)
        context.current_page.select_option(element_name, product_item_option, el)
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step(
    'on page "{page_name}" the user selects option "{option}" from the "{element_name}" field for item "{parent_element_name}"')
def step_impl(context, page_name="", option="", element_name="", parent_element_name=""):
    try:
        print(
            f'on page "{page_name}" the user selects option "{option}" from the "{element_name}" for item "{parent_element_name}"')
        el = get_element(page_name, element_name, parent_element_name)
        context.current_page.select_option(element_name, option, el)
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step('wait for jquery "{jquery}" to finish')
def step_impl(context, jquery=""):
    try:
        print(f'wait for jquery "{jquery}" to finish')
        CommonPageObject().wait_for_query(jquery)
        context.current_page.select_option(jquery)
    except Exception as expt:
        print(f"Thrown exception on jquery {jquery}: {expt}")
        raise


@step('on page "{page_name}" the text "{text}" is displayed')
def step_impl(context, page_name="", text=""):
    try:
        print(f'on page "{page_name}" the text "{text}" is displayed')
        assert_boolean_true(context.current_page.get_find_tables(text),
                            msg_fmt="text {} is not displayed on the page {}".format(text, page_name))
        print(f"\t page {page_name} element with text '{text}' is displayed, value is {text}")
    except Exception as expt:
        print(f"Thrown exception on {page_name}, text '{text}': {expt}")
        raise


@step('on page "{page_name}" waiting for element "{element_name}" text to contain "{text_value}"')
def step_impl(context, page_name="", element_name="", text_value=""):
    try:
        print(f'on page "{page_name}" waiting for element "{element_name}" text to contain "{text_value}"')
        __element_text_to_contain(context, element_name, page_name, text_value)
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step('on page "{page_name}" waiting for element "{element_name}" text to contain current date')
def step_impl(context, page_name="", element_name=""):
    try:
        print(f'on page "{page_name}" waiting for element "{element_name}" text to contain current date')
        el = get_element(page_name, element_name)
        actual_value = CommonPageObject().wait_element(element_name, el).text.lower().strip()
        if actual_value == '':
            actual_value = CommonPageObject().get_attribute_value(element_name, el, 'value').lower().strip()
        expected_value = date.today().strftime("%d/%m/%Y").lower().strip()
        check = (actual_value == expected_value) or re.search(expected_value, actual_value)
        assert_true(check,
                    msg_fmt="expected value '{}' is not contained in the actual value '{}'".format(expected_value,
                                                                                                   actual_value))
    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")
        raise


@step('on page "{page_name}" the user enters the answer to the security question')
def step_impl(context, page_name=""):
    try:
        print(f'on page "{page_name}" the user enters the answer to the security question')
        el = get_element(page_name, "question_text")
        submit_button = get_element(page_name, "submit_btn")
        question = (el.text.split(' ')[-1]).replace("?", "")

        element_question = get_element(page_name, "answer_text")
        CommonPageObject().enter_text("answer_text", element_question, question)
        CommonPageObject().click_element("submit_btn", submit_button)
    except Exception as expt:
        print(f"Managed Error since authentication is not always required: {expt}")


@step('on page "{page_name}" the "{attribute}" is recorded for element "{element_name}"')
def step_impl(context, page_name="", attribute="", element_name=""):
    try:
        print(f'on page "{page_name}" the "{attribute}" is recorded for element "{element_name}"')
        el = get_element(page_name, element_name)
        if element_name == 'priced_shipping_method_name' and 'order_total_price':
            CommonPageObject().wait_for_load_screen()
        value = CommonPageObject().get_attribute_value(element_name, el, attribute)

        match element_name.strip().lower():
            case 'order_number':
                context.example_table_dict["SALES_ORDER_NUMBER"] = value
                save_order_number(value)
            case 'customer_order_id':
                context.example_table_dict["CUSTOMER_ORDER_ID"] = value
            case 'customer_name':
                context.example_table_dict["CUSTOMER_NAME"] = value
            case 'customer_deposit_num':
                context.example_table_dict["CUSTOMER_DEPOSIT_NUM"] = value
            case 'memo':
                context.example_table_dict["MEMO"] = value
            case 'sales_subsidiary':
                context.example_table_dict["SALES_SUBSIDIARY"] = value
            case 'amount_debit':
                context.example_table_dict["AMOUNT_DEBIT"] = value
            case 'amount_debit_posting':
                context.example_table_dict["AMOUNT_DEBIT_POSTING"] = value
            case 'deposit_ref_number':
                context.example_table_dict["DEPOSIT_REF_NUMBER"] = value
            case 'payment_amount':
                context.example_table_dict["PAYMENT_AMOUNT"] = value
            case 'transfer_order_number':
                context.example_table_dict["TRANSFER_ORDER_NUMBER"] = value
            case 'inventory_transfer_number':
                context.example_table_dict["INVENTORY_TRANSFER_NUMBER"] = value
            case 'payment_select_saved_card':
                context.example_table_dict["PAYMENT_SELECT_SAVED_CARD"] = value
            case 'priced_shipping_method', 'free_shipping_method':
                if element_name == 'price_shipping_method':
                    value = price_to_float(value)
                context.example_table_dict["SHIPPING_COST"] = value
            case 'priced_shipping_method_name', 'free_shipping_method_name':
                context.example_table_dict["SHIPPING_METHOD_NAME"] = value
            case 'order_total_price':
                value = price_to_float(value)
                context.example_table_dict["ORDER_TOTAL_PRICE"] = value
            case 'storefront_item_price':
                value = price_to_float(value)
                context.example_table_dict["STOREFRONT_ITEM_PRICE"] = value
            case _:
                print(f"The element '{element_name}' is not defined in the match case to save to the dictionary table")

        check = bool(value != ' ' or '')
        context.utils.capture_screenshot(f'{element_name}_{value}')
        print(f'The attribute "{attribute}" for element "{element_name}" is "{value}"')
        assert_true(value)
        assert_true(check, msg_fmt="The value for '{}' is blank '{}'".format(element_name, value))

        for item in context.test_data:
            if item['TC'] == context.data['TEST_CASE_ID']:
                if element_name == 'priced_shipping_method' or element_name == 'free_shipping_method':
                    item['shipping_cost'] = price_to_float(value)
                elif element_name == 'priced_shipping_method_name' or element_name == 'free_shipping_method_name':
                    item['shipping_method_name'] = value
                else:
                    item[f'{element_name}'] = value

    except Exception as expt:
        raise CommonStepsException(
            f'on page "{page_name}" the "{attribute}" is recorded for element "{element_name}" UNSUCCESSFUL - {expt}')


@step('the user waits for "{value}" seconds')
def step_impl(context, value=None):
    try:
        print(f'the user waits for "{value}" seconds')
        wait_for_seconds(value)
        CommonPageObject().driver_wrapper.driver.refresh()
    except Exception as expt:
        print(f"Thrown exception on user waiting for {value} seconds: {expt}")


@step('the user switches to the "{window_name}" window')
def step_impl(context, window_name=""):
    try:
        print(f'the user switches to the "{window_name}" window')
        CommonPageObject().switch_to_window(window_name)
    except Exception as expt:
        print(f"Thrown exception on user switches to the '{window_name}' window: {expt}")


@given('the user is executing the TestCase with TC "{tc}"')
def step_impl(context, tc):
    try:
        print(f'the user is executing the TestCase with ID "{tc}"')
        context.data['TEST_CASE_ID'] = tc

        for item in context.test_data:
            if item['TC'] == context.data['TEST_CASE_ID']:

                if "item_id" in item and "sales_channel" in item:
                    item_id = f"{item['item_id']}"
                    sales_channel = f"{item['sales_channel']}"
                    context.product_item = find_item(context, item_id, sales_channel)
    except Exception as expt:
        raise CommonStepsException(f'the user is executing the TestCase with TC "{tc}" UNSUCCESSFUL')


@step('the user pauses for "{value}" seconds')
def step_impl(context, value=None):
    try:
        print(f'the user pauses for "{value}" seconds')
        wait_for_seconds(value)
    except Exception as expt:
        print(f"Thrown exception on the user pauses for '{value}' seconds: {expt}")


@step('on page "{page_name}" the user clicks on the "{element_name}" with the json value "{text}"')
def step_impl(context, page_name="", element_name="", text=""):
    json_value = __get_value_from_json(context, text)
    try:
        json_value = __get_value_from_json(context, text)
        el = get_element(page_name, element_name, json_value)
        CommonPageObject().click_element(element_name, el)
    except Exception as expt:
        raise CommonStepsException(
            f'on page "{page_name}" the user clicks on the "{element_name}" with the json value "{json_value}" UNSUCCESSFUL')


@given('"description: "{description}"')
def step_impl(context, description=""):
    try:
        test_description = description
        allure.dynamic.description(
            test_description
        )
        print(f'test description added as "{description}"')
    except Exception as expt:
        raise CommonStepsException(f'unable to add the test description')


@then('on page "{page_name}" verify no errors are displayed for "{element_name}"')
def step_verify_no_errors_displayed(context, page_name="", element_name=""):
    try:
        error_elements = []

        # Check for elements using CSS selector
        try:
            el = get_element(page_name, element_name)
            if el.text != '':
                error_elements.append(el.text)
        except NoSuchElementException or TimeoutException:
            pass  # No element found with this CSS selector

        # If any error elements are found, log mismatch and continue
        if error_elements:
            for error in error_elements:
                context.mismatches.append(
                    f"Error displayed on page '{page_name}': {error.strip()}"
                )
                print(f"Error displayed on page '{page_name}': {error.strip()}")
    except Exception as e:
        print(f"Error verifying error elements on page '{page_name}': {e}")
        raise


def __enter_text_check_value(page_name="", text="", element_name=""):
    el = get_element(page_name, element_name)
    CommonPageObject().enter_text(element_name, el, text)
    actual_value = CommonPageObject().get_attribute_value(element_name, el, "value").lower().strip()
    expected_value = text.lower().strip()
    check = actual_value == expected_value or (actual_value.find(expected_value) > 0)
    assert_true(check, msg_fmt="expected value '{}' is not contained in the actual value '{}'".format(expected_value,
                                                                                                      actual_value))


def __element_attribute_is_recorded(context, page_name="", attribute="", element_name="", to_json=False):
    try:
        print(f'on page "{page_name}" the "{attribute}" is recorded for element "{element_name}"')
        el = get_element(page_name, element_name)
        value = CommonPageObject().get_attribute_value(element_name, el, attribute).strip()
        context.utils.capture_screenshot(f'{element_name}_{value}')

        print(f'The attribute for element "{element_name}" is "{value}"')
        assert value, f'The attribute for element "{element_name}" is expected to be present'
        assert len(value) > 0, f'The attribute for element "{element_name}" is expected to be not empty'

        if to_json is True:
            for item in context.test_data:
                if item['TC'] == context.data['TEST_CASE_ID']:
                    item[f'{element_name}'] = value

    except Exception as expt:
        print(f"Thrown exception on {page_name}.{element_name}: {expt}")


def __element_text_to_contain(context, element_name, page_name, text_value):
    el = get_element(page_name, element_name, text_value)
    actual_value = CommonPageObject().wait_element(element_name, el).text.lower().strip()
    if actual_value == '':
        actual_value = CommonPageObject().get_attribute_value(element_name, el, 'value').lower().strip()
    expected_value = text_value.lower().strip()
    if expected_value == 'customer_order_id':
        expected_value = str('sales order #' + context.example_table_dict["CUSTOMER_ORDER_ID"]).strip().lower()
    elif expected_value == 'customer_name':
        expected_value = context.example_table_dict["CUSTOMER_NAME"].strip().lower()
    elif expected_value == 'customer_deposit_num':
        expected_value = context.example_table_dict["CUSTOMER_DEPOSIT_NUM"].strip().lower()
    elif expected_value == 'memo':
        expected_value = context.example_table_dict["MEMO"].strip().lower()
    elif expected_value == 'sales_subsidiary':
        expected_value = context.example_table_dict["SALES_SUBSIDIARY"].strip().lower()
    elif expected_value == 'amount_debit':
        expected_value = context.example_table_dict["AMOUNT_DEBIT"].strip().lower()
    elif expected_value == 'amount_debit_posting':
        expected_value = context.example_table_dict["AMOUNT_DEBIT_POSTING"].strip().lower()
    elif expected_value == 'deposit_ref_number':
        expected_value = context.example_table_dict["DEPOSIT_REF_NUMBER"].strip().lower()
    elif expected_value == 'payment_amount':
        expected_value = context.example_table_dict["PAYMENT_AMOUNT"].strip().lower()
    elif expected_value == 'payment_select_saved_card':
        expected_value = context.example_table_dict["PAYMENT_SELECT_SAVED_CARD"].strip().lower()
    check = (actual_value == expected_value) or re.search(expected_value, actual_value)
    assert_true(check, msg_fmt="expected value '{}' is not contained in the actual value '{}'".format(expected_value,
                                                                                                      actual_value))


def __get_value_from_json(context, key):
    value = next((item.get(key, '') for item in context.test_data if item['TC'] == context.data['TEST_CASE_ID']), '')
    assert value, f'The dict key "{key}" is expected to be present'
    assert len(value) > 0, f'The dict key "{key}" is expected to be not empty'
    return value


def find_item(context, item_id, sales_channel):
    for item in context.items_decode_table:
        if item["item_id"] == item_id and item["sales_channel"].lower() in sales_channel.lower():
            return item
    return None


def find_delivery_method(context, shipping_method_name, subsidiary):
    for item in context.delivery_method_data:
        if (item["storefront_name"].lower() == shipping_method_name.lower() and
                subsidiary.lower() in item["subsidiary"].lower()):
            return item["netsuite_names"]
    return None


def save_order_number(order_number):
    file_path = 'order_numbers.csv'
    file_exists = os.path.exists(file_path)

    with open('order_numbers.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['order_number'])

        writer.writerow([order_number])


def price_to_float(value):
    price_pattern = r'[£$€]'
    non_numeric_pattern = r'[^\d.]'
    cleaned_value = re.sub(price_pattern, '', value)
    # Remove non-numeric characters (except decimal point)
    value = re.sub(non_numeric_pattern, '', cleaned_value)
    return value
