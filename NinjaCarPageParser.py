import multiprocessing

import requests, re, bs4 as bs, uuid
from Print import Print
from urllib.parse import urlparse

from unidecode import unidecode


class NinjaCarPageParser:


    def __init__(self, ninja_auth, params):
        self.ninja_auth = ninja_auth
        self.params = params
        self.cars = []


    def _runner(self, cars_params ):

        car_page = self.fetch_car(cars_params)

        car_data = self.parse_car_page(car_page)

        car_data['images'] = self.image_processor(car_data['car_image_url_list'], folder='static')

        car_data['auclist'] = self.image_processor(car_data['car_auclist_url'], folder='auclists')

        del car_data['car_image_url_list'], car_data['car_auclist_url']

        self.cars.append({**car_data, **cars_params})


    def run(self):

        for cars_params_idx, cars_params in enumerate(self.params, start=1):

            Print.log(f'[+] Processing car: {cars_params_idx} / {len(self.params)}...')

            with multiprocessing.Pool(processes=20) as pool:

                pool.starmap(self._runner, args=cars_params)

                pool.join()

        return self.cars
    

    def fetch_car(self, seni_car_detail):
        try:

            data = {**seni_car_detail, **self.ninja_auth.metadata}

            r = requests.post(
                'https://www.ninja-cartrade.jp/ninja/cardetail.action',
                headers=self.ninja_auth.headers,
                data={"action": "init_serchcondition", "site": "2", "carListData": "", **data})
            
            return r.text
        
        except Exception as e:
            Print.error(e)


    def image_processor(self, items, folder):

        image_names = []

        for i in items:

            r = requests.get(i, headers=self.ninja_auth.headers)
            image_name = str(uuid.uuid4()) + '.jpg'

            with open(f"{folder}/{image_name}", "wb") as file:

                file.write(r.content)

                image_names.append(image_name)

        return image_names


    def parse_car_page(self, car_page):

        page = bs.BeautifulSoup(car_page, 'html.parser')

        page_car_details = page.find('div', {'class': 'vehicleDetailLeftBox'})

        car_year = page_car_details.text.strip()[:4]

        car_name = ' '.join(re.findall("(\w+)", page.find('div', {'class': 'vehicleDetailName'}).text))

        car_place = ' '.join(re.findall("(\w+)", page.find('div', {'class': 'vehicleDetailPlace'}).text))

        car_score = page_car_details.find('div', {'class': 'vehicleDetailEvaluation'}).find('span').text

        car_price = page.find('div', {'class': 'vehicleDetailBtmLine'}).find('span').text

        car_bid = page.find('div', {'class': 'vehicleDetailBtmLine2'}).text[11:].strip()

        car_auclist_src = page.find('img', {'class': 'imgboder'})["src"]

        local_car_images = page.find('div', {'class': 'vehicleDetailImageBox'}).findAll('img')

        car_images_src = []

        for i in local_car_images[1:]: car_images_src.append(i['src'])

        table_details = page.find('table', {'class': 'vehicleDetailTable'}).findAll("tr")

        car_details_type = table_details[0].findAll("td")[0].text.strip().replace(u'\xa0', u' ')

        car_details_mileage = table_details[0].findAll("td")[1].text.strip().replace(u'\xa0', u' ')

        car_details_color = table_details[1].findAll("td")[0].text.strip().replace(u'\xa0', u' ').lower()

        car_details_body_type = table_details[1].findAll("td")[1].text.strip().replace(u'\xa0', u' ')

        car_details_ac = table_details[2].findAll("td")[0].text.strip().replace(u'\xa0', u' ')

        car_details_displacement = table_details[2].findAll("td")[1].text.strip().replace(u'\xa0', u' ')

        car_details_transmission = table_details[3].findAll("td")[0].text.strip().replace(u'\xa0', u' ')

        car_details_steering = table_details[3].findAll("td")[1].text.strip().replace(u'\xa0', u' ')

        car_details_jsi = table_details[4].findAll("td")[0].text.strip().replace(u'\xa0', u' ')

        # Equipment:
        table_equipment = page.find('table', {'class': 'vehicleDetailEqTable'}).findChildren("td")

        car_equipment = []

        for i in table_equipment:
            
            if "onBack" in str(i):

                car_equipment.append({"text": unidecode(i.get_text(separator=' ', strip=True)), "status": True})

            else:

                car_equipment.append({"text": unidecode(i.get_text(separator=' ', strip=True)), "status": False})
        try:

            car_special_marks = page.find('div', {'class': 'revisionText'}).text.strip()
        except:
            car_special_marks = ''

        car_image_url_list = []

        meta = f'&memberCode={self.ninja_auth.metadata["memberCode"]}' + f'&branchCode={self.ninja_auth.metadata["branchCode"]}'

        detail_path = 'https://www.ninja-cartrade.jp/ninja/cardetail.action?'

        for car_image in car_images_src:
            car_image_url_list.append(detail_path + urlparse(car_image).query + meta)

        car_auclist_url = detail_path + urlparse(car_auclist_src).query + meta

        return {
            "car_image_url_list": car_image_url_list,
            "car_auclist_url": [car_auclist_url],
            "equipment": car_equipment,
            "bid_info":  unidecode(car_bid),
            "price": unidecode(car_price),
            "score": unidecode(car_score),
            "place": unidecode(car_place),
            "name": unidecode(car_name),
            "year": unidecode(car_year),
            "special_marks": unidecode(car_special_marks),
            "details": {
                "type": unidecode(car_details_type),
                "mileage": unidecode(car_details_mileage),
                "color": unidecode(car_details_color),
                "body": unidecode(car_details_body_type),
                "ac": unidecode(car_details_ac),
                "displacement": unidecode(car_details_displacement),
                "transmission": unidecode(car_details_transmission),
                "steering": unidecode(car_details_steering),
                "jsi": unidecode(car_details_jsi)
            }
        }