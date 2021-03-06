import sys
import datetime
import requests
import json
import glob
import re
import numpy as np
import os
import csv


DATAPATH='C:/NBA'
url_base='http://data.nba.com/5s/json/cms/noseason/scoreboard/%s/games.json'

def get_season(seasonnum,startd,endd):
	datelist=[]
	numberd= (endd-startd).days
	for i in range(0,numberd+1):
		datelist.append(str.replace((startd+datetime.timedelta(days=i)).isoformat(),'-',''))
		
	f=open('%s/listofgames_%s.csv' % (DATAPATH,seasonnum), 'w')
	f.write('game,season,home,away\n')
	for dayx in datelist:
		gamelist=get_games(dayx)
		for n in range(len(gamelist)):
			gamenum=gamelist[n]['id']
			homet,awayt=gamelist[n]['home']['abbreviation'],gamelist[n]['visitor']['abbreviation']
			f.write(','.join([str(gamenum),str(seasonnum),homet,awayt]) + '\n')
	f.close()

def dateprocess(datex):
	m,d,y = datex.split('/')
	return datetime.date(int(y),int(m),int(d))

def get_games(datex):
	url_games=url_base%datex
	getgames=requests.get(url_games)
	try:
		return getgames.json()['sports_content']['games']['game']
	except:
		return []

get_season(2015,dateprocess("10/27/2015"),dateprocess("4/13/2016"))
	
def read_listofgames(filex,teamx):
	f=open(filex,'r')
	f.readline()
	for linex in f.readlines():
		listx=linex.split(',')
		if listx[2]==teamx or listx[3]==teamx:
			gamenum=listx[0]
			playbyplay(gamenum,teamx)

def playbyplay(gamenum,teamname):
	user_agent={'User-agent': 'Mozilla/5.0'}
	url_p='http://stats.nba.com/stats/playbyplay'
	params_p={'GameID':0, 'RangeType':0, 'StartPeriod':0, 'EndPeriod':0, 'StartRange':0, 'EndRange':0}
	f = open('%s/%s/playbyplay_%s.json' % (DATAPATH,teamname,gamenum), 'w')
	params_p['GameID'] = gamenum  
	p = requests.get(url_p, params_p, headers=user_agent).json()['resultSets'][0]
	json.dump(p, f)    
	f.close()

teamlist=["ATL","BKN","BOS","CHA","CHI","CLE","DAL","DEN","DET","GSW","HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOP","NYK","OKC","ORL","PHI","PHX","POR","SAC","SAS","TOR","UTA","WAS"]
for team in teamlist:
	os.makedirs(DATAPATH+"/"+team+"/")

def pullfull:
	for team in teamlist:
		read_listofgames("c:/nba/listofgames_2015.csv",team)
		parsecsv(team)
		listed=generateplayerslist(team)
		generateshots(listed,team)
		

read_listofgames("c:/nba/listofgames_2015.csv",teamname)

def parsecsv(teamname):
	files = glob.glob(DATAPATH +'/'+teamname+'/'+ '*.json')
	for singlefile in files:
		singlefile = singlefile.replace('\\','/')
		input = open(singlefile)
		data = json.load(input)
		input.close()
		data = data['rowSet']
		outputpath=''.join([singlefile,".csv"])
		with open(outputpath, 'w') as csvfile:
			output = csv.writer(csvfile)
			for row in data:
    				output.writerow(row)

def generateplayerslist(teamname):
	listofplayers=[]
	files = glob.glob(DATAPATH +'/'+teamname+'/'+ '*.csv')
	for singlefile in files:
		singlefile = singlefile.replace('\\','/')
		with open(singlefile, "r") as csvfile:
			datareader = csv.reader(csvfile)
			shotlog=[]
			for row in datareader:
				if row!=[]:
					if int(row[2])==1 or int(row[2])==2:
						if row[7]!='':
							if row[7].find('Jump Shot')!=-1:
								descr=row[7].split("' ")[0].split(" ")
								if descr[0]=="MISS":
									row.extend(descr[1:])
								else:
									row.extend(descr)
								shotlog.append(row)
		for row in shotlog:
			if row[12] not in listofplayers:
				listofplayers.append(row[12])
	return listofplayers

