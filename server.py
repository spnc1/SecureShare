import http.server # Built-in server library
import ssl # HTTPS Server (TLS)
import cgi # Form data management
import privateInfo # Private

# Database integration
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# CONFIG -----------------------------------------------------
serverAddress = ('0.0.0.0', 8443)



# SERVER -----------------------------------------------------
class fileServer(http.server.BaseHTTPRequestHandler):
    
    # METHODS
    def setCORSheaders(self):
        self.send_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS") # Allowed methods (do commands)
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        # Necessary setup for file upload

    def do_OPTIONS(self):
        self.send_response(200)
        self.setCORSheaders()
        self.end_headers()

    def do_POST(self):
        print(f'Received request: {self.path}')

        match self.path:
            case '/login': pass
            case '/signup': pass



# PROGRAM ----------------------------------------------------
if __name__ == "__main__":

    # DATABASE ---------------------------------------------------
    # Using TLS for secure connection and zlib to compress messages and minimize data sent between MongoDB and the server
    client = MongoClient(privateInfo.uri, server_api = ServerApi('1'), tls = True, tlsCAFile = '/etc/ssl/cert.pem', compressors = "zlib", zlibCompressionLevel = 6)

    # Ping the database
    print('MongoDB Connection: ', end='')
    try: client.admin.command('ping'), print("Successful")
    except Exception as e: print(e)



    # SERVER -----------------------------------------------------
    httpd = http.server.HTTPServer(serverAddress, fileServer)

    # Using a SSL wrapper to ensure secure connection between client and server
    sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslContext.load_cert_chain('./certificates/cert.pem', './certificates/key.pem')
    httpd.socket = sslContext.wrap_socket(httpd.socket, server_side=True)

    print(f'Server: Running on https://{serverAddress[0]}:{serverAddress[1]}...')
    httpd.serve_forever()