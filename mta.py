# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 21:07:11 2015

"""
# read subway/bus info from below, or drop in FF/IE
#http://web.mta.info/status/serviceStatus.txt

import urllib
from lxml import etree
import os
import datetime
import logging

class MTA(object):
    '''class to hold data about a NYC MTA line'''
    def __init__(self, name, status, text, date, time):
        '''data attributes are named same as XML attributes'''
        self.name=name
        self.status=status
        self.text=text
        self.date=date
        self.time=time
    def getName(self):
        return self.name
    def getStatus(self):
        return self.status
    def getText(self):
        return self.text
    def getDate(self):
        return self.date
    def getTime(self):
        return self.time
    def getMode(self):
        return self.mode

class Subway(MTA):
    '''class to hold data about a NYC Subway line'''
    def __init__(self, name, status, text, date, time):
        super(Subway, self).__init__(name, status, text, date, time)
        self.Mode='subway'

class Bus(MTA):
    '''class to hold data about a NYC Bus line'''
    def __init__(self, name, status, text, date, time):
        '''data attributes are named same as XML attributes'''
        super(Bus, self).__init__(name, status, text, date, time)
        self.Mode='bus'
        
class BT(MTA):
    '''class to hold data about a NYC Bridge and Tunnel line'''
    def __init__(self, name, status, text, date, time):
        '''data attributes are named same as XML attributes'''
        super(BT, self).__init__(name, status, text, date, time)
        self.Mode='bt'

class LIRR(MTA):
    '''class to hold data about a NYC Bridge and Tunnel line'''
    def __init__(self, name, status, text, date, time):
        '''data attributes are named same as XML attributes'''
        super(LIRR, self).__init__(name, status, text, date, time)
        self.Mode='lirr'
        
class MetroNorth(MTA):
    '''class to hold data about a MetroNorth line'''
    def __init__(self, name, status, text, date, time):
        '''data attributes are named same as XML attributes'''
        super(MetroNorth, self).__init__(name, status, text, date, time)
        self.Mode='metronorth'
    
class MTAStatus():
    '''Get data from MTA web site
       this mtaData() function returns a dictionary of k,v
       
        KEY-> value is Subway() instance
       '123' -> Subway('123', 'GOOD ...', 'Text', 'Date', 'Time')
       '456' -> Subway('456', 'GOOD ...', 'Text', 'Date', 'Time')
       
       NOTE: ... all MTA Subway lines are not availble
       
       Data is scraped from http://web.mta.info/status/serviceStatus.txt
       
       Drop above http, in your favorite browser to see the data
    
    '''
    def __init__(self):
        url='http://web.mta.info/status/serviceStatus.txt'
        self.subwayDataAsXML=urllib.urlopen(url).read()
        #open('subwayData.xml', "w").write(xmlData)
        self.root = etree.XML(self.subwayDataAsXML)
        
        # write XML data for later reference
        debugXMLfile = "xml\\mta_%s.xml" % (datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        open(debugXMLfile,"w").write(self.subwayDataAsXML)
        logging.debug('firefox.exe %s\\%s' % (os.getcwd(), debugXMLfile) )

        # get MTA metadata
        self.responseCode = self.root.xpath('responsecode')[0].text
        self.timeStamp = self.root.xpath('timestamp')[0].text
    def getReportTime(self):
        return self.timeStamp
    def getSubway(self):
        '''Subway data'''
        self.subwayDict = {}    
        # iterate through XML data, only care about Subway data for now
        for count in range(len(self.root.xpath('subway/line/name'))):
            name = self.root.xpath('subway/line/name')[count].text
            status = self.root.xpath('subway/line/status')[count].text
            text = self.root.xpath('subway/line/text')[count].text
            date = self.root.xpath('subway/line/Date')[count].text    
            time = self.root.xpath('subway/line/Time')[count].text
            s = Subway(name, status, text, date, time)

            #s = Subway(self.root.xpath('subway'))
            self.subwayDict[s.getName()] = s
        return self.subwayDict

    def getBus(self):
        '''Bus data'''
        self.busDict = {}    
        # iterate through XML data, only care about Subway data for now
        for count in range(len(self.root.xpath('bus/line/name'))):
            name = self.root.xpath('bus/line/name')[count].text
            status = self.root.xpath('bus/line/status')[count].text
            text = self.root.xpath('bus/line/text')[count].text
            date = self.root.xpath('bus/line/Date')[count].text    
            time = self.root.xpath('bus/line/Time')[count].text
            bus = Bus(name, status, text, date, time)
            # set the SubwayName = Subway() class data
            self.busDict[bus.getName()] = bus
        return self.busDict

    def getBT(self):
        ''' Bridge and Tunnel data'''
        self.btDict = {}    
        # iterate through XML data, only care about Subway data for now
        for count in range(len(self.root.xpath('BT/line/name'))):
            name = self.root.xpath('BT/line/name')[count].text
            status = self.root.xpath('BT/line/status')[count].text
            text = self.root.xpath('BT/line/text')[count].text
            date = self.root.xpath('BT/line/Date')[count].text    
            time = self.root.xpath('BT/line/Time')[count].text
            bt = BT(name, status, text, date, time)
            # set the SubwayName = Subway() class data
            self.btDict[bt.getName()] = bt
        return self.btDict
    def getLIRR(self):
        ''' Bridge and Tunnel data'''
        self.lirrDict = {}    
        # iterate through XML data, only care about Subway data for now
        for count in range(len(self.root.xpath('LIRR/line/name'))):
            name = self.root.xpath('LIRR/line/name')[count].text
            status = self.root.xpath('LIRR/line/status')[count].text
            text = self.root.xpath('LIRR/line/text')[count].text
            date = self.root.xpath('LIRR/line/Date')[count].text    
            time = self.root.xpath('LIRR/line/Time')[count].text
            lirr = LIRR(name, status, text, date, time)
            # set the SubwayName = Subway() class data
            self.lirrDict[lirr.getName()] = lirr
        return self.lirrDict

    def getMetroNorth(self):
        ''' Bridge and Tunnel data'''
        self.mnDict = {}    
        # iterate through XML data, only care about Subway data for now
        for count in range(len(self.root.xpath('MetroNorth/line/name'))):
            name = self.root.xpath('MetroNorth/line/name')[count].text
            status = self.root.xpath('MetroNorth/line/status')[count].text
            text = self.root.xpath('MetroNorth/line/text')[count].text
            date = self.root.xpath('MetroNorth/line/Date')[count].text    
            time = self.root.xpath('MetroNorth/line/Time')[count].text
            mn = MetroNorth(name, status, text, date, time)
            # set the SubwayName = Subway() class data
            self.mnDict[mn.getName()] = mn
        return self.mnDict

if __name__ == '__main__':
    logging.basicConfig(filename='mta.log', level=logging.DEBUG)
    logging.info('Started')

    mtaStatus=MTAStatus()
    timeMTA_ReportedData=mtaStatus.getReportTime()
    
    subwayDictionary=mtaStatus.getSubway()
    print 'as of %s MTA Reported\n\n' % (timeMTA_ReportedData) # this is provided by MTA
    for name in sorted(subwayDictionary.keys()):
        print 'Subway Line: %5s has Status: %s' % (subwayDictionary[name].getName(), subwayDictionary[name].getStatus())
        
    busDictionary=mtaStatus.getBus()
    for busName in sorted(busDictionary.keys()):
        print 'Bus Line: %5s has Status: %s' % (busDictionary[busName].getName(), busDictionary[busName].getStatus())

    btDictionary=mtaStatus.getBT()
    for btName in sorted(btDictionary.keys()):
        print 'BT Line: %5s has Status: %s' % (btDictionary[btName].getName(), btDictionary[btName].getStatus())

    lirrDictionary=mtaStatus.getLIRR()
    for lirrName in sorted(lirrDictionary.keys()):
        print 'LIRR Line: %5s has Status: %s' % (lirrDictionary[lirrName].getName(), lirrDictionary[lirrName].getStatus())
        
    mnDictionary=mtaStatus.getMetroNorth()
    for mnName in sorted(mnDictionary.keys()):
        print 'MetroNorth Line: %5s has Status: %s' % (mnDictionary[mnName].getName(), mnDictionary[mnName].getStatus())
    logging.info('Normal Termination')
