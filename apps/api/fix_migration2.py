import glob
import os
import subprocess

def fix_migration():
    files = glob.glob('d:/SEVA/apps/api/alembic/versions/*_digital_twin_domain_expansion.py')
    if not files:
        print("Migration file not found")
        return
    file = files[0]
    with open(file, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if "op.drop_table" in line or "op.drop_index" in line:
            continue
        new_lines.append(line)
        
    with open(file, 'w') as f:
        f.writelines(new_lines)
    print("Fixed migration file:", file)
    
    subprocess.run(["alembic", "upgrade", "head"], cwd="d:/SEVA/apps/api")

if __name__ == "__main__":
    fix_migration()
