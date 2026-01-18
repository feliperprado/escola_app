from flask import Flask, render_template, request, redirect, session, jsonify, flash
from functools import wraps
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_muito_segura_2024"

# Configuração do SQLite (banco de dados local)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print("✓ Banco de dados SQLite configurado")

# ====== MODELOS DO BANCO DE DADOS ======

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # professor, pais
    turma = db.Column(db.String(50))
    aluno_id = db.Column(db.String(50))

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    responsavel = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))

class Frequencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    aluno_id = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Presente, Ausente
    hora = db.Column(db.String(10))

class Conteudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(50), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    professor = db.Column(db.String(100))

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    aluno_id = db.Column(db.String(50), nullable=False)
    atividade = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Feito, Não fez
    data_entrega = db.Column(db.String(20))

class Leitura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    aluno_id = db.Column(db.String(50), nullable=False)
    livro = db.Column(db.String(100), nullable=False)
    paginas = db.Column(db.String(100))
    status = db.Column(db.String(10), nullable=False)  # Sim, Não

class Atestado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.String(50), nullable=False)
    responsavel = db.Column(db.String(100))
    data_falta = db.Column(db.String(20), nullable=False)
    motivo = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pendente')  # Pendente, Aprovado, Rejeitado
    documento = db.Column(db.Text)
    data_envio = db.Column(db.String(50), nullable=False)

# Criar tabelas se não existirem
with app.app_context():
    db.create_all()
    print("✓ Tabelas de banco de dados criadas")

# ====== DECORADORES DE AUTENTICAÇÃO ======

def login_required(f):
    """Requer que o usuário esteja autenticado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa fazer login primeiro', 'warning')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def professor_required(f):
    """Requer que o usuário seja professor ou operador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('tipo_usuario') not in ['professor', 'operador']:
            flash('Acesso restrito a professores', 'danger')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def pais_required(f):
    """Requer que o usuário seja pai/responsável"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('tipo_usuario') != 'pais':
            flash('Acesso restrito a pais/responsáveis', 'danger')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

# ====== FUNÇÕES AUXILIARES ======

def get_usuarios():
    """Retorna dicionário de usuários do banco de dados"""
    usuarios = Usuario.query.all()
    usuarios_dict = {}
    for user in usuarios:
        usuarios_dict[user.usuario] = {
            'senha': user.senha,
            'tipo': user.tipo,
            'turma': user.turma,
            'aluno_id': user.aluno_id
        }
    return usuarios_dict

def get_alunos_turma(turma):
    """Retorna alunos de uma turma"""
    alunos = Aluno.query.filter_by(turma=turma).all()
    alunos_list = []
    for aluno in alunos:
        alunos_list.append({
            'id': aluno.aluno_id,
            'nome': aluno.nome,
            'turma': aluno.turma,
            'responsavel': aluno.responsavel,
            'email': aluno.email,
            'telefone': aluno.telefone
        })
    return alunos_list

def registrar_frequencia(data, turma, aluno_id, status):
    """Registra frequência do aluno"""
    try:
        freq = Frequencia(
            data=data,
            turma=turma,
            aluno_id=aluno_id,
            status=status,
            hora=datetime.now().strftime("%H:%M:%S")
        )
        db.session.add(freq)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Erro ao registrar frequência: {e}")
        return False

def get_frequencia_aluno(aluno_id):
    """Retorna frequência de um aluno"""
    frequencias = Frequencia.query.filter_by(aluno_id=aluno_id).order_by(Frequencia.data.desc()).all()
    freq_list = []
    for freq in frequencias:
        freq_list.append({
            'data': freq.data,
            'status': freq.status
        })
    return freq_list

def get_atividades_aluno(aluno_id):
    """Retorna atividades de um aluno"""
    atividades = Atividade.query.filter_by(aluno_id=aluno_id).order_by(Atividade.data.desc()).all()
    ativ_list = []
    for ativ in atividades:
        ativ_list.append({
            'atividade': ativ.atividade,
            'status': ativ.status,
            'data': ativ.data
        })
    return ativ_list

# ====== ROTAS PÚBLICAS ======

@app.route('/')
def index():
    """Página de login"""
    if 'user_id' in session:
        if session.get('tipo_usuario') == 'pais':
            return redirect('/pais/dashboard')
        else:
            return redirect('/professor/dashboard')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Processa login do usuário"""
    usuario = request.form.get('usuario', '').strip()
    senha = request.form.get('senha', '').strip()
    
    if not usuario or not senha:
        flash('Usuário e senha são obrigatórios', 'danger')
        return redirect('/')
    
    usuarios = get_usuarios()
    
    if usuario in usuarios and usuarios[usuario]['senha'] == senha:
        session['user_id'] = usuario
        session['tipo_usuario'] = usuarios[usuario]['tipo']
        session['turma'] = usuarios[usuario].get('turma', '')
        
        if usuarios[usuario]['tipo'] == 'pais':
            session['aluno_id'] = usuarios[usuario].get('aluno_id', '')
            return redirect('/pais/dashboard')
        else:
            return redirect('/professor/dashboard')
    
    flash('Usuário ou senha incorretos', 'danger')
    return redirect('/')

