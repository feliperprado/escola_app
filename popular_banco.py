#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para popular o banco de dados com dados iniciais
Execute uma única vez para criar usuários e alunos de teste
"""

from app import app, db, Usuario, Aluno
from datetime import datetime

def popular_banco():
    """Popula o banco de dados com dados iniciais"""
    
    with app.app_context():
        print("\n" + "="*60)
        print("  POPULADOR DE BANCO DE DADOS")
        print("="*60 + "\n")
        
        # Verificar se já existem dados
        if Usuario.query.first():
            print("⚠ Banco de dados já contém dados!")
            resposta = input("Deseja limpar e recriar? (s/n): ").lower()
            if resposta == 's':
                db.drop_all()
                db.create_all()
                print("✓ Banco de dados limpo")
            else:
                print("Operação cancelada")
                return
        
        # Criar usuários
        print("\n👤 Criando usuários...")
        
        usuarios = [
            Usuario(usuario='professor1', senha='123456', tipo='professor', turma='5A'),
            Usuario(usuario='professor2', senha='123456', tipo='professor', turma='5B'),
            Usuario(usuario='pai_joao', senha='123456', tipo='pais', aluno_id='aluno_001'),
            Usuario(usuario='pai_maria', senha='123456', tipo='pais', aluno_id='aluno_002'),
        ]
        
        for user in usuarios:
            db.session.add(user)
            print(f"  ✓ {user.usuario} ({user.tipo})")
        
        db.session.commit()
        
        # Criar alunos
        print("\n👨‍🎓 Criando alunos...")
        
        alunos = [
            Aluno(
                aluno_id='aluno_001',
                nome='João Silva',
                turma='5A',
                responsavel='Maria Silva',
                email='maria@email.com',
                telefone='(11) 99999-9999'
            ),
            Aluno(
                aluno_id='aluno_002',
                nome='Maria Santos',
                turma='5A',
                responsavel='João Santos',
                email='joao@email.com',
                telefone='(11) 88888-8888'
            ),
            Aluno(
                aluno_id='aluno_003',
                nome='Pedro Costa',
                turma='5A',
                responsavel='Ana Costa',
                email='ana@email.com',
                telefone='(11) 77777-7777'
            ),
            Aluno(
                aluno_id='aluno_004',
                nome='Carlos Oliveira',
                turma='5B',
                responsavel='Roberto Oliveira',
                email='roberto@email.com',
                telefone='(11) 66666-6666'
            ),
            Aluno(
                aluno_id='aluno_005',
                nome='Ana Ferreira',
                turma='5B',
                responsavel='Lucia Ferreira',
                email='lucia@email.com',
                telefone='(11) 55555-5555'
            ),
        ]
        
        for aluno in alunos:
            db.session.add(aluno)
            print(f"  ✓ {aluno.nome} ({aluno.turma})")
        
        db.session.commit()
        
        print("\n" + "="*60)
        print("  ✓ Banco de dados populado com sucesso!")
        print("="*60)
        
        print("\n📝 Credenciais de teste:\n")
        print("👨‍🏫 PROFESSOR:")
        print("  Usuário: professor1")
        print("  Senha: 123456")
        print("  Turma: 5A")
        
        print("\n👨‍👩‍👧 PAI/RESPONSÁVEL:")
        print("  Usuário: pai_joao")
        print("  Senha: 123456")
        print("  Filho: João Silva")
        
        print("\n🌐 Acesse a aplicação em:")
        print("  http://localhost:5000\n")

if __name__ == '__main__':
    popular_banco()
