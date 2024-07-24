import os
from logging_notification import log_event, notify_admin

def check_DDOS_attack_dns():
    ddos_log_file_path = os.path.abspath('tests/Ataque DNS - tcpdump.txt')  # Path to the attack log file
    
    with open(ddos_log_file_path, 'r') as file:
        attacks_per_ip = {}  # Dictionary to count attacks by attacker and victim IPs
        final_message = ''
        ip_blocked = False
        blocked_ips_list = []

        for line in file:
            attacker_ip = line.split()[2]
            victim_ip = line.split()[4][:-1]  # Remove the ':' at the end of the victim's IP
            if (attacker_ip, victim_ip) in attacks_per_ip:
                attacks_per_ip[(attacker_ip, victim_ip)] += 1
                if attacks_per_ip[(attacker_ip, victim_ip)] >= 10:  # Define an appropriate threshold
                    ip_blocked = True
                    if attacker_ip not in blocked_ips_list:
                        message = f'Blocked IP: {attacker_ip} due to suspected attack on IP: {victim_ip}'
                        final_message += message + '\n'
                        blocked_ips_list.append(attacker_ip)

                        # Log the event
                        log_event(message)
                        
                        # Notify the administrator
                        notify_admin('DDOS Attack',message)

                        # Block IP (implement the actual blocking logic here)
                        # os.system(f"sudo iptables -A INPUT -s {attacker_ip} -j DROP")

            else:
                attacks_per_ip[(attacker_ip, victim_ip)] = 1

    if ip_blocked:
        return final_message
    else:
        no_attack_message = 'No DDOS-like behavior detected'
        log_event(no_attack_message)  # Log that no DDOS-like behavior was detected
        return no_attack_message
