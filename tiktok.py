import time
import os
from editing import *
import misc

def tik_tok_farmer(folder, number):
    get = misc.getme(folder, mute=True)  # optional arguments: mute, headless, incognito, all False by default
    try:

        get.site("https://www.tiktok.com/en")
        time.sleep(3)
        get.by_xpath("/html/body/div/div/div[1]/div/div[3]/button").click()
        get.by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div[2]/div[2]").click()


        get.by_xpath("/html/body/div[2]/div/form/fieldset[1]/div[1]/input").send_keys("nrubenstein0405@gmail.com")
        get.by_xpath("/html/body/div[2]/div/form/fieldset[1]/div[2]/input").send_keys("Nacny123")
        get.by_xpath("/html/body/div[2]/div/form/fieldset[2]/input[1]").click()
        get.by_xpath("/html/body/div/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[2]/h2").click() # click following
        get.by_class_name("item-video-container").click() # click first video
        time.sleep(0.5)

        url = get.current_url()
        for num in range(number):
            time.sleep(0.5)
            get.site("https://qload.info/")
            time.sleep(1)
            get.by_xpath("/html/body/main/div[1]/div[2]/div/form/div/input").send_keys(url) # put in url to downloader
            get.by_xpath("/html/body/main/div[1]/div[2]/div/form/div/div/button").click()   # click download

            #misc.wait_download_complete(folder)
            time.sleep(10)

            get.site("https://www.tiktok.com/following?lang=en") # back to tiktok following
            get.by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[1]").click()
            time.sleep(0.1)
            get.by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[2]").click()
            time.sleep(0.2)
            get.by_class_name("item-video-container").click() # get first video

            for i in range(num+1):
                time.sleep(0.1)
                get.by_class_name("arrow-right").click() #iterate to correct video
                time.sleep(0.1)

            url = get.current_url()
    finally:
        files = os.listdir(folder)
        for i in range(len(files)):
            os.rename(folder+'/'+files[i],folder+'/'+f"video{i}.mp4")
        time.sleep(15)
        get.close()

if __name__ == "__main__":
    tik_tok_farmer("/Users/calebstevens/documents/Selenium_data/tiktok", 30)
    #concat("/users/calebstevens/documents/Selenium_data/tiktok",resolution='tiktok')
