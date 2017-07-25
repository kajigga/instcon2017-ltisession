"""
This file creates your application.
"""
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask import render_template_string
from flask import make_response
from pylti.flask import lti
from pylti.common import LTI_PROPERTY_LIST, LTI_ROLES
from tools_list import tools
import requests, urllib
from flask import jsonify

app = Flask(__name__)
app.debug = True
app.secret_key = 'a-really-long-should-be-unique-random-string'
G_API_KEY = 'AIzaSyBmuO_9hgtG24L_8GQYGUQx5EosQ25MF0M'

# Canvas sends some custom LTI launch parameters. Add these to the list of
# known parameters so that pylti will save them.
LTI_PROPERTY_LIST.extend([
  'custom_canvas_api_domain',
  'custom_canvas_course_id',
  'custom_canvas_enrollment_state',
  'custom_canvas_user_id',
  'custom_canvas_user_login_id',
  'ext_content_return_types',
  'ext_outcome_data_values_accepted',
  'ext_outcome_result_total_score_accepted',
  'ext_content_intended_use',
  'ext_content_return_url',
  'ext_content_file_extensions'
])
# Canvas uses full standard roles from the LTI spec. PYLTI does not include
# them by default so we add these to the list of known roles.

# NOTE: We can use my pylti package unless the main pylti maintainers accept my
# pull request

# This is the Administrator role and all of the different variations
LTI_ROLES[ 'urn:lti:instrole:ims/lis/Administrator' ] = [
 'urn:lti:instrole:ims/lis/Administrator',
 'urn:lti:sysrole:ims/lis/SysAdmin'
]

# This is the Instructor role
LTI_ROLES[ 'urn:lti:instrole:ims/lis/Instructor' ] = [ 'urn:lti:instrole:ims/lis/Instructor', ]

# This is the student role
LTI_ROLES[ 'urn:lti:instrole:ims/lis/Student' ] = [
 'urn:lti:instrole:ims/lis/Student',
 'urn:lti:instrole:ims/lis/Learner'
]
# LTI Consumers
consumers = {
 "abc123": {"secret": "secretkey-for-abc123"}
}

# Configure flask app with PYLTI config, specifically the consumers
app.config['PYLTI_CONFIG'] = {'consumers': consumers}

app.config['SERVER_NAME'] = 'coolwebteacher.pythonanywhere.com'
# Make sure app uses https everywhere. This will become important when there
# are actually LTI endpoints and configuration used.
#app.config['PREFERRED_URL_SCHEME'] = 'https'

@app.route('/')
def index():
    # "index.html" is a file found in the "templates" folder. It is mostly regular
    # HTML with some special templating syntax mixed in. The templating
    # language is called Jinja.
    return render_template('index.html')

@app.route('/hello_world')
def hello_world():
    return 'Hello World!'

def error(*args, **kwargs):
  # TODO Make a better Error Message screen
  return '{}'.format(kwargs['exception'])

@app.route('/lti/testlaunch', methods=['GET', 'POST'])
def lti_test_launch():
    # POST parameters
    return render_template('lti_test_launch.html', post=request.form,
        get=request.args)

@app.route('/lti/launch', methods=['POST'])
@lti(error=error, request='initial')
def first_lti_launch(lti, tool_id=None, *args, **kwargs):
  try:
    tool_id = int(request.args.get('tool_id', tool_id)) # parameters come in as strings convert this to an int
    return redirect(url_for(tools[tool_id]['entry'], _external=True, _scheme='https'))
  except Exception:
    # If we get to this point, no config id matches a known config.
    # redirect the user to the profile page
    return redirect(url_for('lti_profile', _external=True, _scheme='https'))

@app.route('/lti/profile', methods=['GET'])
@lti(error=error, request='session')
def lti_profile(lti, *args, **kwargs):
  return render_template('lti_profile.html')

@app.route('/lti/mapit')
@lti(error=error, request='session')
def mapit_launch(lti):
  # Don't forget to add the template file.
  return render_template('mapit_launch.html',G_API_KEY=G_API_KEY)

