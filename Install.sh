sudo apt install python3
sudo apt install pip
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg
sudo pip install pyaudio
sudo pip3 install PyQt5
sudo pip3 install vosk
sudo pip3 install pynput
sudo apt-get install --reinstall libxcb-xinerama0
sudo apt-get install python3-PyQt5
sudo apt install chrome-gnome-shell
sudo apt install gnome-tweak-tool
sudo apt install git
sudo apt-get remove libportaudio2
sudo apt-get install libasound2-dev
git clone -b alsapatch https://github.com/gglockner/portaudio
cd portaudio
./configure && make
sudo make install
sudo ldconfig
cd ..
sudo pip3 install pyaudio
sudo pip install fuzzywuzzy
