
import os, sys


dictMap = {'Acne':'http://www.dailystrength.org/c/Acne/forum',
'ADHD':'http://www.dailystrength.org/c/ADHD-ADD/forum',
'Alcohalism':'http://www.dailystrength.org/c/Alcoholism/forum',
'Asthma':'http://www.dailystrength.org/c/Asthma/forum',
'Back-Pain':'http://www.dailystrength.org/c/Back-Pain/forum',
'Bipolar-Disorder':'http://www.dailystrength.org/c/Bipolar-Disorder/forum',
'Bone-Cancer':'http://www.dailystrength.org/c/Bone-Cancer/forum',
'COPD':'http://www.dailystrength.org/c/COPD-Emphysema/forum',
'Diets-Weight-Maintenance':'http://www.dailystrength.org/c/Diets-Weight-Maintenance/forum',
'Fibromyalgia':'http://www.dailystrength.org/c/Fibromyalgia/forum',
'Gastric-Bypass-Surgery':'http://www.dailystrength.org/c/Gastric-Bypass-Surgery/forum',
'Immigration-Law':'http://www.dailystrength.org/c/Immigration-Law/forum',
'Infertility':'http://www.dailystrength.org/c/Infertility/forum',
'Loneliness':'http://www.dailystrength.org/c/Loneliness/forum',
'Lung-Cancer':'http://www.dailystrength.org/c/Lung-Cancer/forum',
'Migraine':'http://www.dailystrength.org/c/Migraine-Headaches/forum',
'Miscarriage':'http://www.dailystrength.org/c/Miscarriage-Stillbirth/forum',
'Pregnancy':'http://www.dailystrength.org/c/Pregnancy/forum',
'Rheumatoid-Arthritis':'http://www.dailystrength.org/c/Rheumatoid-Arthritis/forum',
'War-In-Iraq':'http://www.dailystrength.org/c/War-in-Iraq/forum'}


allURLsFile = open("AllURLsListing.txt", "w")
for temp in sorted(dictMap):
    if os.path.exists(temp + "/XML"):
        for files in os.listdir(temp + "/XML"):
            urlPath = files.split('.')[0]
            allURLsFile.write(dictMap[temp]+"/"+urlPath+"\n")
        print "listing " + temp + " completed"
    else:
        print temp + " doesn't exist"


allURLsFile.close()