import logging
import os
from datetime import datetime

class Logger:
    '''Gerenciador de logs da aplicação'''
    
    LOG_FILE = 'logs/habitica_guild_manager.log'
    
    @staticmethod
    def setup():
        '''Configura o sistema de logging'''

        # Garante que a pasta logs existe
        os.makedirs(os.path.dirname(Logger.LOG_FILE), exist_ok=True)
        
        # Configura o logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S',
            handlers=[
                logging.FileHandler(Logger.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()  # Também mostra no console
            ]
        )
    
    @staticmethod
    def info(mensagem):
        '''Log de informações normais'''
        logging.info(mensagem)
    
    @staticmethod
    def error(mensagem):
        '''Log de erros'''
        logging.error(mensagem)
    
    @staticmethod
    def warning(mensagem):
        '''Log de avisos'''
        logging.warning(mensagem)
    
    @staticmethod
    def convite_enviado(name, username):
        '''Log específico para convites enviados'''
        mensagem = f'📨 Convite enviado - Nome: {name}, Username: {username}'
        logging.info(mensagem)

    @staticmethod
    def membro_removido(name, username):
        '''Log específico para membros removidos'''
        mensagem = f'👋 Membro removido - Nome: {name}, Username: {username}'
        logging.info(mensagem)