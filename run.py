import sys
import os
# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from apps import app


### Run Main ======================================== 
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT'))