# -*- coding: utf-8 -*-
import urllib2 , re , mp3play , time , datetime , sys , ctypes , pickle , os , os.path , codecs
from datetime import date, datetime , timedelta
from BeautifulSoup import BeautifulSoup
from sgmllib import SGMLParser
#=====================================================================
#function shipcheck, entershipnumber, shipsetting
#Three function too load user's ship setting, which may only enable
#correct(range 1-10) ship number.
#May affect announced event data.
def shipcheck(nstring):
    try :int(nstring)
    except ValueError:
        return False
    shipint = int(nstring)
    if shipint < 1 or shipint > 10 :
        return False
    else :
        return True
def entershipnumber():
    shipnumber = raw_input('Please Enter The NUMBER of your Ship(Game Server)')
    shipcheckResult = shipcheck(shipnumber)
    if shipcheckResult :
        ship = str(shipnumber)
        return ship
    else :
        print 'This is not an vaild number, please try again'
        shipnumber = entershipnumber()
        ship = str(shipnumber)
        return ship
def shipsetting():
    settingfile = 'ship.ini'
    if os.path.isfile(settingfile):
        with open(settingfile, 'rb') as settingFile:
            setting = settingFile.read()
        settingFile.close()
        shipcheckResult = shipcheck(setting)
        if shipcheckResult :
            shipNumber = str(setting)
            return shipNumber
        else :
            print 'PLEASE INPUT A VALID SHIP (GAME SERVER) IN THE CONFIGURATION FILE, THEN RESTART THE PROGRAME'
            shipNumber = entershipnumber()
            with open(settingfile, 'wb') as updateSettingFile:
                updateSettingFile.write(shipNumber)
            updateSettingFile.close()
            return shipNumber
    else :
        print 'WELCOME TO USE PSO2 URGENT QUEST ALERT'
        shipNumber = entershipnumber()
        print shipNumber
        with open(settingfile, 'w+') as createSettingFile:
            createSettingFile.write(shipNumber)
        createSettingFile.close()
        return shipNumber
shipSetting = shipsetting()
#=====================================================================
#Main Setting Part
#name:timezoneData——timezone adjustment as integer
#url,preloadurl,sysurl :Some network file
#alertfile,sysfile,filename,preloadfile: Some local file
timezoneLocal = time.localtime()
timezoneUTC = time.gmtime()
if timezoneLocal[3] - timezoneUTC[3] < -12 :
    timezoneAdjust = timezoneLocal[3] - timezoneUTC[3] + 24
else :
    timezoneAdjust = timezoneLocal[3] - timezoneUTC[3]
timezoneData = int(timezoneAdjust)
if timezoneData > 0 :
    timezone = '+' + str(timezoneData)
else :
    timezone = str(timezoneData)
ctypes.windll.kernel32.SetConsoleTitleA("PSO2 Urgent Quest Alert")
url = "http://pso2.swiki.jp/index.php?%E7%B7%8A%E6%80%A5%E6%8E%B2%E7%A4%BA%E6%9D%BF%2FShip" + shipSetting
if shipSetting > 5:
    preloadurl = 'http://localhost/preload1.html'
else :
    preloadurl = 'http://localhost/preload2.html'
sysurl = 'http://localhost/sys.html'
user_agent = 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0);'
headers = { 'User-Agent' : user_agent }
reqRaw = urllib2.Request(url,'', headers)
reqPre = urllib2.Request(preloadurl,'', headers)
reqSys = urllib2.Request(sysurl,'', headers)
alertfile = 'alert.mp3'
sysfile = 'data.dat'
filename = 'data1.dat'
preloadfile = 'data2.dat'
print '===================================================='
print '             PSO2 URGENT QUEST ALERT\n'
print 'Version:0.21'
print 'Local Time Zone: UTC' + timezone
print 'Game Server: ' + shipSetting
print '\n===================================================='
#=====================================================================
#function soundalert: play mp3 file as sound alert.
def soundalert():
    mp3 = mp3play.load(alertfile)
    mp3.play()
    time.sleep(min(60, mp3.seconds()))
    mp3.stop()
