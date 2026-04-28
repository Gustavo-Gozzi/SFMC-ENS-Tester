from flask import request, jsonify, make_response
import os
import base64

class Ens:
    
    @staticmethod
    def get_user_credentials():    
        credential = {
            "clientId": os.environ.get('clientId'),
            "clientSecret": os.environ.get('clientSecret')
        }

        return credential

    @staticmethod
    def validate_token():
        print("Inicio da função Validate Token")
        data = request.form if request.form else request.get_json(force=True, silent=True)
        auth_header = request.headers.get('Authorization')
        print("Header:")
        print(auth_header)
        
        token = auth_header.split(" ")

        text_encoded = token[1]

        auth_encoded = base64.b64decode(text_encoded)
        auth_decodificado = auth_encoded.decode('utf-8')

        credentials = auth_decodificado.split(":")

        client_id_recebido = credentials[0]
        client_secret_recebido = credentials[1]
        
        print(client_id_recebido)
        print(client_secret_recebido)

        if not data: 
            print("Nao recebemos nada! (mas o mce chegou aqui!)")
            return jsonify({"error": "invalid_request"}), 400

        credential = Ens.get_user_credentials()
        print("MCE passou por aqui e extraímos os dados!")

        flag_clientId =  client_id_recebido ==  credential["clientId"]
        flag_clientSecret = client_secret_recebido == credential["clientSecret"]

        if flag_clientId and flag_clientSecret:
            print("MCE Chegou aqui e passou o clientId e Secret! Tome o token!")
            response = {
                "access_token": "token_teste_1234",
                "token_type": "Bearer",
                "expires_in": 3600
            }
            print(response)
            return jsonify(response), 200
        
        else:
            print("O MCE Chegou até aqui, mas as credenciais estão invalidas ;/") 
            return jsonify({"error": "invalid_client"}), 401

    
    @staticmethod
    def see_response():
        data = request.get_json()
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            print("Acesso negado!")
            return jsonify({"erro": "Token não fornecido"}), 401
        
        partes_do_header = auth_header.split(" ")
        token_fornecido = partes_do_header[1]
        print(f"Token recebido: {token_fornecido}")
        print(data)
        return jsonify({"msg": "sucesso"}), 200