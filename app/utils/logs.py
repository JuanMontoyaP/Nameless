"""
Set the logger format
"""

import logging

logging.basicConfig(
    filename='app.log',
    format='[%(asctime)s] - %(levelname)s - %(filename)s - %(funcName)s:%(lineno)d - %(message)s',
    level=logging.DEBUG
)
LOGGER = logging.getLogger(__name__)