@app.route('/logout')
def logout():
    """Faz logout do usuário"""
    session.clear()
    flash('Você foi desconectado com sucesso', 'success')
    return redirect('/')

# ====== ROTAS DO PROFESSOR ======

@app.route('/professor/dashboard')
@professor_required
def professor_dashboard():
    """Dashboard do professor"""
    turma = session.get('turma', '')
    alunos = get_alunos_turma(turma)
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    
    return render_template('professor/dashboard.html', 
                         alunos=alunos, 
                         turma=turma,
                         data_hoje=data_hoje)

@app.route('/professor/frequencia', methods=['GET', 'POST'])
@professor_required
def frequencia():
    """Gerenciador de frequência"""
    turma = session.get('turma', '')
    alunos = get_alunos_turma(turma)
    
    if request.method == 'POST':
        data = request.form.get('data', datetime.now().strftime("%d/%m/%Y"))
        
        for aluno in alunos:
            aluno_id = aluno.get('id', '')
            presente = request.form.get(f'frequencia_{aluno_id}') == 'presente'
            status = "Presente" if presente else "Ausente"
            registrar_frequencia(data, turma, aluno_id, status)
        
        flash('Frequência registrada com sucesso!', 'success')
        return redirect('/professor/frequencia')
    
    return render_template('professor/frequencia.html', alunos=alunos, turma=turma)

@app.route('/professor/conteudo', methods=['GET', 'POST'])
@professor_required
def conteudo():
    """Gerenciador de conteúdo de aulas"""
    if request.method == 'POST':
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        materia = request.form.get('materia', '')
        conteudo_texto = request.form.get('conteudo', '')
        turma = session.get('turma', '')
        
        try:
            cont = Conteudo(
                data=data,
                turma=turma,
                materia=materia,
                conteudo=conteudo_texto,
                professor=session['user_id']
            )
            db.session.add(cont)
            db.session.commit()
            flash('Conteúdo lançado com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao salvar conteúdo: {e}', 'danger')
        
        return redirect('/professor/conteudo')
    
    return render_template('professor/conteudo.html', turma=session.get('turma', ''))

@app.route('/professor/atividades', methods=['GET', 'POST'])
@professor_required
def atividades():
    """Gerenciador de atividades e tarefas"""
    turma = session.get('turma', '')
    alunos = get_alunos_turma(turma)
    
    if request.method == 'POST':
        atividade = request.form.get('atividade', '')
        data_entrega = request.form.get('data_entrega', '')
        
        for aluno in alunos:
            aluno_id = aluno.get('id', '')
            fez = request.form.get(f'atividade_{aluno_id}') == 'fez'
            status = "Feito" if fez else "Não fez"
            
            try:
                ativ = Atividade(
                    data=datetime.now().strftime("%d/%m/%Y"),
                    turma=turma,
                    aluno_id=aluno_id,
                    atividade=atividade,
                    status=status,
                    data_entrega=data_entrega
                )
                db.session.add(ativ)
            except Exception as e:
                print(f"Erro ao registrar atividade: {e}")
        
        db.session.commit()
        flash('Atividades registradas com sucesso!', 'success')
        return redirect('/professor/atividades')
    
    return render_template('professor/atividades.html', alunos=alunos, turma=turma)

