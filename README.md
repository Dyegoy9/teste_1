Busca a componente organizacional do Padrão TSS no site correspondente a variável url
O script usa a biblioteca requests para retornar o conteúdo html da página e a biblioteca bealtiful soup 
para realizar queries no html da página.
Requisitos:

*biliotecas do requirements.txt

Nota: Como sites são dinâmicos, ou seja, seu conteúdo varia frequentemente, é possível que o conteúdo procurado pelas querys de scripts Webscraping não funcionem caso seja mudado o conteúdo de uma tag html, para contornar esse fato, procurei usar tags que são modificadas menos frequentemente na medida do possível.