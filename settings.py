from os import getenv
from dotenv import load_dotenv

load_dotenv()

CALENDARS_DIR = getenv('CALENDARS_DIR')
JSON_DIR = getenv('JSON_DIR')

assert CALENDARS_DIR, 'No CALENDARS_DIR env var found, please set'
assert JSON_DIR, 'No JSON_DIR env var found, please set'
