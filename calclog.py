import logging
import os
from datetime import datetime

FILEPATH = os.path.dirname(os.path.realpath(__file__))
date = datetime.now().strftime('%m-%d-%Y')

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d-%Y %I:%M%p',
                    filename= FILEPATH + '/logs/calc' + date + '.log',
                    filemode='a')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%m-%d-%Y %I:%M%p')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)