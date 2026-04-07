import os
import re

migrations_dir = r'c:\Users\Mupenda\Documents\PYTHON\DJANGO\ChurchManageApp\church_management_app\migrations'

for filename in os.listdir(migrations_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        filepath = os.path.join(migrations_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace old app name with new app name in dependencies
        new_content = content.replace("'church_management',", "'church_management_app',")
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Fixed: {filename}')
        else:
            print(f'OK: {filename}')

print('Done!')
