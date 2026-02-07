# Como executar o app

## Docker (recomendado)

```bash
./run_docker.sh
```

### Manual rápido do script `run_docker.sh`

1. **Pré-requisitos**  
   - Docker instalado e em execução.

2. **Passo a passo**  
   - No terminal, execute:
     ```bash
     ./run_docker.sh
     ```
   - O script faz o build da imagem, remove um container antigo (se existir) e inicia o app.
   - Acesse: `http://localhost:5000`

3. **Personalizar porta e credenciais (opcional)**  
   ```bash
   export PORT=5000
   export SECRET_KEY="uma_chave_segura"
   export ADMIN_USER="admin"
   export ADMIN_PASSWORD="senha"
   ./run_docker.sh
   ```

Variáveis opcionais:

```bash
export SECRET_KEY="uma_chave_segura"
export ADMIN_USER="admin"
export ADMIN_PASSWORD="senha"
export PORT=5000
./run_docker.sh
```

A aplicação ficará disponível em `http://localhost:5000`.

## Windows (PowerShell)

```powershell
python -m pip install -r requirements.txt
$env:SECRET_KEY="uma_chave_segura"
$env:ADMIN_USER="admin"
$env:ADMIN_PASSWORD="senha"
python app.py
```

## Linux/macOS

```bash
python -m pip install -r requirements.txt
export SECRET_KEY="uma_chave_segura"
export ADMIN_USER="admin"
export ADMIN_PASSWORD="senha"
python app.py
```

## PDF (wkhtmltopdf)

Para a geração de PDF, instale o `wkhtmltopdf` no sistema operacional e garanta que o binário esteja no PATH.

- Windows: https://wkhtmltopdf.org/downloads.html
- Linux: `sudo apt-get install wkhtmltopdf`
- macOS (Homebrew): `brew install wkhtmltopdf`