#=====================================================================
#function strQ2B, strB2Q: convert full-shape interger to half-shape
def strQ2B(u):  
    r = ""  
    for uchar in u:  
        inside_code=ord(uchar)  
        if inside_code == 12288:  
            inside_code = 32    
        elif (inside_code >= 65281 and inside_code <= 65374):   
            inside_code -= 65248  
  
        r += unichr(inside_code)  
    return r  
      
def strB2Q(u):  
    r = ""  
    for uchar in u:  
        inside_code=ord(uchar)  
        if inside_code == 32:      
            inside_code = 12288  
        elif inside_code >= 32 and inside_code <= 126:      
            inside_code += 65248  
  
        r += unichr(inside_code)  
    return r
#=====================================================================
#Check Quest Function: questcheck(s,t)
#s as a string encoding with unicode, or use type"get" as requesting 
#t as type(full, name, code, type, get)
def questcheck(s,t):
    if t != 'get':
        eventList = []
        eventItemFalse = re.search('無|ちん|沈|平和|なし|ありません',s)
        eventItemDF = re.search('エル|巨躯',s)
        eventItemLoser = re.search('歯医者|ルーサー|敗者',s)
        eventItemRiripaBase1 = re.search('襲来|第一|１',s)
        eventItemRiripaBase2 = re.search('侵入|第二|２',s)
        eventItemRiripaBase3 = re.search('絶望|第三|３',s)
        eventItemDarker = re.search('ゆり|巢穴|異常|百合',s)
        eventItemNaberius = re.search('ナベ|鍋|森林',s)
        eventItemAmduscia = re.search('アムド',s)
        eventItemLilipa = re.search('リリ|りり',s)
        eventItemArksShip = re.search('市街地|ダーカー',s)
        eventItemInteRanking = re.search('IR|インラン|淫乱',s)
        if eventItemFalse :
            event = 'none';
        elif eventItemDF :
            event = 'elder'
        elif eventItemLoser :
            event = 'loser'
        elif eventItemRiripaBase1 :
            event = 'td1'
        elif eventItemRiripaBase2 :
            event = 'td2'
        elif eventItemRiripaBase3 :
            event = 'td3'
        elif eventItemDarker :
            event = 'dk1'
        elif eventItemNaberius :
            event = 'naberius'
        elif eventItemAmduscia :
            event = 'amduscia'
        elif eventItemLilipa :
            event = 'lilipa'
        elif eventItemArksShip :
            event = 'arksship'
        elif eventItemInteRanking :
            event = 'ir'
        else :
            event = 'unknown'
    elif t == 'get':
        eventData = s[1]
        event = eventData[1]
    if event == 'none':
        eventReturn = 'FALSE'
    elif event == 'elder':
        eventReturn = 'TRUE' ;eventType = 'DF' ;eventCode = 'elder';eventDisplay = 'Dark Falz Elder'
    elif event == 'loser':
        eventReturn = 'TRUE' ;eventType = 'DF' ;eventCode = 'loser';eventDisplay = 'Dark Falz Loser'
    elif event == 'td1' :
        eventReturn = 'TRUE' ;eventType = 'TD' ;eventCode = 'td1'; eventDisplay = 'Mining Base Defense: Invasion'
    elif event == 'td2' :
        eventReturn = 'TRUE' ;eventType = 'TD' ;eventCode = 'td2'; eventDisplay = 'Mining Base Defense: Intrusion'
    elif event == 'td3' :
        eventReturn = 'TRUE' ;eventType = 'TD' ;eventCode = 'td3'; eventDisplay = 'Mining Base Defense: Despair'
    elif event == 'dk1' :
        eventReturn = 'TRUE' ;eventType = 'DK' ;eventCode = 'dk1'; eventDisplay = 'The Cradle of Darkness'
    elif event == 'dk2' :
        eventReturn = 'TRUE' ;eventType = 'DK' ;eventCode = 'dk2'; eventDisplay = 'The Beckoning Darkness'
    elif event == 'naberius' :
        eventReturn = 'TRUE' ;eventType = 'P' ;eventCode = 'naberius'; eventDisplay = 'Naberius'; eventDetail = '"The Oncoming Darkness"'
    elif event == 'naberius1' :
        eventReturn = 'TRUE' ;eventType = 'PS' ;eventCode = 'naberius1'; eventDisplay = 'The Oncoming Darkness';
    elif event == 'amduscia' :
        eventReturn = 'TRUE' ;eventType = 'P' ;eventCode = 'amduscia'; eventDisplay = 'Amduscia';eventDetail = '"Volcanic Guerillas", "Rampaging Malice"'
    elif event == 'amduscia1' :
        eventReturn = 'TRUE' ;eventType = 'PS' ;eventCode = 'amduscia1'; eventDisplay = 'Volcanic Guerrillas'
    elif event == 'amduscia2' :
        eventReturn = 'TRUE' ;eventType = 'PS' ;eventCode = 'amduscia2'; eventDisplay = 'Rampaging Malice'
    elif event == 'lilipa' :
        eventReturn = 'TRUE' ;eventType = 'P' ;eventCode = 'lilipa'; eventDisplay = 'Lilipa';eventDetail = '"Desert Guerillas", "Mega Mecha Awakening", "Lead Border-Breaker"'
    elif event == 'lilipa1' :
        eventReturn = 'TRUE' ;eventType = 'PS' ;eventCode = 'lilipa1'; eventDisplay = 'Desert Guerrilla Warfare'
    elif event == 'lilipa2' :
        eventReturn = 'TRUE' ;eventType = 'PS' ;eventCode = 'lilipa2'; eventDisplay = 'Mega Mech Awakening'
    elif event == 'lilipa3' :
        eventReturn = 'TRUE' ;eventType = 'PS' ;eventCode = 'lilipa3'; eventDisplay = 'Lead Border-Breaker'
    elif event == 'arksship' :
        eventReturn = 'TRUE' ;eventType = 'P' ;eventCode = 'arksship'; eventDisplay = 'Arks Ship';eventDetail = '"Urban Recovery", "Urban Mop-Up Operation", "The Oncoming Darkness"'
    elif event == 'arksship1' :
        eventReturn = 'TRUE' ;eventType = 'PS' ;eventCode = 'arksship1'; eventDisplay = 'Urban Recovery'
    elif event == 'arksship2' :
        eventReturn = 'TRUE' ;eventType = 'PS' ;eventCode = 'arksship2'; eventDisplay = 'Urban Mop-Up Operation'
    elif event == 'arksship3' :
        eventReturn = 'TRUE' ;eventType = 'PS' ;eventCode = 'arksship3'; eventDisplay = 'The Oncoming Darkness'
    elif event == 'ir'  :
        eventReturn = 'TRUE' ;eventType = 'IR';eventCode = 'ir'; eventDisplay = 'Interrupt Ranking'
    elif event == 'unknown' :
        eventReturn = 'UNKNOWN'
    else :
        print 'f(questcheck): unknow event type'
    if t == 'full' :
        if eventReturn == 'TRUE' and eventType == 'P' :
            return [eventReturn,eventType,eventCode,eventDisplay,eventDetail]
        elif eventReturn == 'TRUE' :
            return [eventReturn,eventType,eventCode,eventDisplay]
        else :
            return [eventReturn]
    elif t =='name' :
        if eventReturn == 'TRUE' :
            return True , str(eventDisplay)
        else :
            return False
    elif t =='code' :
        if eventReturn == 'TRUE' :
            return True , str(eventCode)
        else :
            return False
    elif t =='type' :
        if eventReturn == 'TRUE' :
            return True , str(eventType)
        else :
            return False
    elif t =='get' :
        if s[0] =='pre':
            questType = ' ANNOUNCED'
        elif s[0] == 'raw' :
            questType = ' '
        eventLocalTime = localtime(eventData[0])
        print ''
        if eventType == 'DF' :
            print time.strftime('%H:%M:%S') + questType + 'URGENT QUEST OF APPROACHING [' + eventDisplay +'] IS STARTING AT ' + datetime.strftime(eventLocalTime , '%H:%M')
        elif eventType == 'TD' or eventType == 'DK' or eventType =='PS' :
            print time.strftime('%H:%M:%S') + questType + 'URGENT QUEST [' + eventDisplay +'] IS STARTING AT ' + datetime.strftime(eventLocalTime , '%H:%M')
        elif eventType == 'P' :
            print time.strftime('%H:%M:%S') + questType + 'URGENT EVENT OF [' + eventDisplay +'] IS STARTING AT ' + datetime.strftime(eventLocalTime , '%H:%M')
            if t =='raw' :
                print time.strftime('%H:%M:%S') + ' INCLUDE URGENT QUEST :' + eventDetail
        elif eventType == 'IR' :
            print time.strftime('%H:%M:%S') + ' INTERRUPT RANKING IS STARTING AT ' + datetime.strftime(eventLocalTime , '%H:%M')
            if t == 'pre' :
                print time.strftime('%H:%M:%S') + ' TARGET:' + eventData[2].decode('utf-8')
        print ''
    else :
        print 'f(questcheck): unknow string'
        return
