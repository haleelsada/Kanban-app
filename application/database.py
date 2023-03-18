from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import os

engine = None
Base = declarative_base()
db = SQLAlchemy()
