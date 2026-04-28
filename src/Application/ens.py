from flask import request, jsonify, make_response
import os

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
        credential = Ens.get_user_credentials()
        data = request.get_json()
        print("MCE passou por aqui!")

        if not data: 
            print("Nao recebemos nada! (mas o mce chegoua qui!)")
            return jsonify({"erro": "Nenhum json enviado"}), 400


        client_id_recebido = data.get("clientId")
        clienst_secret_recebido = data.get("clientSecret")

        if client_id_recebido == credential["clientId"] and clienst_secret_recebido == credential["clientSecret"]:
            print("MCE Chegou aqui e passou o clientId e Secret! Tome o token!")
            return jsonify({
                "status": "sucesso",
                "msg": "Credenciais Validas",
                "access_token": "token_teste_1234",
                "expires_in": 3600
            }), 200
        
        else:
            print("O MCE Chegou até aqui, mas as credenciais estão invalidas ;/") 
            return jsonify({"erro": "credenciais invalidas"}), 401

    
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