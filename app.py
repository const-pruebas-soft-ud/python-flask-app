import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)

# Contadores de visitas
visit_count = 0
greeting_count = 0


@app.route('/')
def index():
   global visit_count
   visit_count += 1
   print('Request for index page received')
   return render_template('index.html', visits=visit_count)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   global greeting_count
   name = request.form.get('name')

   if name:
       greeting_count += 1
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name=name, greetings=greeting_count)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(port=80)
