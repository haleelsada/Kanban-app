import os
from datetime import datetime
import math

# to get no of days passed since a specific date (here 2020/1/1), just to get count of dates
def datenum(d1):
	if d1==None:
		return None
	d1 = [int(i) for i in d1.split('-')]
	s = (d1[0] - 2020) * 365
	months = [31, 30, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	for i in range(d1[1] - 1):
		s = s + months[i]
	s = s + d1[2]
	return s


# to see if the deadline is passed or not
def deadline(s):
	#d2 count of today,d1 count of deadline day
	time=datetime.today().strftime('%Y-%m-%d')

	d1=datenum(s)

	d2=datenum(time)
	
	return abs(d1-d2)


def chart(cards):
	try:
		m=min([datenum(i.Created) for i in cards])

	except:
		m=datenum(datetime.today().strftime('%Y-%m-%d'))


	mindate=m
	today=datenum(datetime.today().strftime('%Y-%m-%d'))
	print(m,today)
	x=[]
	for i in range(((today-mindate)//7)+1):
		x.append('week'+str(i+1))
	y =[]
	temp = mindate
	for i in range(((today-mindate)//7)+1):
		n,m = 0,0
		for c in cards:
			if c.Completed==None:c.Completed='2025-00-00'

			if datenum(c.Deadline)<(temp+7) and datenum(c.Completed)>temp and datenum(c.Completed)<(temp+7) and datenum(c.Deadline)>temp:
				n+=1
			if datenum(c.Completed) < (temp + 7) and datenum(c.Completed) > temp and datenum(c.Deadline) < temp:
				n+=1
			if datenum(c.Deadline) < (temp + 7) and datenum(c.Deadline) > temp:
				m+=1
			if datenum(c.Deadline) < temp and datenum(c.Completed) > temp:
				m+=1
		if n==0:n=1
		if m==0:m=n

		y.append(round(n/m,2))
		temp+=7
	return [x,y]



