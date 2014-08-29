# Acquire the performance and network(ping) status of the remote host
# Return as a dictionary

import ssh
from django.utils import timezone
from ping import quiet_ping

def sshConn(host, port, username, password):
    try:
        sshconn = ssh.SSHClient()
        sshconn.set_missing_host_key_policy(ssh.AutoAddPolicy())
        sshconn.connect(host, port, username, password)
        return sshconn
    except Exception,e:
        print e
        return

def sshGetStatus(sshconn, command):
    stdin, stdout, stderr = sshconn.exec_command(command)
    stdout = stdout.read()
    stderr = stderr.read()
    if stdout:
        return stdout
    elif stderr:
        print '[remote command error] %s' % stderr
        return 
    else:
        print '[remote command unknow error]'
        return

def pingStatus(host):
    ping_result = quiet_ping(host, timeout=1)
    return ping_result


def perfStatus(host, port, username, password):
    
    perf_stat_dict = {}
    sshconn = sshConn(host, port, username, password)
    
    if sshconn:
        # By SSH
        hostname = 'hostname'
        kernel_version = 'uname -s -r'
        os_version = 'cat /etc/redhat-release'
        uptime = 'cat /proc/uptime'
        loadavg = 'cat /proc/loadavg'
        cpu_procs = 'cat /proc/cpuinfo | grep processor | wc -l'
        meminfo = 'cat /proc/meminfo'
        
        
        meminfo = sshGetStatus(sshconn, meminfo)
        meminfo_list = meminfo.split('\n')[0:4]
        for mem in meminfo_list:
            '''
            MemTotal:       65902628 kB
            MemFree:        59911836 kB
            Buffers:          353520 kB
            Cached:          3547180 kB
            '''
            if 'MemTotal' in mem:
                mem_total = mem.split()[1]
            elif 'MemFree' in mem:
                mem_free = mem.split()[1]
            elif 'Buffers' in mem:
                buffers = mem.split()[1]
            elif 'Cached' in mem:
                cached = mem.split()[1]
        
        mem_real_used = int(mem_total) - int(mem_free) - int(buffers) - int(cached)
        
        r_hostname = sshGetStatus(sshconn, hostname).strip()
        r_kernel_version = sshGetStatus(sshconn, kernel_version).strip()
        r_os_version = sshGetStatus(sshconn, os_version).strip()
        r_uptime = round(float(sshGetStatus(sshconn, uptime).split()[0].split('.')[0])/3600/24, 2)
        r_loadavg = sshGetStatus(sshconn, loadavg)[0:14]
        r_cpu_procs = int(sshGetStatus(sshconn, cpu_procs))
        r_meminfo = '%.2f %.2f %.2f%%' % (round(float(mem_total)/1024/1024, 2), round(float(mem_real_used)/1024/1024, 2) ,round(float(mem_real_used)/float(mem_total), 2)*100)
        
        #print '<uptime>\n%s'       % r_uptime
        #print '<loadavg>\n%s'      % r_loadavg
        #print '<cpu_procs>\n%d'    % r_cpu_procs
        #print '<meminfo>\n%s'      % r_meminfo
        #print '<ping>\n%r'         % r_ping
        
        sshconn.close()
        
        perf_stat_dict['hostname']  = r_hostname
        perf_stat_dict['kernel_version'] = r_kernel_version
        perf_stat_dict['os_version'] = r_os_version
        perf_stat_dict['uptime']    = r_uptime
        perf_stat_dict['loadavg']   = r_loadavg
        perf_stat_dict['meminfo']   = r_meminfo    
        perf_stat_dict['cpu_procs'] = r_cpu_procs
    
    # Ping
    r_ping = pingStatus(host)
    perf_stat_dict['ping'] = r_ping  
    
    # Last check time
    r_last_check = timezone.now()
    perf_stat_dict['last_check'] = r_last_check
        
    return perf_stat_dict
    
    ''' returns
        {
            'ping': (0, 0.47707557678222656, 0.3682374954223633),
            'uptime': 38.11,                         days
            'hostname': 'dbnode0',
            'loadavg': '0.08 0.02 0.01', 
            'meminfo': '62.85 1.99 3.00%',           G
            'cpu_procs': 24 
        }
        
        OR
        
        {'ping': (100, None, None)}           # KeyError
    '''
