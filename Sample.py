import os, hashlib, warnings, requests, json
import base64
from Crypto.Cipher import DES3

class PayTest(object):

    """this is the getKey function that generates an encryption Key for you by passing your Secret Key as a parameter."""

    def __init__(self):
        pass

    def getKey(self,secret_key):
        hashedseckey = hashlib.md5(secret_key.encode("utf-8")).hexdigest()
        hashedseckeylast12 = hashedseckey[-12:]
        seckeyadjusted = secret_key.replace('FLWSECK-', '')
        seckeyadjustedfirst12 = seckeyadjusted[:12]
        return seckeyadjustedfirst12 + hashedseckeylast12

    """This is the encryption function that encrypts your payload by passing the text and your encryption Key."""

    def encryptData(self, key, plainText):
        blockSize = 8
        padDiff = blockSize - (len(plainText) % blockSize)
        cipher = DES3.new(key, DES3.MODE_ECB)
        plainText = "{}{}".format(plainText, "".join(chr(padDiff) * padDiff))
        # cipher.encrypt - the C function that powers this doesn't accept plain string, rather it accepts byte strings, hence the need for the conversion below
        test = plainText.encode('utf-8')
        encrypted = base64.b64encode(cipher.encrypt(test)).decode("utf-8")
        return encrypted


    def pay_via_card(self):
        data = {
            'PBFPubKey': 'FLWPUBK-xxxxxxxxxxxxxxxxxxxxx-X',
            "cardno": "4775750000424189",
            "cvv": "953",
            "expirymonth": "10",
            "expiryyear": "20",
            "currency": "NGN",
            "country": "NG",
            "amount": "12",
            "email": "user@flutterwavego.com",
            "phonenumber": "256783474784",
            "firstname": "Michael",
            "lastname": "Katagaya",
            "IP": "355426087298442",
            "txRef": "test01",
            "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
        }

        sec_key = 'FLWSECK-xxxxxxxxxxxxxxxxxxxxx-X'

        # hash the secret key with the get hashed key function
        hashed_sec_key = self.getKey(sec_key)

        # encrypt the hashed secret key and payment parameters with the encrypt function

        encrypt_3DES_key = self.encryptData(hashed_sec_key, json.dumps(data))

        # payment payload
        payload = {
            "PBFPubKey": "FLWPUBK-xxxxxxxxxxxxxxxxxxxxx-X",
            "client": encrypt_3DES_key,
            "alg": "3DES-24"
        }

        # card charge endpoint
        endpoint = "https://api.ravepay.co/flwv3-pug/getpaidx/api/charge"

        # set the content type to application/json
        headers = {
            'content-type': 'application/json',
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        print(response.json())

        
rave = PayTest()
rave.pay_via_card()
