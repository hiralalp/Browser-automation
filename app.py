from flask import Flask, render_template
from flask import request
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
global firefoxdriver,chromedriver

global chrome_flag,firefox_flag

app = Flask(__name__)

class BrowserAutomation():

	def __init__(self):
		self.chrome=None
		self.firefox=None

	def start(self,browser,url):

		if browser=="chrome":
			#global chromedriver
			chromedriver=webdriver.Chrome(executable_path="chromedriver.exe")	
			chromedriver.maximize_window() 	
			chromedriver.get(url)	
			self.chrome=chromedriver

			chrome_flag=True

			return "Chrome Browser Started............."

			


		elif browser=="firefox":
			binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
			options = Options()
			options.binary = binary
			cap = DesiredCapabilities().FIREFOX
			cap["marionette"] = True 
			firefoxdriver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path="geckodriver.exe")
			
			firefoxdriver.maximize_window()
			firefoxdriver.get(url)
			self.firefox=firefoxdriver

			firefox_flag=True

			return "Firefox Browser Started............."

		else:

			return "Please enter the correct url"


		

	def stop(self,browser):
		
		if browser=='chrome' and self.chrome!=None:
			self.chrome.quit()
			return "chrome browser killed successfully!!"

		elif browser=='firefox' and self.firefox!=None:
			self.firefox.quit()
			return "firefox browser killed successfully!!"

		else:
			return "Please enter the correct url....."


		

	def geturl(self,browser):
		
		if browser=='chrome':
			url = self.chrome.current_url
			return url
		elif browser=='firefox':
			url = self.firefox.current_url
			return url
		else:
			return "Enter the correct Browser name......"

	def cleanup(self,browser):
		if browser == "firefox":
			self.firefox.delete_all_cookies()			
			return "Cleared Firefox Data"

		elif browser == "chrome":
			self.chrome.delete_all_cookies()
			return "Cleared Chrome Data"

		else:
			return "enter the correct details....."

		
global browser_obj
browser_obj=BrowserAutomation()


@app.route('/start')
def start():
	browser = request.args.get('browser', default = 'chrome', type = str)
	url = request.args.get('url', default = 'https://www.google.com', type = str)
	
	status=browser_obj.start(browser,url)

	return render_template('index.html', variable1=status)

@app.route('/stop')
def stop():
	browser = request.args.get('browser', default = 'chrome', type = str)

	status=browser_obj.stop(browser)

	return render_template('index.html', variable1=status)

@app.route('/cleanup')
def cleanup():

	browser = request.args.get('browser', default = 'chrome', type = str)

	status=browser_obj.cleanup(browser)

	return render_template('index.html', variable1=status)
	
		
	

	

@app.route('/geturl')
def geturl():
	browser = request.args.get('browser', default = 'chrome', type = str)
	
	status=browser_obj.geturl(browser)

	return status


@app.route('/')
def hello():
	return "Welcome to our server!!!!!"

if __name__ == '__main__':
	app.run(debug=True)