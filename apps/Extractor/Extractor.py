import csv
import traceback
import logging.config
import os
from apps.Config import Config as configure

logging.config.fileConfig(fname='apps/Config/logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def make_tmp_folder_to_extract_result(temp_path):
    """
    Create folder to save extract result
    """
    target_path = os.path.join(temp_path, configure.RESULT_PATH)
    if not os.path.isdir(target_path):
        try:
            os.makedirs(target_path)
        except OSError:
            logger.error(f"Creation of the directory {target_path} failed")
            raise Exception("Creation of the directory {} failed" % target_path)
    logger.info("Successfully created the directory %s" % target_path)
    return target_path

def make_folder_for_company_result(path, target):
    """
    Create folder to save gzip result - under save extract result
    """
    target_path = os.path.join(path, target)
    if not os.path.isdir(target_path):
        try:
            os.makedirs(target_path)
        except Exception:
            logger.error(f"Creation of the directory {target_path} failed")
            raise Exception("Creation of the directory {} failed" % target_path)
    logger.info("Successfully created the directory %s" % target_path)
    return target_path

def extract_data_to_csv(source_path, account_id):
    """
    Extract data by account ID and save as csv
    """
    # Read source file
    fd = open(source_path, 'rt')
    reader = csv.reader(fd)
    source_folder_path = os.path.dirname(source_path)
    dst_folder_path = os.path.join(source_folder_path, configure.RESULT_PATH)

    dst_path = source_path.replace(source_folder_path, dst_folder_path)
    fw = open(dst_path, 'w', newline='')
    writer = csv.writer(fw)
    
    # Extract
    index = 0
    headers = []
    has_content = False
    for row in reader:
        if index == 0:
            headers = row
        else:
            obj = {}
            for i, val in enumerate(row):
                obj[headers[i]] = val
            # Write header
            if index == 1:
                writer.writerow(obj)
            # Write row if usage account matched
            if obj["lineItem/UsageAccountId"] in account_id:
                writer.writerow(row)
                if not has_content:
                    has_content = True
        index = index + 1
    if not fd.closed:
        fd.close()
    if not fw.closed:
        fw.close()
    
    # If not any row matched, raise ValueError to skip result
    if not has_content:
        raise ValueError

    return dst_path