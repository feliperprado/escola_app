#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de teste para validar a estrutura do Sistema de Frequência Escolar
Verifica se todos os arquivos e pastas estão no lugar correto
"""

import os
import sys

def verificar_estrutura():
    """Verifica se a estrutura do projeto está correta"""
    
    print("\n" + "="*60)
    print("  VERIFICADOR DE ESTRUTURA - Sistema Frequência Escolar")
    print("="*60 + "\n")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Arquivos necessários na raiz
    arquivos_raiz = [
        'app.py',
        'requirements.txt',
        'README.md',
        'SETUP_GOOGLE_SHEETS.md'
    ]
    
    # Pastas necessárias
    pastas = [
        'templates',
        'templates/professor',
        'templates/pais',
        'static',
        'static/css',
        'static/js'
    ]
    
    # Arquivos nos templates
    templates_base = [
        'templates/login.html',
        'templates/base.html',
        'templates/erro.html'
    ]
    
    templates_prof = [
        'templates/professor/dashboard.html',
        'templates/professor/frequencia.html',
        'templates/professor/conteudo.html',
        'templates/professor/atividades.html',
        'templates/professor/leitura.html',
        'templates/professor/atestados.html',
        'templates/professor/relatorio.html'
    ]
    
    templates_pais = [
        'templates/pais/dashboard.html',
        'templates/pais/atestado.html',
        'templates/pais/meus_atestados.html',
        'templates/pais/conteudo.html'
    ]
    
    # Verificar arquivos na raiz
    print("📁 Verificando arquivos na raiz...")
    for arquivo in arquivos_raiz:
        caminho = os.path.join(base_dir, arquivo)
        if os.path.exists(caminho):
            print(f"  ✓ {arquivo}")
        else:
            print(f"  ✗ {arquivo} - NÃO ENCONTRADO")
    
    # Verificar pastas
    print("\n📁 Verificando pastas...")
    for pasta in pastas:
        caminho = os.path.join(base_dir, pasta)
        if os.path.exists(caminho) and os.path.isdir(caminho):
            print(f"  ✓ {pasta}/")
        else:
            print(f"  ✗ {pasta}/ - NÃO ENCONTRADA")
    
    # Verificar templates base
    print("\n📄 Verificando templates base...")
    for arquivo in templates_base:
        caminho = os.path.join(base_dir, arquivo)
        if os.path.exists(caminho):
            print(f"  ✓ {arquivo}")
        else:
            print(f"  ✗ {arquivo} - NÃO ENCONTRADO")
    
    # Verificar templates professor
    print("\n👨‍🏫 Verificando templates do professor...")
    for arquivo in templates_prof:
        caminho = os.path.join(base_dir, arquivo)
        if os.path.exists(caminho):
            print(f"  ✓ {arquivo}")
        else:
            print(f"  ✗ {arquivo} - NÃO ENCONTRADO")
    
    # Verificar templates pais
    print("\n👨‍👩‍👧 Verificando templates dos pais...")
    for arquivo in templates_pais:
        caminho = os.path.join(base_dir, arquivo)
        if os.path.exists(caminho):
            print(f"  ✓ {arquivo}")
        else:
            print(f"  ✗ {arquivo} - NÃO ENCONTRADO")
    
    # Verificar dependências
    print("\n📦 Verificando dependências...")
    try:
        import flask
        print(f"  ✓ Flask {flask.__version__}")
    except ImportError:
        print(f"  ✗ Flask - NÃO INSTALADO")
    
    try:
        import gspread
        print(f"  ✓ gspread {gspread.__version__}")
    except ImportError:
        print(f"  ✗ gspread - NÃO INSTALADO")
    
    try:
        import oauth2client
        print(f"  ✓ oauth2client")
    except ImportError:
        print(f"  ✗ oauth2client - NÃO INSTALADO")
    
    # Verificar credentials.json
    print("\n🔐 Verificando credenciais...")
    credentials_path = os.path.join(base_dir, 'credentials.json')
    if os.path.exists(credentials_path):
        print(f"  ✓ credentials.json encontrado")
    else:
        print(f"  ⚠ credentials.json - NÃO ENCONTRADO")
        print(f"    Siga o guia em SETUP_GOOGLE_SHEETS.md para configurar")
    
    print("\n" + "="*60)
    print("  Verificação concluída!")
    print("="*60 + "\n")

if __name__ == '__main__':
    verificar_estrutura()
