import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from pathlib import Path
import os

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def config_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--start-maximized',  # --window-size=500,500'
                 '--incognito']  # ,'--headless'
    for argument in arguments:
        chrome_options.add_argument(argument)
        # inicializando o webdriver
    chrome_options.add_experimental_option('prefs', {
        # Desabilitar notificações
        'profile.default_content_setting_values.notifications': 2
    })
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def scrape_product_info():
    try:
        url = 'https://iqsinais.com/candles'
        driver = config_driver()

        data_formatada = datetime.now().strftime('%d/%m/%Y')

        # Inicializa um DataFrame vazio
        driver.get(url)
        time.sleep(2)  # Aguarda o carregamento da página
        driver.find_element(By.ID, 'date').send_keys(data_formatada)
        driver.find_element(By.ID, 'gale').send_keys('2G')
        driver.find_element(By.ID, 'data_candles').send_keys(
            'EURUSD 10:00 CALL\nEURUSD 10:06 CALL\nEURUSD 10:10 CALL\nEURUSD 10:12 PUT\nEURUSD 10:15 PUT')
        driver.execute_script("document.body.style.zoom='50%'")
        time.sleep(2)
        driver.find_element(By.ID, 'get_candles').click()
        time.sleep(2)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.find_element(By.ID, 'button_modal').click()
        time.sleep(2)
        texto = driver.find_element(By.ID, 'text_export').text

        return texto

    except Exception as e:
        return f"Erro na busca dos dados: {e}"


def export_file(texto):
    try:
        # Definando pasta download
        home = str(Path.home())
        downloads_path = os.path.join(home, 'Downloads', 'Nova_pasta')
       # Criar diretório se não existir
        os.makedirs(downloads_path, exist_ok=True)

        # Gerar nome do arquivo com data/hora
        data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"sinais_{data_hora}.txt"

        caminho_completo = os.path.join(downloads_path, nome_arquivo)

        # Processar o conteúdo para melhor formatação
        linhas = texto.split('\n')
        conteudo_formatado = "\n".join(
            [linha.strip() for linha in linhas if linha.strip()])

        # Salvar em arquivo
        with open(caminho_completo, 'w', encoding='utf-8') as arquivo:
            arquivo.write("=== RELATÓRIO DE SINAIS ===\n\n")
            arquivo.write(conteudo_formatado)
            arquivo.write("\n\nArquivo gerado em: " +
                          datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        return caminho_completo
    except Exception as e:
        return f"Erro na busca dos dados: {e}"


if __name__ == "__main__":
    # Exemplo de uso
    texto = scrape_product_info()
    caminho_salvo = export_file(texto)
    print(f"Arquivo salvo com sucesso em: {caminho_salvo}")
