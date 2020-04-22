from flask import Flask, render_template, Blueprint, redirect, url_for, request
from blueprints.admin import admin
from blueprints.user import user

app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')

#@app.route("/")
#@app.route("/home")
def home():
	return render_template('home.html')

#@app.route("/about")
def about():
	return "<h1> About Page <h1>"

@app.route('/student')
def student():
   return render_template('student.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)

#@app.route('/user/<name>/', endpoint = 'user')
def greet(name):
	#return render_template('greet.html', name=name)

	if name == 'admin':
		return redirect(url_for('admin.greeting'))
	else:
		return redirect(url_for('user.greeting', name=name))


@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/success', methods = ['POST', 'GET'])
def success():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('greet',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('greet',name = user))



#app.add_url_rule('/', '', home)
app.add_url_rule('/home/', 'home', home)
app.add_url_rule('/about/', 'about', about)
app.add_url_rule('/user/<name>/', 'greet', greet)

# set FLASK_APP=flaskblog.py
# flask run
# set FLASK_DEBUG=1
if __name__ == '__main__': #if running script directly
	app.run(debug=True)
