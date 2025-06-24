import paramiko
from sshtunnel import SSHTunnelForwarder
import subprocess
import logging


class ssh:
    def __init__(self, hostname, port=22, username=None, password=None, key_file=None, debug=False):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_file = key_file

        if not debug:
            logging.getLogger("paramiko").setLevel(logging.WARNING)
        else:
            logging.getLogger("paramiko").setLevel(logging.INFO)

    def exec(self, command):
        """
        Execute a command remotely via SSH and return its output.
        Uses paramiko for a direct SSH connection.
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connect_kwargs = {
            "hostname": self.hostname,
            "port": self.port,
            "username": self.username,
        }
        if self.key_file:
            connect_kwargs["key_filename"] = self.key_file
        if self.password:
            connect_kwargs["password"] = self.password

        client.connect(**connect_kwargs)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode().strip()
        client.close()
        return output

    def socksproxy(self, localport):
        """
        Start a SOCKS proxy on localhost at the given localport via SSH.
        Uses subprocess with ssh -D. Returns a SocksProxy object with a .close() method.
        Attempts to use key_file if provided, otherwise uses password with sshpass if available.
        """
        class SocksProxy:
            def __init__(self, proc):
                self.proc = proc
            def close(self):
                self.proc.terminate()
                self.proc.wait()

        ssh_cmd = [
            "ssh",
            "-N",
            "-D", f"{localport}",
            "-p", str(self.port),
            f"{self.username}@{self.hostname}"
        ]
        # Insert key if provided
        if self.key_file:
            ssh_cmd.insert(1, "-i")
            ssh_cmd.insert(2, self.key_file)
        # Use sshpass if password is provided and no key_file
        elif self.password:
            ssh_cmd = ["sshpass", "-p", self.password] + ssh_cmd
        proc = subprocess.Popen(ssh_cmd)
        return SocksProxy(proc)

    def portforward(self, localport, remotehost, remoteport):
        """
        Start a local port forward: localport -> remotehost:remoteport via SSH.
        Uses sshtunnel. Returns a PortForward object with a .close() method.
        """
        class PortForward:
            def __init__(self, tunnel):
                self.tunnel = tunnel
            def close(self):
                self.tunnel.stop()
        tunnel = SSHTunnelForwarder(
            (self.hostname, self.port),
            ssh_username=self.username,
            ssh_password=self.password if not self.key_file else None,
            ssh_pkey=self.key_file,
            local_bind_address=('127.0.0.1', localport),
            remote_bind_address=(remotehost, remoteport),
            allow_agent=True,
            set_keepalive=30,
            threaded=True,
        )
        tunnel.start()
        return PortForward(tunnel)

    def get(self, remotepath, localpath):
        """
        Download a file from the remote host to the local machine using paramiko SFTP.
        """
        transport = paramiko.Transport((self.hostname, self.port))
        connect_kwargs = {
            "username": self.username,
        }
        if self.key_file:
            private_key = paramiko.RSAKey.from_private_key_file(self.key_file)
            connect_kwargs["pkey"] = private_key
        if self.password:
            connect_kwargs["password"] = self.password
        transport.connect(**connect_kwargs)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remotepath, localpath)
        sftp.close()
        transport.close()

    def put(self, localpath, remotepath):
        """
        Upload a file from the local machine to the remote host using paramiko SFTP.
        """
        transport = paramiko.Transport((self.hostname, self.port))
        connect_kwargs = {
            "username": self.username,
        }
        if self.key_file:
            private_key = paramiko.RSAKey.from_private_key_file(self.key_file)
            connect_kwargs["pkey"] = private_key
        if self.password:
            connect_kwargs["password"] = self.password
        transport.connect(**connect_kwargs)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(localpath, remotepath)
        sftp.close()
        transport.close()