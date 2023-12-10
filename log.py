from logging import ERROR, basicConfig


basicConfig(level=ERROR,
    filename='resources/logs/my_log.log',
    filemode='w',
    format='%(levelname)s: %(asctime)s -- %(message)s - %(module)s - %(process)s')
