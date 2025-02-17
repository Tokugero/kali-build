# Many of these shamelessly stolen from https://github.com/Crypto-Cat/

alias .....='cd ../../../../'
alias ....='cd ../../../'
alias ...='cd ../../'
alias ..='cd ..'
alias pbcopy='xclip -selection clipboard'
alias pbpaste='xclip -selection clipboard -o'
alias aslr_off='echo 0 | sudo tee /proc/sys/kernel/randomize_va_space'
alias autoclean='sudo apt-get autoclean -y'
alias autoremove='sudo apt-get autoremove -y'
alias burpsuite='java -jar --add-opens=java.desktop/javax.swing=ALL-UNNAMED --add-opens=java.base/java.lang=ALL-UNNAMED /usr/bin/burpsuite'
alias c='clear'
alias diff='colordiff'
alias docker_fix='sudo mkdir /sys/fs/cgroup/systemd; sudo mount -t cgroup -o none,name=systemd cgroup /sys/fs/cgroup/systemd'
alias dvwa_start='sudo service mysql start && sudo service apache2 start'
alias gcc_no_protections='gcc -fno-stack-protector -z execstack -no-pie'
alias gen_nmap='/home/tokugero/scripts/gen_nmap.py'
alias ghidra_auto='python3 /home/tokugero/.local/bin/auto_ghidra.py'
alias gobusterz='gobuster dir -w /usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-medium.txt -o gobuster.txt -u $1'
alias h='history'
alias httpup='sudo ~/apps/up-http-tool/up'
alias ifconfig='sudo ifconfig'
alias installz='sudo apt-get install $1 -y'
alias jwt_tool='python /home/tokugero/apps/jwt_tool/jwt_tool.py'
alias l='ls -lart'
alias mobsf_emulator='emulator -avd $1 -writable-system -no-snapshot'
alias mount='sudo mount | column -t'
alias mscanz='sudo masscan -p1-65535,U:1-65535 $1 --rate=1000 -e tun0 --wait 5 > mscan.txt'
alias msfelfscan='/usr/share/framework2/msfelfscan'
alias nasm_shell='/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb'
alias nse-help='nmap --script-help'
alias nse='ls /usr/share/nmap/scripts | grep'
alias pattern_create='/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l $1'
alias pattern_offset='/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q $1' 
alias qmapz='sudo nmap -sV -sC $1'
alias root='sudo -i'
alias s='sudo'
alias smbup='sudo python3 /usr/share/doc/python3-impacket/examples/smbserver.py -smb2support share $(pwd)'
alias ss='searchsploit $1'
alias ssm='searchsploit -m $1'
alias ssx='searchsploit -x $1'
alias vhostbusterz='gobuster vhost -w /usr/share/wordlists/amass/subdomains.lst -t 10 -o vhostbuster.txt --append-domain -u $1'
alias vpn-hackerone='sudo wg-quick up /home/tokugero/ctf/hackerone/wg.conf'
alias vpn-htb='sudo openvpn --config /home/tokugero/ctf/htb/htbvip.ovpn'
alias vpn-thm='sudo openvpn --config /home/tokugero/ctf/thm/thm.ovpn'
alias webup='echo "EXPOSING PORT 9080" && sudo python -m http.server 9080'
urlencode() { #Encode URL encoded values
    python3 -c "from pwn import *; print(urlencode('$1'));"
}
urldecode() { #Decode URL encoded values
    python3 -c "from pwn import *; print(urldecode('$1'));"
}
ffuf-vhost() { #Fast Fuzzer vhost lookup, give domain
    arg_count=3
    if [[ $2 && $2 != -* ]]; then
        wordlist=$2
    else
        wordlist='/usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt'
        arg_count=2
    fi
    ffuf -c -H "Host: FUZZ.$1" -u http://$1 -w $wordlist ${@: $arg_count};
}
ffuf-dir() { #Fast fuzzer directory fuzz
    arg_count=3
    if [[ $2 && $2 != -* ]]; then
        wordlist=$2
    else
        wordlist='/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-medium.txt'
        arg_count=2
    fi
    ffuf -c -u $1FUZZ -w $wordlist ${@: $arg_count};
}
ffuf-req() { #fast fuzzer http request with generic wordlist
    arg_count=2
    if [[ $1 && $1 != -* ]]; then
        wordlist=$1
    else
        wordlist='/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-medium.txt'
        arg_count=1
    fi
    ffuf -c -ic -request new.req -request-proto http -w $wordlist ${@: $arg_count};
}
plzsh() { #Starts a reverse shell listener with pretty terminal
    if [[ $1 ]]; then
        port=$1
    else
        port=1337
    fi
    stty raw -echo; (echo 'python3 -c "import pty;pty.spawn(\"/bin/bash\")" || python -c "import pty;pty.spawn(\"/bin/bash\")"' ;echo "stty$(stty -a | awk -F ';' '{print $2 $3}' | head -n 1)"; echo reset;cat) | nc -lvnp $port && reset
}
qssh() { #SSH without host key checking
    sshpass -p $2 ssh -o StrictHostKeyChecking=no $1@$3 ${@: 4};
}
rdp() { #Opens RDP session with FreeRDP
    xfreerdp /u:$1 /p:$2 /v:$3 /size:1440x810 /clipboard /cert-ignore ${@: 4};
}
extract() { #Extracts files regardless of extension, probably
  if [ -z "$1" ]; then
    echo "Usage: extract <path/file_name>.<zip|rar|bz2|gz|tar|tbz2|tgz|Z|7z|xz|ex|tar.bz2|tar.gz|tar.xz>"
  else
    if [ -f $1 ]; then
      case $1 in
        *.tar.bz2)   tar xvjf $1    ;;
        *.tar.gz)    tar xvzf $1    ;;
        *.tar.xz)    tar xvJf $1    ;;
        *.lzma)      unlzma $1      ;;
        *.bz2)       bunzip2 $1     ;;
        *.rar)       unrar x -ad $1 ;;
        *.gz)        gunzip $1      ;;
        *.tar)       tar xvf $1     ;;
        *.tbz2)      tar xvjf $1    ;;
        *.tgz)       tar xvzf $1    ;;
        *.zip)       unzip $1       ;;
        *.Z)         uncompress $1  ;;
        *.7z)        7z x $1        ;;
        *.xz)        unxz $1        ;;
        *.exe)       cabextract $1  ;;
        *)           echo "extract: '$1' - unknown archive method" ;;
      esac
    else
      echo "$1 - file does not exist"
    fi
  fi
}
startroom() { #Creates a new directory and copies the skel files into it
    if [[ $1 ]]; then
        room=$1
        mkdir -p $room
    else
        room="room"
    fi
    cd $room
    cp ~/.local/build/.ctfskel/* .
    sed -i "s/TEMPLATE/$room/g" engagement.ipynb
    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
}
help() { #Prints this help message
    echo "Custom commands provided by aliases, so you don't have to look them up yourself. \n\n\n"
    echo "Aliases:\n"
    cat ~/.local/build/.bash_aliases | grep alias | grep -v "grep" | awk '{for (i=2; i<NF; i++) printf $i " "; print $NF}' | pygmentize -g
    cat ~/.local/build/aliases | grep alias | grep -v "grep" | awk '{for (i=2; i<NF; i++) printf $i " "; print $NF}' | pygmentize -g

    echo "\nFunctions:\n"
    cat ~/.local/build/.bash_aliases | grep \(\) | tr "\(" " " | awk '{printf $1 " "; for (i=4; i<NF; i++) printf $i " "; print $NF}' | pygmentize -l zsh
    cat ~/.local/build/aliases | grep \(\) | tr "\(" " " | awk '{printf $1 " "; for (i=4; i<NF; i++) printf $i " "; print $NF}' | pygmentize -l zsh
}
. ~/.local/build/aliases
