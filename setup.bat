curl.exe -o python_installer.exe https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe
start /wait python_installer.exe
del python_installer.exe

curl.exe -o get-pip.py https://bootstrap.pypa.io/get-pip.py
python get-pip.py
del get-pip.py
pip install --upgrade pip

curl.exe -o game.py https://raw.githubusercontent.com/DivingMad/Bingo/main/game.py
curl.exe -o requirements.txt https://raw.githubusercontent.com/DivingMad/Bingo/main/requirements.txt

pip install -r requirements.txt

mkdir pieces
cd pieces
curl.exe -o king.jpg https://raw.githubusercontent.com/DivingMad/Bingo/main/pieces/king.jpg
curl.exe -o tank.jpg https://raw.githubusercontent.com/DivingMad/Bingo/main/pieces/tank.jpg
curl.exe -o assassin.jpg https://raw.githubusercontent.com/DivingMad/Bingo/main/pieces/assassin.jpg
curl.exe -o thresh.jpg https://raw.githubusercontent.com/DivingMad/Bingo/main/pieces/thresh.jpg
