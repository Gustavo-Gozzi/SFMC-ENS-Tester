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
        data = request.form if request.form else request.get_json(force=True, silent=True)
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        print(f"Dados brutos capturados: {data}")

        if not data: 
            print("Nao recebemos nada! (mas o mce chegou aqui!)")
            return jsonify({"error": "invalid_request"}), 400

        credential = Ens.get_user_credentials()
        print("MCE passou por aqui e extraímos os dados!")

        # 2. Captura lidando com camelCase ou snake_case (segurança extra)
        client_id_recebido = data.get("clientId") or data.get("client_id")
        client_secret_recebido = data.get("clientSecret") or data.get("client_secret")
        print(f"{client_id_recebido} | {client_secret_recebido}")

        if client_id_recebido == credential["clientId"] and client_secret_recebido == credential["clientSecret"]:
            print("MCE Chegou aqui e passou o clientId e Secret! Tome o token!")
            
            # 3. O RETORNO PADRÃO OAUTH 2.0 STRICT
            # Removi "status" e "msg". Adicionei "token_type".
            return jsonify({
                "access_token": "token_teste_1234",
                "token_type": "Bearer",
                "expires_in": 3600
            }), 200
        
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