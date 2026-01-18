# 📚 GUIA RÁPIDO DE USO - Sistema de Frequência Escolar

## 🚀 Início Rápido

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Configure Google Sheets
Siga o guia em `SETUP_GOOGLE_SHEETS.md`

### 3. Execute a aplicação
```bash
python app.py
```

Acesse: **http://localhost:5000**

---

## 👥 Tipos de Usuários

### 👨‍🏫 **PROFESSOR**
- Controlar frequência de alunos
- Lançar conteúdo de aulas
- Registrar atividades (quem fez/não fez)
- Acompanhar leitura diária
- Aprovar/rejeitar atestados
- Visualizar relatórios

**Credenciais de teste:**
- Usuário: `professor1`
- Senha: `123456`

### 👨‍👩‍👧 **PAI/RESPONSÁVEL**
- Visualizar frequência do filho(a)
- Acompanhar atividades
- Ver conteúdo de aulas
- Enviar atestados e justificativas
- Acompanhar status de atestados

**Credenciais de teste:**
- Usuário: `pai_joao`
- Senha: `123456`

---

## 📋 Principais Funcionalidades

### Para PROFESSOR

#### 1️⃣ Controle de Frequência
- Acesse: **Frequência**
- Selecione a data
- Marque presença/ausência de cada aluno
- Clique em "Salvar Frequência"

#### 2️⃣ Lançamento de Conteúdo
- Acesse: **Conteúdo**
- Informe a disciplina
- Descreva o conteúdo ensinado
- O sistema registra data/hora automaticamente

#### 3️⃣ Atividades e Tarefas
- Acesse: **Atividades**
- Descreva a atividade
- Defina data de entrega
- Marque quem fez/não fez
- Salve os dados

#### 4️⃣ Acompanhamento de Leitura
- Acesse: **Leitura**
- Defina o livro/material
- Indique as páginas lidas
- Marque quem leu/não leu

#### 5️⃣ Gerenciar Atestados
- Acesse: **Atestados**
- Veja atestados enviados pelos pais
- Aprove (falta justificada) ou rejeite (sem comprovação)

#### 6️⃣ Visualizar Relatórios
- Acesse: **Relatório**
- Veja resumo da turma
- Visualize frequência, atividades
- Imprima ou exporte relatório

---

### Para PAI/RESPONSÁVEL

#### 1️⃣ Acompanhar Frequência
- No **Dashboard** vê as últimas frequências
- Visualiza presença/ausência

#### 2️⃣ Enviar Atestado
- Clique em "Enviar Atestado"
- Informe a data da falta
- Selecione o motivo
- Descreva a situação ou cole dados do atestado médico
- Envie

#### 3️⃣ Acompanhar Status
- Acesse "Meus Atestados"
- Veja se foi: ⏳ Pendente, ✅ Aprovado ou ❌ Rejeitado

#### 4️⃣ Ver Conteúdo de Aulas
- Acesse "Conteúdo"
- Veja o que está sendo ensinado
- Acompanhe progresso do aprendizado

---

## 📊 Fluxo de Dados

```
┌─────────────────────────────────────────────┐
│     GOOGLE SHEETS (Drive Institucional)     │
│  ├─ Usuarios                                │
│  ├─ Alunos                                  │
│  ├─ Frequencia                              │
│  ├─ Conteudo                                │
│  ├─ Atividades                              │
│  ├─ Leitura                                 │
│  └─ Atestados                               │
└────────────────┬────────────────────────────┘
                 │
         ┌───────▼────────┐
         │  APLICAÇÃO     │
         │   FLASK        │
         │  (app.py)      │
         └───────┬────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼────┐  ┌───▼────┐  ┌───▼────┐
│Professor│  │  Pais  │  │ Móvel  │
│ Desktop │  │ Desktop│  │ (RWD)  │
└────────┘  └────────┘  └────────┘
```

---

## 🔐 Segurança

### Senhas Padrão
As credenciais de teste devem ser alteradas ANTES de usar em produção!

### Google Sheets
- Compartilhe a planilha apenas com o email da conta de serviço
- Mantenha o arquivo `credentials.json` seguro
- Adicione ao `.gitignore`

### Sessão
- A chave de sessão deve ser alterada em `app.py`
- Use uma senha forte e aleatória

---

## 🛠️ Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erro: "credentials.json not found"
```bash
# Baixe o arquivo JSON do Google Cloud Console
# Renomeie para: credentials.json
# Coloque na pasta raiz do projeto
```

### Erro: "Worksheet not found"
- Verifique se a planilha se chama exatamente: **"Sistema_Frequencia_Escola"**
- Verifique os nomes das abas (sheets)

### Erro: "Unauthorized"
- A conta de serviço não tem permissão na planilha
- Compartilhe a planilha com o email da conta de serviço

---

## 📱 Usando em Celular

A aplicação é **100% responsiva**:
1. Abra em um navegador: `http://[seu-ip]:5000`
2. Substitua `localhost` pelo IP do computador
3. Use normalmente no celular

### Dica para encontrar seu IP:
```bash
ipconfig  # Windows
ifconfig  # Linux/Mac
```

Procure por "IPv4 Address"

---

## 🎯 Próximas Melhorias

- [ ] App nativo para iOS/Android
- [ ] Notificações via WhatsApp
- [ ] Avaliações numéricas
- [ ] Chat professor-responsável
- [ ] Exportar PDF automático
- [ ] Backup automático no Drive
- [ ] Dark mode

---

## 📞 Suporte

Para dúvidas:
1. Consulte o `README.md`
2. Veja `SETUP_GOOGLE_SHEETS.md`
3. Verifique erros com: `python verificar_estrutura.py`

---

**Bom uso! 🎓**
