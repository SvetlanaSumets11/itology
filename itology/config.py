from environs import Env


env = Env()
env.read_env('.env')


ACCOUNT_TYPE = (('Individual', 'Individual'), ('Company', 'Company'))
USER_TYPE = (('Customer', 'Customer'), ('Expert', 'Expert'))
SIZE_IMAGE = 150

TRELLO_API_TOKEN = env('TRELLO_API_TOKEN')
TRELLO_API_KEY = env('TRELLO_API_KEY')
INVITATION_LINK = 'https://api.trello.com/1/boards/{id}/members'
COLORS = ('orange', 'green', 'purple', 'blue', 'lime', 'red', 'yellow', 'sky', 'black', 'pink')
