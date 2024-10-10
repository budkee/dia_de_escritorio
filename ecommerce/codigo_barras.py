import os
import random
import barcode
import gspread
from barcode.writer import ImageWriter
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --------------- Conexão Google Sheets e Google Drive ---------------
def conectar_sheets():
    # Define o escopo da API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Autentica com o arquivo de credenciais (credentials.json)
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    
    # Autentica e abre o cliente do Google Sheets
    client = gspread.authorize(creds)
    
    # Abra a planilha pelo nome
    planilha = client.open('Aurora Modas | Produtos e Serviços')  
    return planilha.worksheet('produtos')


def conectar_drive():
    # Define o escopo da API
    scope = ['https://www.googleapis.com/auth/drive']
    
    # Autentica com o arquivo de credenciais (credentials.json)
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    
    # Conecta-se ao serviço do Google Drive
    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service


# --------------- 1. Gerar Código de Barras ---------------
# Gerar um número aleatório de 12 dígitos para EAN-13
def gerar_numero_ean13():
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

# Gerar o código de barras e salvar como imagem
def gerar_codigo_de_barras(numero):
    
    EAN = barcode.get_barcode_class('ean13')
    codigo = EAN(numero, writer=ImageWriter())
    
    # Verifica se o diretório existe, caso contrário, cria-o
    pasta_img = "./img"
    if not os.path.exists(pasta_img):
        os.makedirs(pasta_img)
    
    # Salva o arquivo sem incluir a extensão .png manualmente
    arquivo_nome = f'codigo_de_barras_{numero}'
    caminho_completo = os.path.join(pasta_img, arquivo_nome)  # Usa os.path.join para garantir o caminho correto
    
    # O método save() adiciona automaticamente a extensão .png
    caminho_completo = codigo.save(caminho_completo)
    
    print(f"Código de barras salvo como {caminho_completo}")
    return caminho_completo  # Retorna o caminho completo com a extensão correta

# Fazer upload da imagem para o Google Drive
def upload_para_drive(service, arquivo, pasta_id):
    # O nome do arquivo será apenas o nome base (sem o caminho completo)
    nome_arquivo_no_drive = arquivo.split('/')[-1]  # Extrai o nome do arquivo do caminho
    
    file_metadata = {
        'name': nome_arquivo_no_drive,  # Nome do arquivo no Drive
        'parents': [pasta_id]  # ID da pasta onde será salvo
    }
    
    media = MediaFileUpload(arquivo, mimetype='image/png')
    
    # Faz o upload do arquivo
    arquivo_drive = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    print(f"Arquivo {nome_arquivo_no_drive} enviado ao Google Drive. ID: {arquivo_drive.get('id')}")

# ----------------- 2. Criar a imagem a partir da Planilha -----------------
# Função para obter um número de uma célula específica da planilha
def obter_numero_da_planilha(sheet, celula):
    """
    Obtém o número de código de barras de uma célula específica da planilha.
    
    Args:
    sheet: Objeto de planilha do gspread.
    celula: A célula específica da planilha (ex: 'B2') de onde o número será obtido.
    
    Retorna:
    O número contido na célula.
    """
    numero = sheet.acell(celula).value  # Pega o valor da célula especificada
    print(f"Número obtido da célula {celula}: {numero}")
    return numero

# Função para obter números de um intervalo de células da planilha
def obter_numeros_da_planilha(sheet, intervalo):
    """
    Obtém os números de um intervalo de células da planilha.
    
    Args:
    sheet: Objeto de planilha do gspread.
    intervalo: Intervalo de células (ex: 'B2:B10') de onde os números serão obtidos.
    
    Retorna:
    Lista com os números contidos no intervalo.
    """
    numeros = sheet.get(intervalo)  # Pega os valores do intervalo especificado
    print(f"Números obtidos do intervalo {intervalo}: {numeros}")
    return [numero[0] for numero in numeros]  # Converte a lista de listas para uma lista simples


