#!/usr/bin/python3.6
import os
from start_flask_webapp_with_virtual_env import reload_webapp

if __name__ == '__main__':
  domain = '{}.pythonanywhere.com'.format(os.getenv('USERNAME'))
  reload_webapp(domain)
