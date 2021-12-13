import requests
from bs4 import BeautifulSoup

url = "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss"

# Realiza as requisições ao link dado e retorna o conteúdo da página
def get_page_content(link):
    try:
        file = requests.get(link)
        return file.content
    except:
        print(f'Não foi possivel obter o conteúdo do link {link}')
        print("Verifique sua conexão com a internet ou a disponibilidade do site")
        return 0

# Busca a ultima versão do Padrão TSS no primeiro site
def query1(content):
    try:
        soup_content = BeautifulSoup(content,'html.parser')
        #Busca sempre o a versão do arquivo referente ao mês anterior ao que o código é rodado
        item = soup_content.find('a',string = f'Clique aqui para acessar a versão Novembro/2021')
        url = item.get('href')
        return url
    except:
        if item == None:
            print(f'Não foi possível encontrar o link da ultima versão Novembro/2021 do Padrão TISS na página principal')
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