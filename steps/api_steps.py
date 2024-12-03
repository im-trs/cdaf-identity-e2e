import json
import time
from datetime import datetime

import requests
from asserts import *
from behave import *


@given('a webhook connection to xyz "{endpoint}"')
def step_impl(context, endpoint=""):
    celigo_endpoint_vars = context.endpoint_url = context.toolium_config.get('xyz', endpoint).split(',')
    context.endpoint_url = celigo_endpoint_vars[0].strip()
    context.endpoint_token = celigo_endpoint_vars[1].strip()


@step('the payload template "{template}"')
def step_impl(context, template):
    with open(f'./api/payloads/{template}') as f:
        context.payload = json.dumps(json.load(f)).replace("TOKEN", context.endpoint_token)
        context.logger.info(f"> template: {context.payload}")


@step('the field "{field}" is "{value}"')
def step_impl(context, field, value):
    context.payload = context.payload.replace(field.upper(), value)


@when("the request is sent")
def step_impl(context):
    context.payload = context.payload.replace("ORDERDATE", datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    context.logger.info(f"> payload: {context.payload}")
    context.r = requests.post(context.endpoint_url, data=context.payload, headers={"Content-Type": "application/json"})
    context.logger.info(f"status code '{context.r.status_code}', reason '{context.r.reason}', content '{context.r.content}'")


@then('the server http status response is "{status_code}"')
def step_impl(context, status_code):
    assert_equal(context.r.status_code, int(status_code), msg_fmt=f"{context.r.status_code} is wrong, expected {status_code}")


@step("wait for Celigo process to finish")
def step_impl(context):
    # pause threads for 60 seconds
    time.sleep(60)