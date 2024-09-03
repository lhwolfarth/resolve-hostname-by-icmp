import os
import subprocess
import scapy.all as scapy

# Variável para definir a pasta onde o arquivo de hosts separado será criado
custom_hosts_dir = "/home/user/"  # Substitua pelo caminho desejado
custom_hosts_file = os.path.join(custom_hosts_dir, "custom_hosts")

def snmp_get(ip, community):
    oid = "1.3.6.1.2.1.1.5.0"
    if ':' in ip:  # Detecta IPv6
        command = f"snmpget -v2c -c {community} [{ip}] {oid}"
    else:  # IPv4
        command = f"snmpget -v2c -c {community} {ip} {oid}"

    try:
        result = subprocess.check_output(command, shell=True, universal_newlines=True)
        hostname = result.split('STRING: ')[1].strip().strip('"')
        return hostname
    except subprocess.CalledProcessError:
        return None

def update_hosts_file(ip, hostname, hosts_file):
    updated = False

    # Verifica se o arquivo de hosts existe, caso contrário, cria-o
    if not os.path.exists(hosts_file):
        with open(hosts_file, 'w') as file:
            pass  # Cria o arquivo vazio

    with open(hosts_file, 'r') as file:
        lines = file.readlines()

    with open(hosts_file, 'w') as file:
        for line in lines:
            if hostname in line:
                # Atualiza o IP para o hostname existente
                file.write(f"{ip} {hostname}\n")
                updated = True
            else:
                file.write(line)

        if not updated:
            # Adiciona novo par IP-hostname
            file.write(f"{ip} {hostname}\n")

def process_packet(packet, community):
    ip = None

    if packet.haslayer(scapy.IP):  # Pacote IPv4
        if packet.haslayer(scapy.ICMP):
            ip = packet[scapy.IP].src

    elif packet.haslayer(scapy.IPv6):  # Pacote IPv6
        if packet.haslayer(scapy.ICMPv6EchoRequest):
            ip = packet[scapy.IPv6].src

    if ip:
        hostname = snmp_get(ip, community)
        if hostname:
            # Atualiza o arquivo /etc/hosts
            update_hosts_file(ip, hostname, "/etc/hosts")
            # Atualiza o arquivo de hosts personalizado
            if not os.path.exists(custom_hosts_dir):
                os.makedirs(custom_hosts_dir)
            update_hosts_file(ip, hostname, custom_hosts_file)

def main():
    community = "public"  # Substitua pelo seu community string
    print("Listening for ICMP packets...")
    scapy.sniff(filter="ip or ip6", prn=lambda packet: process_packet(packet, community), store=0)

if __name__ == "__main__":
    main()
