from environs import Env


env = Env()
env.read_env('.env')


ACCOUNT_TYPE = (('Individual', 'Individual'), ('Company', 'Company'))
USER_TYPE = (('Customer', 'Customer'), ('Expert', 'Expert'))
STATUS = (
    ('Not active', 'Not active'),
    ('In development', 'In development'),
    ('Developed', 'Developed'),
    ('Confirmed', 'Confirmed'),
)
SIZE_IMAGE = 150

TRELLO_API_TOKEN = env('TRELLO_API_TOKEN')
TRELLO_API_KEY = env('TRELLO_API_KEY')
INVITATION_LINK = 'https://api.trello.com/1/boards/{id}/members'
COLORS = ('orange', 'green', 'purple', 'blue', 'lime', 'red', 'yellow', 'sky', 'black', 'pink')

DOWNLOAD_FILE_LINK = env('DOWNLOAD_FILE_LINK')
REDIRECT_DOWNLOAD_FILE_LINK = env('REDIRECT_DOWNLOAD_FILE_LINK')
