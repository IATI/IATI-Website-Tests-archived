import os
import pytest
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException, BadHostKeyException
import re

class TestIATIBackupServer:

    @classmethod
    def setup_class(self):
        """
        Create a SSH client for use by test methods.
        Login credentials are stored as environment variables.
        """
        hostname = os.environ["backup_server_hostname"]
        username = os.environ["backup_server_username"]
        password = os.environ["backup_server_password"]

        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
                )
            self.client.connect(hostname, username=username, password=password, timeout=5)
        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")
        except SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
        except BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)
        except Exception as e:
            print("Operation error: %s" % e)

    def test_ping(self):
        """
        Test that the server can be pinged. This indicates that it is
        at least online
        """
        server_address = "83.170.85.222"

        result = os.system("ping -c 1 {}".format(server_address))

        assert result == 0  # 0 indicates the network is active

    def test_csv2iati_backup_made_daily(self):
        """
        Tests that a csv2iati backups has been made within the past 24 hours, and
        that this file has:
        - a filesize greater than 0 bytes
        - a filename matching a regex pattern (which defines the expected filename)
        """
        stdin, stdout, stderr = self.client.exec_command(
            "find /home/backups/csv2iati -maxdepth 1 -type f -mtime -1 -print0 | xargs -0 du | xargs echo -n"
            )
        stdout_unicode = stdout.read().decode('utf-8')
        filesize_str, filename = stdout_unicode.split(" ")

        filesize = int(filesize_str)
        result = re.search(r"\d{4}-\d{2}-\d{2}.sqlite", filename)  # Returns True is the regex pattern is found in the filename

        assert filesize > 0
        assert result

    def test_at_least_1GB_disk_space_available(self):
        """
        Test that there is sufficient space available for future backups.
        Filters the output of 'df' to return the KBs available to the server's main disk.
        """

        stdin, stdout, stderr = self.client.exec_command("df /dev/xvda1 | awk '{print $4}' | sed -n 2p | xargs echo -n")

        disk_space_available = int(stdout.read())

        assert disk_space_available > 1000000  # 1000000KB ~ 1GB
