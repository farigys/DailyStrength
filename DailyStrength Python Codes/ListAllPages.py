'''
Created on Oct 31, 2013

@author: bgyawali
'''
'''
this program reads the url given, and then finds all the threads in the URLs, and lists the URLs to all the threads. 

For example: if we give the URL for bone-cancer: i.e., http://www.dailystrength.org/c/Bone-Cancer/forum, 
it reads the starting page and the last page: in this case, it is 1 and 4.
then it loops from page 1 to page 4 and lists the link to all the threads.

FindHighest number finds the largest number in the pages of the URL. I.e., in the above url, the highest number is 4. so, this program returns 4. 
FindAllThreads lists the URLs for threads 1 to 4. 
 
'''
import mechanize, os, shutil, sys
from time import sleep
from BeautifulSoup import *




# ## this method will lists all the threads present in a seed URL and puts it into a dictionary and returns back.
# ## example: normally a seedURL contains 20 threads. it will list all the threads and puts the urls to the threads into the dictionary
def findAllThreads(seedUrl, threads):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_equiv(False)
    print "crawling link: " + seedUrl
    br.open(seedUrl)
    for l in br.links():
        newUrl = l.base_url.rpartition('/')[0] + l.url        
        # ## populating all forum links
        if(re.search('/c/.+/forum/[0-9]+.*', newUrl)):
            threads.append(newUrl)
               

    # return threads

# ## this method will return the highest number of pages present in the given seed URL. Eg. the bone cancer forum contains 4 pages. So, it will return 4
def findHighestPageNumber(seedUrl):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    print "seed url : " + seedUrl
    br.open(seedUrl)
    html = br.response().read()
    soup = BeautifulSoup(html)
    mainBody = soup.findAll("div", {"class":"modulepad sg_modulepad"})
    myPageArray = []
    for t in mainBody:
        for j in my_range(3, len(t.contents[1].contents[4].contents[1].contents) - 1, 2):
            val = str(t.contents[1].contents[4].contents[1].contents[j].contents[0])
            if(str.isdigit(val)):
                myPageArray.append(int(val))
                
    myPageArray = sorted(myPageArray)
    maxmPage = myPageArray[len(myPageArray) - 1]
    return maxmPage
    
            
def my_range(start, end, step):
    while start <= end:
        yield start
        start += step



## this method writes the urls of the threads to the file. 
def writeAndCrawlAllThreads(crawledPagesFile, crawledThreadsFile, minPage, maxmPage, seedUrl, crawledThreadsDict):
	print len(crawledThreadsDict)
	print minPage, maxmPage
    
    # ## starting from minimum page to maximum page, it will crawl all the threads
	for j in range(minPage, maxmPage + 1):
		newUrl = seedUrl + "/page-" + str(j)
		# print seedUrl
		threads = []
		findAllThreads(newUrl, threads)
		for i in range(len(threads)):
			if threads[i] not in crawledThreadsDict:
				crawledThreadsFile.write(threads[i] + "\n")
		crawledPagesFile.write(newUrl + "\n")
		print "page " + newUrl + " completed"
		sleep(10) 






def get_user_params():

    user_params = {}
    # get user input params
    user_params['seedUrl'] = raw_input('Seed URL: ')
    user_params['outputDir'] = raw_input('\nOutput Directory: ')

    
    if user_params['seedUrl'] == '' or user_params['outputDir'] == '':
		print "Invalid seed URL or Output directory. Try again"
		sys.exit()   
    return user_params



def dump_user_params(user_params):

    # dump user params for confirmation
    print 'Seed URL:    ' + user_params['seedUrl']
    print 'Output Directory:   ' + user_params['outputDir']
    return




        
def main():
    
	user_params = get_user_params()
	dump_user_params(user_params)
    # this program first finds the highest number of page in the given u rl
	maxmPage = findHighestPageNumber(user_params['seedUrl'])
	minPage = 1
    # # create the output directory if it doesn't exist
	if not os.path.exists(user_params['outputDir']):
		os.makedirs(user_params['outputDir'])

    # # this file is to list all the pages whose threads are crawled.
    # # e.g., if all the 20 threads in page http://www.dailystrength.org/c/Bone-Cancer/forum/page-2 are written to 
	allPagesFileName = user_params['outputDir'] + "/PagesCrawled.txt"
    # ## this file is to list all the threads
	allThreadsFilesName = user_params['outputDir'] + "/FilesLists.txt"
	crawledThreadsDict = {}
	if(os.path.exists(allPagesFileName)):
		crawledPagesFile = open(allPagesFileName, "r")
		allPages = crawledPagesFile.readlines()
		print(len(allPages))
        # ## this is to find the last page that is crawled before. 
        # ## for example: in the previous run, the threads upto page 2 are listed, then in this run, it will start crawling from page 3
		if(len(allPages) > 1):
			lastPage = allPages[len(allPages) - 1]
			parts = lastPage.rsplit('/', 1)
			m = re.search('page-([0-9]*)', parts[1])
			minPage = int(m.group(1)) + 1
			
		elif(len(allPages) == 1 and allPages[0].strip() != ""):
			minPage = 2
		crawledThreadsFile = open(allThreadsFilesName, "r")
		allThreads = crawledThreadsFile.readlines()
        # ## read the FilesLists.txt file and puts in dictionary saying these threads are already listed. 
		for r in range(len(allThreads)):
			crawledThreadsDict[allThreads[r].strip("\n")] = 1
		crawledPagesFile = open(allPagesFileName, "a")
		crawledThreadsFile = open(allThreadsFilesName, "a")
		# ## this method now lists the remaining threads into the file FilesLists.txt
		writeAndCrawlAllThreads(crawledPagesFile, crawledThreadsFile, minPage, maxmPage, user_params['seedUrl'], crawledThreadsDict)
		
		
		
	else:	
		crawledPagesFile = open(allPagesFileName, "w")
		crawledThreadsFile = open(allThreadsFilesName, "w")
		writeAndCrawlAllThreads(crawledPagesFile, crawledThreadsFile, minPage, maxmPage, user_params['seedUrl'], crawledThreadsDict)
	crawledPagesFile.close()
	crawledThreadsFile.close()
     
        
if __name__ == "__main__":    
    main()
