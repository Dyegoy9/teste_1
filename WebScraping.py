import requests
from bs4 import BeautifulSoup
from datetime import date

"""O código busca a ultima versão do TISS no 

"""
# Obtendo o mês e ano atuais para uma busca mais genérica no site
data_atual = date.today()
mes_atual = data_atual.month
ano_atual = data_atual.year

# mapeamento dos meses do ano por meio de um dicionário
meses_map ={
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro',
}

url = "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss"


# Realiza as requisições ao link solicitado
def get_page_content(link):
    try:
        file = requests.get(link)
        return file.content
    except:
        print(f'Não foi possivel obter o conteúdo do link {link}')
        return 0

# Busca a ultima versão do TSS no primeiro site
def query1(content):
    try:

        soup_content = BeautifulSoup(content,'html.parser')
        #Busca sempre o a versão do arquivo referente ao mês anterior ao que o código é rodado
        item = soup_content.find('a',string = f'Clique aqui para acessar a versão {meses_map[mes_atual-1]}/{ano_atual}')
        url = item.get('href')
        return url
    except:
        if item == None:
            print('Não foi possível encontrar o link da ultima versão do Padrão TISS na página principal')
        else:
            return None

#Busca o arquivo componente organizacional no segundo site 
def query2(content):
    try:
        site = BeautifulSoup(content,'html.parser')
        # Usa a classe do arquivo como busca, visando minimizar erros por modificações da página
        items = site.findAll('a',attrs={'class':'btn btn-primary btn-sm center-block internal-link'})
    
        #Usa um condicional para filtrar apenas o componente organizacional
        for item in items:
            text = item.find('span').get_text()
            text_ref = ' documento referente ao Componente Organizacional.'
            if text == text_ref:
                return item.get('href')
    except:
        if items == []:
            print('Não foi possível encontrar a Componente Organizacional do Padrão TISS')
        else:
            return None

# Faz o donwload do arquivo encontrado pela função query2
def download_file(file_content):
    try:
        with open('Componente_organizacional.pdf','wb') as file:
            file.write(file_content)
    except:
        print("Não foi possível obter o arquivo correspondente ao Componente organizacional do Padrão TISS")

def main():
    content = get_page_content(url)
    if content != 0:
        url1 = query1(content)
        if url1 != None:
            content_1 = get_page_content(url1)
            if content_1 != 0:
                url2 = query2(content_1)
                if url2 != None:
                    content_2 = get_page_content(url2)
                    download_file(content_2)
                    print("Arquivo Obtido com sucesso!!!")

main()