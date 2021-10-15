import configparser

configFile = 'config.ini'

config = configparser.ConfigParser()
config.read(configFile)


DB_NAME = config['postgres']['DB_NAME']
PASSWORD = config['postgres']['PASSWORD']
USERNAME = config['postgres']['USERNAME']