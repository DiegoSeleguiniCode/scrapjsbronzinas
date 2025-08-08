import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

categorias = [
    "BRONZINA MANCAL VW",
    "ARRUELA ENCOSTO",
    "BUCHA DE COMANDO",
    "BUCHAS CATERPILLAR",
    "BUCHA DE BIELA",
    "SEDES DE VÁLVULA",
    "BUCHA MANGA DE EIXO"
]

driver = webdriver.Chrome()
driver.get('https://www.jsbronzinas.com.br/categoria/categoria')
wait = WebDriverWait(driver, 10)
todos_produtos = []

for categoria in categorias:
    print(f"\nCategoria: {categoria}")
    select_element = wait.until(EC.presence_of_element_located((By.NAME, "cat")))
    select = Select(select_element)
    select.select_by_visible_text(categoria)
    time.sleep(0.5)
    buscar_btn = driver.find_element(By.XPATH, '//button[contains(text(), "buscar")]')
    buscar_btn.click()
    time.sleep(2)
    cards = driver.find_elements(By.CLASS_NAME, "service")
    if not cards:
        print("Nenhum produto encontrado para esta categoria.")
    for card in cards:
        try:
            nome = card.find_element(By.CLASS_NAME, "text-center").text
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            # Abre o link do produto em uma nova aba
            driver.execute_script("window.open(arguments[0], '_blank');", link)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1.2)

            # Busca a div col-md-5 ml-auto (descrição+infos)
            try:
                desc_div = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "col-md-5") and contains(@class, "ml-auto")]'))
                )
                descricao_texto = desc_div.text

                # Busca todas as divs w-100 DENTRO da descrição
                preco = ""
                abreviacao = ""
                w100_divs = desc_div.find_elements(By.CLASS_NAME, "w-100")
                for div in w100_divs:
                    texto = div.text.strip()
                    if texto.startswith("Preço:"):
                        match_preco = re.search(r'Preço:\s*R\$\s*([\d\.,]+)', texto)
                        if match_preco:
                            preco = match_preco.group(1).replace('.', ',')
                    elif texto.startswith("Abreviação:"):
                        match_abr = re.search(r'Abreviação:\s*([^\n\r]+)', texto)
                        if match_abr:
                            abreviacao = match_abr.group(1).strip()
            except Exception as e:
                descricao_texto = ""
                preco = ""
                abreviacao = ""

            # Limpa a descrição, removendo preço e abreviação se estiverem nela
            descricao_limpa = re.sub(r'Preço:.*', '', descricao_texto)
            descricao_limpa = re.sub(r'Abreviação:.*', '', descricao_limpa)
            descricao_limpa = descricao_limpa.strip()

            print(f"  - {nome}")
            print(f"    Descrição: {descricao_limpa}")
            print(f"    Preço: {preco}")
            print(f"    Abreviação: {abreviacao}")

            todos_produtos.append({
                "Categoria": categoria,
                "Nome": nome,
                "Descrição": descricao_limpa,
                "Preço": preco,
                "Abreviação": abreviacao
            })

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.6)
        except Exception as e:
            print("  [Erro ao extrair produto]", e)

driver.quit()

# Salva em Excel
df = pd.DataFrame(todos_produtos)
df.to_excel("produtos_jsbronzinas.xlsx", index=False)
print("\nArquivo Excel gerado: produtos_jsbronzinas.xlsx")
