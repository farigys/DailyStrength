'''
Created on Sep 11, 2013

@author: bgyawali

this program will read the HTML file and converts the content into XML format

besides converting into XML format, it also lists the authors in file peopleLists.txt and the treatments in treatments.txt file

There is another program PeopleCrawler.py which will crawl the HTML files of the people by reading peopleLists.txt file,
The program to crawl the treatments is not yet implemented
'''
from BeautifulSoup import *
import os, shutil
from lxml import etree
import xml.etree.ElementTree as ET



# ## to parse the main content of the forum. 
def parseForumMainContent(soup, people, treatments, root):
    # ## for the problem statement
    problem = ET.SubElement(root, "problem")
    discussion = soup.findAll("table", {"class":"discussion_topic"})
    for t in discussion:

        # ## name of author        
        personIdBlock = t.contents[1].contents[1].contents[1].contents[0].contents[1].contents[3].contents[1]
        people[personIdBlock.get('href')] = str(personIdBlock.contents[0]).strip()
        person = ET.SubElement(problem, "person")
        person.set("id", personIdBlock.get('href'))
        person.text = str(personIdBlock.contents[0]).strip() 
        
        
        date = ""
        # ## contents 
        contentBlock = t.contents[1].contents[3].contents[1]
        contentElement = ET.SubElement(problem, "content")
        for index in range(len(contentBlock.contents)):
            contentPart = contentBlock.contents[index]
            
            # #parses all the text strings
            if (isinstance(contentPart, NavigableString) and  not isinstance(contentPart, Comment)):
                if(str(contentPart).strip() != ""):
                    textElement = ET.SubElement(contentElement, "text")
                    #print str(contentPart).strip()
                    textElement.text = str(str(contentPart).strip().encode('utf-8').decode('ascii', 'ignore'))
            # # parses anything having tag
            else:
                # ## parses if the tag is 'a'
                if (isinstance(contentPart, Tag) and contentPart.name == 'a'):
                    # ## checks if the hyperlink points to treatments
                    if(re.search('treatment', contentPart.get('href'))):
                        treatments[contentPart.get('href')] = contentPart.contents[0]
                        splits = contentPart.get('href').split('/')
                        treatmentElement = ET.SubElement(contentElement, "treatment")
                        treatmentElement.set("id", splits[len(splits) - 1])
                        treatmentElement.text = str(contentPart.contents[0])                    
                    # ## for those hyperlinks which point to anything else besides treatment
                    elif (isinstance(contentPart, Tag)):
                        if(len(contentPart.contents) != 0):
                            textElement = ET.SubElement(contentElement, "text")
                            textElement.text = str(str(contentPart.contents[0]).strip().encode('utf-8').decode('ascii', 'ignore'))                    
                # # parses the date inside the span   
                elif(isinstance(contentPart, Tag) and contentPart.name == 'span'):
                    splits = contentPart.contents[0].split()
                    date = splits[2].replace(',', ' ') + splits[3] + splits[4]
                

        # ## adding date element        
        dateElement = ET.SubElement(problem, "date")
        dateElement.text = str(date)
        # print "<date>"+date+"</date>"
        # print "<content>"+mystr.strip()+"</content>\n\n"
        
    ### number of replies
    numberOfReplies = '0'
    discussion = soup.findAll("table", {"id":"discussions_tool_bar"})
    for t in discussion:
        #print str(t.contents[1].contents[1].contents[1].contents[0]).strip()
        matching = re.search(r'[0-9]+',str(t.contents[1].contents[1].contents[1].contents[0]).strip())
        numberOfReplies =  matching.group(0)
    return numberOfReplies

        
        
        


