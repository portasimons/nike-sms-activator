import re
import requests
import uuid
import time


def get_number(api_key, service, country): # renting number (str)
    request_url = "http://sms-activate.ru/stubs/handler_api.php?api_key=" + api_key + "&action=getNumber&service=" + service + "&country=" + country
    return requests.get(request_url).text


def parse_operation_id(response): # parsing response operation ID (str)
    pattern = ":(.*):"
    response = re.search(pattern, response)
    if response:
        response = response.group(1)
    return response


def parse_number(response): # extract response phone number (str)
    pattern = "ACCESS_NUMBER:.*:(.*)"
    response = re.search(pattern, response)
    if response:
        response = response.group(1)
    return response


def request_set_status(api_key, operation_id, status): # set activation status
    request_url = "http://sms-activate.ru/stubs/handler_api.php?api_key=" + api_key + "&action=setStatus&status=" + status + "&id=" + operation_id
    response = requests.post(request_url).text
    return response


def request_status(api_key, operation_id): # request current activation status
    request_url = "http://sms-activate.ru/stubs/handler_api.php?api_key=" + api_key +\
                  "&action=getStatus&id=" + operation_id
    return requests.get(request_url).text


def get_sms(api_key, operation_id): # receive SMS from activation service
    while True:
        response = request_status(api_key=api_key, operation_id=operation_id)
        if response.startswith("STATUS_OK:"):
            return response.replace("STATUS_OK:", "")
        if response == "STATUS_WAIT_CODE":
            time.sleep(5)
            continue
        #if response == "STATUS_CANCEL"


def main():
    # parameters
    api_key = "65300244ffA1d0b9464eAcbAe801bb38"
    country = "0"
    service = "ew"

    # renting phone number
    get_number_response = get_number(api_key=api_key, service=service, country=country)
    phone_number = parse_number(response=get_number_response)
    operation_id = parse_operation_id(response=get_number_response)

    # starting activation
    sms_response = get_sms(api_key=api_key, operation_id=operation_id)

if __name__ == "__main__":
    main()