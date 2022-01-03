import configparser

configFile = 'config.ini'

config = configparser.ConfigParser()
config.read(configFile)


DB_NAME:str = config['postgres']['DB_NAME']
DB_PASSWORD:str = config['postgres']['PASSWORD']
DB_USERNAME:str = config['postgres']['USERNAME']
HOST:str = config['postgres']['HOST']
PORT:str = config['postgres']['PORT']