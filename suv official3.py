import requests
import pandas as pd
import numpy as np
import glob
import os
import json
import csv
from scipy.spatial.distance import euclidean

##generate gamelist with tracking info
JSONPATH="I:/nba/json/"
##files = glob.glob(JSONPATH +'*.json')
##f2=open('%s/listofgames_%s.csv' % (JSONPATH,"tracking"), 'w')
##for singlefile in files:
##      gamenum=(singlefile.split("\\")[1]).split(".")[0]
##      f2.write(gamenum + '\n')
##f2.close()


##pull and parse playbyplay
DATAPATH='C:/NBA'
url_base='http://data.nba.com/5s/json/cms/noseason/scoreboard/%s/games.json'
teamlist=["ATL","BKN","BOS","CHA","CHI","CLE","DAL","DEN","DET","GSW","HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NOP","NYK","OKC","ORL","PHI","PHX","POR","SAC","SAS","TOR","UTA","WAS"]
##for team in teamlist:
##      os.makedirs(DATAPATH+"/"+team+"/home/")
##      os.makedirs(DATAPATH+"/"+team+"/away/")

def read_listofgames(filex,teamx):
        f=open(filex,'r')
        f.readline()
        for linex in f.readlines():
                listx=linex.split(',')
                if listx[2]==teamx:
                        gamenum='00'+listx[0]
                        playbyplayhome(gamenum,teamx)
                if listx[3]==teamx+'\n':
                        gamenum='00'+listx[0]
                        playbyplayaway(gamenum,teamx)

def playbyplayhome(gamenum,teamname):
        user_agent={'User-agent': 'Mozilla/5.0'}
        url_p='http://stats.nba.com/stats/playbyplay'
        params_p={'GameID':0, 'RangeType':0, 'StartPeriod':0, 'EndPeriod':0, 'StartRange':0, 'EndRange':0}
        f = open('%s/%s/home/playbyplay_%s.json' % (DATAPATH,teamname,gamenum), 'w')
        params_p['GameID'] = gamenum  
        p = requests.get(url_p, params_p, headers=user_agent).json()['resultSets'][0]
        json.dump(p, f)    
        f.close()

def playbyplayaway(gamenum,teamname):
        user_agent={'User-agent': 'Mozilla/5.0'}
        url_p='http://stats.nba.com/stats/playbyplay'
        params_p={'GameID':0, 'RangeType':0, 'StartPeriod':0, 'EndPeriod':0, 'StartRange':0, 'EndRange':0}
        f = open('%s/%s/away/playbyplay_%s.json' % (DATAPATH,teamname,gamenum), 'w')
        params_p['GameID'] = gamenum  
        p = requests.get(url_p, params_p, headers=user_agent).json()['resultSets'][0]
        json.dump(p, f)    
        f.close()

def parsecsv(teamname):
        files = glob.glob(DATAPATH +'/'+teamname+'/home/' + '*.json')
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
        files = glob.glob(DATAPATH +'/'+teamname+'/away/' + '*.json')
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

##for team in teamlist:
##      read_listofgames("c:/nba/listofgames_2015_track.csv",team)
##      parsecsv(team)


##
def read_track(gamenum):
        filename=JSONPATH+gamenum+".json"
        input = open(filename)
        data = json.load(input)
        input.close()
        return data

def generateplayerslist(teamname):
        listofplayers=[]
        files = glob.glob(DATAPATH +'/'+teamname+'/home/'+ '*.csv')
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
        files = glob.glob(DATAPATH +'/'+teamname+'/away/'+ '*.csv')
        for singlefile in files:
                singlefile = singlefile.replace('\\','/')
                with open(singlefile, "r") as csvfile:
                        datareader = csv.reader(csvfile)
                        shotlog=[]
                        for row in datareader:
                                if row!=[]:
                                        if int(row[2])==1 or int(row[2])==2:
                                                if row[9]!='':
                                                        if row[9].find('Jump Shot')!=-1:
                                                                descr=row[9].split("' ")[0].split(" ")
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
                
