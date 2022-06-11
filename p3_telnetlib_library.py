
import telnetlib, sys;

class p3_telnetlib_library:
    def __init__(self, network_device_type, network_device_ip, network_device_port, network_device_username, network_device_password, network_device_enable_password):
        self.network_device_type = network_device_type;
        self.network_device_ip = network_device_ip;
        self.network_device_port = network_device_port;
        self.network_device_username = network_device_username;
        self.network_device_password = network_device_password;
        self.network_device_enable_password = network_device_enable_password;
        
    def connect(self):
        try:
            self.telnet_client_instance = telnetlib.Telnet(host=self.network_device_ip, port=self.network_device_port);
        except:
            return False;
            
        if 'cisco' in self.network_device_type:
            self.telnet_client_instance.read_until(b'Username: ', 4);
            self.telnet_client_instance.write(self.network_device_username.encode('ascii') + b'\n');
            self.telnet_client_instance.read_until(b'Password: ', 4);
            self.telnet_client_instance.write(self.network_device_password.encode('ascii') + b'\n');
            auth_status_flag = self.telnet_client_instance.read_until(b'>', 4);
            if 'Login invalid' in auth_status_flag.decode('ascii'):
                return False;
            if '#' not in auth_status_flag.decode('ascii'):
                self.telnet_client_instance.write('enable'.encode('ascii') + b'\n');
                self.telnet_client_instance.read_until(b'Password: ', 4);
                self.telnet_client_instance.write(self.network_device_enable_password.encode('ascii') + b'\n');
                enable_status_flag = self.telnet_client_instance.read_until(b'#', 4);
                if 'Password' in enable_status_flag.decode('ascii'):
                    return False;
            self.telnet_client_instance.write('terminal length 0'.encode('ascii') + b'\n');
            self.telnet_client_instance.read_until(b'#', 4);
        else:
            return False;
            
    def exec_configuration_file(self, configuration_file_path):
        if 'cisco' in self.network_device_type:
            bytes_string = bytes();
            with open(configuration_file_path, 'r') as configuration_file_instance:
                self.telnet_client_instance.write(b'\n');
                bytes_string += self.telnet_client_instance.read_until(b'#', 4);
                for command in configuration_file_instance:
                    self.telnet_client_instance.write(command.strip().encode('ascii') + b'\n');
                    bytes_string += self.telnet_client_instance.read_until(b'#', 4);
            return bytes_string.decode('ascii');
        else:
            return False;
                    
    def exec_sequence_of_commands(self, sequence_of_commands):
        if 'cisco' in self.network_device_type:
            bytes_string = bytes();
            self.telnet_client_instance.write(b'\n');
            bytes_string += self.telnet_client_instance.read_until(b'#', 4);
            for command in sequence_of_commands:
                self.telnet_client_instance.write(command.encode('ascii') + b'\n');
                bytes_string += self.telnet_client_instance.read_until(b'#', 4);
            return bytes_string.decode('ascii');
        else:
            return False;
            
    def exec_specific_command(self, command):
        if 'cisco' in self.network_device_type:
            bytes_string = bytes();
            self.telnet_client_instance.write(b'\n');
            bytes_string += self.telnet_client_instance.read_until(b'#', 4);
            self.telnet_client_instance.write(command.encode('ascii') + b'\n');
            bytes_string += self.telnet_client_instance.read_until(b'#', 4); 
            return bytes_string.decode('ascii');
        else:
            return False;            
                
def main():
    telnet_client_instance = p3_telnetlib_library('cisco', '10.254.13.1', 23, 'adm1n', '', '');
    if telnet_client_instance.connect() != False:
        print(telnet_client_instance.exec_specific_command('show clock'));
        
if __name__ == '__main__':
    main();
