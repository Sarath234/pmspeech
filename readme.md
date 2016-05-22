### This project is to analyse PM speeches
* Data scraped from [archivepmo.nic.in](http://archivepmo.nic.in/) & [pmindia.gov.in](http://pmindia.gov.in/en/tag/pmspeech/)
* To scrape the data [scrapy](http://scrapy.org/) is used.
* To scrape ABV, MMS speeches from [archivepmo.nic.in](http://archivepmo.nic.in/)
	```scrapy runspider pmspeech.py -o 	abvmmsspeech.json```
* To scrape Modi's speeches from [pmindia.gov.in](http://pmindia.gov.in/en/tag/pmspeech/)
	```scrapy runspider pmspeech_modi.py -o modispeech.json```
