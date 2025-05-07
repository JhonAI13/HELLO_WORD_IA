# Hello Word IA
Este repositório contém um script Python que implementa um cliente de chat usando a biblioteca `requests` para comunicação com uma API de LLM local (via llmstudio) e `rich` para exibição estilizada no terminal. A lógica foca em extrair "pensamentos" (Think) e respostas finais da IA, tudo posicionado em português do Brasil.

---

## 🚀 Visão Geral
![Desmonstração](<arquivo/demonstração.gif>)

O script:

* Faz requisições HTTP para uma API de LLM rodando localmente em `http://127.0.0.1:1234/v1/chat/completions`.
* Mostra status de "Pensando..." e pausas entre pensamento e resposta.
* Separa marcações `<think>...</think>` do texto da IA, exibindo o pensamento em um painel distinto.
* Garante que todas as respostas sejam em Português do Brasil.

> ℹ️ **Observação**: A API está sendo executada localmente via llmstudio. Durante testes, o uso do português foi para forçar o uso do thinking da IA.

---

## 📋 Pré-requisitos

* Python 3.8+
* API Key armazenada em arquivo `.env` (variável `API_KEY`)
* llmstudio configurada e rodando localmente

## ⚙️ Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/JhonAI13/HELLO_WORD_IA
   cd HELLO_WORD_IA
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .\.venv\\Scripts\\activate  # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` na raiz do projeto com sua chave de API:

   ```env
   API_KEY=sua_chave_aqui
   ```

---

## 📂 Estrutura do Código

```
HELLO_WORD_IA.py       # Script principal
requirements.txt  # Dependências do projeto
.env.example      # Exemplo de arquivo de variáveis de ambiente
```

### Descrição das Funções

* **`separar_think(texto: str) -> tuple[str, str]`**

  * Extrai o conteúdo entre as tags `<think>...</think>`.
  * Retorna uma tupla `(pensamento, texto_restante)`. Se não houver tags, retorna `('[sem pensamento]', texto_original)`.

* **`carregar_api_key() -> str`**

  * Carrega a variável `API_KEY` do arquivo `.env` usando `python-dotenv`.

* **`criar_headers(api_key: str) -> dict[str, str]`**

  * Gera o cabeçalho HTTP para autenticação das requisições.

* **`main() -> None`**

  * Loop principal de interação:

    1. Lê entrada do usuário.
    2. Monta histórico de mensagens (incluindo instrução de sistema para PT-BR).
    3. Envia requisição POST para a API local.
    4. Processa resposta: exibe painel com pensamento e resposta formatada.

---

## ▶️ Uso

Execute o script:

```bash
python HELLO_WORD_IA.py
```

No terminal, digite suas mensagens; para sair, digite `sair`, `exit` ou `quit`.

---

## 📝 Arquivo `requirements.txt`

```txt
python-dotenv
requests
rich
```
