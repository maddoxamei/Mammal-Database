from flask import Blueprint, render_template

user = Blueprint('user', __name__)
@user.route('/greeting/<name>/')
def greeting(name):
	return render_template('greet.html', name=name)
	#return 'Hello, lowly normal user!'