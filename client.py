import uiautomator2 as u2

d = u2.connect() # connect to device
print(d.info)

d.app_start("com.ss.android.ugc.aweme", ".main.MainActivity")

sess = d.session("com.ss.android.ugc.aweme", attach=True)

d.swipe(200, 500, 200, 100, 0.1)