def caldist(eventnum,playerx,gamenum):
        trackdata=data
        for singleevent in trackdata:
                if singleevent['eventId']==eventnum:
                        hometeam = singleevent["home"]
                        awayteam = singleevent["visitor"]
                        players = hometeam["players"]
                        players.extend(awayteam["players"])
                        id_dict = {}
                        for player in players:
                                id_dict[player['playerid']] = [player["firstname"],player["lastname"],player["jersey"]]
                        id_dict.update({-1: ['ball', 'ball', np.nan]})
                        momentslist = singleevent["moments"]
                        headers = ["team_id", "player_id", "x_loc", "y_loc", "radius", "moment", "game_clock", "shot_clock"]
                        player_moments = []
                        for moment in momentslist:
                                for player in moment[5]:
                                        player.extend((momentslist.index(moment), moment[2], moment[3]))
                                        player_moments.append(player)
                        ##print(player_moments[0]) ##
                        if not player_moments:
                                return 0
                        df2 = pd.DataFrame(player_moments)
                        ##print(df[0:3])
                        df = df2.iloc[:,0:8]
                        ##print(df[0:3])
                        df.columns=headers
                        ##print(df[0:3])
                        df["first_name"] = df.player_id.map(lambda x: id_dict[x][0])
                        df["last_name"] = df.player_id.map(lambda x: id_dict[x][1])
                        ##print(df[0:3])
                        playername=playerx
                        playermove=df[df.last_name==playername]
                        if len(playermove)==0:
                                return 0
                        teamnum=playermove.team_id.iloc[0]
                        ##oppomove=df[df.team_id!=teamnum].groupby("last_name")[["x_loc", "y_loc"]]
                        ballmove=df[df.last_name=='ball']
                        eventstotal=min(len(playermove),len(ballmove))
                        totaldiffn=10
                        k=0
                        for i in range(eventstotal):
                                j=eventstotal-1-i
                                xdiff=ballmove.x_loc.iloc[j]-playermove.x_loc.iloc[j]
                                ydiff=ballmove.y_loc.iloc[j]-playermove.y_loc.iloc[j]
                                totaldiff=np.sqrt(xdiff**2+ydiff**2)
                                if totaldiff<totaldiffn:
                                        totaldiffn=totaldiff
                                        k=j
                                if totaldiff>totaldiffn:
                                        if totaldiffn<0.5:
                                                break
                        oppomove=df[df.team_id!=teamnum]
                        oppomove=oppomove[oppomove.team_id!=-1]
                        oppomoveshot=oppomove[oppomove.game_clock==playermove.game_clock.iloc[k]]
                        distarray=[]
                        for i in range(len(oppomoveshot)):
                                xdiff=oppomoveshot.x_loc.iloc[i]-playermove.x_loc.iloc[k]
                                ydiff=oppomoveshot.y_loc.iloc[i]-playermove.y_loc.iloc[k]
                                totaldiff=np.sqrt(xdiff**2+ydiff**2)
                                distarray.append(totaldiff)
                        return min(distarray)

def calrun(eventnum,playerx,gamenum):
        trackdata=data2
        for singleevent in trackdata:
                if singleevent['eventId']==eventnum:
                        hometeam = singleevent["home"]
                        awayteam = singleevent["visitor"]
                        players = hometeam["players"]
                        players.extend(awayteam["players"])
                        id_dict = {}
                        for player in players:
                                id_dict[player['playerid']] = [player["firstname"],player["lastname"],player["jersey"]]
                        id_dict.update({-1: ['ball', 'ball', np.nan]})
                        momentslist = singleevent["moments"]
                        headers = ["team_id", "player_id", "x_loc", "y_loc", "radius", "moment", "game_clock", "shot_clock"]
                        player_moments = []
                        for moment in momentslist:
                                for player in moment[5]:
                                        player.extend((momentslist.index(moment), moment[2], moment[3]))
                                        player_moments.append(player)
                        ##print(player_moments[0:5])
                        if not player_moments:
                                return 0
                        df2 = pd.DataFrame(player_moments)
                        ##print(df2[0:3])
                        ##print(df2.shape)
                        df = df2.iloc[:,0:8]
                        ##print(df)
                        ##print(df.shape)
                        df.columns=headers
                        ##print(df[0:3])
                        df["first_name"] = df.player_id.map(lambda x: id_dict[x][0])
                        df["last_name"] = df.player_id.map(lambda x: id_dict[x][1])
                        ##print(df[-5:])
                        playername=playerx
                        playermove=df[df.last_name==playername]
                        totaldist=move_dist(playermove[["x_loc", "y_loc"]])
                        totaltime = df.game_clock.max() - df.game_clock.min()
                        if totaltime==0:
                                return 0
                        totalspeed=totaldist/totaltime
                        if np.isnan(totalspeed)==True:
                                return 0
                        if totalspeed>25:
                                return 0
                        ##print(totalspeed)
                        return totalspeed

