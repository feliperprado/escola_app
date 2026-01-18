# 📁 ESTRUTURA DO PROJETO

```
escola_app/
│
├── 📄 app.py                          # Arquivo principal com todas as rotas
├── 📄 config.py                       # Configurações da aplicação
├── 📄 requirements.txt                # Dependências Python
├── 📄 .gitignore                      # Arquivos a ignorar no Git
│
├── 📄 README.md                       # Documentação principal
├── 📄 GUIA_RAPIDO.md                 # Guia rápido de uso
├── 📄 SETUP_GOOGLE_SHEETS.md         # Como configurar Google Sheets
├── 📄 verificar_estrutura.py         # Script para validar estrutura
│
├── 📁 templates/                      # Arquivos HTML (Jinja2)
│   │
│   ├── 📄 login.html                 # Página de login
│   ├── 📄 base.html                  # Template base (navbar, sidebar)
│   ├── 📄 erro.html                  # Página de erro
│   │
│   ├── 📁 professor/                 # Templates do professor
│   │   ├── 📄 dashboard.html         # Dashboard principal professor
│   │   ├── 📄 frequencia.html        # Registrar frequência
│   │   ├── 📄 conteudo.html          # Lançar conteúdo
│   │   ├── 📄 atividades.html        # Registrar atividades
│   │   ├── 📄 leitura.html           # Registrar leitura diária
│   │   ├── 📄 atestados.html         # Gerenciar atestados
│   │   └── 📄 relatorio.html         # Ver relatórios
│   │
│   └── 📁 pais/                      # Templates dos pais
│       ├── 📄 dashboard.html         # Dashboard pais
│       ├── 📄 atestado.html          # Enviar atestado
│       ├── 📄 meus_atestados.html    # Ver status atestados
│       └── 📄 conteudo.html          # Ver conteúdo de aulas
│
├── 📁 static/                        # Arquivos estáticos
│   ├── 📁 css/
│   │   └── 📄 style.css              # Estilos personalizados
│   └── 📁 js/
│       └── (JavaScript conforme necessário)
│
└── 📁 uploads/                       # Pasta para uploads (opcional)

```

---

## 📊 Arquivos por Função

### Backend (Python/Flask)
- **app.py** - Todas as rotas, lógica e integração com Google Sheets
- **config.py** - Configurações de ambiente

### Frontend (HTML/CSS)
- **templates/login.html** - Autenticação
- **templates/base.html** - Layout principal
- **templates/professor/** - Interface professor
- **templates/pais/** - Interface pais
- **static/css/style.css** - Estilos responsivos

### Documentação
- **README.md** - Guia completo
- **GUIA_RAPIDO.md** - Instruções de uso
- **SETUP_GOOGLE_SHEETS.md** - Como configurar dados
- **.gitignore** - Arquivos a não versionar

---

## 🔗 Fluxo de Rotas

### Rotas Públicas
```
GET  /                    → login.html
POST /login              → Autenticação
GET  /logout             → Limpar sessão
```

### Rotas Professor (auth required)
```
GET  /professor/dashboard        → Dashboard
GET  /professor/frequencia       → Marcar frequência
POST /professor/frequencia       → Salvar frequência
GET  /professor/conteudo         → Lançar conteúdo
POST /professor/conteudo         → Salvar conteúdo
GET  /professor/atividades       → Registrar atividades
POST /professor/atividades       → Salvar atividades
GET  /professor/leitura          → Registrar leitura
POST /professor/leitura          → Salvar leitura
GET  /professor/atestados        → Ver atestados pendentes
POST /professor/aprovar-atestado → Aprovar atestado
POST /professor/rejeitar-atestado → Rejeitar atestado
GET  /professor/relatorio        → Ver relatórios
```

### Rotas Pais (auth required)
```
GET  /pais/dashboard              → Dashboard pais
GET  /pais/atestado               → Formulário atestado
POST /pais/atestado               → Enviar atestado
GET  /pais/meus-atestados         → Ver status atestados
GET  /pais/conteudo               → Ver conteúdo de aulas
```

---

## 🗄️ Google Sheets (estrutura esperada)

### Planilha: "Sistema_Frequencia_Escola"

**Aba: Usuarios**
- usuario (text)
- senha (text)
- tipo (text: professor/pais)
- turma (text)
- aluno_id (text)

**Aba: Alunos**
- id (text)
- nome (text)
- turma (text)
- responsavel (text)
- email (text)
- telefone (text)

**Aba: Frequencia**
- data (date)
- turma (text)
- aluno_id (text)
- status (text: Presente/Ausente)
- hora (time)

**Aba: Conteudo**
- data (datetime)
- turma (text)
- materia (text)
- conteudo (text)
- professor (text)

**Aba: Atividades**
- data (date)
- turma (text)
- aluno_id (text)
- atividade (text)
- status (text: Feito/Não fez)
- data_entrega (date)

**Aba: Leitura**
- data (date)
- turma (text)
- aluno_id (text)
- livro (text)
- paginas (text)
- status (text: Sim/Não)

**Aba: Atestados**
- aluno_id (text)
- responsavel (text)
- data_falta (date)
- motivo (text)
- status (text: Pendente/Aprovado/Rejeitado)
- documento (text)
- data_envio (datetime)

---

## 🔐 Variáveis de Sessão

```python
session['user_id']        # Username do usuário logado
session['tipo_usuario']   # 'professor' ou 'pais'
session['turma']          # Turma do professor/aluno
session['aluno_id']       # ID do aluno (para pais)
```

---

## 📦 Dependências

```
Flask==3.0.0           # Framework web
gspread==6.0.0         # API Google Sheets
oauth2client==4.1.3    # Autenticação Google
google-auth==2.25.2    # Auth Google
```

---

## 🎯 Fluxo de Desenvolvimento

1. Clone/copie o projeto
2. Configure `credentials.json` (Google)
3. Instale dependências: `pip install -r requirements.txt`
4. Execute: `python app.py`
5. Acesse: `http://localhost:5000`
6. Use credenciais de teste para testar

---

## ✅ Checklist de Configuração

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Google Cloud Project criado
- [ ] APIs Google Sheets e Drive ativadas
- [ ] Conta de Serviço criada e JSON baixado
- [ ] Arquivo JSON renomeado para `credentials.json`
- [ ] Planilha criada: "Sistema_Frequencia_Escola"
- [ ] Planilha compartilhada com email da conta de serviço
- [ ] Abas criadas com nomes exatos
- [ ] Dados de teste inseridos
- [ ] Aplicação executada: `python app.py`
- [ ] Login testado com credenciais de teste

---

**Desenvolvido com ❤️ para educadores - v1.0**
