import os
import re

def convert_typescript_to_python(ts_code):

    # Remplacer des mots-clés TypeScript par leurs équivalents Python
    ts_code = re.sub(r'\blet\b|\bconst\b', '', ts_code)  # Retirer 'let' et 'const'
    ts_code = re.sub(r'\bfunction\b', 'def', ts_code)  # Remplacer 'function' par 'def'
    ts_code = re.sub(r';', '', ts_code)  # Retirer les points-virgules
    ts_code = re.sub(r'\bconsole\.log\b', 'print', ts_code)  # Remplacer console.log par print
    
    # Gestion des types
    ts_code = re.sub(r'(\w+):\s*\w+', r'\1', ts_code)  # Retirer les annotations de type

    # Conversion des fonctions fléchées
    ts_code = re.sub(r'(\w+)\s*=\s*([\s\S]*?)\s*=>', r'def \1():\n    \2', ts_code)
    
    # Conversion des classes
    ts_code = re.sub(r'\bclass\b', 'class', ts_code)
    ts_code = re.sub(r'\bconstructor\b', 'def __init__', ts_code)  # Remplacer le constructeur

    # Conversion des structures conditionnelles et de boucle
    ts_code = re.sub(r'\bif\s*\((.*?)\)\s*{', r'if \1:', ts_code)
    ts_code = re.sub(r'\belse\s*{', r'else:', ts_code) 
    ts_code = re.sub(r'\bfor\s*\((.*?)\)\s*{', r'for \1:', ts_code) 
    ts_code = re.sub(r'\bwhile\s*\((.*?)\)\s*{', r'while \1:', ts_code) 
    
    # Conversion des instanciations d'objets
    ts_code = re.sub(r'(\w+)\s*=\s*new\s+(\w+)\(\)', r'\1 = \2()', ts_code)
    ts_code = re.sub(r'\b(\w+)\.push\((.*?)\)', r'\1.append(\2)', ts_code)  # Conversion des push pour les listes
    ts_code = re.sub(r'\b(\w+)\.length\b', r'len(\1)', ts_code)  # Conversion des lengths
    ts_code = re.sub(r'(\w+)\s*=\s*\[\]', r'\1 = []', ts_code)  # Conversion des initialisations de tableau
    ts_code = re.sub(r'(\w+)\s*=\s*\(\)', r'\1 = ()', ts_code)  # Conversion des initialisations de tuple

    # Conversion des try/catch
    ts_code = re.sub(r'try\s*{', r'try:', ts_code)
    ts_code = re.sub(r'\} catch\s*\((.*?)\)\s*{', r'except \1:', ts_code)
    ts_code = re.sub(r'\bfinally\s*{', r'finally:', ts_code)

    # Conversion des imports
    ts_code = re.sub(r'import\s+(.*?)\s+from\s+(.*?);', r'from \2 import \1', ts_code)

    # Gestion des commentaires
    ts_code = re.sub(r'//(.*?)\n', r'# \1\n', ts_code)  # Commentaires sur une seule ligne
    ts_code = re.sub(r'/\*(.*?)\*/', r'"""\1"""', ts_code, flags=re.DOTALL)  # Commentaires multi-lignes

    # Conversion des ternaires
    ts_code = re.sub(r'\b(\w+)\s*=\s*\((.*?)\)\s*\?\s*(.*?)\s*:\s*(.*?)\s*;', r'\1 = \3 if \2 else \4', ts_code)

    # Remplacer 'this' par 'self' dans les classes
    ts_code = re.sub(r'\bthis\b', 'self', ts_code)

    # Conversion des dictionnaires (y compris l'ajout de guillemets pour les clés)
    ts_code = re.sub(r'(\w+):', r'"\1":', ts_code)  # Ajoute des guillemets autour des clés de dictionnaires

    # Conversion des fonctions async
    ts_code = re.sub(r'\basync\s+function\b', 'async def', ts_code)  # Remplacer async function par async def
    ts_code = re.sub(r'\bawait\s+', 'await ', ts_code)  # Conserver await

    # Supprimer l'export, non nécessaire en Python
    ts_code = re.sub(r'\bexport\b', '', ts_code)

    return ts_code

def convert_file(ts_file_path):
    with open(ts_file_path, 'r') as ts_file:
        ts_code = ts_file.read()
        py_code = convert_typescript_to_python(ts_code)

    # Écrire le code Python dans un fichier .py
    py_file_path = ts_file_path.replace('.ts', '.py')
    with open(py_file_path, 'w') as py_file:
        py_file.write(py_code)

def convert_single_file(ts_file_path):
    if os.path.isfile(ts_file_path) and ts_file_path.endswith('.ts'):
        convert_file(ts_file_path)
        print(f'Converted: {ts_file_path} to {ts_file_path.replace(".ts", ".py")}')
    else:
        print(f'Error: {ts_file_path} is not a valid TypeScript file.')

if __name__ == "__main__":
    # Spécifiez le chemin vers votre fichier TypeScript ici
    ts_file_path = './account.ts'  # Remplacez par le chemin de votre fichier .ts
    convert_single_file(ts_file_path)
