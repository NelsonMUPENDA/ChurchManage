import os
import re

migrations_dir = r'c:\Users\Mupenda\Documents\PYTHON\DJANGO\ChurchManageApp\church_management_app\migrations'

for filename in os.listdir(migrations_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        filepath = os.path.join(migrations_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace model references in migrations
        new_content = content.replace("to='church_management.", "to='church_management_app.")
        new_content = new_content.replace('to="church_management.', 'to="church_management_app.')
        new_content = new_content.replace("model_name='church_management.", "model_name='church_management_app.")
        new_content = new_content.replace('model_name="church_management.', 'model_name="church_management_app.')
        new_content = new_content.replace("swappable='church_management.", "swappable='church_management_app.")
        new_content = new_content.replace('swappable="church_management.', 'swappable="church_management_app.')
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print('Fixed:', filename)
        else:
            print('OK:', filename)

print('Done!')
