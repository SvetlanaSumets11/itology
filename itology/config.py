from environs import Env


env = Env()
env.read_env('.env')


# ACCOUNT_TYPE = (('Individual', 'Персона'), ('Company', 'Компанія'))
# USER_TYPE = (('Customer', 'Замовник'), ('Expert', 'Експерт'))
ACCOUNT_TYPE = (('Individual', 'Individual'), ('Company', 'Company'))
USER_TYPE = (('Customer', 'Customer'), ('Expert', 'Expert'))

PROJECT_NOT_ACTIVE = 'Not active'
PROJECT_IN_DEVELOPMENT = 'In development'
PROJECT_DEVELOPED = 'Developed'
PROJECT_CONFIRMED = 'Confirmed'
STATUS = (
    (PROJECT_NOT_ACTIVE, PROJECT_NOT_ACTIVE),
    (PROJECT_IN_DEVELOPMENT, PROJECT_IN_DEVELOPMENT),
    (PROJECT_DEVELOPED, PROJECT_DEVELOPED),
    (PROJECT_CONFIRMED, PROJECT_CONFIRMED),
)

SIZE_IMAGE = 150

TRELLO_API_TOKEN = env('TRELLO_API_TOKEN')
TRELLO_API_KEY = env('TRELLO_API_KEY')
INVITATION_LINK = 'https://api.trello.com/1/boards/{id}/members'
COLORS = ('orange', 'green', 'purple', 'blue', 'lime', 'red', 'yellow', 'sky', 'black', 'pink')

DOWNLOAD_FILE_LINK = env('DOWNLOAD_FILE_LINK')
REDIRECT_DOWNLOAD_FILE_LINK = env('REDIRECT_DOWNLOAD_FILE_LINK')
CERTIFICATE_PATTERN_PATH = env('CERTIFICATE_PATTERN_PATH')
