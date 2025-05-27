# Carrega variáveis de ambiente e define chave da API
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

model_ia = 'llama3-70b-8192'

GROQ_API = os.getenv("GROQ_API")
if not GROQ_API:
    raise ValueError("Erro: A variável 'GROQ_API' não foi encontrada. Verifique o arquivo .env.")
os.environ["GROQ_API_KEY"] = GROQ_API

# Bibliotecas LangChain
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import YoutubeLoader, PyPDFLoader
from youtube_transcript_api import TranscriptsDisabled, NoTranscriptFound
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document

# Extras para scraping direto
import requests
from bs4 import BeautifulSoup

# Utilitários
def status(msg, tipo='info'):
    icones = {
        'info': '🔄',
        'ok': '✅',
        'erro': '❌',
        'aviso': '⚠️'
    }
    print(f"{icones.get(tipo, '')} {msg}")

def url_valida(url):
    return url.startswith("http://") or url.startswith("https://")

def menu_principal():
    print("\n" + "="*60)
    print("🤖  Bem-vindo ao AsimoBot — Seu assistente inteligente!")
    print("="*60)
    print("Escolha uma fonte de conhecimento:")
    print("  [1] 🌐 Site da Web")
    print("  [2] 📄 Arquivo PDF")
    print("  [3] 🎥 Vídeo do YouTube")
    print("-"*60)

# Instancia modelo
chat = ChatGroq(model=model_ia)

# Geração de resposta
def resposta_bot(mensagens, documento):
    system_message = '''Você é um assistente amigável chamado Asimo.
Você utiliza as seguintes informações para formular as suas respostas, e sempre responde de forma sucinta e compacta: {informacoes}'''
    mensagens_modelo = [('system', system_message)]
    mensagens_modelo += mensagens

    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({'informacoes': documento}).content

def resumir_documento(texto, modelo_chat, tam_chunk=1000, sobreposicao=100):
    status("Resumindo o conteúdo antes do envio ao modelo...", "info")
    splitter = RecursiveCharacterTextSplitter(chunk_size=tam_chunk, chunk_overlap=sobreposicao)
    partes = splitter.create_documents([texto])

    # O LangChain espera uma lista de Document
    partes_docs = [Document(page_content=parte.page_content) for parte in partes]

    try:
        chain = load_summarize_chain(modelo_chat, chain_type="map_reduce")
        resumo = chain.run(partes_docs)
        return resumo
    except Exception as e:
        status(f"Erro ao resumir conteúdo: {e}", "erro")
        return texto  # Fallback: retorna o original

# NOVA função carrega_site usando BeautifulSoup puro
def carrega_site():
    url_site = input('Digite a URL do site: ')
    if not url_valida(url_site):
        status("URL inválida. Tente novamente com http(s)://...", "erro")
        return None
    try:
        headers = {
            "User-Agent": os.getenv("USER_AGENT") or "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url_site, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove elementos inúteis
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()

        # Foca em conteúdo central
        main_content = soup.find('main') or soup.find('article') or soup.body
        tags = main_content.find_all(['h1', 'h2', 'h3', 'p', 'li']) if main_content else []

        texto_extraido = '\n'.join(tag.get_text(strip=True) for tag in tags if tag.get_text(strip=True))

        print("\n🧪 DEBUG: Conteúdo extraído com BeautifulSoup filtrado:")
        print(texto_extraido[:1000])

        if not texto_extraido.strip():
            status("Nenhum conteúdo textual válido foi encontrado na página.", "aviso")
            return None

        return texto_extraido[:3000]  # Limita ainda mais para evitar tokens excessivos

    except Exception as e:
        status(f"Erro ao carregar o site: {e}", "erro")
        return None

# Carregamento de PDF
def carrega_pdf(caminho=None):
    if not caminho:
        caminho = input("Digite o caminho do arquivo PDF (ou pressione Enter para usar 'Plano de Estudos - Python_25.pdf'): ").strip()
        if caminho == '':
            caminho = 'Plano de Estudos - Python_25.pdf'

    if not os.path.exists(caminho):
        status(f"Arquivo '{caminho}' não encontrado. Verifique o nome e tente novamente.", "erro")
        return None
    try:
        loader = PyPDFLoader(caminho)
        lista_documentos = loader.load()
        documento = ''.join([doc.page_content for doc in lista_documentos if doc.page_content.strip()])
        if not documento:
            status("Nenhum conteúdo válido foi extraído do PDF.", "aviso")
            return None
        return documento
    except Exception as e:
        status(f"Erro ao carregar o PDF: {e}", "erro")
        return None

# Carregamento de YouTube
def carrega_youtube():
    url_youtube = input('Digite a URL do Youtube: ')
    try:
        loader = YoutubeLoader.from_youtube_url(url_youtube, language=["pt", "pt-BR", "en"])
        lista_documentos = loader.load()
        if not lista_documentos or not any(doc.page_content.strip() for doc in lista_documentos):
            status("Nenhuma legenda válida foi encontrada para esse vídeo.", "aviso")
            return None
        documento = ''.join([doc.page_content for doc in lista_documentos])
        return documento
    except (TranscriptsDisabled, NoTranscriptFound):
        status("Este vídeo não possui legendas disponíveis.", "aviso")
        return None
    except Exception as e:
        status(f"Erro ao carregar o vídeo: {e}", "erro")
        return None

# Seleção da fonte
documento = None
while not documento:
    menu_principal()
    selecao = input("Digite sua opção (1, 2 ou 3): ")
    if selecao == '1':
        status("Carregando dados do site...", "info")
        documento = carrega_site()
    elif selecao == '2':
        status("Carregando dados do PDF...", "info")
        documento = carrega_pdf()
    elif selecao == '3':
        status("Carregando dados do vídeo...", "info")
        documento = carrega_youtube()
    else:
        status("Opção inválida. Tente novamente!", "erro")

# Se carregou com sucesso, tenta resumir
if documento:
    documento = resumir_documento(documento, chat)

# Início do chat
mensagens = []
historico = []

while True:
    pergunta = input("Usuário: ")
    if pergunta.lower() == 'x':
        break
    mensagens.append(('user', pergunta))
    resposta = resposta_bot(mensagens, documento)
    mensagens.append(('assistant', resposta))
    historico.append({'usuario': pergunta, 'bot': resposta})
    print(f'Bot: {resposta}\n→ Pergunte mais ou digite "x" para sair.')

# Salvamento do histórico
data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nome_arquivo = f"historico_asimobot_{data_hora}.json"

try:
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)
    status(f"Histórico salvo com sucesso em: {nome_arquivo}", "ok")
except Exception as e:
    status(f"Erro ao salvar o histórico: {e}", "erro")

print("Muito obrigado por usar o AsimoBot!")
