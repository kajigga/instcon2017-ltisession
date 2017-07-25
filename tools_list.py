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
  },{
     'domain' : domain,
     'title' : 'Lorem Ipsum',
     'description' : '''This is the step 6 LTI Tool, which enables a richtext
     editor button that, when clicked, allows the user to insert a Lorem Ipsum
     text snippet.''',
     'editor_button':{
         'icon_url':'https://dl.dropboxusercontent.com/u/1647772/lorem.png',
         "selection_width":550,
         "selection_height":400
     }
 }
]
