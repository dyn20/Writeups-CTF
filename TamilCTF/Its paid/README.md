# Category: Web 
#### _My English is bad. I'm sorry if it confuses you while reading my writeup._

In this challenge, you can see a page sells course, you don't have money and you can't by any course.

![](img1.png)

But when you by a course, you can edit its price to 0 and you can by any course you want.

![](img2.png)

After buying a course, you will receive a link to a video.

To save time, I use Burp Intruder to get link to all course video.

![](img5.png)

All link are:
- /static/courses/coursessss1.mp4
- /static/courses/2nddcourseeeee.mp4
- /static/courses/thirdcourseeee.mp4
- /static/courses/4thhhcourseee.mp4
- /static/courses/fith555coursee.mp4 
- /static/courses/sixth6courseeeee.mp4
- /static/courses/seven.mp4
- /static/courses/it's88.mp4

The thing we need is in 6th video:

![](img3.png)

Okay, let go to `/admin` and login with the email and password in the video:

But we haven't gotten flag yet, they say "Only special persons can see this". Check the cookie and you will see a cookie name "persion_special", it's setted `false` by default, edit it to `true` and you will get the flag.

![](img4.png)

## _Thank you for your being here!_
