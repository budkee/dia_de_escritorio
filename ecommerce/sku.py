import gspread
from unidecode import unidecode
from oauth2client.service_account import ServiceAccountCredentials

# Configurar as credenciais e a conexão com a planilha
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Abrir a planilha e a aba desejada
spreadsheet = client.open("Aurora Modas | Produtos e Serviços")
worksheet = spreadsheet.worksheet("produtos")

# Função para gerar SKU com base nos atributos
def gerar_sku(nome, codigo_barras):
    # Remove acentos e divide o atributo em palavras
    atributo_sem_acento = unidecode(nome)
    
    # Divide o atributo em palavras 
    palavras = atributo_sem_acento.split()
    
    # Pega as 3 primeiras e 3 últimas letras de cada palavra no nome
    inicio_nome = ''.join([palavra[:1].upper() for palavra in palavras])
    fim_nome = ''.join([palavra[-1:].upper() if len(palavra) > 3 else palavra.upper() for palavra in palavras])
    
    # Pega os 4 primeiros números do código de barras
    inicio_codigo = codigo_barras[:4]
    
    # Concatena as partes para formar o SKU
    sku = f"{inicio_nome}{inicio_codigo}{fim_nome}"
    
    return sku

# Obter todos os valores da planilha (colunas A a F, por exemplo)
data = worksheet.get_all_values()

# Atualizar a coluna D com os SKUs gerados
for i, row in enumerate(data[1:], start=2):  # Pulando o cabeçalho (linha 1)
    codigo_barras = row[1]  # Supondo que o código de barras esteja na coluna B
    nome = row[4]  # Supondo que o nome esteja na coluna E
    sku = gerar_sku(nome, codigo_barras)
    worksheet.update_cell(i, 4, sku)  # Colocando o SKU na coluna D (coluna 4)

print("Coluna D atualizada com os SKUs.")
