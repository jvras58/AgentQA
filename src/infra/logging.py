"""Define o logger para a aplicação, configurando o nível de log com base no modo de debug."""

import logging

from src.core.config import settings

log_level = logging.DEBUG if settings.debug_mode else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

def get_logger(name: str) -> logging.Logger:
    """Retorna um logger configurado com o nome fornecido."""
    logger = logging.getLogger(name)
    return logger
