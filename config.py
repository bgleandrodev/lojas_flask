# config.py
import os
import logging
import configparser
from dotenv import load_dotenv

# carrega variáveis de ambiente do .env
load_dotenv()


class AppConfig:
    """Classe centralizada para gerenciar todas as configurações da aplicação"""

    def __init__(self):
        # ConfigParser sem interpolação para evitar problemas com %(asctime)s
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read('config.ini')
        self._load_settings()

    def _load_settings(self):
        """Carrega todas as configurações do arquivo .ini e variáveis de ambiente"""

        # ==================== CONFIGURAÇÕES GERAIS ====================
        self.pagination_per_page = self.config.getint('DEFAULT', 'pagination_per_page')
        self.max_per_page = self.config.getint('DEFAULT', 'max_per_page')

        # ==================== CONFIGURAÇÕES DA IA ====================
        self.ai_model = self.config.get('AI', 'model')
        self.ai_temperature = self.config.getfloat('AI', 'temperature')
        self.ai_max_tokens = self.config.getint('AI', 'max_tokens')
        self.ai_enabled = self.config.getboolean('AI', 'enabled')
        self.ai_base_url = self.config.get('AI', 'base_url')

        # ==================== CONFIGURAÇÕES DO BANCO DE DADOS ====================
        self.database_path = self.config.get('DATABASE', 'database_path')
        self.init_products = self.config.getboolean('DATABASE', 'init_products')

        # ==================== CONFIGURAÇÕES DE LOGGING ====================
        self.log_level = self.config.get('LOGGING', 'log_level')
        self.log_format = self.config.get('LOGGING', 'log_format')
        self.log_dir = self.config.get('LOGGING', 'log_dir')
        self.log_file = self.config.get('LOGGING', 'log_file')

        # ==================== CONFIGURAÇÕES DE SEGURANÇA ====================
        self.secret_key_env = self.config.get('SECURITY', 'secret_key_env')
        self.debug_env = self.config.get('SECURITY', 'debug_env')

        # ==================== VARIÁVEIS DE AMBIENTE ====================
        self.secret_key = os.getenv(self.secret_key_env, 'dev-key-change-in-production')
        self.debug = os.getenv(self.debug_env) == 'development'

    def get_log_level(self):
        """Retorna o nível de logging como inteiro para uso no logging.basicConfig"""
        return getattr(logging, self.log_level.upper(), logging.INFO)


# instância global para uso em outros módulos
app_config = AppConfig()