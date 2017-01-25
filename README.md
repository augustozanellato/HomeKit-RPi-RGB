#Simple RGB LED Controller

This example is a simple GPIO LED controller for the Raspberry Pi. It lets you turn a red, blue and green LED on and off through a Javascript powered Web-interface, yeah, I know its aesthetically awful, but hey, I'm a coder, not a designer :P

##Requirements

You'll need Python Flask and pigpio installed to run this example, install with:

```bash
sudo apt-get install python-pip
pip install flask
```

If you need to install pigpio:
```bash
wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make -j4
sudo make install
```

##Running

Start up with:

```bash
sudo pigpiod
python2 ./rgb.py
```

And then visit:

http://[your Pi address>]:5000
