import os
from start_flask_webapp_with_virtualenv import reload_webapp

if __name__ == '__main__': 
  domain = '{}.pythonanywhere.com'.format(os.getenv('USERNAME'))
  reload_webapp(domain)
