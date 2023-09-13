import os
import sys

def requirements_install():
    """Instala as dependências de um projeto.k"""

    # Verifica se o arquivo requirements.txt existe.
    if not os.path.exists("requirements.txt"):
        print("O arquivo requirements.txt não existe.")
        sys.exit(1)

    # Instala as dependências.
    os.system("pip install -r requirements.txt")

if __name__ == "__main__":
  requirements_install()