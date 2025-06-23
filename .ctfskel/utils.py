import requests
import urllib3
import urllib
from pprint import pprint
from chepy import Chepy
from bs4 import BeautifulSoup
import re
import json
import paramiko
from paramiko.channel import ChannelStdinFile, ChannelFile, ChannelStderrFile


def ssh(host: str, port: int, username="", password="") -> paramiko.SSHClient:
    ssh_user = paramiko.SSHClient()
    ssh_user.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_user.connect(host, port, username, password)
    return ssh_user

# Make all the needful exportable
__all__ = [
    "requests",
    "urllib3",
    "urllib",
    "pprint",
    "BeautifulSoup",
    "re",
    "Chepy",
    "json",
]

__all__ += [
    "ssh",
]