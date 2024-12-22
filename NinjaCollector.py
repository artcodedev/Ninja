import requests
import bs4 as bs
from Print import Print

from Ninja.NinjaParamsDriver import NinjaParamsDriver


class NinjaCollector:


    def __init__(self, ninja_auth):
        self.ninja_auth = ninja_auth
        self.brands = []
        self.corners = []


    def collect(self):

        self.collect_brands()

        self.collect_corners()

        Print.log(f'[+] Collected {len(self.brands)} brands & {len(self.corners)} corners')

        ninja_params_driver = NinjaParamsDriver(self.ninja_auth, self.brands, self.corners)

        return ninja_params_driver.parse()


    def collect_brands(self):
        try:
            r = requests.post('https://www.ninja-cartrade.jp/ninja/makersearch.action',
                headers=self.ninja_auth.headers, data={"action": "makerHenko", "bodyType": ""}).json()
            
            brands = []
            for item in r["makerChoiceSearchConditionList"]:
                for brand in item["carCategoryList"]:
                    brands.append(
                        {
                            "BrandGroupingCode": brand["BrandGroupingCode"],
                            "BrandName": brand["BrandName"]
                        })
            self.brands = brands
        except Exception as e:
            Print.error(e)


    def collect_corners(self):
        try:
            r = requests.post('https://www.ninja-cartrade.jp/ninja/searchcondition.action',
                              headers=self.ninja_auth.headers,
                              data={"site": "2", **self.ninja_auth.metadata}
                              )
            
            labels = bs.BeautifulSoup(r.text, 'html.parser').find('div', {'class': 'vehicleSearchKaijoBox'}).findChildren("input", recursive=True)

            for i in labels:
                r = requests.post('https://www.ninja-cartrade.jp/ninja/searchcondition.action',
                                  headers=self.ninja_auth.headers,
                                  data={"action": "getCornerList", "cornerSearchKaijo": i.attrs['value']}).json()
                
                for corner in r["cornerSearchCornerList"]:

                    self.corners.append({
                        "cornerSearchKaijo": i.attrs['value'],
                        "cornerSearchCheckCorner": f'{corner["KaijoCode"]}-{corner["AuctionCount"]}-{corner["LaneCode"]}-{corner["CornerNo"]}'
                    })

        except Exception as e:
            Print.error(e)