#=====================================================================
#Check Event Function: eventcheck(s,t)
#return list of information of urgent quest
def netrequest():
    web = urllib2.urlopen(reqRaw)
    raw = BeautifulSoup(web)
    def eventcheck(s):
        eventCheck = re.search('(?P<eventGroup1>.+?)時(?P<eventGroup2>.+?) --  ',s)
        if eventCheck :
            eventTimeFTH1 = eventCheck.group('eventGroup1')
            eventTimeFTH2 = eventTimeFTH1.strip().decode('utf-8')
            eventTimeStr = strQ2B(eventTimeFTH2).encode('utf-8')
            eventTimeCheck = re.search('[^0-9]+?(?P<eventTime>[0-9]+)',eventTimeStr)
            if eventTimeCheck :
                eventTimeUTCRaw = int(eventTimeCheck.group('eventTime')) - 9
            else:
                eventTimeUTCRaw = int(eventTimeStr) - 9
            if eventTimeUTCRaw < 0 :
                eventTime = eventTimeUTCRaw + 24
                eventTzAdjust = 1
            else :
                eventTime = eventTimeUTCRaw
                eventTzAdjust = 0
            eventDataReturn = questcheck(eventCheck.group('eventGroup2'),'code')
            if eventDataReturn :
                eventData = eventDataReturn[1]
                return True , [eventData , eventTime , eventTzAdjust]
            else :
                return False
        else:
            return False
    rawul = raw.find('ul', {'class':'list1'})
    itemOutput = []
    for item in rawul.findAll('li', { 'class' : 'pcmt' }):
        itemList = []
        raw = BeautifulSoup(str(item))
        rawItem = raw.find('li', { 'class' : 'pcmt' }).contents
        rawEventStr = str(rawItem[1])
        rawEventAnyis = eventcheck(rawEventStr) 
        if rawEventAnyis :
            rawEvent = rawEventAnyis[1]
            while True :
                rawDateCheck = re.match('<span class="comment_date">',str(rawItem[0]))
                if not rawDateCheck:
                    del rawItem[0]
                else :
                    rawEnteryTimeGet = re.match('<span class="comment_date">(\d+-\d+-\d+) (.+) (\d+:\d+:\d+)',str(rawItem[0]))
                    rawEnteryTimeGroup = rawEnteryTimeGet.group(1),rawEnteryTimeGet.group(3)
                    rawEnteryTimeStr = ''.join(rawEnteryTimeGroup)
                    if rawEvent[2] >= 0:
                        rawEnteryTime = datetime.strptime(rawEnteryTimeStr,'%Y-%m-%d%H:%M:%S')
                        rawEventTimeGroup = rawEnteryTimeGet.group(1), str(rawEvent[1])
                        rawEventTimeStr = ''.join(rawEventTimeGroup)
                        rawEventTime = datetime.strptime(rawEventTimeStr,'%Y-%m-%d%H') - timedelta(days=rawEvent[2])
                        itemList.append(rawEvent[0])
                        itemList.append(rawEventTime)
                        itemList.append(rawEnteryTime)
                        break
                    else :
                        itemList.append('False')
                        break
        else :
            itemList.append('False')
        if itemList[0] != 'False':
            itemOutput.append(itemList)
    if itemOutput:
        return itemOutput
    else :
        return False
