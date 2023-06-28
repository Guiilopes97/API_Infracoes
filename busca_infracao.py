from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def busca_infracao(infracao):
    all_arr = []

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe", headless=True)
        page = browser.new_page()
        page.goto("https://www.detran.sp.gov.br/wps/portal/portaldetran/cidadao/infracoes/servicos/consultaTabelaInfracoes")
        
        if infracao.isnumeric():
            page.get_by_placeholder("ex: 99999").fill(str(infracao))
        else:
            page.get_by_placeholder("ex: celular").fill(infracao)

        page.get_by_role("button", name="Pesquisar").click()
        
        try:
            tabela = page.locator("#resultadoTabelaMultas div").filter(has_text="Código da infração Infração Responsável Valor da multa Outras informações Órgão ").first.inner_html(timeout=5000)

            soup = BeautifulSoup(tabela, 'html.parser')

            tr = soup.find_all('tr')
            for row in tr:
                arr = []
                all_td = row.find_all('td')
                i = 0
                for td in all_td:
                    
                    dados = td.get_text().replace('\n','')

                    if i == 7:
                        dados = dados.split(" - ")
                        arr.append(dados[0])
                        arr.append(dados[1])
                    else:
                        arr.append(dados)

                    i += 1

                all_arr.append(arr)
        except:
            return "Nenhuma infração encontrada."

        browser.close()

        return all_arr[1:]
