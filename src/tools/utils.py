import os


def delete_folder(folder_path):
    try:
        # Delete files in the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)

        # Delete empty subdirectorys
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)

        # Delete main folder
        os.rmdir(folder_path)
        print(
            f"Cartella '{folder_path}' e tutti i suoi contenuti eliminati con successo."
        )
    except Exception as e:
        print(f"Si è verificato un errore durante l'eliminazione: {e}")
