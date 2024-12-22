import bs4 as bs, requests, re
from Print import Print


class NinjaParamsDriver:


    def __init__(self, ninja_auth, brands, corners):
        self.ninja_auth = ninja_auth
        self.scores = []
        self.colors = []
        self.brands = brands
        self.corners = corners


    def collect_cars_params_list(self):
        params_list = []

        empty = b'Result\xe3\x80\x80\xef\xbc\x9a\xe3\x80\x800 items'

        too_much = 'Result　：　More than 1,000items'

        data = {"action": "seniConditionSearch", "site": "2", **self.ninja_auth.metadata}

        for brand_idx, brand in enumerate(self.brands, start=1):

            if brand["BrandName"] != 'MAZDA':
                continue

            data["BrandGroupingCode"] = brand["BrandGroupingCode"]

            Print.log(f'[+] Collecting {brand["BrandName"]} ({brand_idx}/{len(self.brands)})...')

            for color_idx, color in enumerate(self.colors, start=1):

                if color != 'ckColor_Black':
                    continue

                Print.log(f'[+] Collecting {color[8:]}: {color_idx}/{len(self.colors)}')

                r = requests.post('https://www.ninja-cartrade.jp/ninja/searchresultlist.action', headers=self.ninja_auth.headers, data={**data, **{color: "true"}})
                
                if empty in r.content:
                    Print.warning(f'0')
                    continue

                if too_much in r.text:
                    for score_idx, score in enumerate(self.scores, start=1):

                        Print.log(f'[+] Collecting {score[8:]}: {score_idx}/{len(self.scores)}')

                        data_s1 = data={**data, color: "true", score: "true"}

                        r = requests.post('https://www.ninja-cartrade.jp/ninja/searchresultlist.action', headers=self.ninja_auth.headers, data=data_s1)
                        
                        if empty in r.content:
                            Print.warning(f'0')
                            continue

                        if too_much in r.text:
                            for corner_idx, corner in enumerate(self.corners, start=1):

                                Print.log(f'[+] Collecting Corner: {corner["cornerSearchCheckCorner"]}, {corner_idx}/{len(self.corners)}')

                                data_s2 = {**data, color: "true", score: "true", **corner}

                                r = requests.post('https://www.ninja-cartrade.jp/ninja/searchresultlist.action', headers=self.ninja_auth.headers, data=data_s2)
                                
                                if empty in r.content:
                                    Print.warning(f'0')
                                    continue

                                else:
                                    res = self.parse_cars_params(r.text, brand["BrandName"])
                                    params_list.append(res)
                                    Print.log(f'{len(res)}')
                        else:
                            res = self.parse_cars_params(r.text, brand["BrandName"])
                            params_list.append(res)
                            Print.log(f'{len(res)}')
                else:
                    res = self.parse_cars_params(r.text, brand["BrandName"])
                    params_list.append(res)
                    Print.log(f'{len(res)}')

        # flat list
        return [x for xs in params_list for x in xs]

    def parse(self):

        self.scores = ["ckScore_S", "ckScore_6", "ckScore_5", "ckScore_4_5", "ckScore_4",
                       "ckScore_3_5", "ckScore_3","ckScore_2", "ckScore_1", "ckScore_R",
                       "ckScore_RA", "ckScore_X", "ckScore_AST", "ckScore_OTHER"]
        
        self.colors = ["ckColor_Yellow", "ckColor_Orange", "ckColor_Green",
                       "ckColor_Gray", "ckColor_Gold", "ckColor_Silver",
                       "ckColor_Purple", "ckColor_Brown", "ckColor_Black",
                       "ckColor_Blue", "ckColor_Beige", "ckColor_White",
                       "ckColor_Red", "ckColor_Pearl", "ckColor_Pink",
                       "ckColor_Wine"]
        
        return self.collect_cars_params_list()

    def parse_cars_params(self, html, brand):
        try:

            children = bs.BeautifulSoup(html, 'html.parser').find('table', {'class': 'listTable3'}).findChildren("tbody", recursive=False)

            car_details = []

            for child in children:
                attribute = child.find("td", {"class": "textLeft"}).findChildren("a", recursive=False)[-1]

                p = re.findall("'(\w+)'", attribute['onclick'])

                car_details.append({
                    "carKindType": p[0],
                    "kaijoCode": p[1],
                    "auctionCount": p[2],
                    "bidNo": p[3],
                    "zaikoNo": "",
                    "listnumber": "1",
                    "brand": brand
                })

            return car_details
        
        except Exception as e:
            with open(f'../results/er.html', 'w') as file:
                Print.error('er')
                file.write(html)
