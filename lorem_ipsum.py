from flask import Blueprint, render_template
from flask import jsonify
from flask import request, redirect, url_for, session
from pylti.flask import lti

import urllib
import requests
from common import error

lorem_ipsum = Blueprint('lorem_ipsum', __name__, template_folder='templates')

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

@lorem_ipsum.route('/lti/baconipsum/choose', methods=['GET', 'POST'])
@lti(error=error, request='session')
def baconIpsumChoose(lti, *args, **kwargs):
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

@lorem_ipsum.route('/lti/baconipsum/fetch')
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

