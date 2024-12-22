import uuid
from Print import Print
import requests


class NinjaDataBase:
    def __init__(self):
        pass

    @staticmethod
    def send(cars):
        for car in cars:
            data = {
                "body_code": str(uuid.uuid4()),
                "vin_code": str(uuid.uuid4()),
                "data": {
                    "body": car["details"]["body"],
                    "color": car["details"]["color"],
                    "brand": car["brand"],
                    "model": ' '.join(car["name"].split(" ")[1:]),
                    "year": car["year"],
                },
                "ninja": {
                    "uuid": str(uuid.uuid4()),
                    "data": {
                        "bid_info": car["bid_info"],
                        "price": car["price"],
                        "score": car["score"],
                        "place": car["place"],
                        "name": car["name"],
                        "year": car["year"],
                        "special_marks": car["special_marks"],
                        "images": car["images"],
                        "auclist": car["auclist"],
                        "car_kind_type": car["carKindType"],
                        "kaijo_code": car["kaijoCode"],
                        "auction_count": car["auctionCount"],
                        "bid_no": car["bidNo"],
                        "zaiko_no": car["zaikoNo"],
                        "list_number": car["listnumber"],
                        "brand": car["brand"]
                    },
                    "details": car["details"],
                    "equipment": car["equipment"],
                }
            }
            r = requests.post('http://127.0.0.1:5500/cars', json=data)

            if (r.status_code == 200):
                Print.ok("[+] data is upload")
            else: 
                Print.error("[+] error in upload db")