lorem_types = {
 'regular':{
 'name':'regular',
 'label':'Regular Lorem Ipsum text'
 },
 'with_bacon':{
 'name':'with_bacon',
 'label':'Bacon Ipsum - tasty but not so good looking'
 },
 'random_text':{
 'name':'random_text',
 'label':'Random Text'
 },
 'arresteddevelopment_quotes': {
 'name': 'arresteddevelopment_quotes',
 'label':'Quotes from Arrested Development'
 },
 'doctorwho_quotes':{
 'name':'doctorwho_quotes',
 'label':'Quotes from Dr. Who'
 },
 'dexter_quotes':{
 'name':'dexter_quotes',
 'label':'Quotes from Dexter'
 },
 'futurama_quotes':{
 'name':'futurama_quotes',
 'label':'Quotes from Futurama'
 },
 'holygrail_quotes':{
 'name':'holygrail_quotes',
 'label':'Quotes from Monty Python and the Holy Grail'
 },
 'simpsons_quotes':{
 'name':'simpsons_quotes',
 'label':'Quotes from the Simpsons'
 },
 'starwars_quotes':{
 'name':'starwars_quotes',
 'label':'Quotes from Star Wars'
 }}

@app.route('/lti/baconipsum/choose', methods=['GET', 'POST'])
#@lti(error=error, request='session')
def baconIpsumChoose(*args, **kwargs):
  if request.method == 'GET':
    # Prompt the user to select the size of the bacon
    return render_template('baconIpsumChoose.html', lorem_types=lorem_types)

  elif request.method=='POST':
    # Then do an api request to http://baconipsum.com/api/
    # to get some bacon.  Write the text to a file and return to the LTI "on done" url"
    # TODO This needs to be fixed to  be
    # an oEmbed link.  i.e. http://oembed.com/
    #
    # https://canvas.instructure.com/doc/api/editor_button_tools.html

    # For some reason, we can't use https here... see
    # canvas-lms/app/controllers/external_content_controller.rb
    red_args = {'oembed' :{
        'url':     url_for('baconIpsumFetch', _external=True, _scheme='https', args=['lkjlkjlk']),
        'endpoint':'',
        'width':'400',
        'height':'400',
        'embed_type':'oembed',
        },
    'link': { # works
        'url':     url_for('baconIpsumFetch', _external=True, _scheme='https',args=['lkjlkjlk']),
        'title':'this is the title',
        'text':'link text',
        'embed_type':'link'
        },
    'img': { # works
        # Other options:
        # - http://placehold.it/
        # - http://www.webresourcesdepot.com/8-free-placeholder-image-services-for-instant-dummy-images/
        'url':     'https://placekitten.com/g/%d/%d',
        'title':'this is the title',
        'alt': 'random kitten',
        'embed_type':'image',
        'width':300,
        'height':250
      },
    'iframe': { # works, the iframe is created but something on the
                # Canvas side is borking up the iframe code
        'return_type':'iframe',
        'embed_type':'iframe',
        }
    }

    success_url = session.get('launch_presentation_return_url','')

    #redirect_url = success_url % urllib.urlencode(red_args['oembed'])
    wanted_type = request.form.get('wanted_type','oembed')
    if wanted_type in red_args.keys():
      #redirect_url = success_url % urllib.urlencode(red_args['img'])
      if wanted_type == 'img':
        height = int(request.args.get('height',100))
        width  = int(request.args.get('width',100))
        red_args['img']['url'] = red_args['img']['url'] % (height,width)
        red_args['img']['height'] = height
        red_args['img']['width']  = width
      elif wanted_type == 'iframe':
        height = request.form.get('iframe_height',100)
        width  = request.form.get('iframe_width',100)
        red_args['iframe']['url'] = request.form.get('iframe_url')
        red_args['iframe']['title'] = request.form.get('iframe_title')
        red_args['iframe']['height'] = height
        red_args['iframe']['width']  = width
      elif wanted_type == 'link':
        pass
      elif wanted_type == 'oembed':
        show = request.form.get('show','none')
        url_for('baconIpsumFetch', _external=True, _scheme='https',args=['lkjlkjlk'])
        red_args['oembed']['endpoint'] = url_for('baconIpsumFetch', _external=True, _scheme='https',**dict(request.form))
        red_args['oembed']['url'] = red_args['oembed']['endpoint'] #.replace('https','http')

      redirect_url = success_url +"?"+ urllib.urlencode(red_args[wanted_type])
    return redirect(redirect_url)

# Make sure you don't include the @lti decorator on this route. Canvas won't be
# able to request the information otherwise.

# Make sure you don't include the @lti decorator on this route. Canvas won't be
# able to request the information otherwise.