@app.route('/professor/leitura', methods=['GET', 'POST'])
@professor_required
def leitura():
    """Registro de leitura diária"""
    turma = session.get('turma', '')
    alunos = get_alunos_turma(turma)
    
    if request.method == 'POST':
        livro = request.form.get('livro', '')
        paginas = request.form.get('paginas', '')
        
        for aluno in alunos:
            aluno_id = aluno.get('id', '')
            leu = request.form.get(f'leitura_{aluno_id}') == 'leu'
            status = "Sim" if leu else "Não"
            
            try:
                leit = Leitura(
                    data=datetime.now().strftime("%d/%m/%Y"),
                    turma=turma,
                    aluno_id=aluno_id,
                    livro=livro,
                    paginas=paginas,
                    status=status
                )
                db.session.add(leit)
            except Exception as e:
                print(f"Erro ao registrar leitura: {e}")
        
        db.session.commit()
        flash('Leitura registrada com sucesso!', 'success')
        return redirect('/professor/leitura')
    
    return render_template('professor/leitura.html', alunos=alunos, turma=turma)

@app.route('/professor/atestados')
@professor_required
def atestados():
    """Visualizar e gerenciar atestados"""
    atestados_list = Atestado.query.all()
    atestados_data = []
    for atestado in atestados_list:
        atestados_data.append({
            'id': atestado.id,
            'aluno_id': atestado.aluno_id,
            'responsavel': atestado.responsavel,
            'data_falta': atestado.data_falta,
            'motivo': atestado.motivo,
            'status': atestado.status,
            'documento': atestado.documento,
            'data_envio': atestado.data_envio
        })
    
    return render_template('professor/atestados.html', atestados=atestados_data)

@app.route('/professor/aprovar-atestado/<int:atestado_id>', methods=['POST'])
@professor_required
def aprovar_atestado(atestado_id):
    """Aprova um atestado"""
    try:
        atestado = Atestado.query.get(atestado_id)
        if atestado:
            atestado.status = "Aprovado"
            db.session.commit()
            flash('Atestado aprovado!', 'success')
        else:
            flash('Atestado não encontrado', 'danger')
    except Exception as e:
        flash(f'Erro ao aprovar: {e}', 'danger')
    
    return redirect('/professor/atestados')

@app.route('/professor/rejeitar-atestado/<int:atestado_id>', methods=['POST'])
@professor_required
def rejeitar_atestado(atestado_id):
    """Rejeita um atestado"""
    try:
        atestado = Atestado.query.get(atestado_id)
        if atestado:
            atestado.status = "Rejeitado"
            db.session.commit()
            flash('Atestado rejeitado!', 'success')
        else:
            flash('Atestado não encontrado', 'danger')
    except Exception as e:
        flash(f'Erro ao rejeitar: {e}', 'danger')
    
    return redirect('/professor/atestados')

@app.route('/professor/relatorio')
@professor_required
def relatorio():
    """Relatório completo da turma"""
    turma = session.get('turma', '')
    
    # Coletar dados de frequência
    frequencia = Frequencia.query.filter_by(turma=turma).all()
    frequencia_list = []
    for freq in frequencia:
        frequencia_list.append({
            'data': freq.data,
            'aluno_id': freq.aluno_id,
            'status': freq.status
        })
    
    # Coletar dados de atividades
    atividades = Atividade.query.filter_by(turma=turma).all()
    atividades_list = []
    for ativ in atividades:
        atividades_list.append({
            'data': ativ.data,
            'aluno_id': ativ.aluno_id,
            'atividade': ativ.atividade,
            'status': ativ.status,
            'data_entrega': ativ.data_entrega
        })
    
    alunos = get_alunos_turma(turma)
    
    return render_template('professor/relatorio.html', 
                         turma=turma,
                         alunos=alunos,
                         frequencia=frequencia_list,
                         atividades=atividades_list)

