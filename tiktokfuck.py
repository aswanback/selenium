import time
import os
import misc

def tik_tok_farmer(folder, number):
    get = misc.getme(folder, mute=True)  # optional arguments: mute, headless, incognito, all False by default

    get.site("https://accounts.google.com/o/oauth2/v2/auth/identifier?client_id=1096011445005-sdea0nf5jvj14eia93icpttv27cidkvk.apps.googleusercontent.com&response_type=token&redirect_uri=https%3A%2F%2Fwww.tiktok.com%2Flogin%2F&state=%7B%22client_id%22%3A%221096011445005-sdea0nf5jvj14eia93icpttv27cidkvk.apps.googleusercontent.com%22%2C%22network%22%3A%22google%22%2C%22display%22%3A%22popup%22%2C%22callback%22%3A%22_hellojs_6gt23cml%22%2C%22state%22%3A%22%22%2C%22redirect_uri%22%3A%22https%3A%2F%2Fwww.tiktok.com%2Flogin%2F%22%2C%22scope%22%3A%22basic%22%7D&scope=openid%20profile&prompt=consent&flowName=GeneralOAuthFlow")
    time.sleep(1)
    get.by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys("nrubenstein0405@gmail.com")
    get.by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button").click()
    get.by_xpath("/html/body/div[1]/div/div[1]/form/button").click()


if __name__ == "__main__":
    tik_tok_farmer("/Users/andrewswanback/documents/sd", 30)