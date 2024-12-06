import requests
import socket
import asyncio

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException as e:
        print(f"Error retrieving IP address: {e}")
        return None

    
async def check_public_ip_reachable(ip: str, port: int = 8080):
    await asyncio.sleep(1)
    try:
        sock = socket.create_connection((ip, port), timeout=5)
        print(f"Server is accessible at {ip}:{port}")
        return True
    except (socket.timeout, socket.error):
        print(f"Server is not accessible at {ip}:{port}")
        return False

