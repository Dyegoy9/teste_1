import requests
from bs4 import BeautifulSoup

url = "https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss"

# makes request to the given webpage link
def get_page_content(link):
    try:
        contador = 0
        while True:
            file = requests.get(link)
            print(f"Requesting page {link}")
            if file.status_code == 200:
                print("request succed")
                print("................................................................................")
                break
            else:
                contador = contador + 1
                print('Some error ocorred ,trying again')
                print(f'attempt {contador}')
            if contador == 7:
                break
        return file.content
    except:
        print(f'Cannot get {link} webpage content')
        print("Please check your internet connection or website disponibility and try again")
        return 0

# Find last version of TISS on first webpage
def query1(content):
    try:
        soup_content = BeautifulSoup(content,'html.parser')
        #Busca sempre o a versão do arquivo referente ao mês anterior ao que o código é rodado
        item = soup_content.find('a',string = f'Clique aqui para acessar a versão Novembro/2021')
        url = item.get('href')
        return url
    except ConnectionRefusedError:
        if item == None:
            print(f'Cannot find Novembro/2021 TISS version on first webpage')
        else:
            return None

#Find organizational component on second website 
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
            print('Cannot find "Componente Organizacional do Padrão TISS"')
        else:
            return None
# makes download of file found by query2 function
def download_file(file_content):
    try:
        with open('Componente_organizacional.pdf','wb') as file:
            file.write(file_content)
        return "'Componente organizacional do TISS' downloaded with sucess !!!"
    except:
        print("Cannot get file 'Componente organizacional do Padrão TISS'")
        return False

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
                    message = download_file(content_2)
                    print(message)

main()