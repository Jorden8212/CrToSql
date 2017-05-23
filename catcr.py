import requests
from bs4 import BeautifulSoup
import re
import shutil
import os
import MySQLdb

HTML_PARSER = "html.parser"
ROOT_URL = 'http://pet-hotels.com.tw/'
LIST_URL = 'http://pet-hotels.com.tw/tag/cats-only/'
SHOP_PATH = 'shop/'
SPACE_RE = re.compile(r'\s+')

def get_link():

   id=0
   for i in range(1,10):
      if i == 1:
         origCode = requests.get(LIST_URL)
      else:
         origCode = requests.get(LIST_URL+'page/'+str(i)+'/')
      
      if origCode.status_code == requests.codes.ok:
         soup = BeautifulSoup(origCode.content,HTML_PARSER)
         shopLinkTag = soup.find_all('a', attrs = {'class':'f-left'})
      else:
         break     
      
      
      for link in shopLinkTag:
         shopLink = link['href']
         insert = get_info(shopLink)
         insToMySQLdb(str(id)+','+insert)
         id=id+1
       
       

def get_info(shopLink):
   origCode = requests.get(shopLink)

   dname = ''
   dtype = ''
   dbudget = ''
   dfeature = ''
   dlink = ''
   dTel = ''
   dLine =''
   dHome =''
   
   #print('a1')
   if origCode.status_code == requests.codes.ok:
      #print('b1')
      soup = BeautifulSoup(origCode.content,HTML_PARSER)
      infoTag = soup.find('div',attrs = {'class':'entry-content-info clearfix'})
      name = infoTag.find ('h1', attrs = {'class':'entry-title f-left'} )
      budget = soup.find_all('p',attrs = {'class':'cate_info'})
      piclink = soup.select('a[rel="pic"]')
      features = soup.find_all('p',attrs = {'class':'features-subtitle'})
      feature_detail = soup.find_all('p',attrs = {'class':'f-left'})
      googlemap = soup.find_all('iframe',attrs = {'class':'gmap_iframe'})
      line = soup.find('td',attrs = {'class':'wtd'})
      contactInfo = soup.find('table',attrs = {'class':'info'})
      contactInfo_str = str(contactInfo)
      homePage = soup.find_all('a',attrs = {'target':'_blank'})
      """tel = soup.find('td',attrs = {'class':'wtd'})"""      

      
      if name is not None:#Link & name
         print(shopLink+'\n')
         dname = re.sub(r'\[.+','',name.text)
         print(dname)   
      else:
         exit()

      for content in budget:#Type & budget
         if dtype =='':
            dtype = content.text
            print(dtype+'\n')
         else:
            dbudget = content.text
            print(dbudget+'\n')

      for i in range(1,5):#feature&detail
         s='features_list features0'+str(i)+' clearfix'
         features = soup.find('div',attrs = {'class':s})
         if features is not None:
            for a in features:
               dfeature=dfeature+a.text+''
         print dfeature


      for link in googlemap:#googlemap without api
         sub = '&'+link['src'].split('&')[-3]+'&'+link['src'].split('&')[-2]+'&'+link['src'].split('&')[-1]
         dlink = re.sub(sub,'',link['src'])
         print (dlink+'\n')

      """for number in tel:#Tel
         print ('Tel:'+number+'\n')"""

      for i in range(1,3):#phone & line
         if dTel == '':
            dTel = contactInfo_str.split('<th>')[i].split('<td')[1].split('>')[1].split('</td')[0]
            print dTel
         else:
            dLine = contactInfo_str.split('<th>')[i].split('<td')[1].split('>')[1].split('</td')[0]
            print dLine

      for link in homePage:
         dHome = link['href']
         print dHome
         break


      #下面的code是下載圖片    
      """if piclink is not None:
         i = 0
         for pic in piclink:
            #file_path = "C:\Users\Jorden\Desktop\potel\picture"
            #dir_name = "picture"
            #if not os.path.exists(file_path):
            #  os.makedirs(dir_name)

            if pic['href'] != '':
               #print 'f'
               donpic = shopLink.split('/')[4]+str(i)#//select shopname
               #print donpic
               pic_res = requests.get(pic['href'],stream=True)#//get picture resource and check stream
               f = open(donpic+'.jpg','wb')#//create & open the file (automatic create when file doesnt exist) and type "write with binary"
               shutil.copyfileobj(pic_res.raw,f)#//shutil tool to download
               f.close()
               i=i+1#//name numbering """

      print '---------------------------------------------------------------'
      
      return "'"+dname+"','"+dtype+"','"+dbudget+"','"+dfeature+"','"+dlink+"','"+dTel+"','"+dLine+"','"+dHome+"'"
      


      



def insToMySQLdb(insert):
   
   db = MySQLdb.connect(host="localhost", user="root", passwd="Star57421", db="potel",charset='utf8')

   cursor = db.cursor()

   insdb = "insert ignore into cat values("+insert+")"

   #print insdb

   cursor.execute(insdb)

   db.commit()

   db.close()

   


if __name__ == '__main__':
   get_link()  
