import logging

 
# add filemode="w" to overwrite
logging.basicConfig(filename="sample.log", level=logging.DEBUG)

logging.debug("This is a debug message")
logging.info("Informational message")
logging.error("An error has happened!")

try:
    raise RuntimeError
except Exception as err:
    logging.exception("Error!")
