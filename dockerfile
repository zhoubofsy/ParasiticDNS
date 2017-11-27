
from centos:7.4.1708

add ./get-pip.py /root/get-pip.py

run python /root/get-pip.py

run pip install pylru dnslib gevent

workdir /root/dns