#=====================================================================
#function: datarequest(type)
#type: sys/pre
#request internet data of system and announced event and return a list
def datarequest(t):
    if t == 'sys':
        geturl = sysurl
    elif t == 'pre':
        geturl = preloadurl
    class ListName(SGMLParser):
        def __init__(self):
            SGMLParser.__init__(self)
            self.is_li = ""
            self.name = []
        def start_li(self, attrs):
            for name,value in attrs:
                if name == 'class' and value =="pcmt":
                    self.is_li = 1
                    break
        def end_li(self):
            self.is_li = ""
        def handle_data(self, text):
            if self.is_li == 1:
                self.name.append(text)
    try:
        content = urllib2.urlopen(geturl).read()
    except urllib2.HTTPError as e:
        print time.strftime('%H:%M:%S') + ' ERROR ' + str(e.code)
        print time.strftime('%H:%M:%S') + ' ERROR: failed to connect with server'
        raw_input('Press Enter to retry')
        sysrequest(t)
    except urllib2.URLError as e:
        print time.strftime('%H:%M:%S') + ' ' + str(e.reason)
        print time.strftime('%H:%M:%S') + ' ERROR: failed to connect with server'
        raw_input('Press Enter to retry')
        sysrequest(t)
    l = ListName()
    l.feed(content)
    lOut = l.name
    if lOut:
        return lOut
    else :
        print time.strftime('%H:%M:%S') + ' REQUEST ERROR: FAILED TO LOAD DATA FROM SERVER'
        raw_input('Press Enter to retry')
        sysrequest(t)
