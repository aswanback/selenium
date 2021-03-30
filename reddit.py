import time
import re
import os
from editing import *
import misc

def reddit(folder,subreddit):  #def reddit_farmer(subreddit, timeframe, number,filepath, ):
    get = misc.getme(folder)

    get.site("https://www.reddit.com/" + subreddit + "/")

    get.by_class_name("_3Oa0THmZ3f5iZXAQ0hBJ0k").click()
        #url = get.by_xpath("/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[4]/div/a/img").get_attribute('href')
        #print(url)
        #get.site(url)
    #get.web.switch_to.window(get.web.window_handles[1])
        #new_url = get.current_url()
        #print(new_url)
        #filename = new_url.translate({ord(i): None for i in '/:'})
        #misc.download_by_link(url=new_url,filepath=folder,filename=filename)

    get.site("https://www.reddit.com/" + subreddit + "/")

    last_height = get.web.execute_script("return document.body.scrollHeight")

    while True:

        get.web.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(0.5)
        new_height = get.web.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height



reddit('/users/calebstevens/documents/Selenium_data/reddit/', "r/memes")