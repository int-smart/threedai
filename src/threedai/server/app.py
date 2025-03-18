from flask import Flask
from flask_cors import CORS
import os
import argparse

from ..gui import interface
from ..ml import model

class AIServer:
    def __init__(self, host='0.0.0.0', port=5000, model_path=None):
        self.app = Flask(__name__)
        CORS(self.app)
        self.host = host
        self.port = port
        
        # Initialize the ML model
        self.model = model.NeuralModel(model_path)
        
        # Register routes
        from . import routes
        routes.register_routes(self.app, self.model)
        
    def run(self):
        self.app.run(host=self.host, port=self.port, debug=True)

def start_server(host='0.0.0.0', port=5000, model_path=None):
    server = AIServer(host, port, model_path)
    server.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the threedai server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    parser.add_argument('--model', default=None, help='Path to the model weights')
    
    args = parser.parse_args()
    start_server(args.host, args.port, args.model)