#=====================================================================
#function localdata(type1,type2,list)
#type1 :sys/raw/pre
#type2 :get/write
#write and read data form local
def localdata(t1,t2,l):
    if t1 == 'sys':
        f = sysfile
    elif t1 == 'raw':
        f = filename
    elif t1 == 'pre':
        f = preloadfile
    else :
        print 'f(filerequest): unknow request type'
    if t2 == 'get' :
        if os.path.isfile(f):
            try:
                with codecs.open(f, 'rb') as fGet:
                    returnData = pickle.load(fGet)
                fGet.close()
            except EOFError:
                os.remove(f)
                return False
            return returnData
        else :
            return False
    elif t2 == 'write' :
        with codecs.open(f, 'w+', encoding='utf8') as fWrite:
            pickle.dump(l, fWrite)
        fWrite.close()
#=====================================================================
#function sys(type)
#type:status/time/msg
#return server statue/server maintence time/system message
def sys(t):
    def sysdata():
        sysolddata = localdata('sys','get','')
        sysnewdata = datarequest('sys')
        if sysnewdata:
            if not sysolddata:
                localdata('sys','write',sysnewdata)
                return ['new',sysnewdata]
            else :
                if sysnewdata[0] != sysolddata[0]:
                    localdata('sys','write',sysnewdata)
                    return ['new',sysnewdata]
                else:
                    return ['no',sysolddata]
    sysUtcTime = datetime.utcnow()
    sysdata = sysdata()
    sys = sysdata[1]
    data = str(sysdata[0])
    sysStatus = str(sys[1])
    sysCloseTime = datetime.strptime(sys[3],'%Y-%m-%d %H:%M')
    sysCloseTimeLimit = sysCloseTime - timedelta(hours = 2)
    sysOpenTime = datetime.strptime(sys[5],'%Y-%m-%d %H:%M')
    sysMsg1 = [sys[7],sys[8]]
    sysMsg2 = [sys[10],sys[11]]
    returnList = []
    if t == 'status':
        if sysUtcTime.day == sysCloseTimeLimit.day and sysUtcTime.hour > sysCloseTimeLimit.hour and sysUtcTime.hour < sysCloseTime.hour:
            return ['closing']
        elif sysUtcTime.day == sysCloseTime.day and sysUtcTime.hour > sysCloseTime.hour and sysUtcTime.hour < sysOpenTime.hour:
            return ['closed']
        elif sysStatus == 'FALSE':
            return ['failed',data]
        elif sysStatus == 'TRUE':
            return ['normal',data]
        else:
            print 'f(sys): unknow status'
            return ['normal',data]
    elif t == 'time' :
        returnList.append(sysCloseTime)
        returnList.append(sysOpenTime)
        return returnList , data
    elif t == 'msg':
        returnList.append(sysMsg1)
        returnList.append(sysMsg2)
        return returnList , data
    else:
        print 'f(sys): unknow string'
