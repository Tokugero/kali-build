{
  description = "CTF engagement room — rootless VPN netns + network tooling";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # wpscan ships under an unfreeRedistributable license; allow just
        # that package rather than a blanket unfree allowance.
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfreePredicate = pkg:
            builtins.elem (nixpkgs.lib.getName pkg) [ "wpscan" ];
        };

        # Rootless tunnel stack. pasta(1) bridges an unprivileged user+net
        # namespace to host networking; openvpn / wireguard-go provide the
        # egress TUN inside it; unbound is the split-DNS resolver (dnsmasq
        # can't run here — it calls setgroups() which pasta's setgroups=deny
        # blocks). No kernel modules, no sudo.
        tunnelStack = with pkgs; [
          passt              # pasta(1) — rootless netns bridge
          openvpn            # primary tunnel: HTB / THM .ovpn
          wireguard-tools    # wg(8) + wg-quick strip — WireGuard path
          wireguard-go       # userspace WireGuard daemon
          unbound            # split-DNS resolver (username:"" skips setuid)
          iproute2
          iputils            # ping inside the netns
          util-linux         # unshare(1) / nsenter(1)
          procps             # pgrep — holder discovery walk
          getent             # getent for endpoint resolution
        ];

        # Network recon / exploitation — these run as host processes INSIDE
        # the netns (launched from the joined shell), so every byte they send
        # egresses through the VPN tunnel. Offline analysis tools (mft,
        # ropper, uncompyle6, rsactftool, …) stay as the repo's docker
        # aliases — they never touch the target so tunnel routing is moot.
        netTools = with pkgs; [
          nmap
          rustscan
          ffuf
          gobuster
          feroxbuster
          nuclei
          naabu
          httpx            # projectdiscovery httpx ("Fast HTTP toolkit")
          subfinder
          katana
          dnsx
          whatweb
          nikto
          wpscan
          netexec          # successor to crackmapexec
          smbmap
          samba            # smbclient
          openldap         # ldapsearch
          evil-winrm
          responder
          kerbrute
          certipy          # certipy-ad — AD CS abuse
          ldapdomaindump
          sshpass
          openssh
          curl
          wget
          jq
        ];

        # Python: base interpreter + AD/exploit libs available on PATH
        # (impacket-* scripts, bloodhound-python). The notebook's heavier
        # pip-only deps (jupyterlab, pwntools, chepy, selenium, …) live in a
        # .venv that .envrc bootstraps from requirements.txt via uv — pip is
        # the right channel for those, they churn faster than nixpkgs.
        pyTools = with pkgs; [
          python3
          uv
          python3Packages.impacket
          python3Packages.bloodhound-py
          geckodriver       # selenium backend for utils/screenshot.py
        ];

        # Wordlists. The notebook calls `$(wordlists_path)/seclists/...`;
        # seclists installs its tree at $out/share/wordlists/seclists, so the
        # shim prints that parent dir. Add pkgs.wordlists for rockyou et al.
        wordlistTools = with pkgs; [
          seclists
          (writeShellScriptBin "wordlists_path" ''
            echo "${pkgs.seclists}/share/wordlists"
          '')
        ];
      in {
        devShells.default = pkgs.mkShell {
          packages = tunnelStack ++ netTools ++ pyTools ++ wordlistTools;

          shellHook = ''
            export SECLISTS="${pkgs.seclists}/share/wordlists/seclists"
            echo "[ctf room] tunnel+tools ready — 'room-enter <vpn>' to drop into the VPN netns"
          '';
        };
      });
}