def move_dist(player_locations):
        diff = np.diff(player_locations, axis=0)
        dist = np.sqrt((diff ** 2).sum(axis=1))
        return dist.sum()

for teamname in teamlist:
        listx=generateplayerslist(teamname)
        shotarray=[]
        errorcount=0
        files = glob.glob(DATAPATH +'/'+teamname+'/home/'+ '*.csv')
        filea = glob.glob(DATAPATH +'/'+teamname+'/away/'+ '*.csv')
        for playerx in listx:
                totalms=0
                countmd=0
                countmk=0
                countms=0
                feet1=0
                feet2=0
                run1=0
                run2=0
                ddist1=0
                ddist2=0
                for singlefile in files:
                        singlefile = singlefile.replace('\\','/')
                        with open(singlefile, "r") as csvfile:
                                datareader = csv.reader(csvfile)
                                shotlog=[]
                                gamenum=(singlefile.split("_")[-1]).split(".")[0]
                                filename=JSONPATH+gamenum+".json"
                                input = open(filename)
                                data = json.load(input)
                                input.close()
                                data=data['events']
                                data2=data
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
                                        eventnum=row[1]
                                        cad=caldist(eventnum,playerx,gamenum)
                                        car=calrun(eventnum,playerx,gamenum)
                                        try:
                                                dr=cad*car
                                        except TypeError:
                                                dr=0
                                        if dr!=0:
                                                ddist1+=cad
                                                run1+=car
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
                                                                        eventnumy=rowy[1]
                                                                        cad=caldist(eventnumy,playerx,gamenum)
                                                                        car=calrun(eventnumy,playerx,gamenum)
                                                                        try:
                                                                                dr=cad*car
                                                                        except TypeError:
                                                                                dr=0
                                                                        if dr!=0:
                                                                                ddist2+=cad
                                                                                run2+=car
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
                for singlefile in filea:
                        singlefile = singlefile.replace('\\','/')
                        with open(singlefile, "r") as csvfile:
                                datareader = csv.reader(csvfile)
                                shotlog=[]
                                gamenum=(singlefile.split("_")[-1]).split(".")[0]
                                filename=JSONPATH+gamenum+".json"
                                input = open(filename)
                                data = json.load(input)
                                input.close()
                                data=data['events']
                                data2=data
                                for row in datareader:
                                        if row!=[]:
                                                if int(row[2])==1 or int(row[2])==2:
                                                        if row[9]!='':
                                                                if row[9].find('Jump Shot')!=-1:
                                                                        descr=row[9].split("' ")[0].split(" ")
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
                                        eventnum=row[1]
                                        cad=caldist(eventnum,playerx,gamenum)
                                        car=calrun(eventnum,playerx,gamenum)
                                        try:
                                                dr=cad*car
                                        except TypeError:
                                                dr=0
                                        if dr!=0:
                                                ddist1+=cad
                                                run1+=car
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
                                                                        eventnumy=rowy[1]
                                                                        cad=caldist(eventnumy,playerx,gamenum)
                                                                        car=calrun(eventnumy,playerx,gamenum)
                                                                        try:
                                                                                dr=cad*car
                                                                        except TypeError:
                                                                                dr=0
                                                                        if dr!=0:
                                                                                ddist2+=cad
                                                                                run2+=car
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
                playershots=[playerx,countmd,totalms,feet1,countmk,countms,feet2,ddist1,ddist2,run1,run2]
                print(playershots)
                shotarray.append(playershots)
        outputfile = DATAPATH + "/" + 'tr-output.csv'
        outputwriter = open(outputfile, 'a')
        csv.writer(outputwriter).writerows(shotarray)
        outputwriter.close()

        shotarray=[]
        errorcount=0
        files = glob.glob(DATAPATH +'/'+teamname+'/home/'+ '*.csv')
        filea = glob.glob(DATAPATH +'/'+teamname+'/away/'+ '*.csv')
        for playerx in listx:
                totalms=0
                countmd=0
                countmk=0
                countms=0
                feet1=0
                feet2=0
                run1=0
                run2=0
                ddist1=0
                ddist2=0
                for singlefile in files:
                        singlefile = singlefile.replace('\\','/')
                        with open(singlefile, "r") as csvfile:
                                datareader = csv.reader(csvfile)
                                shotlog=[]
                                gamenum=(singlefile.split("_")[-1]).split(".")[0]
                                filename=JSONPATH+gamenum+".json"
                                input = open(filename)
                                data = json.load(input)
                                input.close()
                                data=data['events']
                                data2=data
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
                                        eventnum=row[1]
                                        cad=caldist(eventnum,playerx,gamenum)
                                        car=calrun(eventnum,playerx,gamenum)
                                        try:
                                                dr=cad*car
                                        except TypeError:
                                                dr=0
                                        if dr!=0:
                                                ddist1+=cad
                                                run1+=car
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
                                                                        eventnumy=rowy[1]
                                                                        cad=caldist(eventnumy,playerx,gamenum)
                                                                        car=calrun(eventnumy,playerx,gamenum)
                                                                        try:
                                                                                dr=cad*car
                                                                        except TypeError:
                                                                                dr=0
                                                                        if dr!=0:
                                                                                ddist2+=cad
                                                                                run2+=car
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
                for singlefile in filea:
                        singlefile = singlefile.replace('\\','/')
                        with open(singlefile, "r") as csvfile:
                                datareader = csv.reader(csvfile)
                                shotlog=[]
                                gamenum=(singlefile.split("_")[-1]).split(".")[0]
                                filename=JSONPATH+gamenum+".json"
                                input = open(filename)
                                data = json.load(input)
                                input.close()
                                data=data['events']
                                data2=data
                                for row in datareader:
                                        if row!=[]:
                                                if int(row[2])==1 or int(row[2])==2:
                                                        if row[9]!='':
                                                                if row[9].find('Jump Shot')!=-1:
                                                                        descr=row[9].split("' ")[0].split(" ")
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
                                        eventnum=row[1]
                                        cad=caldist(eventnum,playerx,gamenum)
                                        car=calrun(eventnum,playerx,gamenum)
                                        try:
                                                dr=cad*car
                                        except TypeError:
                                                dr=0
                                        if dr!=0:
                                                ddist1+=cad
                                                run1+=car
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
                                                                        eventnumy=rowy[1]
                                                                        cad=caldist(eventnumy,playerx,gamenum)
                                                                        car=calrun(eventnumy,playerx,gamenum)
                                                                        try:
                                                                                dr=cad*car
                                                                        except TypeError:
                                                                                dr=0
                                                                        if dr!=0:
                                                                                ddist2+=cad
                                                                                run2+=car
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
                playershots=[playerx,countmd,totalms,feet1,countmk,countms,feet2,ddist1,ddist2,run1,run2]
                shotarray.append(playershots)
        outputfile = DATAPATH + "/" + 'tr-outputcold.csv'
        outputwriter = open(outputfile, 'a')
        csv.writer(outputwriter).writerows(shotarray)
        outputwriter.close()
