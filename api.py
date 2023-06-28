from functools import wraps
from flask import Flask, jsonify, request
import busca_infracao as bi

app = Flask(__name__)

# Função para verificar o token de autenticação
def verificar_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')

        # Verificar se o token está presente e é válido
        if token and token.startswith('Bearer '):
            token = token.split(' ')[1]

            # Token válido
            if token == "__BEARER_TOKEN__":
                return f(*args, **kwargs)
        
        # Token inválido ou ausente
        return jsonify({'mensagem': 'Acesso não autorizado'}), 401
    
    return decorator


def ajustInfracao(infracoes):
    try:
        infracao = []
        for multa in infracoes:           
            infracao.append(
                {
                    "codigoInfracao": multa[0],
                    "infracao": multa[1],
                    "responsavel": multa[2],
                    "valor": multa[3],
                    "outrasInformacoes": multa[4],
                    "orgãoAutuador": multa[5],
                    "artigosCTB": multa[6],
                    "pontuacao": multa[7],
                    "gravidade": multa[8],
                }
            )
    except:
        infracao = []
        infracao.append(
            {
                "codigoInfracao": multa[0],
                "infracao": multa[1],
                "responsavel": multa[2],
                "valor": multa[3],
                "outrasInformacoes": multa[4],
                "orgãoAutuador": multa[5],
                "artigosCTB": multa[6],
                "pontuacao": multa[7],
                "gravidade": multa[8],
            }
        )

    return infracao


@app.route('/infracao/<infracao>', methods=['GET'])
@verificar_token
def obter_placa(infracao):

    if len(infracao) < 5:
        return jsonify(
            { 
                "message": "A palavra-chave ou expressão tem que ter no mínimo 5 caracter"
            }
        ),200
    

    infracao = bi.busca_infracao(infracao)

    if infracao == 'Nenhuma infração encontrada.':

        return jsonify(
            { 
                "message": infracao 
            }
        ),200
    
    else:
        data = ajustInfracao(infracao)

        return jsonify(
            {
            "quantidadeInfracoes": len(data),
            "infracoes": data
            }
        ),200
                     
    
if __name__ == '__main__':
    app.run()