@app.route('/lti/baconipsum/fetch')
def baconIpsumFetch(*args,**kwargs):
  num_para = int(request.args.get('num_para',5))
  lorem_type = request.args.get('lorem_type','regular').lower()
  show = request.args.get('show','none').lower()
  resp = {
  'version': '1.0',
  'type': 'rich',
  'width': '240',
  'height': '160',
  'provider_name': 'BaconIpsum',
  'html':'<p>lkjlkjlkj</p>'
  }


  #print 'with_bacon', with_bacon
  if lorem_type == 'with_bacon':
    # Now get the bacon ipsum
    bacon_url = "http://baconipsum.com/api/?type=meat-and-filler&paras=%d&start-with-lorem=0" % num_para

    try:
      paragraphs = requests.get(bacon_url).json()
      # paragraphs = json_decode('%s' % bacon_response)
    except Exception,err:
      print 'err',err
      bacon_response = "Hello, this is an error."
      bacon_response = ''.join(bacon_response.splitlines())
      paragraphs = ['',]
    resp['html'] = "<p>%s</p>" % "</p><p>".join(paragraphs)
  elif lorem_type == 'random_text':
    lorem_url = 'http://randomtext.me/api/lorem/p-{}/5-15/'.format(num_para)

    try:
      paragraphs = requests.get(bacon_url).json()
      # paragraphs = json_decode('%s' % bacon_response)
    except Exception,err:
      print 'err',err
      paragraphs = ['']
    resp['html'] = paragraphs['text_out']
  elif '_quotes' in lorem_type:
    show = lorem_type.replace('_quotes', '')
    fillerama_url = "http://api.chrisvalleskey.com/fillerama/get.php?count=10&format=json&show=%s" % show
    response = requests.get(fillerama_url).json()
    paragraphs = [x['quote'] for x in response['db']]
    resp['html'] = render_template('show_quotes.html', paragraphs=response['db'], lorem=lorem_types[lorem_type])
  elif lorem_type == 'regular':
    # No bacon wanted, get regular Lorem Ipsum
    options = ['short','headers','decorate','link','ul','ul','dl','bq']
    lorem_url = "http://loripsum.net/api/%d/%s" % (num_para,'/'.join(options))
    paragraphs = requests.get(lorem_url).text
    paragraphs = paragraphs.replace('loripsum.net', 'canvaslms.com')
    resp['html'] = paragraphs

  #return render_template('baconIpsumFetch.html',paragraphs=paragraphs)
  if request.args.get('html','no')=='yes':
    return render_template('baconIpsumFetch.html',dict(paragraphs=paragraphs))
  else:
    return jsonify(resp)

@app.route('/lti/choose_own_grade')
@lti(error=error, request='session')
def choose_own_grade(lti):
#def choose_own_grade():
  # Don't forget to add the template file.
  return render_template('choose_own_grade_clicks.html')

@app.route('/lti/choose_own_grade_selected', methods=['POST'])
@lti(session='session')
def choose_own_grade_selected(lti):
  resp = lti.post_grade(float(request.form.get('percentage'))/100.0) 
  return jsonify({'response': resp})

@app.route('/lti/config/list')
def lti_config_list():
  # Get list of tools and display them all on a page
  return render_template('lti_config_list.html', tools=tools)

@app.route('/lti/config/<int:tool_id>')
def lti_config(tool_id):
  tool_id = int(tool_id)
  tool_config = tools[tool_id]
  tool_config['url'] = url_for('first_lti_launch', _external=True, _scheme='https', tool_id=tool_id)
  config_xml = render_template('xml/config.xml', tool=tool_config)
  response = make_response(config_xml)
  response.headers["Content-Type"] = "application/xml"
  return response

# I like to make certain values available on any rendered template without
# explicitly naming them. While these values won't change very often, I would
# rather not keep track of where they are used so I don't have to remember to
# change the value everywhere.  Programmers are lazy :)
@app.context_processor
def inject_app_info():
  return {
      'version': 'Step 3',
      'project_name': 'Instcon 2017 - Developing LTI Tools'
      }

if __name__ == '__main__':
  ''' IP and PORT are two environmental variables configured in Cloud9. They
  can change occasionally without warning so the application must be able to
  dynamically detect the change on each startup. Reasonable default values of
  hostname 0.0.0.0 and port 5000 are set as well.'''

  app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',5000)))
