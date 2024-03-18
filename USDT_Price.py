import requests
import logging
import datetime

time = datetime.datetime.now()
logging.basicConfig(level=logging.INFO,
                    filename=f"USDT_module_{time.strftime('%d')}-{time.strftime('%b')}-{time.strftime('%Y')}__{time.strftime('%H')}-{time.strftime('%M')}-{time.strftime('%S')}.log",
                    filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

def precio_usdt ():
    url = "https://criptoya.com/api/binancep2p/usdt/ves/0.1"
    try:
        pregunta = requests.get(url)
        respuesta = pregunta.json()
        compra_venta = (respuesta["totalAsk"],respuesta["totalBid"])
        return compra_venta
    except Exception as e:
        logging.exception("Error - {}".format(e))
    


if __name__ == "__main__":
    print(precio_usdt())