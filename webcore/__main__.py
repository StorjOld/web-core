
from flask import Flask
#import index

app = Flask('index')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
