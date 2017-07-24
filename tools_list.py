domain = 'coolwebteacher.pythonanywhere.com'
tools = [{
   'domain' : domain,
   'title' : 'User Profile',
   'description' : 'User Profile Tool',
   'entry': 'lti_profile',
   'nav' : [
     {
     'type':'course_navigation',
     'enabled': True,
     'default':'enabled',
     'text': 'course navigation text',
     }
   ]
  },{ 
   'domain' : domain,
   'title' : 'Google Map Tool',
   'description' : 'This is the step 4 Google Map Tool',
   'entry': 'mapit_launch',
   'nav' : [
     {
     'type':'course_navigation',
     'enabled': True,
     'default':'enabled',
     'text': 'course navigation text',
     }
   ]
  },
  { 
   'domain' : domain,
   'title' : 'Choose own Gradel',
   'description' : 'This is the step 5 Choose own grade Tool',
   'entry': 'choose_own_grade',
  }
]