# ====== ROTAS DOS PAIS ======

@app.route('/pais/dashboard')
@pais_required
def pais_dashboard():
    """Dashboard do pai/responsável"""
    aluno_id = session.get('aluno_id', '')
    
    # Buscar dados do aluno
    aluno = Aluno.query.filter_by(aluno_id=aluno_id).first()
    aluno_data = {}
    if aluno:
        aluno_data = {
            'id': aluno.aluno_id,
            'nome': aluno.nome,
            'turma': aluno.turma,
            'responsavel': aluno.responsavel,
            'email': aluno.email,
            'telefone': aluno.telefone
        }
    
    # Buscar frequência do aluno
    frequencias = Frequencia.query.filter_by(aluno_id=aluno_id).order_by(Frequencia.data.desc()).limit(10).all()
    frequencia = []
    for freq in frequencias:
        frequencia.append({
            'data': freq.data,
            'status': freq.status
        })
    
    # Buscar atividades do aluno
    atividades = Atividade.query.filter_by(aluno_id=aluno_id).order_by(Atividade.data.desc()).limit(10).all()
    atividades_list = []
    for ativ in atividades:
        atividades_list.append({
            'atividade': ativ.atividade,
            'status': ativ.status,
            'data': ativ.data
        })
    
    return render_template('pais/dashboard.html',
                         aluno=aluno_data,
                         frequencia=frequencia,
                         atividades=atividades_list)

@app.route('/pais/atestado', methods=['GET', 'POST'])
@pais_required
def enviar_atestado():
    """Enviar atestado ou justificativa de falta"""
    if request.method == 'POST':
        data_falta = request.form.get('data_falta')
        motivo = request.form.get('motivo')
        documento = request.form.get('documento')
        aluno_id = session.get('aluno_id', '')
        
        try:
            atestado = Atestado(
                aluno_id=aluno_id,
                responsavel=session.get('user_id'),
                data_falta=data_falta,
                motivo=motivo,
                status="Pendente",
                documento=documento,
                data_envio=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            )
            db.session.add(atestado)
            db.session.commit()
            flash('Atestado enviado com sucesso! Aguarde aprovação do professor.', 'success')
            return redirect('/pais/dashboard')
        except Exception as e:
            flash(f'Erro ao enviar atestado: {e}', 'danger')
    
    return render_template('pais/atestado.html')

@app.route('/pais/meus-atestados')
@pais_required
def meus_atestados():
    """Ver status dos atestados enviados"""
    aluno_id = session.get('aluno_id', '')
    
    atestados = Atestado.query.filter_by(aluno_id=aluno_id).all()
    atestados_data = []
    for atestado in atestados:
        atestados_data.append({
            'id': atestado.id,
            'data_falta': atestado.data_falta,
            'motivo': atestado.motivo,
            'data_envio': atestado.data_envio,
            'status': atestado.status,
            'documento': atestado.documento
        })
    
    return render_template('pais/meus_atestados.html', atestados=atestados_data)

@app.route('/pais/conteudo')
@pais_required
def ver_conteudo():
    """Ver conteúdo de aulas da turma do aluno"""
    # Buscar turma do aluno
    aluno = Aluno.query.filter_by(aluno_id=session.get('aluno_id')).first()
    turma = aluno.turma if aluno else ""
    
    # Buscar conteúdos da turma
    conteudos = Conteudo.query.filter_by(turma=turma).order_by(Conteudo.data.desc()).all()
    conteudos_data = []
    for cont in conteudos:
        conteudos_data.append({
            'data': cont.data,
            'materia': cont.materia,
            'conteudo': cont.conteudo,
            'professor': cont.professor
        })
    
    return render_template('pais/conteudo.html', conteudos=conteudos_data)

# ====== TRATAMENTO DE ERROS ======

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template('erro.html', mensagem="Página não encontrada"), 404

@app.errorhandler(500)
def erro_servidor(error):
    return render_template('erro.html', mensagem="Erro no servidor"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