# # to parse all the replies            
def parseForumReplies(soup, people, treatments, repliesElement):           
    # for replies

    p = soup.findAll("table", {"class":"reply_table"})
    for t in p:
        for index in my_range(1, len(t.contents) - 1, 4):
            # print "<replies>"
            l = t.contents[index]

            # ## reply number
            noOfReplies = l.contents[3].contents[1].contents[1].contents[0].contents[1].contents[1].contents[0]
            match = re.search(r'.*#([0-9]+)', noOfReplies)
            replyElement = ET.SubElement(repliesElement, "reply")
            replyElement.set("id", match.group(1)) 

            # ## reply person id
            personIdBlock = l.contents[1].contents[1].contents[0].contents[1].contents[3].contents[1]
            people[personIdBlock.get('href')] = str(personIdBlock.contents[0]).strip()
            personElement = ET.SubElement(replyElement, "person")
            personElement.set("id", personIdBlock.get('href'))
            personElement.text = str(personIdBlock.contents[0].strip()) 
            #print "reply id " + str(personIdBlock.contents[0].strip()) 
            
            # ## reply date            
            replyDateBlock = l.contents[3].contents[1].contents[1].contents[0].contents[1].contents[3].contents[0]
            replyDate = re.sub(r"[\s]", '', str.strip(str(replyDateBlock)).replace("&nbsp", ""))
            replyDate = replyDate.replace(';', ' ')
            dateElement = ET.SubElement(replyElement, "date")
            dateElement.text = replyDate
            
            # ## reply main body
            contentBlock = l.contents[3].contents[1].contents[3]
            contentElement = ET.SubElement(replyElement, "content")
            for ii in range(len(contentBlock.contents)):
                contentPart = contentBlock.contents[ii]
                # ## parses the text string
                if (isinstance(contentPart, NavigableString) and  not isinstance(contentPart, Comment)):
                    if(str(contentPart).strip() != ""):
                        textElement = ET.SubElement(contentElement, "text")
                        #print "contentpart'" + str(str(contentPart).strip().encode('utf-8').decode('ascii', 'ignore')) + "'"
                        textElement.text = str(str(contentPart).strip().encode('utf-8').decode('ascii', 'ignore'))
                # ## parses the anythingl having tag        
                else:
                    # ## if the tag is 'a'
                    if (isinstance(contentPart, Tag) and contentPart.name == 'a'):
                        # ## if the hyperlink contains the link to treatments
                        if(re.search('http://www.dailystrength.org/treatments', contentPart.get('href'))):
                            treatments[contentPart.get('href')] = contentPart.contents[0]
                            splits = contentPart.get('href').split('/')
                            treatmentElement = ET.SubElement(contentElement, "treatment")
                            treatmentElement.set("id", splits[len(splits) - 1])
                            treatmentElement.text = str(contentPart.contents[0])
                        # ## if link contains anything else besides treatment    
                        elif (isinstance(contentPart, Tag) and contentPart.name != 'br'):       
                            textElement = ET.SubElement(contentElement, "text")
                            if(len(contentPart.contents)>=1):
                                textElement.text = contentPart.contents[0]

  
            
           
               
            
def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

   
    

def get_user_params():

    user_params = {}
    # get user input params
    user_params['inputDir'] = raw_input('Input Directory [Back-Pain/HTML]: ')
    user_params['outputDir'] = raw_input('\nOutput Directory [Back-Pain]: ')
    user_params['inputFile'] = raw_input('\nInput File [Back-Pain/FilesLists.txt]: ')

    
    if user_params['inputDir'] == '' or user_params['outputDir'] == '' or user_params['inputFile'] == '':
        print "Invalid seed URL or Output directory. Try again"
        sys.exit()   
    return user_params



def dump_user_params(user_params):

    # dump user params for confirmation
    print 'Input Directory:    ' + user_params['inputDir']
    print 'Output Directory:   ' + user_params['outputDir']
    print 'Input File:   ' + user_params['inputFile']
    return

    

