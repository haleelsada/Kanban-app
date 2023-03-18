from .database import db


class Card(db.Model):
    __tablename__ = 'Card'
    Cid = db.Column(db.Integer, autoincrement=True, primary_key=True,nullable=False, unique=True)
    Title = db.Column(db.String)
    Content = db.Column(db.String)
    Deadline = db.Column(db.String)
    Created = db.Column(db.String)
    Mark_as_complete = db.Column(db.Integer)
    Uid = db.Column(db.Integer,db.ForeignKey("User.Uid"), nullable=False)
    Lid = db.Column(db.Integer,db.ForeignKey("List.Lid"), nullable=False)
    Last_modified = db.Column(db.String)
    Completed = db.Column(db.String)
	
class List(db.Model):
    __tablename__ = 'List'
    Lid = db.Column(db.Integer, autoincrement=True, primary_key=True,nullable=False, unique=True)
    Lname = db.Column(db.String)
    Discription = db.Column(db.String)
    Uid = db.Column(db.Integer,db.ForeignKey("User.Uid"), nullable=False)

class User(db.Model):
    __tablename__ = 'User'
    Uid = db.Column(db.Integer, autoincrement=True, primary_key=True,nullable=False, unique=True)
    Username = db.Column(db.String,unique=True) 
    Password = db.Column(db.String, unique=True )
    Card = db.relationship("Card")
    List = db.relationship("List")
 
 
 
'''   
engine = db.create_engine("sqlite:///./data.sqlite3",{})

# to get data
#for docs:https://docs.sqlalchemy.org/en/14/core/tutorial.html
#------------
stat=db.select(User)

print(stat)
with engine.connect() as conn:
	for i in conn.execute(stat):
		print(i)
		
print('-----------------')
with db.Session(engine) as session:
	User = session.query(User).filter (User.Uid == 1).all()
	for U in User:
		print("User:{} ".format(U.Username))
		for l in U.List:
			print("Author: {}".format(l.Lname))
			
# here in User even we dont have a column List with the relation we can extract from lists table
		'''
		
