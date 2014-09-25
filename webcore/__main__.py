
from flask import Flask
import webcore

if __name__ == "__main__":
    webcore.index.app.run(debug=True,host='0.0.0.0')
