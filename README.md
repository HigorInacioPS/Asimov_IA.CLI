# 🤖 ChatBot Multimodal com LangChain

Este projeto foi desenvolvido durante o curso da **Asimov Academy** por **Higor Inacio Pereira Sousa** e consiste em um **ChatBot multimodal** que opera no terminal, com capacidade de interagir com três tipos de fontes:

- 🌐 **Sites** (extração de conteúdo textual via URL)
- 📄 **PDFs** (extração de texto e análise)
- 📺 **Vídeos do YouTube** (por meio da transcrição automática)

## 🧠 Objetivo

Criar uma aplicação conversacional que use **modelos de linguagem (LLMs)** para interpretar perguntas do usuário e buscar respostas com base nas informações contidas nas fontes fornecidas.

## 💻 Execução

O projeto foi desenvolvido e testado no **Google Colaboratory**, mas pode ser adaptado para rodar localmente com as dependências corretas.

O chatbot opera via terminal. Para utilizá-lo:
1. Selecione a fonte de conhecimento (site, PDF ou vídeo do YouTube).
2. O conteúdo será carregado e processado.
3. O usuário poderá fazer perguntas com base nesse conteúdo.
4. O bot responde de forma contextualizada, simulando uma conversa inteligente.

## 🔐 Requisito: Chave de API da Groq

O projeto utiliza a API da **Groq** para se comunicar com o modelo de linguagem. Você deve obter uma chave de API gratuita no seguinte site:

👉 [https://console.groq.com/keys](https://console.groq.com/keys)

Após obtê-la, **insira sua chave na linha do código onde está indicado `sua_api_key`**.

## 📦 Bibliotecas Utilizadas

| Biblioteca                             | Finalidade                                                       |
|----------------------------------------|------------------------------------------------------------------|
| `langchain_community.document_loaders` | Leitura e carregamento de sites, PDFs e vídeos do YouTube       |
| `langchain.prompts`                    | Criação de prompts customizados                                 |
| `langchain_groq`                       | Integração com o modelo LLM da Groq                             |

> ✅ Recomenda-se utilizar **Python 3.12.3** para garantir compatibilidade com as bibliotecas.

## 🚀 Como Executar (Google Colab)

1. Faça upload do notebook `IA_Asimov.ipynb` para o Google Colab.
2. Instale as dependências com `!pip install` conforme descrito no notebook.
3. Insira sua chave da Groq na linha indicada.
4. Execute as células e interaja com o bot diretamente no terminal do Colab.

## ✍️ Autor

**Higor Inacio Pereira Sousa**

Projeto educacional com fins de aprendizado prático em Inteligência Artificial e Processamento de Linguagem Natural com LLMs.
