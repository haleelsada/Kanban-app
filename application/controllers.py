
from flask import Flask, request, redirect, session, url_for
from flask import render_template
from flask import current_app as app
from application.models import *
import json
from .functions import *
from datetime import datetime

@app.route("/", methods=["GET", "POST"])
def login():
	if request.method == 'POST':
		name=request.form['name']
		password=request.form['password']
		
		
		users=db.session.query(User).filter(User.Username == name).all()
		
		
		if len(users)!=0 and users[0].Password==password:
			uid=users[0].Uid

			messages = json.dumps([name,uid])
			session['messages'] = messages
			return redirect(url_for('.board',uid=uid))
		else:
			return render_template('notfound.html')
	return render_template("login.html")
	
@app.route("/board/<uid>", methods=["GET", "POST"])
def board(uid):
	messages = session['messages']
	messages=json.loads(messages)
	name=messages[0]
	uid=messages[1]
	
	lists=db.session.query(List).filter(List.Uid == uid).all()
	cards= db.session.query(Card).filter(Card.Uid == uid).all()
	return render_template("board.html",name=name, uid=uid,cards=cards,lists=lists)
	

@app.route("/summary/<uid>")
def summary(uid):
	name=db.session.query(User).filter(User.Uid == uid).first().Username
	lists=db.session.query(List).filter(List.Uid == uid).all()
	cards= db.session.query(Card).filter(Card.Uid == uid).all()
	table1,table2,table3=[],[],[]
	
	c,d,p=0,0,0
	for i in lists:
		li=[i.Lname,len([0 for j in cards if j.Lid==i.Lid]),len([0 for j in cards if j.Lid==i.Lid and j.Mark_as_complete=='Yes'])]
		if li[1]==0:n=0
		else:n=int(li[2]/li[1]*100)
		c,d,=c+li[1],d+li[2]	
		li.append(n)
		li.append(len([0 for j in cards if j.Lid==i.Lid and deadline(j.Deadline)<0]))
		
		p+=li[-1]

		table1.append(li)
		li2=li.copy()
		li2.append(len([0 for j in cards if j.Lid==i.Lid and deadline(j.Deadline)<0]))
		table2.append(li2)
		for j in cards:
			if i.Lid==j.Lid:
				#fig2(j)
				merged_name=i.Lname+'-'+j.Title
				merged_name=merged_name.replace(' ','_')
				ci=[merged_name,j.Title,j.Content,j.Mark_as_complete,j.Created,j.Deadline,j.Last_modified,j.Completed]
				table3.append(ci)
	if c!=0:li=['Total',c,d,int((d/c)*100),p]
	else:li=['Total',c,d,0,p]
	table1.append(li)
	print(len(cards))
	#print('this is len')
	table4=chart(cards)
	#print('this is table4\n',table4)
	return render_template("summary.html",name=name,uid=uid,lists=lists,cards=cards,table1=table1,table2=table2,table3=table3,table4=table4)
	
@app.route("/logout")
def logout():	
	return redirect(url_for('.login'))
	

@app.route("/newlist/<uid>", methods=['GET','POST'])
def newlist(uid):	
	name=db.session.query(User).filter(User.Uid == uid).first().Username
	if request.method == 'POST':
		
		if request.form.get('save')=='Save':
			list1=List(Lname=request.form['listname'],Discription=request.form['discription'],Uid=uid)
			db.session.add(list1)
			db.session.commit()
			return redirect(url_for('.board',uid=uid))
			print('new list created')
	return render_template("newlist.html",name=name,uid=uid)


@app.route("/newcard/<uid>/<lid>", methods=['GET','POST'])
def newcard(uid,lid):	
	name=db.session.query(User).filter(User.Uid == uid).first().Username
	if request.method == 'POST':
		
		if request.form.get('save')=='Save':

			title,content,deadline,flag=request.form['cardname'],request.form['content']\
				,request.form['deadline'],request.form['completed']
			time=datetime.today().strftime('%Y-%m-%d')
			if request.form['completed']=='Yes':
				completed = time
			else: completed = None
			
			card=Card(Title=title,Content=content,Deadline=deadline,Created=time,\
				Mark_as_complete=flag,Uid=uid,Lid=lid,Last_modified=time,Completed=completed)
			
			
			db.session.add(card)
			db.session.commit()
			
			return redirect(url_for('.board',uid=uid))
	
	return render_template("newcard.html",name=name,uid=uid)
	
	
@app.route("/editlist/<uid>/<lid>", methods=['GET','POST'])
def editlist(uid,lid):	
	name=db.session.query(User).filter(User.Uid == uid).first().Username
	listt=db.session.query(List).filter(List.Lid == lid).first()
	if request.method == 'POST':
		
		if request.form.get('save')=='Save':
			list1=db.session.query(List).filter(List.Lid == lid).first()
			
			list1.Lname=request.form['listname']
			list1.Discription=request.form['discription']
			
			db.session.commit()
			return redirect(url_for('.board',uid=uid))
			
		if request.form.get('delete')=='Delete':
			list1=db.session.query(List).filter(List.Lid == lid).first()
			
			db.session.delete(list1)
			cards=db.session.query(Card).filter(Card.Lid == lid).all()
			for i in cards:
				db.session.delete(i)
			db.session.commit()
			return redirect(url_for('.board',uid=uid))
			
			
	
	return render_template("editlist.html",name=name,uid=uid,lid=lid,listt=listt)

	
@app.route("/editcard/<uid>/<cid>", methods=['GET','POST'])
def editcard(uid,cid):	
	name=db.session.query(User).filter(User.Uid == uid).first().Username
	lists=db.session.query(List).filter(List.Uid == uid).all()
	card=db.session.query(Card).filter(Card.Cid == cid).first()
	if request.method == 'POST':
		
		if request.form.get('save')=='Save':
			#card=db.session.query(Card).filter(Card.Cid == cid).first()
			lid=db.session.query(List).filter(List.Lname==request.form['list']).first().Lid
			card.Lid=lid
			card.Cname=request.form['cardname']
			card.Content=request.form['content']
			card.Deadline=request.form['deadline']
			
			time=datetime.today().strftime('%Y-%m-%d')
			card.Last_modified=time
			card.Mark_as_complete=request.form['completed']
			
			temp=card.Completed
			if request.form['completed']=='Yes' and temp==None:
				card.Completed=time
							
			db.session.commit()
			
			return redirect(url_for('.board',uid=uid))
			
		if request.form.get('delete')=='Delete':
			card=db.session.query(Card).filter(Card.Cid == cid).first()
			db.session.delete(card)
			db.session.commit()
			return redirect(url_for('.board',uid=uid))

	return render_template("editcard.html",name=name,uid=uid,card=card,lists=lists)


