.PHONY: install run

# Instalar dependências usando uv
install:
	uv sync

# Modo pacote
package:
	uv pip install -e .

# Executar a Api
run:
	uv run python -m src.main
