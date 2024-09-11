from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import Filters
import requests
from bs4 import BeautifulSoup
import logging

# Configure o logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Função de comando /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Olá! Eu sou um bot que busca artigos e notícias sobre teologia, evangélicos e misticismo no cristianismo. Use /buscar seguido de palavras-chave para iniciar uma pesquisa.')

# Função para realizar a busca com palavras-chave
def buscar(update: Update, context: CallbackContext) -> None:
    # Captura as palavras-chave do usuário
    query = ' '.join(context.args)

    # Verifica se palavras-chave foram fornecidas
    if not query:
        update.message.reply_text('Por favor, forneça palavras-chave para a busca. Exemplo: /buscar teologia cristianismo misticismo')
        return

    # Realiza a busca usando as palavras-chave
    url = f"https://www.google.com/search?q={query}+teologia+evangelical+comentários bíblicos+cristianismo+articles"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Processa e retorna os resultados
    results = []
    for g in soup.find_all('div', class_='g'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3')
            if title:
                title = title.text
                results.append(f"{title}\n{link}\n")

    # Envia os resultados ou uma mensagem de erro caso não encontre nada
    if results:
        update.message.reply_text('\n'.join(results[:5]))  # Limite de 10 resultados
    else:
        update.message.reply_text('Nenhum resultado encontrado.')

# Função principal
def main() -> None:
    # Insira seu token aqui
    TOKEN = '7033995712:AAHiJ-4PmAMFmbLlqS_WAmRm0klo3aD0yBI'

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Configura os comandos e mensagens
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("buscar", buscar))

    # Inicia o bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
