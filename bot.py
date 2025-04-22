import logging
from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import time 
import pandas as pd
import csv
import random

import scraping



load_dotenv()
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.chat_data)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"I'm a bot, please talk to me! {context.args[1]}"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    await context.bot.send_photo(update.effective_chat.id,photo='https://thispersondoesnotexist.com/')


async def salvar_palavra_nova(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    palavra = context.args[0]
    context.user_data['palavra'] = palavra
    selector_significado = 'div.def'  
    selector_nivel= 'span.def-info'  
    arquivo_saida = './dados/significados.csv'

    dados = scraping.scrape_significado_palavra(palavra, selector_significado, selector_nivel)
    scraping.save_to_csv(dados, arquivo_saida)

    seletor_css = 'div.examp'  
    seletor_css_hidden_examples = 'li.eg'  
    selector_nivel= 'span.def-info' 
    arquivo_saida = './dados/exemplos.csv'


    dados = scraping.scrape_significado_palavra(palavra, seletor_css, selector_nivel)
    scraping.save_to_csv(dados, arquivo_saida)

    dados = scraping.scrape_significado_palavra(palavra, seletor_css_hidden_examples, selector_nivel)
    scraping.save_to_csv(dados, arquivo_saida)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"O termo '{palavra}' foi salvo com sucesso")
    

async def mostrar_palavra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    arquivo_saida = './dados/significados.csv'
    with open(arquivo_saida, 'r') as file:
        reader = csv.reader(file)
        lines = list(reader)
        palavra_escolhida = random.choice(lines)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{palavra_escolhida}")


def main():
    """Função principal que define o bot."""
    # Token fornecido pelo BotFather
    TOKEN = TELEGRAM_API_KEY

    # Obter o dispatcher para registrar os manipuladores
    application = ApplicationBuilder().token(TOKEN).build()


    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    echo_handler = CommandHandler('echo', echo)
    salvar_palavra_nova_handler = CommandHandler('salvar', salvar_palavra_nova)
    mostrar_palavra_handler = CommandHandler('mostrar', mostrar_palavra)

    # Diferentes manipuladores para diferentes comandos
    application.add_handler(echo_handler)
    application.add_handler(salvar_palavra_nova_handler)
    application.add_handler(mostrar_palavra_handler)

    application.run_polling()
    
if __name__ == '__main__':
    main()
