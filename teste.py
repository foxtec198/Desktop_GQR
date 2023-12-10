from logging import DEBUG, basicConfig
from logging import critical, error, warning, info, debug

basicConfig(
    level=DEBUG,
    filename='resources/logs/my_log.log',
    filemode='a',
    format='%(levelname)s: %(asctime)s -- %(message)s - %(module)s '
)

txt = 'Estou testando'
debug(txt)