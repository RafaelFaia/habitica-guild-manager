import requests
from config import Config
from logger import Logger
from datetime import datetime, timedelta
from dateutil import parser

def get_all_members_of_group():
    '''Busca todos os membros do grupo (party) do usuário.'''
    
    try:
        # Requisição para obter todos os membros do grupo
        response = requests.get(
            url=f'https://habitica.com/api/v3/groups/{Config.GROUP_ID}/members',
            headers=Config.HEADERS,
            params={'includeAllPublicFields' : 'true'},
            timeout=10
        )
        # Verifica se status_code está entre 200 e 399, se estiver segue o fluxo normal
        response.raise_for_status()
        return response.json().get('data', [])
    # Trata erros de timeout
    except requests.exceptions.Timeout:
        Logger.warning('❌ Timeout ao buscar membros do grupo.')
        return []
    # Trata outros erros de requisição
    except requests.exceptions.RequestException as e:
        Logger.warning(f'❌ Erro na requisição: {e}')
        return []
    
def filter_inactive_members(members):
    '''Filtra membros inativos com base no critério de inatividade (7 dias).'''

    # Lista de membros inativos
    inactive_members = []

    # Data limite para considerar inatividade (7 dias atrás)
    seven_days_ago = (datetime.now() - timedelta(days = 7)).date()

    # Filtra os membros que estão inativos há mais de 7 dias
    for member in members:
        member_last_logged_in = member.get('auth', {}).get('timestamps', {}).get('loggedin')
        member_last_logged_in = (parser.isoparse(member_last_logged_in)).date()
        
        if member_last_logged_in < seven_days_ago:
            inactive_members.append(member)

    return inactive_members

def remove_inactive_members_from_group(inactive_members):
    '''Remove membros inativos do grupo'''

    for inactive_member in inactive_members:
        try:
            # Requisição para remover o membro inativo do grupo
            response = requests.post(
                url=f'https://habitica.com/api/v3/groups/{Config.GROUP_ID}/removeMember/{inactive_member.get("_id")}',
                headers=Config.HEADERS,
                timeout=10
            )
            # Verifica se status_code está entre 200 e 399, se estiver segue o fluxo normal
            response.raise_for_status()
            Logger.membro_removido(inactive_member.get('profile', {}).get('name'), inactive_member.get('auth', {}).get('local', {}).get('username'))
        
        # Trata erros de timeout   
        except requests.exceptions.Timeout:
            Logger.warning('❌ Timeout ao remover membro inativo.')
            continue
        # Trata outros erros de requisição
        except requests.exceptions.RequestException as e:
            Logger.warning(f'❌ Erro na requisição: {e}')
            continue
    

def main():
    '''Função principal para remover membros inativos do grupo'''

    # Configura o sistema de logging
    Logger.setup()

    Logger.info('🚀 Iniciando aplicação Habitica Group Manager - Remove Inactive Members')

    # Valida as configurações essenciais
    Config.validate()

    Logger.info('🔍 Procurando por membros inativos...')

    # Busca todos os membros do grupo
    all_members = get_all_members_of_group()
    
    # Filtra os membros inativos
    inactive_members = filter_inactive_members(all_members)

    if  not inactive_members:
        Logger.info('🛑 Nenhum membro inativo encontrado.')
        return
    
    # Remove os membros inativos do grupo
    remove_inactive_members_from_group(inactive_members)
    Logger.info(f'🛑 Processo concluído. Total de membros removidos: {len(inactive_members)}')

if __name__ == '__main__':
    main()