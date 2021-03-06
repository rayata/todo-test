from flask import Flask
from flask_restful import Api
import logging
import os
from modules import db, resources
from flask_cors import CORS

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s-%(levelname)-8s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

logger.setLevel(logging.INFO)

todo_db = db.ManageTodoDB()
todo_db.create_db_struct()

app = Flask(__name__)
cors = CORS(app)

api = Api(app)


api.add_resource(resources.Tasks, '/tasks')
api.add_resource(resources.Users, '/users')
api.add_resource(resources.TasksDB, '/db')


port = os.getenv("PORT", 5001)
print(port)

if __name__ == '__main__':
    app.run(port=port, host="0.0.0.0", debug=True)
