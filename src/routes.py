from src.Application.ens import Ens
from flask import Flask 

def register_routes(app):

    @app.route('/token', methods=["POST"])
    def validate_token():
        return Ens.validate_token()

    
    @app.rout('/whatsapp', methods=["POST"])
    def whatsapp():
        return Ens.see_response()