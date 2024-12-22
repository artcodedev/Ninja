from NinjaDataBase import NinjaDataBase
from NinjaAuth import NinjaAuth
from NinjaCarPageParser import NinjaCarPageParser
from Ninja.NinjaCollector import NinjaCollector
from Reader import Reader
from chardet import detect
import unidecode


# G0-GO-GO
if __name__ == '__main__':

    ninjaAuth = NinjaAuth()
    ninjaAuth.auth()

    ninjaCollector = NinjaCollector(ninjaAuth)

    params = ninjaCollector.collect()

    ninjaCarPageParser = NinjaCarPageParser(ninjaAuth, params)

    cars = ninjaCarPageParser.run()

    NinjaDataBase.send(cars)

    # TODO: setup correct login
    # TODO: Обработать вылет сессии и старт парсера с того же места
    # TODO: multiprocessing

    # reader = Reader()
    # reader.read()

