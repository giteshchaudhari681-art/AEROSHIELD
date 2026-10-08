import sys
import os
import glob

migration_files = glob.glob('alembic/versions/*_initial_aeroshield_domain.py')
if not migration_files:
    sys.exit("No migration file found")

filepath = migration_files[0]
with open(filepath, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "op.create_index" in line and "postgresql_using='gist'" in line and ('boundary' in line or 'location' in line):
        continue
    new_lines.append(line)

with open(filepath, 'w') as f:
    f.writelines(new_lines)

print("Fixed migration file")
