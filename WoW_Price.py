import requests
from decouple import config
import logging
import datetime
import pycurl
import base64
import json
from io import BytesIO

time = datetime.datetime.now()
logging.basicConfig(level=logging.INFO,
                    filename=f"Token_module_{time.strftime('%d')}-{time.strftime('%b')}-{time.strftime('%Y')}__{time.strftime('%H')}-{time.strftime('%M')}-{time.strftime('%S')}.log",
                    filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

class WowToken:
    
    __token = ""
    
    def autenticar2(self):
        client_id = config("client_id")
        client_secret = config("client_secret")
        url = "https://oauth.battle.net/token"
        try:
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(c.POST, 1)
            c.setopt(c.HTTPHEADER, [
                "Authorization: Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode(),
                "Content-Type: application/x-www-form-urlencoded"
            ])
            c.setopt(c.POSTFIELDS, "grant_type=client_credentials")
            
            buffer = BytesIO()
            #c.setopt(c.WRITEDATA, buffer)
            c.setopt(c.WRITEFUNCTION, buffer.write)
            
            c.perform()
            
            response_code = c.getinfo(c.RESPONSE_CODE)
            response_data = json.loads(buffer.getvalue().decode())
            c.close()
            
            token = response_data["access_token"]
            self.__class__.__token = token
            # if response_code == 200:
            #     print("Access token obtained successfully:")
            #     print(type(response_data))
            # else:
            #     print("Error obtaining access token:", response_code, response_data)
            return self.__class__.__token
        except Exception as e:
            logging.exception("Error - {}".format(response_code))
        
    
    def precio(self):
        try:
            url_wow_token = "https://us.api.blizzard.com/data/wow/token/index?namespace=dynamic-us&locale=en_US&access_token={}".format(self.__class__.__token)
            precio =requests.get(url_wow_token)
            if precio.status_code != 200:
                self.autenticar2()
                url_wow_token = "https://us.api.blizzard.com/data/wow/token/index?namespace=dynamic-us&locale=en_US&access_token={}".format(self.__class__.__token)
                precio =requests.get(url_wow_token)
            respuesta = precio.json()
            precio_token = respuesta["price"] / 10000
            return precio_token
        except Exception as e:
            logging.exception("Error")
        

if __name__ == "__main__":
    prueba = WowToken()
    precios = prueba.precio()
    print(precios)