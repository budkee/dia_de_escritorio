import gspread
from unidecode import unidecode
from oauth2client.service_account import ServiceAccountCredentials

# Configurar as credenciais e a conexão com a planilha
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Abrir a planilha e a aba desejada
spreadsheet = client.open("Aurora Modas | Produtos e Serviços")
worksheet = spreadsheet.worksheet("SKU")


# Função para gerar SKU com base nos atributos
def gerar_sku(atributo):
    # Remove acentos e divide o atributo em palavras
    atributo_sem_acento = unidecode(atributo)
    # print(f"Original: {atributo} -> Sem acento: {atributo_sem_acento}")  # Verificação
    palavras = atributo_sem_acento.split()
    
    if len(palavras) > 1:
        # Se o atributo for composto, pega a primeira letra de cada palavra
        return ''.join(p[0].upper() for p in palavras)
    else:
        # Caso contrário, pega as 3 primeiras letras
        return atributo_sem_acento[:3].upper()


# Obter todos os valores das colunas A a F
data = worksheet.get_all_values()

# Criar ou atualizar a coluna G com os SKUs
for i in range(1, len(data)):  # Começa de 1 para ignorar o cabeçalho
    
    produto = gerar_sku(data[i][0])  
    modelo = gerar_sku(data[i][1])    
    tecido = gerar_sku(data[i][2])    
    estampa = gerar_sku(data[i][3])   
    cor = gerar_sku(data[i][4])       
    tamanho = gerar_sku(data[i][5])  
    
    sku = f"{produto}{modelo}{tecido}{estampa}{cor}{tamanho}"
    
    # Atualiza a coluna G (índice 6) com o SKU
    worksheet.update_cell(i + 1, 7, sku)  # +1 porque o gspread usa 1-indexing

print("Coluna G atualizada com os SKUs.")
