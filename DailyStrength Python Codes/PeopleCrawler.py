'''
Created on Sep 18, 2013

@author: bgyawali


this program downloads all the HTML files for the peoples. 
'''
import mechanize, shutil, os
from time import sleep


def purge_already_fetched(userLinks, outputDir):

    # list of threads that still need downloading
    rem_list = []
    # check each tweet to see if we have it
    for item in userLinks:
        linkId = getLinkId(item)
        thread_file = outputDir + '/' + linkId + ".html"
        if(not os.path.exists(thread_file)):
            rem_list.append(item)
    return rem_list


def getLinkId(userLink):
    link = userLink.split("\t")[0]
    linkId = link.split('/')[2]
    return linkId
        
    

def download_forums(userLink, outputDir):
    link = userLink.split("\t")[0]
    link = "http://www.dailystrength.org" + link
    try:
        linkId = getLinkId(userLink)
        outputFile =   outputDir + "/" + linkId + ".html" 
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.set_handle_equiv(False)
        br.open(link)
        html = br.response().read()
       
        f = open(outputFile, "w")
        f.write(html)
        f.close()
    except (mechanize.HTTPError, mechanize.URLError) as e:
        if isinstance(e,mechanize.HTTPError):
            f = open(outputFile, "w")
            f.close()
        elif isinstance(e, mechanize.URLError):
            print "error in downloading " + str(e)
            print (link)
        else:
            raise e.reason.args
    sleep(5)

def read_total_list(inputDir, inputFile):

    # read total fetch list csv
    total_list = [line.strip() for line in open(inputDir + "/" + inputFile)]
    return total_list

   

### start of main method
def main(inputDirs, inputFile, outputDir):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    
    # ## read the input file
    for dirs in inputDirs:
        userLinks = read_total_list(dirs, inputFile)
        if os.path.exists(outputDir):
            fetch_list = purge_already_fetched(userLinks, outputDir)
        else:
            os.makedirs(outputDir)
            fetch_list = userLinks
        print "condition: " + dirs
        print "Total threads: " + str(len(userLinks))
        print "Threads remaining to download: " + str(len(fetch_list))
        for i in range(0, len(fetch_list)):
			print str(i + 1),        
			download_forums(fetch_list[i], outputDir)
        
         
           
    
    
if __name__ == "__main__":
    inputDirs = ["Acne", "Asthma","Back-Pain", "Bone-Cancer","Diets-Weight-Maintenance", 
                 "Immigration-Law","Loneliness", "Lung-Cancer", "Miscarriage",
                  "Pregnancy", "Rheumatoid-Arthritis", "War-In-Iraq"]
    outputDir = "PeopleHTML"
    inputFile = "peopleLists.txt"
    main(inputDirs, inputFile, outputDir)
    
