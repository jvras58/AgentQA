.PHONY: install run

# Instalar dependências usando uv
install:
	uv sync

# Modo pacote
package:
	uv pip install -e .

# Executar a Api
run:
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
