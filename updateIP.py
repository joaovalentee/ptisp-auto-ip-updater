#from this import d
from pdb import lasti2lineno
from requests import get
from requests import post
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
import sys, getopt

def main (argv):
	username = ''
	password = ''
	domain = ''
	ip = ''
	lastIP = ''
	name = ''

	try:
		opts, args = getopt.getopt(argv, "d:u:p:", ["domain=", "username=", "password="])
	except getopt.GetoptError:
		print('updateIP.py -d <domainName> -u <username> -p <password>')
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-d", "--domain"):
			domain = arg
			name = domain
			print(f"domain is {domain}")
			x = len(domain.split("."))
			if (x > 2):
				print("domain is bigger than simple domain")
				value = domain.split(".")[x-2] + '.' + domain.split(".")[x-1]
				domain = value
			print(f"final domain is {domain} and name is {name}")
		elif opt in ("-u", "--username"):
			username = arg
		elif opt in ("-p", "--password"):
			password = arg
	
	if ((domain == '') or (username == '') or (password == '')):
		print('updateIP.py -d <domainName> -u <username> -p <password>')
		sys.exit()

	print(f"Creating bot for domain {domain} with username {username}")

	try:
		ip = get('https://api.ipify.org').text
		#ip = ip.replace('0', '1')
		print(f'My public IP address is: {ip}')

	except ConnectionError as e:
		print('There was an error making the connection')
		sys.exit()

	if(ip == ''):
			print('Cannot find IP')

	else:
		fileToOpen = domain + '_lastIP.txt'
		
		try:
			f = open(fileToOpen, 'r')
			lastIP = f.read()
			print(f'Last IP is {lastIP} and new IP is {ip}')

		except IOError:
			print('No previous IP saved')

		if (lastIP == ip):
			print('The IP address did not change')

		else:
			print('IP address has changed')
			url = 'https://api.ptisp.pt/parking/' + domain + '/dns/list'
			response = get(url, auth=HTTPBasicAuth(username, password))

			if (response.status_code == 200):
				records = response.json().get('records')
				for r in records:
					if ((r.get("type") == 'A') and (r.get("name") == name+".")):
						print(r)
						if (r.get("address") == lastIP or lastIP == ''):
							r["address"] = ip
							print(f"updating on ptisp {r}")
							postUrl = 'https://api.ptisp.pt/parking/' + domain + '/dns/' + str(r.get("line")) + '/edit'
							print(postUrl)
							postResponse = post(postUrl, json = r, auth=HTTPBasicAuth(username, password))
							if (postResponse.status_code == 200):
								print("IP updated!!!")
							else:
								print(f"Something went wrong <{postResponse.status_code}>")
							print(postResponse)
				
			elif (response.status_code == 401):
				print('Unauthorized')

			else:
				print(f'Error: {response}')

			with open(fileToOpen, 'w') as f:
				f.write(f'{ip}')

if __name__ == "__main__":
	main(sys.argv[1:])