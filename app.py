from flask import Flask
import subprocess
import platform

app = Flask(__name__)

# Add any IPs or websites you want to monitor here
SERVERS = {
    "Google Public DNS": "8.8.8.8",
    "Cloudflare DNS": "1.1.1.1",
    "Local Gateway": "192.168.1.1" 
}

def ping_server(ip):
    # Adjust ping parameters based on Windows vs Linux/Docker
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip]
    # Execute ping silently
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

@app.route('/')
def index():
    # A lightweight, mobile-responsive HTML layout
    html = '''
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Infra Health</title>
        </head>
        <body style="font-family: Arial, sans-serif; padding: 20px; background: #f4f4f9;">
            <h2 style="color: #333;">Network Dashboard</h2>
    '''
    
    for name, ip in SERVERS.items():
        is_up = ping_server(ip)
        color = "green" if is_up else "red"
        status_text = "ONLINE" if is_up else "OFFLINE"
        
        html += f'''
        <div style="background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <strong style="font-size: 1.1em;">{name}</strong> <br>
            <span style="color: #666; font-size: 0.9em;">{ip}</span>
            <span style="float: right; color: {color}; font-weight: bold;">{status_text}</span>
        </div>
        '''
        
    html += '</body></html>'
    return html

if __name__ == '__main__':
    # Listen on all network interfaces
    app.run(host='0.0.0.0', port=5000)
