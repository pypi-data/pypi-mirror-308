import opcua as opc
import os

class ConfigClient:
    def __init__(self, node_config: dict[str, str]):
        self.node_config = node_config
        self.client = None
        self.certificate_path = None
        self.private_key_path = None

    def create_client(self):
        try:
            self.client = opc.Client(self.node_config['url'], timeout=int(self.node_config['timeout']))
            self.__set_parameters()
        except Exception as e:
            print(f"An error occurred while creating OPC client: {e}")

    def __get_paths(self):
            try:
                self.certificate_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'certificate', self.node_config['certificate']))
                self.private_key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'private_key', self.node_config['private_key']))
            except Exception as e:
                print(f"An error occurred while getting certificate and private key paths: {e}")

    def __set_parameters(self): ## set case of no user and password
        try:
            self.__get_paths()
            self.client.application_uri = self.node_config['app_uri']
            self.client.set_user(self.node_config['user'])
            self.client.set_password(self.node_config['password'])
            self.client.set_security_string(f"{self.node_config['policy']},{self.node_config['mode']},{self.certificate_path},{self.private_key_path}")
        except KeyError as e:
            print(f"Error: {e} is missing in OPC server parameters.")
        except Exception as e:
            print(f"An error occurred while setting OPC parameters: {e}")