import os, sys
from datetime import date, timedelta, datetime
import logging

import utils.lib_gen as gen
import utils.mdl_logger
import qsfc.ReadQsfc_WriteLocDb as qsfc_mdl
import aoi.ReadAoi_WriteLocDb as aoi_ml
from utils.mdl_logger import setup_logger

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # -> ...\GCC_Project
#this_folder = os.path.dirname(os.path.abspath(__file__)) # -> ...\GCC_Project\Read_DataBases
this_folder = os.path.abspath('//prod-svm1/tds/gcc/db')
#print(tds_db_folder)
#exit(0)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from utils.sql_db_rw import SqliteDB
from utils.lib_gen import timer

setup_logger('read_dbs_log.html')
logger = logging.getLogger(__name__)
# logger = utils.mdl_logger.get_logger(__name__, 'read_dbs_log.html')


def read_qsfc_data_bases():
    sql_obj = SqliteDB()
    #sql_obj.db_name(os.path.join(PROJECT_ROOT, 'qsfc'), 'db_qsfc.db') # -> ...\GCC_Project\qsfc\db_qsfc.db
    sql_obj.db_name(this_folder, 'db_qsfc.db')  # -> ...\GCC_Project\Read_DataBases\db_qsfc.db

    qsfc = qsfc_mdl.Qsfc()
    qsfc.print_rtext = True
    df = []
    for tbl_name in ['Prod', 'RMA']:
        last_date = sql_obj.get_last_date(tbl_name, 'open_date')
        gen_obj = gen.FormatDates()
        date_from_string = gen_obj.get_next_day(last_date)
        print(f'{tbl_name}: last_date:{last_date}  date_from_string:{date_from_string} today_date_string:{today_date_string}')
        date_from_obj = datetime.strptime(date_from_string, '%d/%m/%Y')
        today_date_obj = datetime.strptime(today_date_string, '%d/%m/%Y')
        print(f'date_from_obj:{date_from_obj} today_date_obj:{today_date_obj}')
        if date_from_obj >= today_date_obj:
            log_txt = f'QSFC Data from {tbl_name} up to {date_from_string} is already inserted'
            logger.info(log_txt)
        else:
            df = qsfc.get_data_from_qsfc(tbl_name, date_from_string, today_date_string)
            if len(df) == 0:
                log_txt = f'No new data for {tbl_name} between {date_from_string} and {today_date_string}'
                logger.warning(log_txt)
            elif df[0] is False:
                log_txt = f'Error during get QSFC {tbl_name} Data, {df[1]}'
                logger.error(log_txt)
            else:
                sql_obj.fill_table(tbl_name, df)
                log_txt = (f'QSFC Data from {tbl_name} between {date_from_string} and {today_date_string} '
                           f'has been inserted successfully')
                logger.info(log_txt)

    return 0

def read_aoi_data_bases():
    aoi = aoi_ml.Aoi()
    aoi.print_rtext = True

    sql_obj = SqliteDB()
    #sql_obj.db_name(os.path.join(PROJECT_ROOT, 'aoi'), 'db_aoi.db') # -> ...\GCC_Project\aoi\db_aoi.db
    sql_obj.db_name(this_folder, 'db_aoi.db')  # -> ...\GCC_Project\Read_DataBases\db_aoi.db
    last_date = sql_obj.get_last_date('AOI_data', 'test_time_formatted')
    gen_obj = gen.FormatDates()
    date_from_string = gen_obj.get_next_day(last_date)
    print(f'last_date:{last_date} date_from_string:{date_from_string} today_date_string:{today_date_string}')
    date_from_obj = datetime.strptime(date_from_string, '%d/%m/%Y')
    today_date_obj = datetime.strptime(today_date_string, '%d/%m/%Y')
    print(f'date_from_obj:{date_from_obj} today_date_obj:{today_date_obj}')
    if date_from_obj >= today_date_obj:
        log_txt = (f'AOI Data up to {date_from_string} is already inserted')
        logger.info(log_txt)
    else:
        df = aoi.get_data_from_aoi(date_from_string, today_date_string)
        if len(df) == 0:
            log_txt = f'No new data for AOI between {date_from_string} and {today_date_string}'
            logger.warning(log_txt)
        elif df[0] is False:
            log_txt = f'Error during get AOI Data, {df[1]}'
            logger.error(log_txt)
        else:
            # db_path = this_folder # os.path.join(PROJECT_ROOT, 'aoi')
            # db_file_name = f'db_aoi.db'
            # sql_obj = SqliteDB()
            # sql_obj.db_name(db_path, db_file_name)
            sql_obj.fill_table("AOI_data", df)
            log_txt = f'AOI Data between {date_from_string} and {today_date_string} has been inserted successfully'
            logger.info(log_txt)

    return 0


if __name__ == '__main__':
    today_date_string = date.today().strftime('%d/%m/%Y')
    logger.info('\n')
    read_qsfc_data_bases()
    read_aoi_data_bases()



