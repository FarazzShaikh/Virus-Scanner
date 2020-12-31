'''
TODO: 
Add description of code here
'''

import requests
import time

'''
Parameters (<file to scan>,<virus total api key>)
'''
def scanFile(filePath, Virus_Total_API_key):

	scanUrl = 'https://www.virustotal.com/vtapi/v2/file/scan'
	scanParams = {'apikey': Virus_Total_API_key}	

	files = {'file': (filePath, open(filePath, 'rb'))}							# file to be sent
	scanResp = requests.post(scanUrl, files=files, params=scanParams)	# send file along w api key

	scanID = scanResp.json().get('scan_id')

	print("\nPlease give us a moment to process your file, this may take upto 60 seconds")
	time.sleep(60)					# allow for processing time	

	# report code

	reportUrl = 'https://www.virustotal.com/vtapi/v2/file/report'

	reportParams = {'apikey': Virus_Total_API_key, 'resource': scanID}		# use scanID to get file report
	reportResp = requests.get(reportUrl, params=reportParams)

	finalReport = reportResp.json()
	finalScans = finalReport['scans']		# get scans from report

	if (finalReport.get('positives') == 0):		# check if file has been flagged
		print("The file is safe!\n")

	else:
		for scan in finalScans:			# for each scan

			if (finalScans[scan].get('detected') == True):		# check if antivirus flagged file

				print(scan + " has flagged this as malicious!")	
				print(finalScans[scan].get('result'))
				print("\n\n")

	print("For a detailed analysis visit:\n" + finalReport.get('permalink') + "\n\n")

