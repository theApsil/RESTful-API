from flask import Flask

app = Flask(__name__)

from app.controllers import todo_controller
from app.views import todo_view
