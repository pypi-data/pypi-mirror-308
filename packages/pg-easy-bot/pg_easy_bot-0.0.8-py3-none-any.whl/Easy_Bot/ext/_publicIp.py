import requests


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException as e:
        print(f"Error retrieving IP address: {e}")
        return None
    
def check_public_ip_reachable(ip: str, port: int = 8080):
    try:
        response = requests.get(f"http://{ip}:{port}", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False