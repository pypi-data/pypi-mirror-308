import requests
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
    print(f"checking ip status for {ip}")
    await asyncio.sleep(5)
    try:
        response = requests.get(f"http://{ip}:{port}", timeout=5)
        if response.status_code == 200:
            print('Public IP is reachable')
            return True
        else:
            print('Public IP is unreachable')
    except requests.RequestException:
        return False
    
