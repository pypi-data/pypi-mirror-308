import requests
import socket
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException as e:
        print(f"Error retrieving IP address: {e}")
        return None
    

def is_local_network():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip.startswith('127.') or local_ip.startswith('192.168.')