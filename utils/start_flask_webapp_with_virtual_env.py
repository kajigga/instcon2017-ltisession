#!/usr/bin/python3.6
"""Create a new Flask webapp with a virtualenv.  Defaults to
your free domain, the latest version of Flask and Python 3.5

Usage:
  pa_start_flask_webapp_with_virtualenv.py [--domain=<domain> --flask=<flask-version> --python=<python-version>] [--nuke]

Options:
  --domain=<domain>         Domain name, eg www.mydomain.com   [default: your-username.pythonanywhere.com]
  --flask=<flask-version> Flask version, eg "1.8.4"  [default: latest]
  --python=<python-version> Python version, eg "2.7"    [default: 3.6]
  --nuke                    *Irrevocably* delete any existing web app config on this domain. Irrevocably.
"""

from docopt import docopt
import getpass
import os
import requests
import shutil
import subprocess
from textwrap import dedent

# from snakesay import snakesay


API_ENDPOINT = 'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/'
PYTHON_VERSIONS = {
    '2.7': 'python27',
    '3.4': 'python34',
    '3.5': 'python35',
    '3.6': 'python36',
}

class SanityException(Exception):
    pass


class AuthenticationError(Exception):
    pass



def call_api(url, method, **kwargs):
    response = requests.request(
        method=method,
        url=url,
        headers={'Authorization': 'Token {}'.format(os.environ['API_TOKEN'])},
        **kwargs
    )
    if response.status_code == 401:
        print(response, response.text)
        raise AuthenticationError('Authentication error {} calling API: {}'.format(
            response.status_code, response.text
        ))
    return response



def _virtualenv_path(domain):
    return os.path.join(os.environ['WORKON_HOME'], domain)


def _project_folder(domain):
    return os.path.expanduser('~/' + domain)

def sanity_checks(domain, nuke):
    print('Running sanity checks')
    token = os.environ.get('API_TOKEN')
    if not token:
        raise SanityException(dedent(
            '''
            Could not find your API token.
            You may need to create it on the Accounts page?
            You will also need to close this console and open a new one once you've done that.
            '''
        ))

    if nuke:
        return
    url = API_ENDPOINT.format(username=getpass.getuser()) + domain + '/'
    response = call_api(url, 'get')
    if response.status_code == 200:
        raise SanityException('You already have a webapp for {}.\n\nUse the --nuke option if you want to replace it.'.format(domain))
    if os.path.exists(_virtualenv_path(domain)):
        raise SanityException('You already have a virtualenv for {}.\n\nUse the --nuke option if you want to replace it.'.format(domain))
    project_folder = _project_folder('instcon2017')

def create_virtualenv(name, python_version, flask_version, nuke):
    print(f'Creating virtualenv with Python{python_version}')

    command = 'mkvirtualenv --python=/usr/bin/python{python_version} {name}'.format(
        name=name, python_version=python_version)
    if nuke:
        command = 'rmvirtualenv {name} && {old_command}'.format(
            name=name, old_command=command
        )
    subprocess.check_call(['bash', '-c', 'source virtualenvwrapper.sh && {}'.format(command)])
    return _virtualenv_path(name)


def start_flask_project(domain, virtualenv_path, nuke):
    print('Starting Flask project')
    return _project_folder(domain)



def create_webapp(domain, python_version, virtualenv_path, project_path, nuke):
    print('Creating web app via API')
    if nuke:
        webapp_url = API_ENDPOINT.format(username=getpass.getuser()) + domain + '/'
        call_api(webapp_url, 'delete')
    post_url = API_ENDPOINT.format(username=getpass.getuser())
    patch_url = post_url + domain + '/'
    response = call_api(post_url, 'post', data={
        'domain_name': domain, 'python_version': PYTHON_VERSIONS[python_version]},
    )
    if not response.ok or response.json().get('status') == 'ERROR':
        raise Exception('POST to create webapp via API failed, got {}:{}'.format(response, response.text))
    response = call_api(patch_url, 'patch', data={'virtualenv_path': virtualenv_path})
    if not response.ok:
        raise Exception('PATCH to set virtualenv path via API failed, got {}:{}'.format(response, response.text))



def add_static_file_mappings(domain, project_path):
    print('Adding static files mappings for /static/ and /media/')

    url = API_ENDPOINT.format(username=getpass.getuser()) + domain + '/static_files/'
    call_api(url, 'post', json=dict(
        url='/static/', path=os.path.join(project_path, 'static')
    ))
    call_api(url, 'post', json=dict(
        url='/media/', path=os.path.join(project_path, 'media')
    ))




def update_wsgi_file(wsgi_file_path, project_path):
    print(f'Updating wsgi file at {wsgi_file_path} with project_path {project_path}')

    template = open(os.path.join(os.path.dirname(__file__), 'wsgi_file_template.py')).read()
    with open(wsgi_file_path, 'w') as f:
        f.write(template.format(project_path=project_path))



def reload_webapp(domain):
    print(print(f'Reloading {domain} via API'))
    url = API_ENDPOINT.format(username=getpass.getuser()) + domain + '/reload/'
    response = call_api(url, 'post')
    if not response.ok:
        raise Exception('POST to reload webapp via API failed, got {}:{}'.format(response, response.text))



def main(domain, flask_version, python_version, nuke):
    if domain == 'your-username.pythonanywhere.com':
        username = getpass.getuser().lower()
        domain = '{}.pythonanywhere.com'.format(username)
    sanity_checks(domain, nuke=nuke)
    virtualenv_path = create_virtualenv(domain, python_version, flask_version, nuke=nuke)
    project_path = start_flask_project('instcon2017', virtualenv_path, nuke=nuke)

    # TODO Make sure this works with the Flask App
    create_webapp(domain, python_version, virtualenv_path, project_path, nuke=nuke)
    add_static_file_mappings(domain, project_path)
    #wsgi_file_path = '/var/www/' + domain.replace('.', '_') + '_wsgi.py'
    wsgi_file_path = '/var/www/' + domain.replace('.', '_') + '_wsgi.py'
    update_wsgi_file(wsgi_file_path, project_path)
    reload_webapp(domain)

    print(print(f'All done!  Your site is now live at https://{domain}'))



if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments['--domain'], arguments['--flask'], arguments['--python'], nuke=arguments.get('--nuke'))

