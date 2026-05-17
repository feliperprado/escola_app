# Sistema de Frequência Escolar - Flask

Uma aplicação web moderna para controle de frequência, atividades e comunicação entre escola e responsáveis.

## 🎯 Funcionalidades

### Para Professores
- ✅ **Controle de Frequência** - Registre presença/ausência de alunos
- 📝 **Lançamento de Conteúdo** - Documente o que foi ensinado em aula
- ✔️ **Registro de Atividades** - Acompanhe quem fez/não fez tarefas
- 📚 **Leitura Diária** - Registre leitura realizada pelos alunos
- 🏥 **Gerenciar Atestados** - Aprove/rejeite justificativas de falta
- 📊 **Relatórios** - Veja relatório completo da turma

### Para Pais/Responsáveis
- 👀 **Visualizar Frequência** - Acompanhe presença do seu filho(a)
- 📋 **Ver Atividades** - Confira o desempenho em tarefas
- 📚 **Consultar Conteúdo** - Veja o que está sendo ensinado
- 📄 **Enviar Atestados** - Justifique faltas com documentos
- ⏳ **Acompanhar Status** - Veja se atestado foi aprovado

## 📋 Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Clone ou copie o projeto

```bash
cd d:\PyCharm_Projetos\escola_app
```

### 2. Crie um ambiente virtual (opcional mas recomendado)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 🏃 Como Executar

### Inicie a aplicação

```bash
# Windows
python app.py

# Linux/Mac
python3 app.py
```

A aplicação estará disponível em: **http://localhost:5000**

## 🔐 Credenciais de Teste

### Professor
- **Usuário:** professor1
- **Senha:** 123456

### Pai/Responsável
- **Usuário:** pai_joao
- **Senha:** 123456

## 📱 Design Responsivo

A aplicação foi desenvolvida com Bootstrap 5 e é totalmente responsiva:
- ✅ Desktop (1920px+)
- ✅ Tablet (768px - 1024px)
- ✅ Mobile (até 768px)

## 🗂️ Estrutura do Projeto

```
escola_app/
├── app.py                 # Arquivo principal
├── credentials.json       # Credenciais Google (não commitir)
├── requirements.txt       # Dependências
├── README.md              # Este arquivo
├── templates/
│   ├── login.html
│   ├── base.html
│   ├── professor/
│   │   ├── dashboard.html
│   │   ├── frequencia.html
│   │   ├── conteudo.html
│   │   ├── atividades.html
│   │   ├── leitura.html
│   │   ├── atestados.html
│   │   └── relatorio.html
│   └── pais/
│       ├── dashboard.html
│       ├── atestado.html
│       ├── meus_atestados.html
│       └── conteudo.html
└── static/
    └── css/
        └── style.css

```

## 🔄 Fluxo de Atestado

1. **Pai/Responsável** envia atestado via formulário
2. **Status:** Pendente ⏳
3. **Professor** recebe notificação
4. **Professor** analisa e aprova/rejeita
5. **Status:** Aprovado ✅ ou Rejeitado ❌
6. **Pai** visualiza resultado no dashboard

## 🎨 Customização

### Cores
Edite as cores no `app.py` na seção de `<style>`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Logotipo
Substitua o emoji 📚 pelo seu logotipo em `templates/login.html`

### Nome da Escola
Altere "Sistema Escolar" em `templates/base.html`

## 📊 Funcionalidades Futuras

- [ ] Integração com WhatsApp para notificações
- [ ] Aplicativo mobile nativo (React Native)
- [ ] Avaliações numéricas e conceituais
- [ ] Chat entre professor e responsáveis
- [ ] Relatório PDF automático
- [ ] Backup automático no Drive
- [ ] Múltiplas turmas por professor

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'flask'"
```bash
pip install flask gspread oauth2client
```

### Erro: "credentials.json não encontrado"
Certifique-se de que o arquivo está na pasta raiz do projeto e o nome está correto.

### Erro ao conectar Google Sheets
Verifique se:
1. Seu arquivo `credentials.json` é válido
2. A planilha se chama exatamente "Sistema_Frequencia_Escola"
3. Sua conta Google tem acesso à planilha

## 📧 Suporte

Para dúvidas ou problemas, verifique o arquivo `app.py` seção "# DECORADORES" para entender a lógica de permissões.

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente para fins educacionais.

---

**Desenvolvido com ❤️ para educadores**

---

## Protótipo Web HTML, CSS e JavaScript do SOE Rosa Romita

Também há uma versão front-end estática criada em `index.html`, `styles.css` e `script.js` para demonstrar o Serviço de Orientação Escolar da escola Rosa Romita sem depender de backend durante a avaliação inicial.

### Como abrir

1. Abra `index.html` diretamente no navegador; ou
2. Execute um servidor local simples:

```bash
python3 -m http.server 8000
```

Depois acesse `http://localhost:8000`.

### Contas de demonstração

Todas usam a senha `123456`:

- `representante@rosaromita.edu.br` — aluno representante com acesso restrito à turma 7A.
- `responsavel@rosaromita.edu.br` — responsável com acesso apenas aos filhos vinculados.
- `professor@rosaromita.edu.br` — professor com acesso às turmas 7A e 8B, documentos e contatos.
- `coordenacao@rosaromita.edu.br` — coordenador SOE com acesso administrativo completo.

### Observação de produção

O protótipo usa `localStorage` para simular autenticação, permissões, anexos e cadastros. Para produção, substitua essa camada por Firebase Auth + Firestore/Storage Rules ou Node.js + MongoDB com criptografia, auditoria e políticas de acesso aderentes à LGPD.
