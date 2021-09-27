Another week ended, another CTF event ended, I realize I'm not making any process. Maybe, I need to review the way I learned.

Anyway, hope that I can do somthing.

# DownUnderCTF
Here are some easy challenges I did in this CTF
## Web challenge
### Inside Out
Open challenge and view source you can see route to Admin panel: "/admin"

Try to access to /admin, you will receive ```Only accessible from the local network```

Access /request?url=http://example.com/ you will see a local IP: 10.96.0.167

Finally: payload: https://web-inside-out-b3d9f3b9.chal-2021.duc.tf/request?url=http://10.96.0.167/admin

Flag: DUCTF{very_spooky_request}

### Cowboy World:
Type: SQL Injection 

Firstly, I try some sqli payload but it didn't work.

It's a challenge for beginner, so I don't think it has something too difficult. 

I try to access robots.txt you will receive some hint, you must do sql injection with username is ```sadcowboy```

Payload: username=sadcowboy&password='+or+1--

Flag: DUCTF{haww_yeeee_downunderctf?}

### Chainreaction:

---To be continued---

