import time
import re
import os
from editing import *
import misc

def reddit(folder,subreddit):  #def reddit_farmer(subreddit, timeframe, number,filepath, ):
    get = misc.getme(folder)
    try:
        get.site("https://www.reddit.com/" + subreddit + "/")
        url = get.by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[4]/div[3]/div/div/div[2]/div[3]/div/div[2]/div/a").get_attribute('href')
        get.site(url)
        get.by_class_name("_3Oa0THmZ3f5iZXAQ0hBJ0k").click()
        get.web.switch_to.window(get.web.window_handles[1])
        new_url = get.current_url()
        print(new_url)
        filename = new_url.translate({ord(i): None for i in '/:'})
        misc.download_by_link(url=new_url,filepath=folder,filename=filename)
    finally:
        time.sleep(10)
        get.close()


