import os 
import requests
from dotenv import load_dotenv
from logger import Logger

# Carrega variáveis do arquivo .env
load_dotenv()

class Config:
    '''Configurações da aplicação'''
    
    # Credenciais necessárias para as requisições na API
    HEADERS = {
        'x-api-user': os.getenv('HABITICA_API_USER'),
        'x-api-key': os.getenv('HABITICA_API_KEY'),
        'x-client': os.getenv('HABITICA_API_USER') + '-habitica-guild-manager'
    }

    # Preenchido dinamicamente pela função get_group_id()
    GROUP_ID = None
    
    # Critérios de filtro
    MIN_LEVEL = int(os.getenv('MIN_LEVEL'))
    WANTED_LANGUAGE = os.getenv('WANTED_LANGUAGE')

    @classmethod
    def get_group_id(cls):
        '''Busca o ID do grupo (party) do usuário'''
        
        # Requisição necessária para obter o ID do grupo
        response = requests.get(
            url=f'https://habitica.com/api/v3/members/{os.getenv('HABITICA_API_USER')}',
            headers=cls.HEADERS
        )
        if response.status_code == 200:
            cls.GROUP_ID = response.json().get('data').get('party').get('_id')
        else:
            Logger.error(f'❌ Erro ao buscar ID do grupo. Status: {response.status_code}, Resposta: {response.text}')
            raise Exception(f'Erro ao buscar ID do grupo. Status: {response.status_code}, Resposta: {response.text}')

    @classmethod
    def validate(cls):
        '''Valida se as configurações essenciais estão presentes'''
        
        # Verifica se as variáveis de ambiente essenciais estão presentes
        if not all(cls.HEADERS.values()):
            Logger.error(f'❌ Variáveis de ambiente faltando. Verifique HABITICA_API_USER, HABITICA_API_KEY.')
            raise ValueError(f'Variáveis de ambiente faltando. Verifique HABITICA_API_USER, HABITICA_API_KEY.')
        
        cls.get_group_id()

        Logger.info('✅ Configurações carregadas com sucesso')