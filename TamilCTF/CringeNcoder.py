import requests
import re

stringlist = 'abcdefghijklmnopqrstuvwxyz0123456789'
url = 'http://45.79.195.170:5000/encode'
notflag = 'cR1Ng3e crinG3 cringE cringe cRINGe cRINGe cring3 crinG3 cringE cringE cRinG3 Cr1nGe cRimG3 criNG3 cRinge cRimG3 cringe cR1Ng3e cRiNge cRinG3 cR1Ng3 CrInGe cRInGE cr1ngE criNG3 cringE cring3 cRinge cR1Ng3 crinGE cringE criNgee cRinG3 CrInGe'.split(' ')
flag=''
for i in notflag:
	for j in stringlist:
		r=requests.post(url,{'text':j})
		character = re.search("font-weight: bolder;\">(.*) </a>",r.text).group(1)
		if i == character:
			print(j)
			flag = flag+j
			break

print('Flag: '+flag)

#Flag: f1nally1nn3pe4ceaf73rs0m4nycring3s

