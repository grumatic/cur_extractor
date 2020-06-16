import json
import logging.config
import traceback
import os

from apps.Utils.JsonReader import get_s3_data_has_cur_data, get_companies_data
from apps.S3Handler.S3Handler import S3HandlerClass
from apps.Utils.GZIPHandler import decompress_gz_file, compress_gz_file
from apps.Extractor.Extractor import make_tmp_folder_to_extract_result, extract_data_to_csv, make_folder_for_company_result
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from apps.Config import Config as configure

logging.config.fileConfig(fname='apps/Config/logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def running_extract():
    logger.info('Start extract CUR data')
    # Get S3 access information from json
    cur_s3_info = get_s3_data_has_cur_data()
    # Get companies information from json
    companies = get_companies_data()

    # Download CUR data from S3
    cur_downloader = S3HandlerClass(
        access_key = cur_s3_info['AccessKey'],
        secret_key = cur_s3_info['SecretKey'],
        account_id = cur_s3_info['AccountId'])

    logger.info('Download CUR data from S3')
    cur_downloaded_files_path = cur_downloader.download_CUR_data(
        bucket_name = cur_s3_info['BucketName'],
        report_name = cur_s3_info['ReportName'],
        report_prefix = cur_s3_info['ReportPrefix']
    )

    logger.info('Decompress downloaded CUR files')
    # Decompress downloaded .gz files
    decompressed_files_list = []
    for cur_file in cur_downloaded_files_path:
        decompressed_file = cur_file.split('.gz')[0]
        decompress_gz_file(cur_file, decompressed_file)
        decompressed_files_list.append(decompressed_file)

    logger.info('Create folder to store extract result')
    # Make folder to store extract result
    result_path = make_tmp_folder_to_extract_result(
        cur_downloader.get_download_path(account_id = cur_s3_info['AccountId'])
        )

    logger.info('Extract CUR data')
    # Extract CUR data 
    for company in companies:
        csv_result_files = []
        gzip_target_folder_path = make_folder_for_company_result(result_path, company['Name'])

        # Extract CUR data
        for cur_csv_file in decompressed_files_list:
            try:
                csv_result_file_path = extract_data_to_csv(cur_csv_file, company['AccountId'])
            except ValueError:
                logger.error(f'There are no content with account id - {company["Name"]} - {os.path.split(cur_csv_file)[1]}')
                continue
            csv_result_files.append(csv_result_file_path)
        
        logger.info('Compress to GZIP')
        # Compress to GZIP file
        gzip_result = []
        for result in csv_result_files:
            gzip_target_file_path = result.replace(os.path.dirname(result), gzip_target_folder_path)            
            dst_file_path = compress_gz_file(result, gzip_target_file_path+'.gz')
            gzip_result.append(dst_file_path)

        # init S3 uploader
        cur_uploader = S3HandlerClass(
            access_key = company['AccessKey'],
            secret_key = company['SecretKey'],
            account_id = company['AccountId'][0]
        )
        logger.info('Upload cur data to company\' S3')
        for upload_target in gzip_result:
            # Upload file on S3
            try:
                cur_uploader.upload_CUR_data(
                    bucket_name = company['BucketName'], 
                    file_name = upload_target, 
                    parent_folder_path = gzip_target_folder_path)
            except Exception:
                continue

    # Remove temp folder
    if configure.NEED_REMOVE_TEMP:
        logger.info('Remove temp folder')
        cur_downloader.remove_download_temp_dir()

    logger.info('Extract and upload done')
    return True

# Scheduler running
scheduler = BackgroundScheduler()
scheduler.add_job(
    running_extract,
    CronTrigger.from_crontab(configure.RUNNING_INTERVAL)
)

try:
    scheduler.start()
except Exception as e:
    traceback.print_exc()
    logger.error("Error occured during schedule task'{}'".format(e))
