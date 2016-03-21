import requests
import smtplib
def get_emails():
	emails={}
	try:
		email_file= open('emails.txt','r')
		for line in email_file:
			(email, name) = line.split(',')
			emails[email] = name.strip()
			
	except FileNotFoundError as err:
		print(err)
	return emails

def get_schedule():
	try:
		schedule_file = open('schedule.txt', 'r')
		schedule = schedule_file.read()
		
	except FileNotFoundError as err:
		print(err)
	return schedule
def get_weather_forecast():
	#connecting to the weather api
	url = 'http://api.openweathermap.org/data/2.5/find?q=Delhi&units=metric&appid=659d414218968c3a0501f80c2efca54c'
	weather_request =requests.get(url)
	weather_json = weather_request.json()
	print(weather_json)
	#parsing  JSON
	description = weather_json['list'][0]['weather'][0]['description']
	print(description)
	temp_min = weather_json['list'][0]['main']['temp_min']
	temp_max = weather_json['list'][0]['main']['temp_max']
	print(temp_min)
	print(temp_max)
	#creating our forecast string
	forecast='The circus forecast for today is '
	forecast += description +' with a high of '+ str(temp_max)
	forecast += ' and a lot of '+ str(temp_min)
	return (forecast)

def send_emails(emails, schedule, forecast):
	# connect to the smtp server
	server = smtplib.SMTP('smtp.gmail.com', '587')
# Start TLS encryption
	server.starttls()
#login
	password = input("Whats your password?")
	from_email= 'meenalpython@gmail.com'
	server.login(from_email, password)
	#send to entire email list
	for to_email, name in emails.items():
		message = 'Subject: Todays Delhi forecast:\n'
		message+='Hi'+name+'!\n\n'
		message+=forecast+'!\n\n'
		message+=schedule+'!\n\n'
		message += 'Hope to see you there!'
		server.sendmail(from_email, to_email, message)

	server.quit()

def main():
	emails = get_emails()
	print(emails)
	schedule = get_schedule()
	print(schedule)
	forecast =get_weather_forecast()
	print(forecast)
	send_emails(emails, schedule, forecast)

main()
