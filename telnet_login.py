import telnetlib, yaml, datetime, logging


HOST = "192.168.118.94"
adminLogin = "admin"
password = "password"
port = "23"


class telnetConnection(telnetlib.Telnet):
	def __init__(self,host,port,login,passwd):
		self.host = host
		self.port = port
		self.login = login
		self.passwd = passwd
		self.yamlCfg = []
		telnetlib.Telnet.__init__(self=self,host=host,port=port)
		self.loggedin = False


	def getCurrentConfig(self):
		if self.loggedin:
			self.write(b"cat /etc/config/cfg.yaml\n")
			self.yamlCfgStr = self.read_until(b":~$ ").decode()
			self.endCutPosition = self.yamlCfgStr.find('root@VP12P:~$')
			self.startCutPosition = self.yamlCfgStr.find('#')
			logging.debug(self.yamlCfgStr)
			logging.debug("Start Cut:" + str(self.startCutPosition) + " End cut: " + str(self.endCutPosition))
			self.yamlCfgStr = self.yamlCfgStr[self.startCutPosition:self.endCutPosition]
			logging.debug(self.yamlCfgStr)
			try:
				self.yamlCfg = yaml.load(self.yamlCfgStr)
			except Exception as e:
				print("Failed to parse yaml. Exception : " + str(e))
				logging.error("Failed to parse yaml. Exception : " + str(e))
				return False
		else:
			print("It is not logged in")
			return False
		return True


	def cpeLogin(self):
		if not self.loggedin:
			self.read_until(b"login: ")
			self.write(adminLogin.encode('ascii') + b"\n")
			self.read_until(b"Password: ")
			self.write(password.encode('ascii') + b"\n")
			self.read_until(b":~$ ")
			self.loggedin = True
		else:
			print("Already logged in")

	def cpeLogout(self):
		if self.loggedin:
			self.write(b"exit\n")
			self.loggedin = False
			return False
		else:
			print("Already logged out")
			return True


"""
telnet = telnetlib.Telnet(HOST,port)
telnet.read_until(b"login: ")
telnet.write(adminLogin.encode('ascii') + b"\n")
telnet.read_until(b"Password: ")
telnet.write(password.encode('ascii') + b"\n")
telnet.read_until(b":~$ ")

telnet.write(b"ls\n")
telnet.read_until(b":~$ ")
telnet.write(b"cat /etc/config/cfg.yaml\n")

print("Get yaml cfg")
beforeTimeStamp = datetime.datetime.now()
print(str(beforeTimeStamp))
yamlCfgStr = telnet.read_until(b":~$ ").decode()
endCutPosition = yamlCfgStr.find('root@VP12P:~$')
startCutPosition = yamlCfgStr.find('#')
yamlCfgStr = yamlCfgStr[startCutPosition:endCutPosition]
print("Got yaml cfg")
yamlCfg = yaml.load(yamlCfgStr)

afterTimeStamp = datetime.datetime.now()
diffTime = afterTimeStamp - beforeTimeStamp


telnet.write(b"exit\n")


print("RESULT: ")
print(yamlCfgStr[startCutPosition:endCutPosition])
print("Start cut: " + str(startCutPosition))
print("End cut: " + str(endCutPosition))
print("Diff time: " + str(diffTime))
"""

'''
vp12telnet = telnetConnection(host=HOST,port=port,login=adminLogin,passwd=password)
vp12telnet.cpeLogin()
vp12telnet.getCurrentConfig()
print(vp12telnet.yamlCfg["Trace"]["Configd"].get("Info","null"))
vp12telnet.cpeLogout()
'''

#print(yamlCfg["Trace"]["Configd"].get("Info","null"))




