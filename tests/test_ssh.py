import os
import pytest
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException, BadHostKeyException
import re

def test_ssh():
    """
    Create a SSH client for use by test methods.
    Login credentials are stored as environment variables.
    """
    hostname = os.environ["backup_server_hostname"]
    username = os.environ["backup_server_username"]
    password = os.environ["backup_server_password"]

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password, timeout=5)
    except AuthenticationException:
        print("Authentication failed, please verify your credentials: %s")
    except SSHException as sshException:
        print("Unable to establish SSH connection: %s" % sshException)
    except BadHostKeyException as badHostKeyException:
        print("Unable to verify server's host key: %s" % badHostKeyException)
    except Exception as e:
        print("Operation error: %s" % e)

    stdin, stdout, stderr = client.exec_command("df /dev/xvda1 | awk '{print $4}' | sed -n 2p | xargs echo -n")

    disk_space_available = int(stdout.read())
    assert disk_space_available < 0  # Should fail, in order to view output