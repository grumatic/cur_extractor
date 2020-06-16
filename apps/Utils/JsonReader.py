import json
import gzip
import shutil
import logging.config
import traceback

from apps.Config import Config as configure

logging.config.fileConfig(fname='apps/Config/logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def get_s3_data_has_cur_data():
    """
    Read S3 config information from json file. 
    """
    try:
        with open('./apps/Config/S3Config.json', 'r') as fd:
            data = fd.read()
        info = json.loads(data)

        return info
    except Exception as e:
        traceback.print_exc()
        logger.error(f'Error during get_s3_data_has_cur_data - {e}')
        raise Exception

def get_companies_data():
    """
    Read Companies information from json file.
    """
    try:
        with open('./apps/Config/Companies.json', 'r') as fd:
            data = fd.read()
        companies = json.loads(data)
                
        return companies['Companies']
    except Exception as e:
        traceback.print_exc()
        logger.error(f'Error during get_companies_data - {e}')
        raise Exception
