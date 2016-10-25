#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import urllib2
import sys
import tempfile
import sqlite3
import json
import os
import re

class MainWindow(wx.Frame):
	def __init__(self,parent,id):
		global ProxyCheckBox
		global createDb
		global CONFIGFILE

		CONFIGFILE = os.path.expanduser('~/tasklist.json')

		wx.Frame.__init__(self,parent,id,style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		panel=wx.Panel(self)
		# wx.Panel.__init__(self, parent = parent)

		# menubar=wx.MenuBar()
		# About_menu=wx.Menu()
		# Bug_menu=wx.Menu()

		# About_menu.Append(-1,"New Window","This will open a new window")
		# About_menu.Append(-1,"Exit","This will exit the program")

		# Bug_menu.Append(-1,"About","This will tell you about %name%")
		# Bug_menu.Append(-1,"Visit Website","This will take you to worm-media.host56.com")

		# menubar.Append(About_menu,"File")
		# menubar.Append(Bug_menu,"Help")
		# self.SetMenuBar(menubar)

		heading = wx.StaticText(self, -1, 'Welcome to Lyricslelo', (80,20))
		heading.SetForegroundColour(wx.BLACK)
		font1 = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		heading.SetFont(font1)

		SearchButton = wx.Button(self,id=-1,label='Search',pos=(20,80),size=(120, 50))
		SearchButton.SetBackgroundColour('#D1D1E2')
		SearchButton.Bind(wx.EVT_BUTTON, self.searchPanel)
		SearchButton.SetToolTip(wx.ToolTip("Click to Get to the Search Option"))

		ProxyButton = wx.Button(self, id=-1, label='ProxyOptions',pos=(300,80),size=(120, 50))
		ProxyButton.SetBackgroundColour('#D1D1E2')
		ProxyButton.Bind(wx.EVT_BUTTON, self.proxyPanel,None)
		ProxyButton.SetToolTip(wx.ToolTip("Click to change Proxy Settings"))
			
		HistoryButton = wx.Button(self, id=-1, label='History',pos=(160,80),size=(120, 50))
		HistoryButton.SetBackgroundColour('#D1D1E2')
		HistoryButton.Bind(wx.EVT_BUTTON, self.historyPanel)
		HistoryButton.SetToolTip(wx.ToolTip("Click to get History"))

		menubar=wx.MenuBar()
		About_menu=wx.Menu()
		Bug_menu=wx.Menu()

		About_menu.Append(1,"About")
		About_menu.Append(2,"Exit")

		# Bug_menu.Append(3,"Report Bug")
		# Bug_menu.Append(4,"Send FeedBack")

		menubar.Append(About_menu,"About")
		# menubar.Append(Bug_menu,"Bug/FeedBack")
		self.SetMenuBar(menubar)

		self.Bind(wx.EVT_MENU, self.AboutPanel, None, 1)
		self.Bind(wx.EVT_MENU, self.closewindow, None, 2)
		self.Bind(wx.EVT_MENU, self.BugPanel, None, 3)
		self.Bind(wx.EVT_MENU, self.FeedBackPanel, None, 4)

		self.Bind(wx.EVT_CLOSE,self.closewindow)

		self.SetSize((450,200))
		self.SetBackgroundColour('#D1D1E2')
		self.SetTitle('Lyricslelo')
		self.Centre()
		self.Show(True)

	def AboutPanel(self,event):
		new5=AboutWindow(parent=None,id=-1)
		new5.Show()
		new5.MakeModal(True)

	def BugPanel(self,event):
		new6=BugWindow(parent=None,id=-1)
		new6.Show()
		new6.MakeModal(True)

	def FeedBackPanel(self,event):
		new7=FeedBackWindow(parent=None,id=-1)
		new7.Show()
		new7.MakeModal(True)

	def searchPanel(self,event):
		print "serach here"
		# An_Instance_Of_ProxyWindow=ProxyWindow(parent=None,id=-1)
		if os.path.exists(CONFIGFILE):
			with open(CONFIGFILE, 'r') as f:
				data = json.load(f)
			for pair in data['checkbox']:
				ProxyCheckBoxValue=pair['status']
		new4=SearchWindow(parent=None,id=-1,ProxyCheckBoxValue=ProxyCheckBoxValue)

	def proxyPanel(self,event):
		print "proxy here"
		new1 = ProxyWindow(parent=None, id=-1)
		new1.Show()
		new1.MakeModal(True)

	def historyPanel(self,event):
		print "history here"
		new2=HistoryWindow(parent=None,id=-1)
		new2.Show()
		new2.MakeModal(True)

	def closewindow(self,event):
		self.Destroy()

class LyricsWindow(wx.Frame):
	def __init__(self,parent,id,Query_title):
		wx.Frame.__init__(self,parent,id,"Lyricslelo",size=(470,768),style=wx.MINIMIZE_BOX | wx.STAY_ON_TOP | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		panel=wx.ScrolledWindow(self,-1)
		# panel.SetBackgroundColour((0xcc, 0xff, 0xcc))

		print Query_title
		createDb = sqlite3.connect("lyricslelo.db")
		QCurs = createDb.cursor()

		# try:
		# 	QCurs.execute('''CREATE TABLE lyricstable (id INTEGER PRIMARY KEY, lyrics_title TEXT, lyrics_content TEXT, lyrics_countoflines TEXT)''')
		# 	createDb.commit()
		# except sqlite3.OperationalError:
		# 	None

		QCurs.execute('''SELECT lyrics_content FROM Lyricstable WHERE lyrics_title=?''',(Query_title,))
		for i in QCurs:
			# Lyrics_details=[str(j) for j in i]
			for j in i:
				Lyrics_details=j
				break

		QCurs.close()

		# image='grey.png'
		# bmp1=wx.Image(image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		# bitmap1 = wx.StaticBitmap(panel, -1, bmp1, (0, 0))

		font2 = wx.Font(11,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD)

		try:
			HS_length=len(max(Lyrics_details.split("\n"),key=len))
			VS_length=len(Lyrics_details.split("\n"))
			print HS_length, VS_length
			lyrics3=wx.StaticText(panel,-1,Lyrics_details,(10,10))
			lyrics3.SetBackgroundColour('#D1D1E2')
			lyrics3.SetFont(font2)

			#panel.SetScrollbars(10,10,HS_length+10,int(Lyrics_details[1])+20,0,0)
			#panel.SetScrollbars(11,11,HS_length,VS_length+120,0,0)
			panel.SetScrollbars(10,10,HS_length,int(VS_length*1.86),0,0)
			# panel.SetScrollbars(10,10,HS_length,VS_length+75,0,0)
			# panel.SetScrollRate(10, 10)

			self.Bind(wx.EVT_CLOSE,self.closewindow)

			self.SetBackgroundColour('#D1D1E2')

			self.alignAsRequired()
			self.Show()
		except UnboundLocalError:
			None
		# lyrics3=wx.StaticText(panel,-1,Query_title,(10,10))
		# lyrics3.SetFont(font2)

		# panel.SetScrollbars(85,50+15,8,15)

	def alignAsRequired(self):
		dw, dh = wx.DisplaySize()
		w, h = self.GetSize()
		x = dw - w
		y = dh - h+5
		self.SetPosition((x, y))

	def closewindow(self,event):
		self.Destroy()

class SearchWindow(wx.Dialog):
	def __init__(self, parent,id,ProxyCheckBoxValue):
		print "serach here"
		global Lyrics
		global countOfLines
		global Show_Lyrics_Window

		Show_Lyrics_Window=False
		Lyrics=''''''
		countOfLines=0
		answer=None
		print ProxyCheckBoxValue
		global ProxyCredentials

		box=wx.TextEntryDialog(None,"ENTER 'https://www.youtube.com/watch?v=...........' OR 'Artist - SongName'","Search Here",defaultValue="https://www.youtube.com/watch?v=450p7goxZqg OR Coldplay - Yellow")
		box.SetBackgroundColour('#D1D1E2')
		if box.ShowModal()==wx.ID_OK:
			answer=box.GetValue()
			box.Destroy()

		elif wx.ID_CANCEL:
		# Message("Bye! See you later")
		# Msg=wx.MessageDialog(None,"Bye! See you later","Bye",wx.OK | wx.CENTRE,(510,400))
		# if Msg.ShowModal()==wx.ID_OK:
			box.Destroy()

		if ProxyCheckBoxValue:
			createDb = sqlite3.connect("lyricslelo.db")
			QCurs = createDb.cursor()
			try:
				QCurs.execute('''CREATE TABLE proxytable (id INTEGER PRIMARY KEY, proxy_address TEXT, proxy_port TEXT, proxy_username TEXT, proxy_password TEXT)''')
				QCurs.execute('''INSERT INTO proxytable (proxy_address,proxy_port,proxy_username,proxy_password) VALUES(?,?,?,?)''',("10..18","80","062.","VVYT%iu2546"))
				createDb.commit()
			except sqlite3.OperationalError:
				None

			QCurs.execute('SELECT * FROM proxytable ORDER BY id DESC')
			for i in QCurs:
			    ProxyCredentials=[str(j) for j in i[1:]]

			QCurs.close()

		def Message(msg):
			Msg=wx.MessageDialog(None,msg,"Lyricslelo",wx.OK | wx.CENTRE,(510,400))
			if Msg.ShowModal()==wx.ID_OK:
				Msg.Destroy()
		def LyricsMethods(url):
			global Lyrics
			global countOfLines
			global countOfDialog
			global keepGoing
			global skip
			global Main_title
			global dialog

			def dialogFunction(msg):
				global keepGoing
				global skip
				global countOfDialog
				countOfDialog+=1
				wx.MilliSleep(250)
				if keepGoing:
					(keepGoing,skip)= dialog.Update(countOfDialog,msg)
				else:
					dialog.Destroy()
					self.Destroy()

			def CheckKeepGoing():
				if keepGoing==False:
					dialog.Destroy()
					self.Destroy()

			def ChangeTitletoQuery(oldS):
				global Main_title
				Main_title=oldS
				s=oldS.lower()
				indexOfAmp=s.find("&")
				if indexOfAmp!=-1:
					s=s[:indexOfAmp]+"and "+s[indexOfAmp+6:]

				def Query1(s):
					dislikedWords=["and",",","(","remix"," vs "," vs. ","featuring","cover","lyric","feat","ft.","acoustic","video"]
					for word in dislikedWords:
						indexOfWord=s.find(word)
						if indexOfWord!=-1:
							s=s[:indexOfWord]
					if s!="":
						if s[-1]!=" ":
							s+=" "
					else:
						Message("Youtube link was not correct. Try Again")
					return s
				def Query2(s):
					dislikedWords=["|","{","[","(","Ft","official","explicit","nsfw","audio","remix","acoustic","(cover","lyric","feat","ft.","acoustic","unstaged","us","video","x"]
					for word in dislikedWords:
						indexOfWord=s.find(word)
						if indexOfWord!=-1 and word=="us":
							if s[indexOfWord-1]=='(':
								s=s[:indexOfWord-2]
							elif s[indexOfWord-1]=='[':
								s=s[:indexOfWord-2]
						if indexOfWord!=-1:
							if s[indexOfWord-1]=='(':
								s=s[:indexOfWord-2]
							elif s[indexOfWord-1]=='[':
								s=s[:indexOfWord-2]
							else:
								s=s[:indexOfWord-1]
					if s[0]!=" ":
						s=" "+s
					return s
				def Query3(s):
					dislikedWords=["|","{","[","(","official","explicit","nsfw","audio","remix","acoustic","(cover","lyric","acoustic","unstaged","us","video"," x "]
					for word in dislikedWords:
						indexOfWord=s.find(word)
						if indexOfWord!=-1 and word=="us":
							if s[indexOfWord-1]=='(':
								s=s[:indexOfWord-2]
							elif s[indexOfWord-1]=='[':
								s=s[:indexOfWord-2]
						if indexOfWord!=-1:
							if s[indexOfWord-1]=='(':
								s=s[:indexOfWord-2]
							elif s[indexOfWord-1]=='[':
								s=s[:indexOfWord-2]
							else:
								s=s[:indexOfWord-1]
					if s[0]!=" ":
						s=" "+s
					return s
				indexOfDashInS=s.find("-")
				if indexOfDashInS!=-1:
					return Query1(s[:indexOfDashInS])+"-"+Query2(s[indexOfDashInS+1:])
				else:
					return Query3(s)

			def YoutubeUrlFound(url):
				indexofequal=url.find("v=")
				indexofAndSign=url[indexofequal:].find("&")
				if indexofAndSign!=-1:
					url_code=url[indexofequal+2:indexofequal+indexofAndSign]
				else:
					url_code=url[indexofequal+2:]

				CheckKeepGoing()

				if ProxyCheckBoxValue:
					if ProxyCredentials[2]=="" or ProxyCredentials[3]=="":
						proxy = urllib2.ProxyHandler({'https': ProxyCredentials[0]+':'+ProxyCredentials[1]})
					else:
						proxy = urllib2.ProxyHandler({'https': ProxyCredentials[2]+':'+ProxyCredentials[3]+'@'+ProxyCredentials[0]+':'+ProxyCredentials[1]})
					auth = urllib2.HTTPBasicAuthHandler()
					opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
					urllib2.install_opener(opener)
					try:
						some= urllib2.urlopen("https://www.googleapis.com/youtube/v3/videos?id="+url_code+"&key=AIzaSyDprqaGw-2lsUguPgI4xqhFYBGuhoBUv9U&part=snippet",timeout=30)
						out=some.read()
						oldS=json.loads(out)['items'][0]["snippet"]["title"]
						print oldS
						dialogFunction("Step 1 completed")
						return ChangeTitletoQuery(oldS)
					except Exception,e:
						if str(e)=="HTTP Error 407: Proxy Authentication Required":
							dialog.Destroy()
							Message("Proxy Authentication Failed")
							keepGoing=False
						else:
							print str(e)
							dialog.Destroy()
							Message("Internet connection lost Or Try using ARTIST - SONGNAME")
						# keepGoing=False
						# CheckKeepGoing()
							# dialog.Destroy()
				else:
					try:
						some= urllib2.urlopen("https://www.googleapis.com/youtube/v3/videos?id="+url_code+"&key=AIzaSyDprqaGw-2lsUguPgI4xqhFYBGuhoBUv9U&part=snippet",timeout=30)
						out=some.read()
						oldS=json.loads(out)['items'][0]["snippet"]["title"]
						print oldS
						dialogFunction("Step 1 completed")
						return ChangeTitletoQuery(oldS)
					except Exception,e:
						print str(e)
						Message("Internet connection lost Or Try using ARTIST - SONGNAME")
						# keepGoing=False
						# CheckKeepGoing()
						dialog.Destroy()

			def If_First_AZLYRICS_SERACH_is_Completed(step1,step2,temp1,sQuery2):
				print "OK"
				dialogFunction("Step "+step1+" completed")
				List=[]

				exit=5
				entry_found=0
				count=0
				exit_found=0
				IndexofLine=0
				temp1.seek(0)
				while True:
					IndexofLine+=1
					line=temp1.readline()
					if len(line)!=0:
						if exit_found==0:	
							if line[12:19]=="hlfound":
								exit=line[24:line.find("of")-1]
								exit_found=1
						if entry_found==0:
							if line[12:15]=='sen':
								entry_found=1
						else:
							count+=1
							List.append([])
							List[-1].append(count)

							i1=line.find("href")
							i2=line[i1:].find('html')
							List[-1].append(line[i1+6:i2+5])

							i3=line[i2:].find("<")
							List[-1].append(line[i2+6+6:i2+i3])

							i4=line[(i2+i3):].find("<b>")
							List[-1].append(line[i2+i3+i4+3:-6])
							List[-1].append(i4)
							entry_found=0
					if IndexofLine>300 and count==0:
						Message("Sorry we coudn't get lyrics with this entry.\n Try searching 'ARTIST - SONGNAME' and Check the spellings")
						keepGoing=False
						break
					if count==int(exit):
						break
				CheckKeepGoing()
				temp1.close()
				ListOfResults=[]
				print List,sQuery2
				if List==[]:
					dialog.Destroy()
				else:
					for item in List:
						f=item[3]
						if item[4]==-1:
							f=item[3][3:]
						if item[2][0]==">":
							item[2]=item[2][1:]
							ListOfResults.append([item[2].lower()+" "+f.lower(),item[1]+".html"])
						else:
							ListOfResults.append([item[2].lower()+" "+f.lower(),item[1]+".html"])

					link=List[0][1]+".html"
					print ListOfResults
					for result in ListOfResults:
						if result[0]==sQuery2.replace("+"," "):
							link=result[1]
							break

				Lyrics=''''''
				countOfLines=0
				def Access_Song_URL(link):
					global Lyrics
					global countOfLines

					CheckKeepGoing()

					indexOfCom=link.find(".com/")
					indexOfSlash=link[indexOfCom+5:].find("/")
					if len(link[indexOfCom+5:indexOfCom+5+indexOfSlash])==1:
						dialog.Destroy()
					try:
						temp = tempfile.TemporaryFile()
						if ProxyCheckBoxValue:
							if ProxyCredentials[2]=="" or ProxyCredentials[3]=="":
								proxy = urllib2.ProxyHandler({'http': ProxyCredentials[0]+':'+ProxyCredentials[1]})
							else:
								proxy = urllib2.ProxyHandler({'http': ProxyCredentials[2]+':'+ProxyCredentials[3]+'@'+ProxyCredentials[0]+':'+ProxyCredentials[1]})
							auth = urllib2.HTTPBasicAuthHandler()
							opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
							urllib2.install_opener(opener)
							try:
								data= urllib2.urlopen(link,timeout=30)
								temp.write(data.read())
							except Exception,e:
								print str(e)
								if str(e)=="HTTP Error 407: Proxy Authentication Required":
									Message("Proxy Authentication Required")
									keepGoing=False
								else:
									Message("Internet connection lost")
									keepGoing=False
						else:
							try:
								data2=urllib2.urlopen(link,timeout=30)
								temp.write(data2.read())
							except Exception,e:
								print str(e)
								Message("Internet connection lost")
								keepGoing=False
					finally:
						CheckKeepGoing()

					dialogFunction("Step "+step2+"completed")
					title_found=0
					lyrics_found=0
					temp3=0
					temp.seek(0)
					def removeNonAscii(s): return "'".join(i for i in s if ord(i)<128)
					while True:
						if temp3==1:
							break
						line=temp.readline()
						if len(line)!=0:
							removeNonAscii(line)
							line=line.replace("’","'")
							if title_found==0:
								if line[1:6]=="title":
									Lyrics+=line[7:line[6:].find("title")+4]+"\n"
									Lyrics+="\n"
									title_found=1
							if lyrics_found==0:
								if line[:18]=='<div style="margin':
									lyrics_found=1
							if lyrics_found==1:
								if line[:4]!="<!--" and line[:4]!="<div":
									if line[:3]=='<i>':
										i5=line.find("</i>")
										#Lyrics+="	   " + line[3:i5]+"\n"
									elif line[:6]=="<br />":
										Lyrics+="\n"
										countOfLines+=1
									elif line[:6]=="</div>":
										temp3=1
									elif line[-2]==">":
										Lyrics+=line[:-7]+"\n"
										countOfLines+=1
									elif line[-3]==">":
										Lyrics+=line[:-8]+"\n"
										countOfLines+=1
									else:
										Lyrics+=line[:-2]+"\n"
										countOfLines+=1
					Lyrics+='''


					'''+"\n"
					Lyrics+="Enjoy!!!"+"\n"
					Lyrics+="Produced by Shubhanshu"
					countOfLines+=6
					temp.close()
				if List!=[]:
					Access_Song_URL(link)
					keepGoing=False
					dialogFunction("Lyrics Found")

			def First_AZLYRICS_SERACH(newS,step1,step2,keepGoing,countOfDialog):
				print "newS = "+newS
				indexOfDashInnewS=newS.find("-")
				if indexOfDashInnewS!=-1:
					if newS[:indexOfDashInnewS-1]==u"beyonce" or newS[:indexOfDashInnewS-1]==u"beyoncé":
						newS="beyonce knowles "+ newS[indexOfDashInnewS:]

					sList=newS.split(" ")
					temp=0
					sQuery2=""
					sQuery=""
					indesOfDash=sList.index("-")
					for num in range(indesOfDash+1,len(sList)):
						sQuery2+=sList[num]+" "
						sQuery+=sList[num]+"+"
					for num in range(indesOfDash):
						if num==indesOfDash-1:
							sQuery2+=sList[num]
							sQuery+=sList[num]
						else:
							sQuery2+=sList[num]+" "
							sQuery+=sList[num]+"+"

					CheckKeepGoing()
					if sQuery[-1]=="!":
						sQuery=sQuery[:-1]
				else:
					sQuery=newS.replace(" ","+")
					if sQuery[0]=='+':
						sQuery=sQuery[1:]
					elif sQuery[-1]=='+':
						sQuery=sQuery[:-1]
				print "Query 1 : "  + sQuery

				StringOfNonASCII=re.sub('[ -~]', '',sQuery)

				if StringOfNonASCII!="":
					ListOfsQuery=list(sQuery)
					DictOfLetters={u'À':'A',u'Á':'A',u'Â':'A',u'Ã':'A',u'Ä':'A',u'Å':'A',u'Ç':'C',u'È':'E',u'É':'E',u'Ê':'E',u'Ë':'E',u'Ì':'I',u'Í':'I',u'Î':'I',u'Ï':'I',u'Ñ':'N',u'Ò':'O',u'Ó':'O',u'Ô':'O',u'Õ':'O',u'Ö':'O',u'Ð':'D',u'Ù':'U',u'Ú':'U',u'Û':'U',u'Ü':'U',u'Ý':'Y',u'à':'a',u'á':'a',u'â':'a',u'ã':'a',u'ä':'a',u'å':'a',u'æ':'a',u'ç':'c',u'è':'e',u'é':'e',u'ê':'e',u'ë':'e',u'ì':'i',u'í':'i',u'î':'i',u'ï':'i',u'ñ':'n',u'ò':'o',u'ó':'o',u'ô':'o',u'õ':'o',u'ö':'o',u'ù':'u',u'ú':'u',u'û':'u',u'ü':'u',u'š':'s',u'Š':'S',u'Ÿ':'Y'}
					for letter in StringOfNonASCII:
						print letter
						if letter in DictOfLetters.keys():
							indexOfLetter=ListOfsQuery.index(letter)
							ListOfsQuery[indexOfLetter]=DictOfLetters[letter]
					sQuery=""
					for falana in ListOfsQuery:
						sQuery+=falana

				print "Ultimate Query : " + sQuery
				try:
					temp1 = tempfile.TemporaryFile()
					if ProxyCheckBoxValue:
						if ProxyCredentials[2]=="" or ProxyCredentials[3]=="":
							proxy = urllib2.ProxyHandler({'http': ProxyCredentials[0]+':'+ProxyCredentials[1]})
						else:
							proxy = urllib2.ProxyHandler({'http': ProxyCredentials[2]+':'+ProxyCredentials[3]+'@'+ProxyCredentials[0]+':'+ProxyCredentials[1]})
						auth = urllib2.HTTPBasicAuthHandler()
						opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
						urllib2.install_opener(opener)

						try:
							data = urllib2.urlopen("http://search.azlyrics.com/search.php?q="+sQuery,timeout=20)
							temp1.write(data.read())
							If_First_AZLYRICS_SERACH_is_Completed(step1,step2,temp1,sQuery2)
						except Exception,e:
							print str(e)
							if str(e)=="HTTP Error 407: Proxy Authentication Required":
								Message("Proxy Authentication Failed")
								keepGoing=False
							else:
								Message("Internet connection lost")
								keepGoing=False
					else:
						try:
							print "Query link : "  + sQuery
							data = urllib2.urlopen("http://search.azlyrics.com/search.php?q="+sQuery,timeout=20)
							print "Query 2 : "  + sQuery
							temp1.write(data.read())
							If_First_AZLYRICS_SERACH_is_Completed(step1,step2,temp1,sQuery)
						except Exception,e:
							print str(e)
							Message("Internet connection lost")
							keepGoing=False
				finally:
					print "finally"
					CheckKeepGoing()

			def Check_The_Search_Query(url):
				global keepGoing
				global countOfDialog
				global dialog
				if url.find("youtube.com")!=-1 or url.find("youtu.be")!=-1:
					dialog = wx.ProgressDialog("Lyrics Loading...", "4 steps remaining... Don't Close In Between, TImeout Is only 30 sec",4 ,parent=None,style=wx.PD_AUTO_HIDE| wx.PD_CAN_ABORT| wx.PD_APP_MODAL)
					skip=True
					countOfDialog=0
					keepGoing=True
					if url.find("youtu.be")!=-1:
						DashIndex=url[::-1].find("/")
						url="https://www.youtube.com/watch?v="+url[len(url)-DashIndex:]
					newS=YoutubeUrlFound(url)
					print newS
					if newS==None:
						dialog.Destroy()
					else:
						First_AZLYRICS_SERACH(newS,"2","3",keepGoing,countOfDialog)
						dialog.Destroy()
				else:
					dialog = wx.ProgressDialog("Lyrics Loading...", "3 steps remaining... Don't Close In Between, TImeout Is only 30 sec",3,parent=None,style=wx.PD_AUTO_HIDE| wx.PD_CAN_ABORT| wx.PD_APP_MODAL)
					skip=True
					keepGoing=True
					countOfDialog=0
					newS=ChangeTitletoQuery(url)
					First_AZLYRICS_SERACH(newS,"1","2",keepGoing,countOfDialog)
					dialog.Destroy()

			Check_The_Search_Query(url)

		if answer!=None:
			LyricsMethods(answer)
			if Lyrics!='''''':
				#Introducing Lyricstable
				createDb = sqlite3.connect("lyricslelo.db")
				createDb.text_factory = str
				QCurs = createDb.cursor()
				try:
					QCurs.execute('''CREATE TABLE lyricstable (id INTEGER PRIMARY KEY, lyrics_title TEXT, lyrics_content TEXT)''')
					createDb.commit()
				except sqlite3.OperationalError:
					None

				QCurs.execute('''INSERT INTO lyricstable (lyrics_title,lyrics_content) VALUES(?,?)''',(Main_title,Lyrics))
				createDb.commit()
				QCurs.close()
				print Main_title

				#To show the lyrics window
				new0=LyricsWindow(parent=None,id=-1,Query_title=Main_title)
				new0.Show()

class ProxyWindow(wx.Frame):

    def __init__(self,parent,id):
    	global user_address
    	global user_port
    	global user_username
    	global user_password
    	global ProxyCheckBox
    	global CONFIGFILE

    	CONFIGFILE = os.path.expanduser('~/tasklist.json')

        wx.Frame.__init__(self, parent, id,style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        # wx.MINIMIZE_BOX | 
        panel1=wx.Panel(self)

        createDb = sqlite3.connect("lyricslelo.db")
        QCurs = createDb.cursor()
        try:
        	QCurs.execute('''CREATE TABLE proxytable (id INTEGER PRIMARY KEY, proxy_address TEXT, proxy_port TEXT, proxy_username TEXT, proxy_password TEXT)''')
        	QCurs.execute('''INSERT INTO proxytable (proxy_address,proxy_port,proxy_username,proxy_password) VALUES(?,?,?,?)''',("10..18","80","062.","VVYT%iu2546"))
        	createDb.commit()
        except sqlite3.OperationalError:
        	None

        QCurs.execute('SELECT * FROM proxytable ORDER BY id DESC')
        for i in QCurs:
            for j in i:
                [lastsave_add,lastsave_port,lastsave_username,lastsave_password]=[str(j) for j in i[1:]]

        font2 = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        ProxyMessage1 = wx.StaticText(self, -1, 'Currently Supporting Only HTTP Proxy Authentication',(2,5))
        ProxyMessage1.SetBackgroundColour('#D1D1E2')
        ProxyMessage2 = wx.StaticText(self,-1,'Leave Username And Password Blank If Not Applicable',(2,22))
        ProxyMessage2.SetBackgroundColour('#D1D1E2')

        address = wx.StaticText(self, -1, 'Address:  ',(30,45))
        user_address = wx.TextCtrl(self, -1, lastsave_add, (100,45))
        address.SetBackgroundColour('#D1D1E2')
        address.SetFont(font2)

        port = wx.StaticText(self, -1, 'Port:  ',(30,75))
        user_port = wx.TextCtrl(self, -1, lastsave_port, (100,75))
        port.SetBackgroundColour('#D1D1E2')
        port.SetFont(font2)

        username = wx.StaticText(self, -1, 'Username:  ',(29,105))
        user_username = wx.TextCtrl(self, -1, lastsave_username, (100,105))
        username.SetBackgroundColour('#D1D1E2')
        username.SetFont(font2)

        password = wx.StaticText(self, -1, 'Password:  ',(30,135))
        user_password = wx.TextCtrl(self, -1, lastsave_password, (100,135),style=wx.TE_PASSWORD)
        password.SetBackgroundColour('#D1D1E2')
        password.SetFont(font2)

        ProxyMessage3 = wx.StaticText(self,-1,' Check The Below Box If The Above Proxy details has to \n  be used Which Means System is not Getting Direct \n  Internet Connection',(2,165))
        ProxyMessage3.SetBackgroundColour('#D1D1E2')

        if os.path.exists(CONFIGFILE):
        	with open(CONFIGFILE, 'r') as f:
        		data=json.load(f)
        	for pair in data['checkbox']:
        		ProxyCheckBox = wx.CheckBox(self, -1 ,'Use Proxy', pos=(100, 210),size=(120,25))
        		ProxyCheckBox.SetBackgroundColour('#D1D1E2')
        		ProxyCheckBox.SetValue(pair['status'])
        else:
        	ProxyCheckBox = wx.CheckBox(self, -1 ,'Use Proxy', pos=(100, 210),size=(120,25))
        	ProxyCheckBox.SetBackgroundColour('#D1D1E2')

        proxySaveButton = wx.Button(self,id=-1,label="Save",pos=(10,240),size=(80,40))
        proxySaveButton.SetBackgroundColour('#D1D1E2')
        proxySaveButton.Bind(wx.EVT_BUTTON, self.proxySave,None)

        ProxyCheckButton = wx.Button(self,id=-1,label="Check",pos=(100,240),size=(80,40))
        ProxyCheckButton.SetBackgroundColour('#D1D1E2')
        ProxyCheckButton.Bind(wx.EVT_BUTTON, self.proxyCheck,None)

        ProxyCancelButton = wx.Button(self,id=-1,label="Cancel",pos=(190,240),size=(80,40))
        ProxyCancelButton.SetBackgroundColour('#D1D1E2')
        ProxyCancelButton.Bind(wx.EVT_BUTTON, self.proxyCancel,None)

        self.Bind(wx.EVT_CLOSE,self.proxyCancel)

        self.SetSize((310,330))
        self.SetBackgroundColour('#D1D1E2')
        self.SetTitle('Proxy Settings')
        self.Centre()
        self.Show(True)

    def proxySave(self,event):
    	print user_address.GetValue(),user_port.GetValue(),user_username.GetValue(),user_password.GetValue()
    	print "Proxy stored"
    	print "Proxy Checked Awesome We are saving the information"

    	createDb = sqlite3.connect("lyricslelo.db")
    	QCurs = createDb.cursor()

    	QCurs.execute('DELETE FROM proxytable WHERE id=1')
    	# self.addProxy("10..18","80","062.","VVYT%iu2546")
    	QCurs.execute('''INSERT INTO proxytable (proxy_address,proxy_port,proxy_username,proxy_password) VALUES(?,?,?,?)''',(str(user_address.GetValue()),str(user_port.GetValue()),str(user_username.GetValue()),str(user_password.GetValue())))
    	createDb.commit()
    	QCurs.close()
    	checkbox = [{'status':ProxyCheckBox.GetValue()}]
    	data = {'checkbox':checkbox,}
    	with open(CONFIGFILE, 'w') as f:
    		json.dump(data, f)
    	print "ok no problem"
    	self.MakeModal(False)
    	self.Destroy()

    def proxyCheck(self,event):
    	dialog = wx.ProgressDialog("Proxy Checker", "Testing..", 4 ,parent=None,style=wx.PD_AUTO_HIDE| wx.PD_CAN_ABORT| wx.PD_APP_MODAL)
    	def Message(msg):
			Msg=wx.MessageDialog(None,msg,"Lyricslelo",wx.OK | wx.CENTRE,(510,400))
			if Msg.ShowModal()==wx.ID_OK:
				Msg.Destroy()

    	print "Checking proxy"
    	dialog.Update(1,"Test 1 Passed")
    	if user_username.GetValue()=="" or user_password.GetValue()=="":
    		proxy = urllib2.ProxyHandler({'http': user_address.GetValue()+':'+user_port.GetValue()})
    	else:
    		proxy = urllib2.ProxyHandler({'http': user_username.GetValue()+':'+user_password.GetValue()+'@'+user_address.GetValue()+':'+user_port.GetValue()})
    	
    	auth = urllib2.HTTPBasicAuthHandler()
    	opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    	urllib2.install_opener(opener)
    	dialog.Update(2,"Test 2 Passed")
    	try:
    		conn = urllib2.urlopen('http://www.azlyrics.com/lyrics/samsmith/staywithme.html',timeout=60)
    		dialog.Update(3,"Test 3 Passed")
    		return_str = conn.read()
    		if len(return_str)!=0:
    			dialog.Update(4,"Test 4 Passed")
    			print "Proxy Checked Awesome We are saving the information"
    			dialog.Destroy()
    			Message("Awesome, Proxy Checked \nNow Save the Settings and Enjoy!! \nBut Don't Forget to Ckeck The 'Use Proxy' Box")
    	except Exception,e:
    		dialog.Destroy()
    		if str(e)=="HTTP Error 407: Proxy Authentication Required":
    			Message("Proxy Authentication Failed \nCheck Settings Again")
    		else:
    			Message("Testing Failed \nCheck Proxy Details Again ")

    def proxyCancel(self,event):
    	checkbox = [{'status':ProxyCheckBox.GetValue()}]
    	data = {'checkbox':checkbox,}
    	with open(CONFIGFILE, 'w') as f:
    		json.dump(data, f)
    	print "ok no problem"
    	self.MakeModal(False)
    	self.Destroy()

class HistoryWindow(wx.Frame):
	def __init__(self,parent,id):
		wx.Frame.__init__(self,parent,id,"History",size=(350,400),style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		panel3=wx.Panel(self,-1)
		panel3.SetBackgroundColour('#D1D1E2')

		global listBox
		self.list1=[]

		createDb = sqlite3.connect("lyricslelo.db")
		QCurs = createDb.cursor()
		try:
			QCurs.execute('''CREATE TABLE lyricstable (id INTEGER PRIMARY KEY, lyrics_title TEXT, lyrics_content TEXT)''')
			#QCurs.execute('''INSERT INTO lyricstable (lyrics_title,lyrics_content,lyrics_countoflines) VALUES(?,?,?)''',('Coldplay','Look at the stars',50))
			#QCurs.execute('''INSERT INTO lyricstable (lyrics_title,lyrics_content,lyrics_countoflines) VALUES(?,?,?)''',('The script','Superheroes',60))
			#QCurs.execute('''INSERT INTO lyricstable (lyrics_title,lyrics_content,lyrics_countoflines) VALUES(?,?,?)''',('John Legend','All of me',40))
			createDb.commit()

		except sqlite3.OperationalError:
			None
		QCurs.execute('SELECT * FROM lyricstable ORDER BY id DESC')
		for i in QCurs:
			self.list1.append([i[0],str(i[1])])

		print self.list1
		# self.list1=['Coldplay - Yellow','Maroon 5 - Sugar','The script - Superheroes','vfvf','cdcdc','cdvcd','vfvf','vfvf']
		#listBox=wx.ListBox(panel3, -1, (300,80), (180,180), self.list1, wx.LB_SINGLE,wx.LB_NEEDED_SB)
		listBox=wx.ListBox(panel3, -1, (0,0), (350,300), [j[1] for j in self.list1], wx.LB_NEEDED_SB)
		listBox.SetBackgroundColour('#D1D1E2')
		try:
			listBox.SetSelection(0)
			Show_Lyrics_Button = wx.Button(panel3,id=-1,label='Show',pos=(60,310),size=(100, 35))
			Show_Lyrics_Button.SetBackgroundColour('#D1D1E2')
			Show_Lyrics_Button.Bind(wx.EVT_BUTTON, self.doubleclick)
			Show_Lyrics_Button.SetToolTip(wx.ToolTip("Click to Get the Selected title's Lyrics"))

			Delete_Lyrics_Button = wx.Button(panel3,id=-1,label='Remove',pos=(180,310),size=(100, 35))
			Delete_Lyrics_Button.SetBackgroundColour('#D1D1E2')
			Delete_Lyrics_Button.Bind(wx.EVT_BUTTON, self.deletelyrics)
			Delete_Lyrics_Button.SetToolTip(wx.ToolTip("Click to Remove the Selected title's Lyrics"))

			self.Bind(wx.EVT_LISTBOX_DCLICK, self.doubleclick, listBox)
		except Exception:
			No_History_Warning = wx.StaticText(panel3, -1, 'No History', (85,20))
			No_History_Warning.SetForegroundColour(wx.RED)
			font1 = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD)
			No_History_Warning.SetFont(font1)

		self.Bind(wx.EVT_CLOSE,self.closewindow)

		self.Centre()
		self.Show()

	def deletelyrics(self,event):
		index=listBox.GetSelection()
		downloadselect = self.list1[index][1]
		# try:
		# 	self.list1.remove(str(downloadselect))
		# except IndexError:
		# 	None
		print self.list1

		createDb = sqlite3.connect("lyricslelo.db")
		QCurs = createDb.cursor()
		# try:
		# 	QCurs.execute('''CREATE TABLE lyricstable (id INTEGER PRIMARY KEY, lyrics_title TEXT, lyrics_content TEXT, lyrics_countoflines TEXT)''')
		# 	createDb.commit()
		# except sqlite3.OperationalError:
		# 	None
		#QCurs.execute('''DELETE FROM lyricstable WHERE lyrics_title = ?''',(str(downloadselect),))
		QCurs.execute('''DELETE FROM lyricstable WHERE id = ?''',(self.list1[index][0],))
		createDb.commit()
		# QCurs.execute('SELECT * FROM lyricstable ORDER BY id DESC')
		# for i in QCurs:
		# 	self.list1.append(str(i[1]))
		QCurs.close()
		self.Destroy()
		new2=HistoryWindow(parent=None,id=-1)
		new2.Show()


	def doubleclick(self,event):
		index=listBox.GetSelection()
		try:
			downloadselect = self.list1[index][1]
			print str(downloadselect)
			try:
				new3=LyricsWindow(parent=None,id=-1,Query_title=str(downloadselect))
				self.MakeModal(False)
				self.Destroy()
			except UnboundLocalError:
				self.Destroy()
		except IndexError:
			None

	def closewindow(self,event):
		self.MakeModal(False)
		self.Destroy()

class AboutWindow(wx.Frame):
	def __init__(self,parent,id):
		wx.Frame.__init__(self,parent,id,"About Lyricslelo",size=(330,250),style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		panel=wx.Panel(self,-1)

		AboutMessage='''Thank you for installing Lyricslelo \nDon't you think that if youtube could also have \nthe lyrics of the songs? So What we have made \nnow like you can enjoy the lyrics of a song while\nwatching its video.\nIts so simple you just have to copy the link of \nsong video and thats it you will see the lyrics of \nthe song Or You can use the songname also But\nDon't forget It must be in the form of \n"ARTISTNAME - SONGNAME"'''

		AboutText = wx.StaticText(self, -1, AboutMessage, (10,10))
		AboutText.SetBackgroundColour('#D1D1E2')
		font1 = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		AboutText.SetFont(font1)

		self.Bind(wx.EVT_CLOSE,self.closewindow)
		self.Centre()
		self.SetBackgroundColour('#D1D1E2')
		self.Show()

	def closewindow(self,event):
		self.MakeModal(False)
		self.Destroy()

class BugWindow(wx.Frame):
	def __init__(self,parent,id):
		wx.Frame.__init__(self,parent,id,"Report Bug",size=(310,330),style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		panel=wx.Panel(self,-1)

		self.Bind(wx.EVT_CLOSE,self.closewindow)
		self.Centre()
		self.Show()

	def closewindow(self,event):
		self.MakeModal(False)
		self.Destroy()

class FeedBackWindow(wx.Frame):
	def __init__(self,parent,id):
		wx.Frame.__init__(self,parent,id,"Send FeedBack",size=(310,330),style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		panel=wx.Panel(self,-1)

		self.Bind(wx.EVT_CLOSE,self.closewindow)
		self.Centre()
		self.Show()

	def closewindow(self,event):
		self.MakeModal(False)
		self.Destroy()

if __name__=="__main__":
	app=wx.App()
	MainWindow(None,-1)
	app.MainLoop()
	sys.exit(1)