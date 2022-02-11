curl.exe -o python_installer.exe https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe
start /wait python_installer.exe
del python_installer.exe
curl.exe -o get-pip.py https://bootstrap.pypa.io/get-pip.py
python get-pip.py
del get-pip.py
pip install --upgrade pip
pip install -r requirements.txt
