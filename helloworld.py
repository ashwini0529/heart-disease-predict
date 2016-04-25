#!/usr/bin/env python
from tornado.ioloop import IOLoop
from tornado.escape import json_encode
from tornado.web import RequestHandler, Application, asynchronous, removeslash
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import engine, Task, coroutine
import os

class heartHandler(RequestHandler):
	def get(self):
		self.render('index.html')
	def post(self):
		x = 0
		age = float(self.get_argument('att1'))
		sex = float(self.get_argument('att2'))
		cp = float(self.get_argument('att3'))
		trestbps = float(self.get_argument('att4'))
		chol  = float(self.get_argument('att5'))
		fbs = float(self.get_argument('att6'))
		restEcg = float(self.get_argument('att7'))
		thalac = float(self.get_argument('att8'))
		exang = float(self.get_argument('att9'))
		oldPeak = float(self.get_argument('att10'))
		slope = float(self.get_argument('att11'))
		ca = float(self.get_argument('att12'))
		thal = float(self.get_argument('att13'))

		#Algo
		if(cp==1):
			self.write('<html><body background = "static/bg.jpg"><p>You have typical angina</p></body></html>')
			x = x+0.25
		elif(cp==2):
			self.write('<html><body background = "static/bg.jpg"><p>You have atypical angina</p></body></html>')
			x = x+0.50
		elif(cp==3):
			x = x+0.75
			self.write('<html><body background = "static/bg.jpg"><p>You have non-anginal pain</p></body></html>')

		else:
			x = x+1
			self.write('<html><body background = "static/bg.jpg"><p>You have asymptomatic pain</p></body></html>')
		if trestbps>120:
			self.write('<html><body background = "static/bg.jpg"><p>Your resting blood pressure is abnormally high. Eat less of Salt and have as many vegetables and fruits everyday. Drink less alcohol and exercise regurlarly.</p></body></html>')
			x=x+1
		else:
			x=x+0
			self.write("<html><body background = 'static/bg.jpg'><p>Your resting blood pressure is normal.Keep up with the diet you're taking.</p></body></html>")
		if (chol<240 and chol>120):
			self.write('<html><body background = "static/bg.jpg"><p>Your cholestrol is on the verge of the risky zone. Limit your intake of foods full of saturated fats, trans fats, and dietary cholesterol.Eat a lot more fiber-rich foods (especially soluble fiber from foods like beans, oats, barley, fruits, and vegetables).</p></body></html>')
		elif(chol>240):
			self.write('<html><body background = "static/bg.jpg"><p>Your cholesterol level lies on the risky zone. Choose protein-rich plant foods (such as legumes or beans, nuts, and seeds) over meat. Lose as much excess weight as possible. Take psylliums (such as Metamucil).</p></body></html>')
			x=x+1
		else:
			x=x+0
			self.write("<html><body background = 'static/bg.jpg'><p>Your cholestrol level is just fine. Keep up with the diet you're taking.</p></body></html>")
		if (fbs==1):
			x=x+1
			self.write('<html><body background = "static/bg.jpg"><p>Your blood sugar level is high. Minimize the amount of salt and sodium you eat. Consume fewer processed and packaged foods. Also cut down on restaurant meals. Cook at home more, and use less salt in cooking and at the table. Lighten up on added sugars and sweets. </p>Cut down on all kinds of sugary drinks (including regular soda, fruit drinks, sports drinks, etc.), flavored hot and iced coffees and teas, pastries, candy, and desserts. You can continue to enjoy small portions on occasion.')
		else:
			self.write("<html><body background = 'static/bg.jpg'><p>Your blood sugar level is just fine. Keep up with the diet you're taking.</p></body></html>")
		if(restEcg==2):
			x=x+1
			self.write('<html><body background = "static/bg.jpg"><p>Your ecg results suggest that you might have hypertrophy. Consult your cardiologist at your earliest convinience.</p></body></html>')
		elif(restEcg==1):
			x=x+0.5
			self.write('<html><body background = "static/bg.jpg">"<p>Your ecg results suggest that you might have ST-T.</p></body></html>')
		else:
			self.write('<html><body background = "static/bg.jpg"><p>Your ecg results suggest that your heart is showing no abnormalities in heartbeats. Keep excersing regularly.</p></body></html>')
		if(thalac>100):
			x=x+1
			self.write('<html><body background = "static/bg.jpg"><p>You have a high heart beat rate then normal. Empty your bladder regularly. Take a fish oil capsule regularly.</p> Get plenty of good sleep.</body></html>')
		else:
			self.write("<html><body background = 'static/bg.jpg'><p>You have a mormal heart beat rate. Keep up with the diet you're taking. Get plenty of good sleep.</p></body></html>")
		if (exang==1):
			x=x+1
		else:
			x=x+0
		if(slope==3):
			x=x+1
		elif(slope==2):
			x=x+0.5
		else:
			x=x+0
		if(thal==7):
			x=x+1
		elif(restEcg==6):
			x=x+0.5
		else:
			x=x+0
		if(ca==3):
			x=x+1
		elif(ca==2):
			x=x+0.5
		else:
			x=x+0
		message = """
		<html>
		<body background="bg.jpg">
		<p>Summary:You have high risk of heart disease. Improve cholesterol levels. You're more likely to get heart disease if you have:</p>
		<p>Total cholesterol level over 200 </p>
		<p>HDL ("good") cholesterol level under 40 </p>
		<p>LDL ("bad") cholesterol level over 160 </p>
		<p>Triglycerides over 150</p>
		<p>Control high blood pressure. More than 50 million people in the U.S. have hypertension, or high blood pressure, making it the most common heart disease risk factor. </p>
		<p>Get active. People who don't exercise are more likely to get heart disease.</p>
		<p>Follow a heart-healthy diet. Eat foods that are low in fat and cholesterol.</p>
		<p>Get to a healthy weight. Losing extra weight is good for your heart. It can also help you lower high blood pressure and manage diabetes.</body></html>
		"""
		if(x>5):
			self.write(message)
		else:
			self.write('<html><body background = "static/bg.jpg">You have a low risk of heart diseases. Please follow all the suggestions provided to you so that you live a long and healthy life.</body></html>')


class loginHandler(RequestHandler):
	def get(self):
		value = self.get_argument('value','')
		if (value=='false'):
			self.write('<html><body background="static/bg.jpg"><p><b>Invalid credentials!! Please try <a href ="/">again</a></b></p></body></html>')
		else:
			self.render('login.html')
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		if((username=='rohan' and password=='rohan') or (username == 'admin' and password == 'admin') or (username == '123' and password =='123')):
			self.redirect('/form')
		else:
			self.redirect('/?value=false')


settings = dict(
		template_path = os.path.join(os.path.dirname(__file__), "templates"),
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		debug=True
	)

#Application initialization
application = Application([
	(r"/form", heartHandler),
	(r"/",loginHandler)
], **settings)

#main init
if __name__ == "__main__":
	server = HTTPServer(application)
	server.listen(8001)
	IOLoop.current().start()