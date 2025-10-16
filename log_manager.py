import json
import os
from logger import Logger

class LogManager:
    '''Gerenciador de log de usuários convidados'''
    
    LOG_FILE = 'logs/invited_uuids.json'
    
    @staticmethod
    def load_invited_uuids():
        '''Carrega todos os UUIDs já convidados do arquivo de log'''

        # Verifica se o arquivo de log existe e carrega os UUIDs
        try:
            if os.path.exists(LogManager.LOG_FILE):
                with open(LogManager.LOG_FILE, 'r', encoding='utf-8') as file:
                    return set(json.load(file))
            return set()
        except Exception as e:
            Logger.warning(f'❌ Erro ao carregar usuários já convidados: {e}')
            return set()
    
    @staticmethod
    def save_new_invites(new_uuids):
        '''Salva novos UUIDs no arquivo de log'''

        try:
            # Garante que o diretório existe
            os.makedirs(os.path.dirname(LogManager.LOG_FILE), exist_ok=True)
            
            # Carrega o arquivo existente
            already_invited_uuids = LogManager.load_invited_uuids()
            
            # Adiciona os novos usuários convidados
            already_invited_uuids.update(new_uuids)
            
            # Salva tudo novamente no arquivo
            with open(LogManager.LOG_FILE, 'w', encoding='utf-8') as file:
                json.dump(list(already_invited_uuids), file, indent=4)
            
        except Exception as e:
            Logger.warning(f'❌ Erro ao salvar novos usuários convidados: {e}')