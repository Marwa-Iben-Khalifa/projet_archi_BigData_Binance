from datetime import datetime
from datetime import timedelta
from multiprocessing.pool import ThreadPool as Pool
import multiprocessing
import wget
import zipfile
from pathlib import Path
import os

# Globals vars
#path = '/home/jovyan/work/data/'
global path
path = '/work/data/'
#path = '/home/ivanb/Documents/testcryptos/'

crypto_list = [
    'BNBBUSD',
    'ETHBUSD',
    'BTCBUSD',
    'AVAXBUSD',
    'MATICBUSD',
    'SOLBUSD'
]

# Process size
pool_size = int((multiprocessing.cpu_count()*2))
# Initialise pool
pool = Pool(pool_size)

for coin in crypto_list:

    # Dates
    end_date = datetime.now()
    start_date = datetime.now()+timedelta(days= -(365*2))
    
    # Create folder if not exists
    folder_name = path

    while start_date < end_date:
        # Increment one day
        def download_and_unzip(my_date, coin_name, folder_nm):
            def return_good_format(val):
                if len(str(val)) == 1:
                    return '0'+str(val)
                else:
                    return str(val)

            _y = return_good_format(my_date.year)
            _m = return_good_format(my_date.month)
            _d = return_good_format(my_date.day)

            _url = 'https://data.binance.vision/data/spot/daily/klines/'+coin_name+'/4h/'+coin_name+'-4h-'+_y+'-'+_m+'-'+_d+'.zip'
            file_name = coin_name+'-4h-'+_y+'-'+_m+'-'+_d

            try:
                print(file_name)
                wget.download(_url, folder_nm+'/'+file_name)
                # Extract zip
                with zipfile.ZipFile(folder_nm+'/'+file_name, 'r') as zip_ref:
                    zip_ref.extractall(folder_nm)
                if os.path.exists(folder_nm+'/'+file_name):
                    os.remove(folder_nm+'/'+file_name)
            except ValueError:
                pass

        # try:
        #     download_and_unzip(start_date, coin, folder_name)
        # except:
        #     pass
        pool.apply_async(download_and_unzip, (start_date, coin, folder_name,))

        start_date = start_date+timedelta(days=1)

    
pool.close()
pool.join()


print('End dl')