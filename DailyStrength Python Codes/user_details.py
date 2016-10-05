__author__ = 'prasha'
import os
from bs4 import BeautifulSoup #pip install beautifulsoup4
import sys

def update_age(age_groups, age):
    if(age.isdigit()):
        for ages in sorted(age_groups):
            start, end = ages
            if(int(age) in range(start, end)):
                age_groups[ages] += 1


def update_gender(genders, gender):
    if(gender in genders):
        genders[gender] += 1

def get_user_details(fname):
    user_details = None
    username = None
    html = open(os.path.join(people_html_dir, fname)).read()
    soup = BeautifulSoup(html)
    #extrat the div that contains the user_details
    user_details_div = soup.find("div", {"id": "user-details"})
    if (user_details_div):
        username_div = user_details_div.findNext('div', {"class": 'username'})
        if(username_div):
            username = username_div.text
        else:
            print fname
        more_details_div = user_details_div.findNext('div', {"class": 'more-details'})
        if (more_details_div):
            user_details = more_details_div.text
    return username, user_details

#python2.7 user_details.py /path/to/html/directory /path/to/output/file
if __name__ == "__main__":
    result = open("id_age_gender_large.txt", "w")
    people_html_dir = "PeopleHTMLTest"
    files = next(os.walk(people_html_dir))[2]
    user_age_gender = {}
    user_only_age = {}
    user_only_gender = {}

    for fname in sorted(files):
        username, user_details = get_user_details(fname)
        if (user_details):
            #print user_details
            username = username.strip()
            user_id, _ = fname.split(".")
            age_gender = user_details.split(",")
            data = "" + username + ","
            if (len(age_gender) > 0):
                if (age_gender[0].strip().isdigit()):
                    user_only_age[user_id] = age_gender[0].strip()
                    data += user_id + "," + age_gender[0].strip() + ","
                elif (age_gender[0].strip() in ["Female", "Male"]):
                    if (len(age_gender) > 1 and age_gender[1].strip().isdigit()):
                        user_age_gender[user_id] = [age_gender[1].strip(), age_gender[0].strip()]
                        data += user_id + "," + age_gender[1].strip() + "," + age_gender[0].strip()
                    else:
                        user_only_gender[user_id] = age_gender[0].strip()
                        data += user_id + ",," + age_gender[0].strip()
                result.write(data + "\n")

    print "have age and gender: ", len(user_age_gender)
    print "have age only: ", len(user_only_age)
    print "have gender only: ", len(user_only_gender)

