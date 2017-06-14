import logging

httpProtocol = "http"
host = "192.168.118.94"
httpPort = "80"
telnetPort = "23"

adminLogin = "admin"
adminPassword = "password"

logFile = "web_test.log"
webDriverServerIP = "192.168.118.37"

logging.basicConfig(filename=logFile, filemode='w', format = u'%(asctime)-8s %(levelname)-8s [%(module)s -> %(funcName)s:%(lineno)d] %(message)-8s', level = logging.INFO)