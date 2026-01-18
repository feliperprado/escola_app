# GUIA: Como Configurar o Google Sheets

## 📋 Passo a Passo

### 1. Crie um Projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Crie um novo projeto
3. Nome sugerido: "Sistema de Frequência Escolar"

### 2. Ative as APIs Necessárias

1. No menu lateral, vá para "APIs e Serviços"
2. Clique em "Ativar APIs e Serviços"
3. Procure e ative:
   - Google Sheets API
   - Google Drive API

### 3. Crie uma Credencial de Conta de Serviço

1. Vá para "Credenciais" no menu lateral
2. Clique em "Criar Credenciais"
3. Escolha "Conta de Serviço"
4. Preencha os dados
5. Clique em "Continuar"
6. Pule a etapa de roles (opcional)
7. Finalize

### 4. Gere a Chave JSON

1. Volte para "Credenciais"
2. Abra a conta de serviço criada
3. Vá para a aba "Chaves"
4. Clique em "Adicionar Chave" → "Criar nova chave"
5. Escolha "JSON"
6. Baixe o arquivo (será chamado algo como `project-key.json`)
7. Renomeie para `credentials.json`
8. Coloque na pasta raiz do projeto

### 5. Crie a Planilha no Google Sheets

1. Acesse: https://sheets.google.com
2. Crie uma nova planilha
3. Renomeie para exatamente: **"Sistema_Frequencia_Escola"**

### 6. Compartilhe a Planilha com a Conta de Serviço

1. No arquivo `credentials.json`, procure por `"client_email"`
2. Copie esse email (ex: `seu-projeto@seu-projeto.iam.gserviceaccount.com`)
3. Na planilha, clique em "Compartilhar"
4. Cole o email e dê permissão de editor

### 7. Crie as Abas (Sheets) e Estruture os Dados

#### Aba 1: Usuarios

| usuario | senha | tipo | turma | aluno_id |
|---------|-------|------|-------|----------|
| professor1 | 123456 | professor | 5A | - |
| professor2 | 123456 | professor | 5B | - |
| pai_joao | 123456 | pais | - | aluno_001 |
| pai_maria | 123456 | pais | - | aluno_002 |

#### Aba 2: Alunos

| id | nome | turma | responsavel | email | telefone |
|----|------|-------|-------------|-------|----------|
| aluno_001 | João Silva | 5A | Maria Silva | maria@email.com | (11) 99999-9999 |
| aluno_002 | Maria Santos | 5A | João Santos | joao@email.com | (11) 88888-8888 |
| aluno_003 | Pedro Costa | 5B | Ana Costa | ana@email.com | (11) 77777-7777 |

#### Aba 3: Frequencia

| data | turma | aluno_id | status | hora |
|------|-------|----------|--------|------|
| 18/01/2024 | 5A | aluno_001 | Presente | 08:00:00 |
| 18/01/2024 | 5A | aluno_002 | Ausente | - |

#### Aba 4: Conteudo

| data | turma | materia | conteudo | professor |
|------|-------|---------|----------|-----------|
| 18/01/2024 15:30:00 | 5A | Matemática | Frações: conceito, tipos e operações | professor1 |
| 18/01/2024 14:00:00 | 5A | Português | Acentuação gráfica | professor1 |

#### Aba 5: Atividades

| data | turma | aluno_id | atividade | status | data_entrega |
|------|-------|----------|-----------|--------|--------------|
| 18/01/2024 | 5A | aluno_001 | Exercícios cap. 5 | Feito | 20/01/2024 |
| 18/01/2024 | 5A | aluno_002 | Exercícios cap. 5 | Não fez | 20/01/2024 |

#### Aba 6: Leitura

| data | turma | aluno_id | livro | paginas | status |
|------|-------|----------|-------|---------|--------|
| 18/01/2024 | 5A | aluno_001 | O Pequeno Príncipe | 10-15 | Sim |
| 18/01/2024 | 5A | aluno_002 | O Pequeno Príncipe | 10-15 | Não |

#### Aba 7: Atestados

| aluno_id | responsavel | data_falta | motivo | status | documento | data_envio |
|----------|-------------|----------|--------|--------|-----------|-----------|
| aluno_001 | Maria Silva | 15/01/2024 | Doença | Pendente | Atestado médico anexado | 16/01/2024 15:30:00 |

## ✅ Pronto!

Agora sua aplicação deve conectar automaticamente ao Google Sheets e sincronizar todos os dados.

## 🔒 Segurança

- ⚠️ **NUNCA** compartilhe o arquivo `credentials.json` no GitHub
- ⚠️ **NUNCA** revele seu email de conta de serviço
- ✅ Adicione `credentials.json` ao `.gitignore`

## 🆘 Troubleshooting

**Erro: "Unauthorized"**
- Verifique se o email da conta de serviço está no compartilhamento

**Erro: "Worksheet not found"**
- Certifique-se que o nome das abas está exatamente como especificado

**Erro: "Authentication failed"**
- Verifique se o arquivo `credentials.json` é válido

---

Dúvidas? Consulte a documentação oficial do gspread: https://docs.gspread.org/
