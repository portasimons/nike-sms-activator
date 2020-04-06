import re
import requests
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


def request_set_status(api_key, operation_id, status): # set activation status (str)
    request_url = "http://sms-activate.ru/stubs/handler_api.php?api_key=" + api_key + "&action=setStatus&status=" + status + "&id=" + operation_id
    response = requests.post(request_url).text
    return response


def request_status(api_key, operation_id): # request current activation status (str)
    request_url = "http://sms-activate.ru/stubs/handler_api.php?api_key=" + api_key +\
                  "&action=getStatus&id=" + operation_id
    return requests.get(request_url).text


def get_sms(api_key, operation_id): # receive SMS from activation service (str)
    retry_count = 0 # variable to count number of SMS requests.
    while True:
        response = request_status(api_key=api_key, operation_id=operation_id)
        if response.startswith("STATUS_OK:"):
            return response.replace("STATUS_OK:", "")
        if response == "STATUS_WAIT_CODE":
            time.sleep(5)
            retry_count += 1
            continue
        if retry_count == 120: # 120 is a max number of SMS requests
            return ""


def finish_activation(api_key, operation_id, sms_response): # returns true if activation successful (bool)
    if sms_response == "":
        response = request_set_status(api_key=api_key, operation_id=operation_id, status="8")
        return False
    else:
        response = request_set_status(api_key=api_key, operation_id=operation_id, status="6")
        return True


def main():
    # parameters
    api_key = "" # insert API-key here
    country = "0" # country code
    service = "ew" # service code

    # renting phone number
    get_number_response = get_number(api_key=api_key, service=service, country=country)
    phone_number = parse_number(response=get_number_response)
    operation_id = parse_operation_id(response=get_number_response)

    # starting activation
    sms_response = get_sms(api_key=api_key, operation_id=operation_id)
    finish_activation(api_key=api_key, operation_id=operation_id, sms_response=sms_response)


if __name__ == "__main__":
    main()