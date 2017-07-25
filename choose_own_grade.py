from flask import Blueprint, render_template
from pylti.flask import lti
from flask import jsonify

choose_grade = Blueprint('choose_grade', __name__,
  template_folder='templates')

@choose_grade.route('/lti/choose_own_grade')
@lti(error=error, request='session')
def choose_own_grade(lti):
#def choose_own_grade():
  # Don't forget to add the template file.
  return render_template('choose_own_grade_clicks.html')

@choose_grade.route('/lti/choose_own_grade_selected', methods=['POST'])
@lti(session='session')
def choose_own_grade_selected(lti):
  resp = lti.post_grade(float(request.form.get('percentage'))/100.0) 
  return jsonify({'response': resp})