#=====================================================================
#function pre()
#return Announced Event
def pre():
    def precheck(l):
        while True:
            if l[1] == 'SERVERCLOSE' or l[1] == 'SERVEROPEN':
                break
            else:
                preTime = datetime.strptime(str(l[0]),'%Y-%m-%d %H:%M')
                preTimeNow = datetime.utcnow()
                if preTime.month < preTimeNow.month or preTime.day < preTimeNow.day or (preTime.day == preTimeNow.day and preTime.hour < preTimeNow.hour):
                    if l[1] == 'IR':
                        del l[0]
                        del l[0]
                        del l[0]
                    else :
                        del l[0]
                        del l[0]
                else :
                    break
        return l
    preUtcTime = datetime.utcnow()
    prenewdata = datarequest('pre')
    preolddata = localdata('pre','get','')
    if prenewdata :
        if not preolddata :
            preupdated = precheck(prenewdata)
            localdata('pre','write',preupdated)
        else :
            if preolddata[-1] != prenewdata[-1]:
                preupdated = precheck(prenewdata)
                localdata('pre','write',preupdated)
            else :
                preupdated = precheck(preolddata)
                localdata('pre','write',preupdated)
        predata = localdata('pre','get','')
        preTime = datetime.strptime(predata[0],'%Y-%m-%d %H:%M')
        preTimeLimit = preTime - timedelta(hours = 2)
        if preUtcTime.day == preTimeLimit.day and preUtcTime.hour < preTime.hour and preUtcTime.hour > preTimeLimit.hour :
            if predata[1] == 'IR':
                return ['event',[ preTime , predata[1] , predata[2]]]
            else :
                return ['event',[ preTime , predata[1] ]]
        else:
            return False
#=====================================================================
#funcion raw(type)
#type:start/loop
#return urgent quest with wiki's data
def raw(t):
    rawUtcTime = datetime.utcnow()
    #timezoneData
    rawnewdata = netrequest()
    rawolddata = localdata('raw','get','')
    if rawnewdata :
        if t == 'start' or ( t == 'loop' and rawnewdata != rawolddata ):
            rawNewest = rawnewdata[-1]
            rawEvent = rawNewest[0]
            rawTime = rawNewest[1]
            rawEnteryTime = rawNewest[2]
            rawTimeLimit = rawTime - timedelta(hours = 2)
            if rawUtcTime.day == rawTime.day and rawUtcTime.hour < rawTime.hour and rawUtcTime.hour > rawTimeLimit.hour:
                localdata('raw','write',rawnewdata)
                return ['newevent',[ rawTime , rawEvent ]]
            else :
                localdata('raw','write',rawnewdata)
                return ['newupdate']
        elif t == 'loop' and rawnewdata == rawolddata :
            return ['noupdate']
        else :
            print 'f(raw): unknow request type'
#=====================================================================
#function: localtime(time)
#input with datetime.datetime data in utc time
#and return a local time
def localtime(t):
    tz = timedelta(hours = timezoneData)
    returntime = t + tz
    return returntime
