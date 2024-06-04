from pymetasploit3.msfrpc import MsfRpcClient
import os

msfpass = os.getenv('MSFPASS', 'yourpassword')  
client = MsfRpcClient(msfpass, port=55553, ssl=True)