# ## main method
def main():
    user_params = get_user_params()
    dump_user_params(user_params)
    outputDir = user_params['outputDir'] + "/XML"
    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)
    os.makedirs(outputDir)
    
    # ## create a dictionary for people links
    people = {}
    treatments = {}
    # ## 
    
    
    # ## read input file
    ### reads the input file containing all the threads. and for each of these threads, it will read HTML files and convert them into XML file
    lines = [line.strip() for line in open(user_params['inputFile'])]
    forumStatisticsFile = open(user_params['outputDir']+"/RepliesPerForum.txt","w")
    # # read each lines of input file.these lines indicate the forum name
    forumCount = len(lines)
    allRepliesCount = 0
    
    ### for each threads, it starts loop to create XML. 
    for i in range(len(lines)):
        
        forumPages = []
        root = etree.Element("doculment")
        
        ### this for loop is to see if any of the threads have sub pages as well or not.
        for files in os.listdir(user_params['inputDir']):
            fileName =lines[i].rsplit("/",1)[1]
            #print fileName, lines[i]
            # ## check if there are multiple pages of the same forum, i.e. page 1, page 2, page 3
            if files.startswith(fileName):
                #print "inside if"
                forumPages.append(files)
        
        ### sort the subpages so that the first page will be main page and the other will be subpages 
        forumPages.sort()
        #print forumPages[0]
        ## start reading the first page, i.e. main page
        print "processing file " + lines[i] + " started. Number of pages: " + str(len(forumPages))
        # # for the first page, we get main post and the replies
        eachHtml = open(user_params['inputDir'] + "/" + forumPages[0], "r")
        content = eachHtml.readlines()
         
        # create beautiful soup object
        newContent=""
        for c in content:
            for l in c:
                if valid_XML_char_ordinal(ord(l)):
                    newContent = newContent+ l
        
        soup = BeautifulSoup(newContent)
        #cleaned_string = 
        
        
        ### this method will parse the main page. i.e. first page and makes the XML tags for the problem only
        replyCount = parseForumMainContent(soup, people, treatments, root)
        allRepliesCount = allRepliesCount + int(replyCount)
        replies = ET.SubElement(root, "replies")
        replies.set("repliesCount",replyCount)
        
        ### initialize replies count and starts creating XML tags for replies
        parseForumReplies(soup, people, treatments, replies)
       
       ### now iterate through all the other pages of the thread, and put the content of the other pages in replies
        # ## find all the replies of the next page if a forum has replies in multiple pages
        for j in range(1, len(forumPages)):
            print forumPages[j]
            # print forumPages[j]
            eachHtml = open(user_params['inputDir'] + "/" + forumPages[j], "r")
            content = eachHtml.readlines()
            newContent=""
            for c in content:
                for l in c:
                    if valid_XML_char_ordinal(ord(l)):
                        newContent = newContent+ l
            # create beautiful soup object
            soup = BeautifulSoup(newContent)
            parseForumReplies(soup, people, treatments, replies)
        
        doc = etree.ElementTree(root)    
        outFile = open(outputDir + "/" + forumPages[0] + ".xml", 'w')
        doc.write(outFile, encoding="utf-8", xml_declaration=True, method="xml", pretty_print=True)
        # print(etree.tostring(root, pretty_print=True))
        forumStatisticsFile.write(forumPages[0] + "\t" + str(replyCount) + "\n")
        print "processing file "+lines[i] + " completed"

    forumStatisticsFile.close()
    peopleFileName = user_params['outputDir'] + "/peopleLists.txt"
    treatmentFileName = user_params['outputDir'] + "/treatmentLists.txt"
    peopleFile = open(peopleFileName, "w")
    for temp in people:
        #print temp + "\t" + people[temp]
        peopleFile.write(temp + "\t" + people[temp] + "\n")
        
    treatmentFile = open(treatmentFileName, "w")    
    for temp in treatments:
        #print temp + "\t" + treatments[temp]        
        treatmentFile.write(temp + "\t" + treatments[temp] + "\n")
                
### this method is used to select only the valid XML characters. if a character is not a valid XML character, then ignore it. 
def valid_XML_char_ordinal(i):    
    return ( # conditions ordered by presumed frequency
        0x20 <= i <= 0xD7FF 
        or i in (0x9, 0xA, 0xD)
        or 0xE000 <= i <= 0xFFFD
        or 0x10000 <= i <= 0x10FFFF
        )


            
        
if __name__ == '__main__':
    main()
