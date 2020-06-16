import gzip
import shutil
import traceback
import logging.config

from apps.Config import Config as configure

logging.config.fileConfig(fname='apps/Config/logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def decompress_gz_file(src_file_name, dst_file_name):
    """ 
    Decomperess .gz file to .csv file
    """ 
    try:
        with gzip.open(src_file_name, 'rb') as f_in:
            with open(dst_file_name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except Exception as e:
        traceback.print_exc()
        logger.error(f'Error during decompress_gz_file - {e}')
        raise Exception

def compress_gz_file(src_file_name, dst_file_name):
    """
    Compress .gz file with .csv file
    """
    try:
        with open(src_file_name, 'rb') as f_in, gzip.open(dst_file_name, 'wb') as f_out:
            f_out.writelines(f_in)
    except Exception as e:
        traceback.print_exc()
        logger.error(f'Error during compress_gz_file - {e}')
        raise Exception
    if not f_out.closed:
        f_out.close()
    
    return dst_file_name
