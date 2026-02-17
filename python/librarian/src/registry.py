import os
import sys

import winreg as registry # pip install winregistry


cwd = os.getcwd()
python_path = sys.executable

key_name = 'Librarian'

# FILE 
key_path = fr'*\\shell\\{key_name}'
command_key_path = fr'*\\shell\\{key_name}\\command'

key = registry.CreateKey(registry.HKEY_CLASSES_ROOT, key_path)
registry.SetValue(key, '', registry.REG_SZ, 'Analisar arquivo com Librarian')

command_key = registry.CreateKey(registry.HKEY_CLASSES_ROOT, command_key_path)
command_path = fr'"{python_path}" "{cwd}\src\librarian.py" "%1"'
registry.SetValue(command_key, '', registry.REG_SZ, command_path)

# FOLDER
key_path = fr'Directory\\shell\\{key_name}'
command_key_path = fr'Directory\\shell\\{key_name}\\command'

key = registry.CreateKey(registry.HKEY_CLASSES_ROOT, key_path)
registry.SetValue(key, '', registry.REG_SZ, 'Analisar pasta com Librarian')

command_key = registry.CreateKey(registry.HKEY_CLASSES_ROOT, command_key_path)
command_path = fr'"{python_path}" "{cwd}\src\librarian.py" "%1"'
registry.SetValue(command_key, '', registry.REG_SZ, command_path)