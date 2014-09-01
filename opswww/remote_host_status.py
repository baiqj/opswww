# Acquire the performance and network(ping) status of the remote host
# Return as a dictionary

import ssh
from django.utils import timezone
from models import Hostlist
from ping import quiet_ping

def sshConn(host, port, username, password):
    try:
        sshconn = ssh.SSHClient()
        sshconn.set_missing_host_key_policy(ssh.AutoAddPolicy())
        sshconn.connect(host, port, username, password)
        return sshconn
    except Exception,e:
        print '%s %s' % (e, host)
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


def perfStatus(host_queue):
    
    while True:
        if not host_queue.empty():
            host_param = host_queue.get()
            
            host = host_param[0]
            port = host_param[1]
            username = host_param[2]
            password = host_param[3]
            
            perf_stat_dict = {'hostip':host,}
        
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
            if r_ping[0] == 100:
                perf_stat_dict['health'] = 'Down'
            else:
                perf_stat_dict['health'] = 'Up'
            perf_stat_dict['ping'] = r_ping  
            
            # Last check time
            r_last_check = timezone.now()
            perf_stat_dict['last_check'] = r_last_check
                
            #print perf_stat_dict
                    
            ''' 
                print perf_stat_dict  [Up]
                
                {
                    'uptime': 41.13,                            #days
                    'meminfo': '62.85 1.97 3.00%',              #G 
                    'kernel_version': 'Linux 2.6.32-431.17.1.el6.x86_64', 
                    'hostname': 'dbnode0', 
                    'ping': (0, 0.5650520324707031, 0.47641992568969727), 
                    'last_check': datetime.datetime(2014, 9, 1, 5, 55, 55, 718382, tzinfo=<UTC>), 
                    'os_version': 'CentOS release 6.5 (Final)', 
                    'loadavg': '0.00 0.00 0.00', 
                    'health': 'Up', 
                    'cpu_procs': 24, 
                    'hostip': u'10.0.0.81'
                }
                
                OR [Down]
                
                {
                    'ping': (100, None, None), 
                    'last_check': datetime.datetime(2014, 9, 1, 5, 55, 4, 437683, tzinfo=<UTC>), 
                    'health': 'Down', 
                    'hostip': u'10.0.3.109'
                }
            '''
            
            # Save to datebase
            host_obj = Hostlist.objects.get(ip = host)
            if perf_stat_dict['health'] == 'Up':
                host_obj.uptime = perf_stat_dict['uptime']
                host_obj.meminfo = perf_stat_dict['meminfo']
                host_obj.kernel_version = perf_stat_dict['kernel_version']
                host_obj.hostname = perf_stat_dict['hostname']
                host_obj.ping_packet_loss = perf_stat_dict['ping'][0]
                host_obj.ping_delay = round(perf_stat_dict['ping'][2], 2)
                host_obj.last_check = perf_stat_dict['last_check']
                host_obj.os_version = perf_stat_dict['os_version']
                host_obj.loadavg = perf_stat_dict['loadavg']
                host_obj.cpu_procs = perf_stat_dict['cpu_procs']
                
            elif perf_stat_dict['health'] == 'Down':
                host_obj.ping_packet_loss = perf_stat_dict['ping'][0]
                host_obj.ping_delay = perf_stat_dict['ping'][2]
                host_obj.last_check = perf_stat_dict['last_check']
                host_obj.meminfo = ''
                host_obj.loadavg = ''
                host_obj.uptime = 0.00
                
            host_obj.save()
                
                
        else:    
            break
    