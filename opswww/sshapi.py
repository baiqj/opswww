import ssh
    
def runCommand(host, port, username, password, command):
    try:
        sshconn = ssh.SSHClient()
        sshconn.set_missing_host_key_policy(ssh.AutoAddPolicy())
        sshconn.connect(host, port, username, password)
        #sshconn.connect('vm1', 22, 'root', '123456')
        stdin, stdout, stderr = sshconn.exec_command(command)
        r_stdout = stdout.read()        
        r_stderr = stderr.read()
        sshconn.close()
        if r_stdout:
            return r_stdout
        if r_stderr:
            return r_stderr 
        
    except Exception, e:
        return e

def sftpGet(host, port, username, password, src_path, dst_path):
    try:
        sshconn = ssh.SSHClient()
        sshconn.set_missing_host_key_policy(ssh.AutoAddPolicy())
        sshconn.connect(host, port, username, password)
        sftp = sshconn.open_sftp()
        sftp.get(src_path, dst_path)
        sshconn.close()
        
        return 0
    
    except Exception, e:
        return e

def sftpPut(host, port, username, password, src_path, dst_path):
    try:
        sshconn = ssh.SSHClient()
        sshconn.set_missing_host_key_policy(ssh.AutoAddPolicy())
        sshconn.connect(host, port, username, password)
        sftp = sshconn.open_sftp()
        sftp.put(src_path, dst_path)
        sshconn.close()
        
        return 0
    except Exception, e:
        return e            
   