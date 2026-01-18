# 🚀 DEPLOY - Colocando a Aplicação em Produção

## Opção 1: PythonAnywhere (Recomendado para começar)

### 1. Crie uma conta
- Acesse: https://www.pythonanywhere.com
- Crie uma conta gratuita

### 2. Upload do projeto
```bash
# Acesse o console do PythonAnywhere
cd ~
git clone [seu-repositorio]
cd escola_app
```

### 3. Configure o ambiente virtual
```bash
mkvirtualenv --python=/usr/bin/python3.9 escola_app
pip install -r requirements.txt
```

### 4. Configure a aplicação web
1. Vá para "Web" no painel
2. Clique em "Add a new web app"
3. Escolha "Python 3.9"
4. Escolha "Manual configuration"
5. Configure o arquivo WSGI (veja abaixo)

### 5. Crie arquivo `wsgi.py`
```python
import sys
path = '/home/seu_usuario/escola_app'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

---

## Opção 2: Heroku

### 1. Instale Heroku CLI
https://devcenter.heroku.com/articles/heroku-cli

### 2. Crie `Procfile` na raiz do projeto
```
web: gunicorn app:app
```

### 3. Instale gunicorn
```bash
pip install gunicorn
pip freeze > requirements.txt
```

### 4. Configure variáveis de ambiente
```bash
heroku config:set SECRET_KEY="sua-chave-super-secreta"
heroku config:set FLASK_ENV=production
```

### 5. Deploy
```bash
heroku login
heroku create seu-app-name
git push heroku main
```

---

## Opção 3: VPS (DigitalOcean, Linode, etc)

### 1. SSH na máquina
```bash
ssh root@seu-ip
```

### 2. Instale dependências
```bash
apt update && apt upgrade
apt install python3 python3-pip python3-venv
apt install nginx
```

### 3. Clone o projeto
```bash
cd /var/www
git clone [seu-repositorio] escola_app
cd escola_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 4. Configure Nginx
Crie `/etc/nginx/sites-available/escola_app`:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /var/www/escola_app/static;
    }
}
```

Ative o site:
```bash
ln -s /etc/nginx/sites-available/escola_app /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 5. Configure Systemd (para iniciar automaticamente)
Crie `/etc/systemd/system/escola_app.service`:
```ini
[Unit]
Description=Sistema Frequencia Escolar
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/escola_app
ExecStart=/var/www/escola_app/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    app:app

[Install]
WantedBy=multi-user.target
```

Inicie o serviço:
```bash
systemctl daemon-reload
systemctl start escola_app
systemctl enable escola_app
```

### 6. SSL (Let's Encrypt)
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d seu-dominio.com
```

---

## Checklist Pré-Deploy

### Segurança
- [ ] Alterar `SECRET_KEY` em `config.py`
- [ ] Definir `DEBUG = False`
- [ ] Usar HTTPS em produção
- [ ] Proteger `credentials.json` (não versionar)

### Performance
- [ ] Usar Gunicorn ou Waitress (não Flask dev server)
- [ ] Usar Nginx ou Apache como proxy reverso
- [ ] Configurar cache (Redis, Memcached)

### Dados
- [ ] Backup da planilha Google Sheets
- [ ] Testar restauração de backups
- [ ] Definir política de retenção de dados

### Monitoramento
- [ ] Configurar logs
- [ ] Monitorar performance (New Relic, DataDog)
- [ ] Alertas para erros críticos

---

## Variáveis de Ambiente em Produção

Crie arquivo `.env`:
```
FLASK_ENV=production
SECRET_KEY=sua-chave-super-secreta-aleatoria
SPREADSHEET_NAME=Sistema_Frequencia_Escola
```

Carregue em `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Monitoramento e Logs

### Logs com Gunicorn
```bash
gunicorn app:app \
    --access-logfile /var/log/gunicorn/access.log \
    --error-logfile /var/log/gunicorn/error.log
```

### Ver logs em tempo real
```bash
tail -f /var/log/gunicorn/error.log
```

---

## Backup Automático

Crie script `backup.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/escola_app"
mkdir -p $BACKUP_DIR

# Backup da planilha (exporta como PDF)
# Use a API do Google Drive

# Backup do código
tar -czf $BACKUP_DIR/codigo_$DATE.tar.gz /var/www/escola_app/

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

Configure cron:
```bash
crontab -e
# Adicione: 0 2 * * * /home/user/backup.sh
```

---

## Upgrade da Aplicação

```bash
cd /var/www/escola_app
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
systemctl restart escola_app
```

---

## Troubleshooting

### Erro 502 Bad Gateway
- Verificar se Gunicorn está rodando: `systemctl status escola_app`
- Verificar logs: `tail -f /var/log/gunicorn/error.log`
- Reiniciar: `systemctl restart escola_app`

### Erro de Conexão Google Sheets
- Verificar credenciais: `cat credentials.json`
- Testar conexão: `python verificar_estrutura.py`
- Validar permissões na planilha

### Aplicação lenta
- Verificar CPU/RAM: `top`
- Aumentar workers: `gunicorn --workers 5 app:app`
- Usar cache (Redis)

---

## Certificado SSL Automático

Renovar automaticamente:
```bash
certbot renew --quiet
```

Cron automático:
```bash
(crontab -l 2>/dev/null; echo "0 12 * * * certbot renew --quiet") | crontab -
```

---

**Pronto para produção! 🎓**
