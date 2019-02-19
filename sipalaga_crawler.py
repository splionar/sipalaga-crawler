from urllib.request import urlretrieve
import pdftotext
import datetime
import tabula
import os
import time
import re
import dateparser
import sys

def create_directory(*args):
    for directory in args:
        if not os.path.exists(directory):
            os.makedirs(directory)

def download_file(download_url, output_dir):
    urlretrieve(download_url, output_dir)

def check_pdf(dir):
    df_1 = tabula.read_pdf(dir, pages='all', pandas_options={'header': None})

    if len(df_1) < 4:
        with open(dir, "rb") as f:
            pdf = pdftotext.PDF(f)

        pdf_text = str(pdf[0]).split('\n')
        station = pdf_text[1].split(':')[-1][1:].replace(' ', '_')
        return(station)
    else:
        return(df_1)

def create_df(dir, df_1):
    with open(dir, "rb") as f:
        pdf = pdftotext.PDF(f)

    pdf_text = str(pdf[0]).split('\n')
    date_pdf_preformat = pdf_text[0].split(' ')[0]
    date_pdf = datetime.datetime.strptime(date_pdf_preformat, '%d-%m-%Y').strftime('%Y-%m-%d')
    date_table_preformat = pdf_text[6].split(',')[-1][1:]
    date_table = dateparser.parse(date_table_preformat).strftime('%Y-%m-%d')

    station = pdf_text[1].split(':')[-1][1:].replace(' ','_')
    location = pdf_text[2].split(':')[-1][1:].replace(' ','_')
    subdistrict = pdf_text[3].split(':')[-1][1:].replace(' ','_')
    district = pdf_text[4].split(':')[-1][1:].replace(' ','_')
    province = pdf_text[5].split(':')[-1][1:].replace(' ','_')

    df = df_1.iloc[3:].reset_index(drop=True)
    df2 = df.dropna(axis='columns')
    df2.insert(0,'date',date_table)
    df2.insert(1,'station',station)
    df2.insert(2,'location',location)
    df2.insert(3,'subdistrict',subdistrict)
    df2.insert(4,'district',district)
    df2.insert(5,'province',province)
    df_string = df2.to_string(header=None, index=False)
    df_string = re.sub(' +', ' ', df_string)
    df_string = df_string.replace(' ',',')
    df_string = df_string+'\n'

    header = 'date,station,location,subdistrict,district,province,time,gwater_mean,gwater_min,gwater_max,' \
             'smoisture_mean,smoisture_min,smoisture_max,precip_composite,precip_min,precip_max,status\n'

    return(df_string, header, date_pdf, province, station)

def append_csv(df_string, header, file_name):
    if os.path.isfile(file_name) == False:
        log = open(file_name, "w+")
        log.write(header)
        log.write(df_string)
        log.close()
    else:
        file = open(file_name, "a")
        file.write(df_string)
        file.close()

def rename_pdf(old_name,date_pdf,province,station):
    if not os.path.exists("pdf/{}".format(province)):
        os.makedirs("pdf/{}".format(province))

    os.rename(old_name, "pdf/{}/{}_{}.pdf".format(province,date_pdf,station))

def main():
    temp_dir = "pdf/temp.pdf"
    download_file(url, output_dir=temp_dir)
    df_1 = check_pdf(temp_dir)
    if type(df_1)== str:
        station = df_1
        os.remove(temp_dir)
        return("{} no data".format(station))
    else:
        df_string, header, date, province, station = create_df(temp_dir, df_1)
        append_csv(df_string, header, 'csv/{}.csv'.format(province))
        rename_pdf(temp_dir, date, province, station)
        return("{} downloaded and converted".format(station))

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

sys.stdout = Logger()

create_directory("pdf","csv")

print("\n"+str(datetime.datetime.now()))

for url_txt in os.listdir("url"):
    with open("url/{}".format(url_txt)) as f:
        url_list = f.readlines()
    url_list = [x.strip() for x in url_list]
    url_list = list(filter(None, url_list))

    count = 0
    for url in url_list:
        if count == 0:
            print("Processing files for {}".format(url_txt))
        message = main()
        count += 1
        print("{}/{} {}".format(count,len(url_list), message))
        time.sleep(3)