import os
import re
import sys
import time

from dotenv import load_dotenv
import requests
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.status import Status

# Constantes de configuração
API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "deepseek-r1-distill-qwen-1.5b"
TEMPERATURE = 0.7
THINK_PATTERN = r'(<think>)(.*?)(</think>)'


def separar_think(texto: str) -> tuple[str, str]:
    """
    Extrai o conteúdo entre <think>...</think> e retorna uma tupla
    (texto_do_pensamento, restante_do_texto).

    Se não houver marcação <think>, retorna ('[sem pensamento]', texto).
    """
    match = re.search(THINK_PATTERN, texto, re.DOTALL)

    if not match:
        return '[sem pensamento]', texto.strip()

    conteudo = match.group(2).strip() or '[sem pensamento]'
    resto = texto.replace(match.group(0), '').strip()
    return conteudo, resto


def carregar_api_key() -> str:
    """
    Carrega a chave de API do ambiente usando python-dotenv.
    """
    load_dotenv()
    api_key = os.getenv('API_KEY')
    return api_key


def criar_headers(api_key: str) -> dict[str, str]:
    """
    Monta o header de autorização para as requisições.
    """
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }


def main() -> None:
    """
    Loop principal de interação com o usuário.
    """
    console = Console()
    api_key = carregar_api_key()
    headers = criar_headers(api_key)

    console.print(
        "🤖 [bold blue]IA pronta para conversar![/bold blue] "
        "Digite 'sair' para encerrar.\n"
    )

    # Inicializa histórico com instrução de sistema
    chat_history: list[dict[str, str]] = [
        {
            'role': 'system',
            'content': (
                'Responda sempre em português do Brasil'
            )
        }
    ]

    while True:
        user_input = console.input('[bold cyan]Você:[/bold cyan] ').strip()
        if user_input.lower() in ('sair', 'exit', 'quit'):
            console.print('[bold green]Encerrando a conversa. Até logo![/bold green]')
            break

        chat_history.append({'role': 'user', 'content': user_input})

        payload = {
            'model': MODEL_NAME,
            'messages': chat_history,
            'temperature': TEMPERATURE
        }

        with console.status('[bold yellow]Pensando...[/bold yellow]',
                             spinner='dots'):
            try:
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                assistant_msg = response.json()['choices'][0]['message']['content']
                assistant_msg = assistant_msg.strip()

            except requests.RequestException as error:
                console.print(f'[bold red]Erro ao se comunicar com a IA:[/bold red] {error}')
                continue

        chat_history.append({'role': 'assistant', 'content': assistant_msg})

        think_text, rest_text = separar_think(assistant_msg)

        if think_text != '[sem pensamento]':
            console.print(Panel(think_text, title='Think', style='yellow'))
            time.sleep(1)  # Pausa de 2 segundos antes da resposta

        console.print(Panel(Markdown(rest_text), title='IA', style='bold blue'))


if __name__ == '__main__':
    main()