def timeclock(timex):
	timelist=timex.split(":")
	return int(timelist[0])*60+int(timelist[1])

def generateshots(listx,teamname):
	shotarray=[]
	errorcount=0
	files = glob.glob(DATAPATH +'/'+teamname+'/'+ '*.csv')
	for playerx in listx:
		totalms=0
		countmd=0
		countmk=0
		countms=0
		feet1=0
		feet2=0
		for singlefile in files:
			singlefile = singlefile.replace('\\','/')
			with open(singlefile, "r") as csvfile:
				datareader = csv.reader(csvfile)
				shotlog=[]
				for row in datareader:
					if row!=[]:
						if int(row[2])==1 or int(row[2])==2:
							if row[7]!='':
								if row[7].find('Jump Shot')!=-1:
									descr=row[7].split("' ")[0].split(" ")
									if descr[0]=="MISS":
										row.extend(descr[1:])
									else:
										row.extend(descr)
									shotlog.append(row)
			i=0
			for row in shotlog:
				if row[12]==playerx and row[2]=='2':
					totalms+=1
			for row in shotlog:
				i+=1
				if row[12]==playerx and row[2]=='1':
					countmd+=1
					try:
						feet1+=int(row[-1])
					except ValueError:
						errorcount+=1
						feet1+=23
						continue
					for rowy in shotlog[i:]:
						if rowy[12]==playerx:
							if (timeclock(row[6])+720*(4-int(row[4])))-(timeclock(rowy[6])+720*(4-int(rowy[4])))<=180:
								if rowy[2]=='1':
									countmk+=1
								if rowy[2]=='2':
									countms+=1
								try:
									feet2+=int(rowy[-1])
								except ValueError:
									errorcount+=1
									feet2+=23
									continue
							break
		playershots=[playerx,countmd,totalms,feet1,countmk,countms,feet2]
		shotarray.append(playershots)
	outputfile = DATAPATH + "/" + 'output.csv'
	outputwriter = open(outputfile, 'a')
	csv.writer(outputwriter).writerows(shotarray)
	outputwriter.close()

def generateshotsc(listx,teamname):
	shotarray=[]
	errorcount=0
	files = glob.glob(DATAPATH +'/'+teamname+'/'+ '*.csv')
	for playerx in listx:
		totalms=0
		countmd=0
		countmk=0
		countms=0
		feet1=0
		feet2=0
		for singlefile in files:
			singlefile = singlefile.replace('\\','/')
			with open(singlefile, "r") as csvfile:
				datareader = csv.reader(csvfile)
				shotlog=[]
				for row in datareader:
					if row!=[]:
						if int(row[2])==1 or int(row[2])==2:
							if row[7]!='':
								if row[7].find('Jump Shot')!=-1:
									descr=row[7].split("' ")[0].split(" ")
									if descr[0]=="MISS":
										row.extend(descr[1:])
									else:
										row.extend(descr)
									shotlog.append(row)
			i=0
			for row in shotlog:
				if row[12]==playerx and row[2]=='1':
					totalms+=1
			for row in shotlog:
				i+=1
				if row[12]==playerx and row[2]=='2':
					countmd+=1
					try:
						feet1+=int(row[-1])
					except ValueError:
						errorcount+=1
						feet1+=23
						continue
					for rowy in shotlog[i:]:
						if rowy[12]==playerx:
							if (timeclock(row[6])+720*(4-int(row[4])))-(timeclock(rowy[6])+720*(4-int(rowy[4])))<=180:
								if rowy[2]=='1':
									countmk+=1
								if rowy[2]=='2':
									countms+=1
								try:
									feet2+=int(rowy[-1])
								except ValueError:
									errorcount+=1
									feet2+=23
									continue
							break
		playershots=[playerx,countmd,totalms,feet1,countmk,countms,feet2]
		shotarray.append(playershots)
	outputfile = DATAPATH + "/" + 'outputcold.csv'
	outputwriter = open(outputfile, 'a')
	csv.writer(outputwriter).writerows(shotarray)
	outputwriter.close()

for team in teamlist:
		listed=generateplayerslist(team)
		generateshotsc(listed,team)
