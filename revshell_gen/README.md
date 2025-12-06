# Reverse Shell Generator

A comprehensive reverse shell payload generator supporting 20+ different languages and platforms.

## Features

- **20+ Shell Types**: Bash, Python, PowerShell, PHP, Ruby, Perl, Java, Node.js, and more
- **Multiple Modes**: Generate specific shells or all at once
- **Color-Coded Output**: Easy-to-read terminal output
- **URL Encoding**: Optional URL encoding for web exploitation
- **Base64 Encoding**: PowerShell base64 encoded payloads

## Usage

### Basic Usage
```bash
python revshell.py <IP> <PORT> <SHELL_TYPE>
```

### Examples
```bash
# Generate a bash reverse shell
python revshell.py 10.10.10.5 4444 bash

# Generate a Python3 reverse shell
python revshell.py 192.168.1.100 9001 python3

# Generate a PowerShell reverse shell
python revshell.py 10.0.0.1 1337 powershell

# List all available shell types
python revshell.py 10.10.10.5 4444 --list

# Generate all available shells
python revshell.py 10.10.10.5 4444 --all
```

## Supported Shell Types

- `bash` - Standard bash reverse shell
- `bash_tcp` - Bash TCP reverse shell (alternative)
- `bash_udp` - Bash UDP reverse shell
- `nc` - Netcat reverse shell
- `nc_openbsd` - Netcat OpenBSD (no -e flag)
- `python` - Python 2 reverse shell
- `python3` - Python 3 reverse shell with PTY
- `perl` - Perl reverse shell
- `php` - PHP reverse shell
- `ruby` - Ruby reverse shell
- `java` - Java reverse shell
- `powershell` - PowerShell reverse shell
- `powershell_base64` - PowerShell base64 encoded
- `nodejs` - Node.js reverse shell
- `socat` - Socat reverse shell
- `awk` - AWK reverse shell
- `lua` - Lua reverse shell
- `golang` - Golang reverse shell
- `telnet` - Telnet reverse shell
- `xterm` - Xterm reverse shell

## Setting Up a Listener

Before executing the reverse shell on the target, set up a listener on your machine:

```bash
# Using netcat
nc -lvnp 4444

# Using socat (more stable)
socat file:`tty`,raw,echo=0 tcp-listen:4444

# Using metasploit
msfconsole -q -x "use exploit/multi/handler; set payload generic/shell_reverse_tcp; set LHOST <YOUR_IP>; set LPORT 4444; exploit"
```

## Upgrading Your Shell

Once you get a basic shell, upgrade it to a fully interactive TTY:

### Python PTY
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
# Then press Ctrl+Z
stty raw -echo; fg
export TERM=xterm
```

### Script Command
```bash
script /dev/null -c bash
```

## Security Notice

⚠️ **WARNING**: This tool is for educational purposes and authorized penetration testing only.

- Only use on systems you own or have explicit permission to test
- Unauthorized access to computer systems is illegal
- The author is not responsible for misuse of this tool

## Requirements

- Python 3.6+
- No external dependencies required

## License

Educational use only. Use responsibly and ethically.
