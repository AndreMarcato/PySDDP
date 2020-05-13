def read_file(dir_name, file_name, mode='r'):
    # Recebe um diretorio e um nome arquivo em maiusculo, retorna a leitura do arquivo

    # Parameters

    #   dir_name (str): String do diretorio
    #   file_name (str): String do nome do arquivo em maiusculo

    # Returns:

    #   file(File):Arquivo lido
    try:
        file = open(dir_name + file_name, mode=mode)
    except FileNotFoundError:
        file = open(dir_name + file_name.lower(), mode=mode)
    return file
