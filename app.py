from flask import Flask
from routes.home import home
from routes.usuarios import usuario

app = Flask(__name__) 

app.register_blueprint(home)
app.register_blueprint(usuario, url_prefix ='/usuario')



app.run(debug=True)