#=====================================================================
#fuction: main(type)
#type: start/loop(affect 'pre' function)
#main loop processe, print and return sleep second
def main(t):
    now = datetime.utcnow()
    mainsys = sys('status')
    if mainsys[0] == 'failed' and t=='start' :
        print time.strftime('%H:%M:%S') + ' GAME SERVER IS UNREACHABLE NOW'
        ss = ( 30 - (now.minute %30 )) *60 - now.second
    elif mainsys[0] == 'failed' and t=='loop' :
        ss = ( 30 - (now.minute %30 )) *60 - now.second
    elif mainsys[0] == 'closed':
        sysTime = sys('time')
        sysOpenTime = localtime(sysTime[1])
        print time.strftime('%H:%M:%S') + ' REGULAR MAINTENANCE TILL ' + datetime.strftime(sysOpenTime,'%H:%M')
        ss = ( 30 - (now.minute %30 )) *60 - now.second
    elif mainsys[0] == 'closing':
        sysTime = sys('time')
        sysCloseTime = localtime(sysTime[0])
        print time.strftime('%H:%M:%S') + ' REGULAR MAINTENANCE WILL START AT ' + time.strftime(sysCloseTime,'%H:%M')
        ss = now.minute *60 - now.second
    elif mainsys[0] == 'normal':
        mainpre = pre()
        if mainpre:
            preData = mainpre[1]
            preTime = preData[0]
            prePrint = ['pre',preData]
            questcheck(prePrint,'event')
            ssInt = ( preTime.hour - now.hour)*3600 - (preTime.minute + now.minute) * 60 - now.second
            if ssInt > 1800:
                print time.strftime('%H:%M:%S') + ' NOTIFY MESSAGE WILL BE RECIVED AT 30 MINNTES BEFORE EVENT START'
                time.sleep(ssInt - 1800)
                ticPlaysound = time.clock()
                print time.strftime('%H:%M:%S') + ' ANNOUNCED EVENT WILL START AT ' + datetime.strftime(localtime(rawTime),'%H:%M')
                tocPlaysound = time.clock()
                ss = ( preTime.hour - now.hour + 1 ) *3600 - now.minute * 60 - now.second - (ticPlaysound - tocPlaysound)
            else :
                ss = ssInt + 3600
        else:
            mainraw = raw(t)
            if mainraw[0] == 'newevent':
                rawData = mainraw[1]
                rawTime = rawData[0]
                rawPrint = ['raw',rawData]
                questcheck(rawPrint,'get')
                ssInt = ( rawTime.hour - now.hour)*3600 - now.minute * 60 - now.second
                if ssInt > 1800:
                    print time.strftime('%H:%M:%S') + ' NOTIFY MESSAGE WILL BE RECIVED AT 30 MINNTES BEFORE EVENT START'
                    time.sleep(ssInt - 1800)
                    ticPlaysound = time.clock()
                    print time.strftime('%H:%M:%S') + ' EVENT WILL START AT ' + datetime.strftime(localtime(rawTime),'%H:%M')
                    tocPlaysound = time.clock()
                    ss = ( rawTime.hour - now.hour + 1 ) *3600 - now.minute * 60 - now.second - (ticPlaysound - tocPlaysound)
                else:
                    ss = ( ssInt + 3600)
            else :
                if t == 'start' :
                    print time.strftime('%H:%M:%S') + ' NO EVENT FOUND'                    
                if now.minute < 10 :
                    ss = 60 - now.second
                elif now.minute >= 10 and now.minute < 45:
                    ss = ( 15 - (now.minute % 15 )) *60 - now.second
                elif now.minute == 45:
                    print time.strftime('%H:%M:%S') + ' NO EVENT FOUND FORM PSO2 ES'
                    ss = 60 - now.second
                elif now.minute > 45 and now.minute < 55:
                    ss = 60 - now.second
                elif now.minute >= 55 :
                    print time.strftime('%H:%M:%S') + ' NO EVENT FOUND'
                    ss = ( 5 - (now.minute % 5 )) *60 - now.second
    return ss
#=====================================================================
#main code
startTic = time.clock()
seconds = main('start')
startToc = time.clock()
startSSAdj = startToc - startTic
startSleepSecond = seconds - startSSAdj
time.sleep(startSleepSecond)
while True:
    loopTic = time.clock()
    loopSeconds = main('loop')
    loopToc = time.clock()
    loopSSAdj = loopTic - loopToc
    loopSleepSecond = loopSeconds - loopSSAdj
    time.sleep(loopSleepSecond)
