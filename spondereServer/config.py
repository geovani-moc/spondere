import configparser

configFile = 'config.ini'

config = configparser.ConfigParser()
config.read(configFile)


DB_NAME:str = config['postgres']['DB_NAME']
DB_PASSWORD:str = config['postgres']['PASSWORD']
DB_USERNAME:str = config['postgres']['USERNAME']
MIN_CONNECTIONS:int = int(config['postgres']['MIN_CONNECTIONS'])
MAX_CONNECTIONS:int = int(config['postgres']['MAX_CONNECTIONS'])
HOST:str = config['postgres']['HOST']
PORT:str = config['postgres']['PORT']