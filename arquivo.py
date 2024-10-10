import os
# from PIL import Image

# Função para renomear os arquivos .jpg, .png e .jpeg
def custom_file_rename(filename, parent_folder_name, counter):
    name, ext = os.path.splitext(filename)
    
    if ext.lower() in (".jpg", ".png", ".jpeg"):
        # Cria o novo nome no formato: nome_da_pasta_00.jpg, nome_da_pasta_01.jpg...
        new_name = f"{parent_folder_name}_{counter:02}{ext}"
        return new_name
    return filename

# Função para renomear a pasta e os arquivos
def rename_folder_and_files(root_folder, new_folder_name):
    # Renomear a pasta principal
    parent_dir = os.path.dirname(root_folder)
    new_folder_path = os.path.join(parent_dir, new_folder_name)

    try:
        os.rename(root_folder, new_folder_path)
        print(f"Pasta renomeada com sucesso para: {new_folder_name}")
    except PermissionError:
        print("Erro: Permissão negada ao tentar renomear a pasta.")
        return

    # Contador para arquivos .jpg, .png e .jpeg
    counter = 0

    # Renomear arquivos e subpastas recursivamente
    for dirpath, dirnames, filenames in os.walk(new_folder_path):
        # Extrair o nome da pasta pai
        parent_folder_name = os.path.basename(new_folder_path)

        # Renomear arquivos
        for filename in filenames:
            old_file_path = os.path.join(dirpath, filename)
            new_file_name = custom_file_rename(filename, parent_folder_name, counter)  # Aplicar regra de renomeação
            new_file_path = os.path.join(dirpath, new_file_name)

            # Só renomeia se o arquivo for .jpg, .png ou .jpeg
            if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                os.rename(old_file_path, new_file_path)
                counter += 1
                print(f"Arquivo renomeado: {new_file_name}")

# Função para verificar o tamanho dos arquivos
def check_file_sizes(root_folder):
    total_size = 0
    print(f"\nTamanho dos arquivos em '{root_folder}':\n")

    # Iterar sobre os arquivos e subpastas
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_size = os.path.getsize(file_path)
            total_size += file_size
            print(f"{filename}: {file_size / 1024:.2f} KB")

    print(f"\nTamanho total da pasta: {total_size / 1024:.2f} KB")

# Função para comprimir imagens e salvá-las em uma nova pasta
def compress_images_in_folder(root_folder, quality=85, max_size=(2560, 2560)):
    # Criar nova pasta para imagens comprimidas
    compressed_folder = os.path.join(root_folder, "compressed_images")
    os.makedirs(compressed_folder, exist_ok=True)
    print(f"\nCompactando imagens em '{root_folder}' e salvando em '{compressed_folder}':\n")

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith('.jpg'):
                input_path = os.path.join(dirpath, filename)
                output_path = os.path.join(compressed_folder, filename)
                compress_image(input_path, output_path, quality, max_size)
                print(f"Imagem comprimida: {filename}")

def compress_image(input_path, output_path, quality=85, max_size=(2560, 2560)):
    with Image.open(input_path) as img:
        img.thumbnail(max_size)  # Redimensionar se exceder o limite
        img.save(output_path, "JPEG", quality=quality)  # Salvar com compressão

# Função para mostrar o menu
def show_menu():
    print("\nMenu:")
    print("1. Renomear pasta e arquivos")
    print("2. Verificar o tamanho de cada arquivo")
    print("3. Comprimir imagens")
    print("4. Sair")

# Interação com o usuário
if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("\nEscolha uma opção: ")

        if choice == '1':
            root_folder = input("Digite o caminho completo da pasta de interesse: ")
            new_folder_name = input("Digite o novo nome da pasta: ")
            rename_folder_and_files(root_folder, new_folder_name)

        elif choice == '2':
            root_folder = input("Digite o caminho completo da pasta para verificar o tamanho dos arquivos: ")
            check_file_sizes(root_folder)

        elif choice == '3':
            root_folder = input("Digite o caminho completo da pasta com imagens para comprimir: ")
            quality = int(input("Digite a qualidade da compressão (0-100): "))
            max_width = int(input("Digite a largura máxima das imagens (em pixels): "))
            max_height = int(input("Digite a altura máxima das imagens (em pixels): "))
            compress_images_in_folder(root_folder, quality, (max_width, max_height))

        elif choice == '4':
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")