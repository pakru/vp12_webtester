import config, logging, telnet_login, atexit
import xpath_constants as xpathes

from time import sleep
from selenium import webdriver
# from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains


chromeCaps = DesiredCapabilities.CHROME.copy()

# print(chromeCaps)
# chromeCaps["prefs"] = {"credentials_enable_service" : "False",
#  					   "profile" : {
#  						   "password_manager_enabled" : "False"
#  					   } }
#
#
# #chromeCaps["credentials_enable_service"] = "false"
# print(chromeCaps)

driver = webdriver.Chrome()

#driver = webdriver.Remote('http://' + config.webDriverServerIP + ':4444/wd/hub',
						  #desired_capabilities=chromeCaps)

vp12Telnet = telnet_login.telnetConnection(host=config.host, port=config.telnetPort, login=config.adminLogin,
										   passwd=config.adminPassword)
vp12Telnet.cpeLogin()


def initDriver():
	# global driver
	logging.info('Init remote driver')
	# driver = webdriver.Remote('http://'+ config.webDriverServerIP +':4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)
	driver.implicitly_wait(10)
	driver.set_window_size(1200, 800)


def wait_until_element_present(how, what, wait_timeout=10):
	logging.info('Waiting for element ' + str(what))
	for i in range(wait_timeout):
		print('.', end='')
		try:
			# print('trying to find element')
			if is_element_present(how, what):
				# print('found')
				logging.info('Element ' + str(what) + ' found')
				return True
		except Exception as e:
			pass
			sleep(1)
	else:
		# print('Didnt found login element')
		print("time out")
		logging.error('Expected element ' + str(what))
		return False


def is_element_present(how, what):
	logging.info('Check if element ' + str(what) + ' present')
	try:
		driver.find_element(by=how, value=what)
	except NoSuchElementException as e:
		logging.info('Didnt found element')
		# print('No such element exception!')
		return False
	except Exception as e:
		print('Exception :' + str(e))
		logging.warning('Unexpected exception ' + str(e) + ' during searching of ' + str(what))
		return False
	return True


def preconfigure():
	pass


def webLogin():
	driver.set_window_size(1200, 800)
	base_url = config.httpProtocol + '://' + config.host + ':' + config.httpPort
	driver.get(base_url)

	wait_until_element_present(By.ID, 'login')

	switchLang(lng="ru")


	driver.find_element_by_id("login").clear()
	driver.find_element_by_id("login").send_keys(config.adminLogin)
	driver.find_element_by_id("password").clear()
	driver.find_element_by_id("password").send_keys(config.adminPassword)

	driver.find_element_by_xpath("//button[@class='btn btn-primary']").click()
	sleep(2)


def switchLang(lng="ru"):
	#Select(driver.find_element_by_xpath("//DIV[@class='dropdown-toggle']")).select_by_visible_text(lng)
	driver.find_element_by_xpath("//div[@class='dropdown-toggle']").click()
	sleep(0.5)
	#driver.find_element_by_xpath("//A[@href='#" + lng + "'][text()='" + lng + "']").click()
	driver.find_element_by_xpath("//a[@href='#ru'][text()='ru']").click()
	sleep(0.5)

def checkNetworkTabs():
	networkTabs = ('Интернет')
	driver.find_element_by_xpath("//a[text()='Сеть']").click()
	sleep(0.5)
	driver.find_element_by_xpath("//span[text()='Интернет']").click()

	if is_element_present(By.XPATH,"//legend[text()='Общие настройки']"):
		pass
	else:
		logging.error("Failure!")
		return False

	driver.find_element_by_xpath("//span[text()='QoS']").click()
	driver.find_element_by_xpath("//span[text()='Настройка MAC-адресов']").click()
	driver.find_element_by_xpath("//span[text()='Локальный DNS']").click()
	driver.find_element_by_xpath("//span[text()='Сетевой экран']").click()
	driver.find_element_by_xpath("//span[text()='Интернет']").click()

def checkSIPCommon():
	pass

