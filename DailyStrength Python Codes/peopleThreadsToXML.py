'''
Created on Sep 18, 2013

@author: bgyawali

this program was written to read the HTML files of each people listed in peopleLists.txt and convert them into XML.

But, this is not a good approach because, if download fails, then this program always starts from the first. 
So, I have already written a program to download HTML files of peoples. That is PeopleCrawler.py program.

Once, all the HTML people files are downloaded, we can convert it into XMl file. To parse HTML and then convert into XML, this program can be used.

But, do not use this program for default. use the logic to parse HTML into XML from here and develop another program. 


'''
import mechanize, shutil, os
from BeautifulSoup import *
from time import sleep
from lxml import etree
import xml.etree.ElementTree as ET



### start of people crawler
def peopleCrawler(soup, root):
        # ## generagint gender, age, and location elements        
        genderElement = ET.SubElement(root, "gender")        
        ageElement = ET.SubElement(root, "age")
        locationElement = ET.SubElement(root, "location")
        # ## to populate gender, age, and location
        discussion = soup.findAll("div", {"class":"more-details"})
        for t in discussion:
            if(len(t.contents) > 1):
                asl = str(t.contents[1].contents[0]).split(",")
                location = ""
                for j in range(2, len(asl)):
                    location = location + "," + asl[j]

                if(len(asl) >= 1):
                    genderElement.text = (str(asl[0]).strip().encode('utf-8').decode('ascii','ignore'))
                else:
                    genderElement.text = 'Undefined'
                if(len(asl) >= 2):
                    ageElement.text = str(asl[1]).strip()
                else:
                    ageElement.text = 'Undefined'                
                locationElement.text = location.strip(",")
               
            
            
            
        # ## creating member since element and parsing html to extract member since contents            
        memberElement = ET.SubElement(root, "memberSince")    
        memberSince = soup.findAll("span", {"id":"memberSince"})
        for t in memberSince:            
            match = re.search(r'Member since (.*)', str(t.contents[0]))
            # print "member since: " + match.group(1).strip() 
            memberElement.text = match.group(1).strip()
            
        # ## creating description element of xml and extracting the description given by the user to himself   
        descriptionElement = ET.SubElement(root, "description")    
        description = soup.findAll("p", {"class":"full"})
        tempCnt = 0
        for t in description:
            if(tempCnt == 0):
                # print "details: " + str(t.contents[0])
                #str(str(contentPart).strip().encode('utf-8').decode('ascii', 'ignore'))
                descriptionElement.text = (str(t.contents[0]).strip().encode('utf-8').decode('ascii','ignore'))
                tempCnt = tempCnt + 1  
        
        
            
        
def emptyCrawler(root):
    genderElement = ET.SubElement(root, "gender")
    ageElement = ET.SubElement(root, "age")
    locationElement = ET.SubElement(root, "location")
    memberElement = ET.SubElement(root, "memberSince")
    descriptionElement = ET.SubElement(root, "description")
    

### start of main method
def main(inputFile, outputDir):
    outputDir = outputDir + "/People"
    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)
    os.makedirs(outputDir)
    
    # ## read the input file
    userLinks = [line.strip() for line in open(inputFile)]
    for i in range(len(userLinks)):
        # ## initialing xml root
        root = etree.Element("document")      
        personElement = ET.SubElement(root, "person")
        link, username = userLinks[i].split("\t")
        linkId = link.split('/')[2]
        personElement.set("id", link)
        personElement.text = username
        link = "http://www.dailystrength.org" + link
                
        # ## initializing mechanize browser to read the html files
        br = mechanize.Browser()
        br.set_handle_robots(False)
        print link + " started processing"
        try:
            br.open(link)
            # br.open(link)
            html = br.response().read()
            # ## this is going to parse the html file
            soup = BeautifulSoup(html)
            peopleCrawler(soup, root)
        except (mechanize.HTTPError, mechanize.URLError) as e:
            if isinstance(e,mechanize.HTTPError):
                emptyCrawler(root)
            else:
                raise e.reason.args
        
        
        
        # ## write the xml to the output
        fileName = open(outputDir + "/" + linkId + ".xml", "w")
        doc = etree.ElementTree(root)    
        doc.write(fileName, encoding="utf-8", xml_declaration=True, method="xml", pretty_print=True)
       # print etree.tostring(root, pretty_print=True)  
        print link + " completed processing"
        sleep(4)   
    
    
if __name__ == "__main__":
    outputDir = "Back-Pain"
    inputFile = outputDir+"/peopleLists.txt"
    main(inputFile, outputDir)
    
