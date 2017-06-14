
SIP_NUMBER_INPUT = "//input[@data-bind='value: SIPAccountParameters.SIP.Number, uniqueId: true']"
SIP_NUMBER_CONFIG = ("VoIP","Lines","Line1","SIPAccountParameters","SIP","Number")
SIP_NUMBER_TEST_VALUE = "1100"

SIP_DISP_NAME_INPUT = "//input[@data-bind='value: SIPAccountParameters.SIP.Username, uniqueId: true']"
SIP_DISP_NAME_CONFIG = ("VoIP","Lines","Line1","SIPAccountParameters","SIP","Username")
SIP_DISP_NAME_TEST_VALUE = "My Display Name"

SIP_PORT_INPUT = "//input[@data-bind='value: SIPAccountParameters.SIP.SIPPort, uniqueId: true']"
SIP_PORT_CONFIG = ("VoIP","Lines","Line1","SIPAccountParameters","SIP","SIPPort")
SIP_PORT_TEST_VALUE = "5070"

SIP_AUTH_LOGIN_INPUT = "//input[@data-bind='value: SIPAccountParameters.SIP.AuthUsername, uniqueId: true']"
SIP_AUTH_LOGIN_CONFIG = ("VoIP","Lines","Line1","SIPAccountParameters","SIP","AuthUsername")
SIP_AUTH_LOGIN_VALUE = "1100"


SIP_ACCOUNT_APPLY_BTN = "(//span[text()='Применить'])[2]"

SIP_ACCOUNT_INPUTS = ((SIP_NUMBER_INPUT,SIP_NUMBER_CONFIG,SIP_NUMBER_TEST_VALUE),
					 (SIP_DISP_NAME_INPUT,SIP_DISP_NAME_CONFIG,SIP_DISP_NAME_TEST_VALUE),
					  (SIP_AUTH_LOGIN_INPUT,SIP_AUTH_LOGIN_CONFIG,SIP_AUTH_LOGIN_VALUE))


SIP_LOGIN_INPUT = "//input[@data-bind='value: SIPAccountParameters.SIP.Username, uniqueId: true']"
SIP_USE_ALTER_NUMBER_CHECKBOX = "checked: SIPAccountParameters.SIP.SIPPort, uniqueId: true"

def getValueFromCfg(cfgDict,pathList):
	resultDict = cfgDict
	for atr in pathList:
		resultDict = resultDict[atr]

	return resultDict