def checkCommonSIP():
	driver.find_element_by_xpath("//a[text()='IP-телефония']").click()
	sleep(1)
	driver.find_element_by_xpath("//span[text()='Общие настройки SIP']").click()
	sleep(1)

	driver.find_element_by_xpath("//INPUT[@id='VoIPCommon-InviteInitTimer']").clear()
	sleep(2)
	driver.find_element_by_xpath("//INPUT[@id='VoIPCommon-InviteInitTimer']").send_keys("550")
	sleep(2)

	driver.find_element_by_xpath("(//SPAN[text()='Применить'])[2]").click()
	sleep(5)

	# assertion
	vp12Telnet.getCurrentConfig()
	cfgValue = xpathes.getValueFromCfg(vp12Telnet.yamlCfg, ("VoIP","Common") )
	if (cfgValue == "550"):
		print("Success")
	else:
		print("Failure")
		print("Cfg value: '" + cfgValue + "'  But we set: '" + "550" + "'")



def checkSIPAccount():

	driver.find_element_by_xpath("//a[text()='IP-телефония']").click()
	sleep(1)
	driver.find_element_by_xpath("//span[text()='SIP аккаунты']").click()
	sleep(1)
	Select(driver.find_element_by_id("SipAccounts-DefaultLine")).select_by_index(1)
	sleep(1)

	#

	checkInputs(xpathes.SIP_ACCOUNT_INPUTS,xpathes.SIP_ACCOUNT_APPLY_BTN)

	"""
	# set
	driver.find_element_by_xpath(xpathes.SIP_NUMBER_INPUT).clear()
	driver.find_element_by_xpath(xpathes.SIP_NUMBER_INPUT).send_keys(xpathes.SIP_NUMBER_TEST_VALUE)
	#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	actions = ActionChains(driver)
	actions.move_to_element(driver.find_element_by_xpath("(//span[text()='Применить'])[2]")).perform()

	#save
	driver.find_element_by_xpath(xpathes.SIP_ACCOUNT_APPLY_BTN).click()
	sleep(2)

	#driver.find_element_by_xpath(xpathes.SIP_NUMBER_INPUT).get_attribute("value")
	#assert
	vp12Telnet.getCurrentConfig()
	if (xpathes.getValueFromCfg(vp12Telnet.yamlCfg,xpathes.SIP_NUMBER_CONFIG) ==
			xpathes.SIP_NUMBER_TEST_VALUE):
		print("Success")
	else:
		print("Failure")
	"""

	#print(xpathes.getValueFromCfg(vp12Telnet.yamlCfg,xpathes.SIP_NUMBER_CONFIG)) # cfg value
	#print(vp12Telnet.yamlCfg.get(xpathes.SIP_NUMBER_CONFIG))
	#print(driver.find_element_by_xpath(xpathes.SIP_NUMBER_INPUT).get_attribute("value"))


def checkInputs(InputsTuple,applyBtnElement):
	#print("Input tuple: " + str(InputsTuple))
	#actions = ActionChains(driver)
	for testData in InputsTuple:
		print("Test data: " + str(testData))
		# set
		#actions.move_to_element(driver.find_element_by_xpath(testData[0])).perform()
		driver.find_element_by_xpath(testData[0]).clear()
		sleep(2)
		driver.find_element_by_xpath(testData[0]).send_keys(testData[2])
		sleep(2)
		# move to appy btn
		#actions.move_to_element(driver.find_element_by_xpath(applyBtnElement)).perform()
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		#save
		driver.find_element_by_xpath(applyBtnElement).click()
		sleep(5)
		# assertion
		vp12Telnet.getCurrentConfig()
		cfgValue = xpathes.getValueFromCfg(vp12Telnet.yamlCfg,testData[1])
		if ( cfgValue == testData[2]):
			print("Success")
		else:
			print("Failure")
			print("Cfg value: '" + cfgValue + "'  But we set: '" + testData[2] + "'")


def webLogout():
	driver.find_element_by_xpath("//A[@id='logout-link']").click()
	if is_element_present(By.ID,"login"):
		logging.info("Successful logout")
		return True
	else:
		logging.error("Failed to logout")
		return False

def assertTrue(what, msg=''):
	logging.info('Assertion if true :' + str(what))
	if what is True:
		return True
	else:
		return False


def assertFalse(what, msg=''):
	logging.info('Assertion if false :' + str(what))
	if what is False:
		return True
	else:
		return False


def closeDriver():
	try:
		driver.quit()
	except Exception as e:
		pass

#atexit.register(closeDriver)

initDriver()
webLogin()
#checkNetworkTabs()
#checkSIPAccount()
checkCommonSIP()
#webLogout()
#closeDriver()
vp12Telnet.cpeLogout()

