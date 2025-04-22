import requests
from bs4 import BeautifulSoup
import csv
import argparse


parser = argparse.ArgumentParser(description='Scrape significados e exemplos de palavras.')
parser.add_argument('--palavra', dest='palavra', type=str, help='Palavra a ser pesquisada')
args = parser.parse_args()

def scrape_significado_palavra(palavra, selector_significado, selector_nivel):
    """
    Faz requisição HTTP GET e extrai dados usando o seletor CSS informado.

    Args:
        url (str): URL da página a ser raspada.
        selector (str): Seletor CSS para localizar os elementos de interesse.

    Returns:
        list[dict]: Lista de dicionários com os dados extraídos.
    """

    headers = requests.utils.default_headers()

    headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (compatible; WebScraper/1.0)',
    }
    )

    url = f'https://dictionary.cambridge.org/pt/dicionario/ingles/{palavra}'

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # lança erro em caso de falha HTTP

    soup = BeautifulSoup(response.text, 'html.parser')
    
    nivel = soup.select_one(selector_nivel)
    nivel = nivel.get_text(strip=True, separator=" ")
    print(nivel)
    
    significados = soup.select(selector_significado)
    results = []
    for elem in significados:
        # Exemplo: extrair texto e link
        significado = elem.get_text(strip=True, separator=" ")
        results.append({'palavra': palavra, 'significado': significado, 'nivel': nivel})

    return results


def save_to_csv(data, output_file):
    """
    Salva lista de dicionários em arquivo CSV.

    Args:
        data (list[dict]): Dados a serem salvos.
        output_file (str): Caminho do arquivo CSV de saída.
    """
    if not data:
        print("Nenhum dado para salvar.")
        return
    

    # Não salvar o cabeçalho se o arquivo já existir
    fieldnames = list(data[0].keys())
    with open(output_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(data)


    print(f"Salvo {len(data)} registros em '{output_file}'")


#pegar o significado
palavra = args.palavra # Substitua pela palavra desejada
selector_significado = 'div.def'  # Substitua pelo seletor correto
selector_nivel= 'span.def-info'  # Substitua pelo seletor correto
arquivo_saida = './dados/significados.csv'

# Execução
dados = scrape_significado_palavra(palavra, selector_significado, selector_nivel)
save_to_csv(dados, arquivo_saida)

seletor_css = 'div.examp'  # Substitua pelo seletor correto
seletor_css_hidden_examples = 'li.eg'  # Substitua pelo seletor correto
selector_nivel= 'span.def-info' 
arquivo_saida = './dados/exemplos.csv'

# Execução
dados = scrape_significado_palavra(palavra, seletor_css, selector_nivel)
save_to_csv(dados, arquivo_saida)

dados = scrape_significado_palavra(palavra, seletor_css_hidden_examples, selector_nivel)
save_to_csv(dados, arquivo_saida)