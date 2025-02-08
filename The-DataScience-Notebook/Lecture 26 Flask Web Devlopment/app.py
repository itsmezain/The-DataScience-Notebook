from flask import Flask

app = Flask(__name__) # => object bna liya flask app ka 

@app.route('/') # => URL bna liya / ka aur niche wla function activate ho jayega 
def index():
    return "<h1 style='color:green'>Hello</h1>"
    
app.run(debug=True) # => Debug = True use iss liye jisse real time update reflect ho website par testing ke liye
