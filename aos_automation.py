from netmiko import ConnectHandler
from paramiko.ssh_exception import AuthenticationException
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

def get_user_input(prompt):
    return input(prompt)

def execute_commands(ip, username, password, commands):
    try:
        device = {
            'device_type': 'aruba_os',
            'ip': ip,
            'username': username,
            'password': password
        }
        
        with ConnectHandler(**device) as ssh:
            print(f"Connected to switch: {ip}")
            
            for command in commands:
                try:
                    output = ssh.send_command(command)
                    print(f"Output for command '{command}' on switch {ip}:")
                    print(output)
                    print()  # Add an extra line for readability
                except Exception as e:
                    print(f"Error executing command '{command}' on switch {ip}: {str(e)}")
                    print()  # Add an extra line for readability
    
    except (NetmikoTimeoutException, NetmikoAuthenticationException, AuthenticationException) as e:
        print(f"Connection to switch {ip} failed: {str(e)}")
        print()  # Add an extra line for readability
    
    except Exception as e:
        print(f"An error occurred while connecting to switch {ip}: {str(e)}")
        print()  # Add an extra line for readability

# Read IP addresses from the file
ip_addresses = []
with open('ips.txt', 'r') as file:
    ip_addresses = [line.strip() for line in file]

# Get user input for variables
username = input("Enter the username: ")
password = input("Enter the password: ")

# Get commands from the user
commands = []
while True:
    command = input("Enter a command (or type 'finished' to exit): ")
    if command.lower() == 'finished':
        break
    commands.append(command)

# Execute commands on each switch
for ip in ip_addresses:
    execute_commands(ip, username, password, commands)