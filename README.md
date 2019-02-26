# SIPALAGA Crawler
A web crawler to download the daily data from Sistem Pemantauan Air Lahan Gambut (SIPALAGA), Badan Restorasi Gambut (http://sipalaga.brg.go.id/) and convert it to csv format.

## Requirements

### Python
Python 3.x is needed to run the script. In Ubuntu, Mint, or Debian:
```bash
 sudo apt-get install python3 python3-pip
```

### OS Dependencies
The following dependencies are needed to run pdftotext (https://github.com/jalan/pdftotext). For Debian, Ubuntu, and friends:
```bash
sudo apt-get update
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev
```
### Packages

```bash
pip3 install pdftotext dateparser tabula-py
```
## Running the script
Clone this repository and execute `sipalaga_crawler.py` using python 3.x. The downloaded .pdf will be contained in `pdf` folder and the conversion to .csv in `csv` folder. `logfile.log` records the print statement from `sipalaga_crawler.py`.

It is recommended to run the script between 23:10 - 23:30 PM Western Indonesian Time (UTC +7) to get the full daily data.
