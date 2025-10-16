import requests 
import time
from config import Config
from log_manager import LogManager
from logger import Logger

def get_users_in_search_of_parties():
    '''Busca usuários que estão procurando por grupos no Habitica.'''
    
    try:
        # Requisição para obter todos os usuários procurando por grupos
        response = requests.get(
            url='https://habitica.com/api/v3/looking-for-party',
            headers=Config.HEADERS,
            timeout=10
        )
        # Verifica se status_code está entre 200 e 399, se estiver segue o fluxo normal
        response.raise_for_status()
        return response.json().get('data', [])
    # Trata erros de timeout
    except requests.exceptions.Timeout:
        Logger.warning('❌ Timeout ao buscar usuários procurando por grupo.')
        return []
    # Trata outros erros de requisição
    except requests.exceptions.RequestException as e:
        Logger.warning(f'❌ Erro na requisição: {e}')
        return []    

def filter_eligible_users(users_searching_for_party):
    '''Filtra usuários elegíveis com base em idioma e nível, além de verificar se já foram convidados.'''
    # Lista de usuários que atendem aos critérios
    eligible_users = []

    # Carrega os UUIDs já convidados
    already_invited_uuids = LogManager.load_invited_uuids()

    # Filtra os usuários com base nos critérios e se já foram convidados, adicionando apenas os elegíveis na lista
    for user in users_searching_for_party:
        if user.get('preferences',{}).get('language') == Config.WANTED_LANGUAGE and user.get('stats',{}).get('lvl') >= Config.MIN_LEVEL and user.get('_id') not in already_invited_uuids:
            eligible_users.append(user)
         
    return eligible_users

    
def invite_users_to_a_group(eligible_users):
    '''Envia convites para até dois usuários elegíveis.'''

    # Pega os UUIDs dos dois primeiros usuários elegíveis
    uuids = [user.get('_id') for user in eligible_users[:2]]
    try:
        # Requisição para enviar convites aos usuários elegíveis
        response = requests.post(
            url = f'https://habitica.com/api/v3/groups/{Config.GROUP_ID}/invite',
            headers = Config.HEADERS,
            json = {'uuids': uuids},
            timeout=10
        )
        # Verifica se status_code está entre 200 e 399, se estiver segue o fluxo normal
        response.raise_for_status()
        # Salva os UUIDs convidados no log
        LogManager.save_new_invites(uuids)

        # Log individual para cada usuário
        for user in eligible_users[:2]:
            name = user.get('profile').get('name')
            username = user.get('auth').get('local').get('username')
            Logger.convite_enviado(name, username)

    # Trata erros de timeout   
    except requests.exceptions.Timeout:
        Logger.warning('❌ Timeout ao enviar convites para usuários.')
        return
    # Trata outros erros de requisição
    except requests.exceptions.RequestException as e:
        Logger.warning(f'❌ Erro na requisição: {e}')
        return
    
def main():
    '''Loop principal para buscar, filtrar e convidar usuários.'''

    # Inicializa o sistema de logging
    Logger.setup()

    Logger.info('🚀 Iniciando aplicação Habitica Group Manager - Invite Users')

    # Valida as configurações essenciais
    Config.validate()
    Logger.info(f'📊 Filtros: Level >= {Config.MIN_LEVEL}, Idioma: {Config.WANTED_LANGUAGE}')

    Logger.info('🔍 Buscando usuários procurando grupo...')

    # Loop infinito para buscar, filtrar e convidar usuários a cada 30 segundos
    try:
        while True:
            users_searching_for_party = get_users_in_search_of_parties()
            if users_searching_for_party:
                eligible_users = filter_eligible_users(users_searching_for_party)
                if eligible_users:
                    invite_users_to_a_group(eligible_users)
            time.sleep(30) # Tempo de espera citado na documentação da API, não colocar abaixo disso.
    except KeyboardInterrupt:
        Logger.info('🛑 Encerrando o script de convite de usuários.')

if __name__ == '__main__':
    main()