# Submenu para o usuário escolher entre leitura de uma ou várias células
def submenu_leitura_celulas(sheet, drive_service, pasta_id):
    """
    Submenu para o usuário escolher entre ler uma célula ou várias células para gerar código de barras.
    
    Args:
    sheet: Objeto de planilha do gspread.
    drive_service: Serviço do Google Drive.
    pasta_id: ID da pasta do Google Drive.
    """
    print("\nSubmenu:")
    print("1. Ler uma única célula")
    print("2. Ler várias células (intervalo)")

    escolha = input("Escolha uma opção (1 ou 2): ")

    if escolha == '1':
        # Lê uma célula específica
        celula_usuario = input("Digite a célula que contém o número do código de barras (ex: 'B2'): ")
        numero_da_planilha = obter_numero_da_planilha(sheet, celula_usuario)
        
        # Gera e salva o código de barras como imagem
        arquivo_gerado = gerar_codigo_de_barras(numero_da_planilha)
        
        # Envia a imagem ao Google Drive
        upload_para_drive(drive_service, arquivo_gerado, pasta_id)

    elif escolha == '2':
        # Lê um intervalo de células
        intervalo_usuario = input("Digite o intervalo de células para gerar os códigos de barras (ex: 'B2:B10'): ")
        numeros_da_planilha = obter_numeros_da_planilha(sheet, intervalo_usuario)
        
        # Para cada número obtido, gera e salva o código de barras
        for numero in numeros_da_planilha:
            arquivo_gerado = gerar_codigo_de_barras(numero)
            upload_para_drive(drive_service, arquivo_gerado, pasta_id)
    else:
        print("Opção inválida. Tente novamente.")
        submenu_leitura_celulas(sheet, drive_service, pasta_id)


# ----------------- 3. Adicionar Números à Planilha -----------------
def adicionar_numeros_na_planilha(sheet, numeros, intervalo):
    """
    Adiciona os números gerados no intervalo especificado na planilha.
    
    Args:
    sheet: Objeto de planilha do gspread.
    numeros: Lista de números de código de barras.
    intervalo: Intervalo de células onde os números serão inseridos.
    """
    # Atualiza o intervalo da coluna B com os números gerados, usando argumentos nomeados
    sheet.update(range_name=intervalo, values=[[numero] for numero in numeros])
    print(f"Números {numeros} adicionados ao intervalo {intervalo} na planilha.")


# Função para exibir o menu e capturar a escolha do usuário
def exibir_menu():
    print("\nEscolha uma opção:")
    print("1. Gerar um novo código de barras + imagem e salvar no Google Drive")
    print("2. Gerar o código de barras a partir do número da planilha")
    print("3. Adicionar apenas o(s) número(s) à planilha")
    print("4. Sair")
    return input("\nDigite o número da opção desejada: ")

# Função principal
def executar_opcao(opcao, sheet, drive_service, pasta_id):
    if opcao == '1':
        # Gera um número de código de barras aleatório
        numero_aleatorio = gerar_numero_ean13()
        # Gera e salva o código de barras como imagem
        arquivo_gerado = gerar_codigo_de_barras(numero_aleatorio)
        # Envia a imagem ao Google Drive
        upload_para_drive(drive_service, arquivo_gerado, pasta_id)

    elif opcao == '2':  
        submenu_leitura_celulas(sheet, drive_service, pasta_id)

    elif opcao == '3':
        # Pergunta o intervalo que o usuário deseja preencher, exemplo: 'B2:B54'
        intervalo_usuario = input("Digite o intervalo para adicionar os códigos de barras (ex: 'B2:B54'): ")
        
        # Define quantos números serão gerados com base no número de linhas do intervalo
        inicio, fim = intervalo_usuario.split(":")
        linha_inicial = int(inicio[1:])  # Extrai o número da linha inicial, por exemplo, 2 em 'B2'
        linha_final = int(fim[1:])  # Extrai o número da linha final, por exemplo, 54 em 'B54'
        quantidade_numeros = linha_final - linha_inicial + 1  # Quantidade de números a serem gerados
        
        # Gera os números de códigos de barras aleatórios (mesma quantidade que o número de linhas)
        numeros_aleatorios = [gerar_numero_ean13() for _ in range(quantidade_numeros)]
        
        # Adiciona os números gerados no intervalo fornecido pelo usuário
        adicionar_numeros_na_planilha(sheet, numeros_aleatorios, intervalo_usuario)

    elif opcao == '4':
        print("Saindo...")

    else:
        print("Opção inválida. Tente novamente.")

# Programa principal com menu interativo
if __name__ == '__main__':
    # Conecta-se ao Google Sheets
    sheet = conectar_sheets()
    
    # Conecta-se ao Google Drive
    drive_service = conectar_drive()
    
    # Defina o ID da pasta no Google Drive onde os arquivos serão salvos
    pasta_id = '13EFkI8RN49KSn5cCS0jTOoR8Y5mpkQgG'  # Substitua pelo ID da sua pasta no Google Drive
    
    while True:
        # Exibe o menu para o usuário
        opcao = exibir_menu()
        
        if opcao == '4':
            print("Encerrando o programa.")
            break
        
        # Executa a opção escolhida
        executar_opcao(opcao, sheet, drive_service, pasta_id)
