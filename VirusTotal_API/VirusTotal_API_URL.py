import requests
import time
import sys
import json
sys.path.append("..")
from config import Virus_Total_API_key

print("Enter the URL you would like to scan:")
url = input()

scanUrl = 'https://www.virustotal.com/vtapi/v2/url/scan'				# url to request scan from
reportUrl = 'https://www.virustotal.com/vtapi/v2/url/report'			# url to request report from

scanParams = {"apikey":Virus_Total_API_key(), 'url' : url}				# sending url to be scanned
scanResp = requests.post(scanUrl, data=scanParams)						# scan request

scanID = scanResp.json().get('scan_id')									# getting scan ID

print("Processing URL...")			
time.sleep(10)															# allowing for processing time

reportParams = {"apikey":Virus_Total_API_key(), 'resource' : scanID}
reportResp = requests.get(reportUrl, params=reportParams)				# getting report of scan ID

report_json = reportResp.json()
print("Your scan ID is " + report_json["scan_id"] + "\n") 
if (report_json["positives"] == 0):
    print("This site is 100% safe\n")	
else:
    print("Our scans picked up some issues with this site. Proceed with caution.More info:")
    scan_report = report_json["scans"]
    for scanner in scan_report:
        if (scan_report[scanner]["detected"] != False ):
            print (scanner + " has detected that it may be a " + scan_report[scanner]["result"])
            print(scan_report[scanner])
print("\n")
print("To get more information on the scan,paste this link in your browser\n")
print(report_json["permalink"])