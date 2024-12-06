import requests
from de.utils import cms_utils
from loguru import logger
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def get_cred(uuid, cred_url, auth_token, iv, key, debug=False, proxy=None):
    headers = {
        'Content-Type': 'application/json',
        f'Authorization': auth_token
    }

    data = {'uuid': uuid}

    try:
        if proxy:
            proxies = {
                'http': proxy,
                'https': proxy
            }
            response = requests.post(cred_url, headers=headers, json=data, verify=False, proxies=proxies)
        else:
            response = requests.post(cred_url, headers=headers, json=data, verify=False)

        if response.status_code == 200:
            print_debug("CMS API Call Successful with status code 200!", debug)
            json_dict = response.json()
            encrypted_cred = json_dict.get("responseData", {}).get("value")

            print_debug(f"Raw response from CMS {response.text}", debug)
            print_debug(f"Got encrypted_cred from CMS {encrypted_cred}", debug)

            try:
                decrypted_cred = cms_utils.decrypt(encrypted_cred, 'AES', iv, key)
                print_debug(f"creds using AES: {decrypted_cred}", debug)
                return decrypted_cred
            except Exception as e:
                decrypted_cred = cms_utils.decrypt(encrypted_cred, 'BASE64', iv, key)
                print_debug(f"creds using B64: {decrypted_cred}", debug)
                return decrypted_cred

        else:
            logger.error(f"CMS API failed with status code {response.status_code} : \n{response.text}")
            return None
    except requests.RequestException as e:
        logger.error(f"An error occurred: {e}")
        return None


def print_debug(message, debug):
    if debug:
        logger.debug(message)
