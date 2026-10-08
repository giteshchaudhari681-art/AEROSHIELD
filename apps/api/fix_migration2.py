import sys
import glob

migration_files = glob.glob('alembic/versions/*_initial_aeroshield_domain.py')
if not migration_files:
    sys.exit("No migration file found")

filepath = migration_files[0]
with open(filepath, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "op.drop_table" in line or "op.drop_index" in line:
        continue
    new_lines.append(line)

with open(filepath, 'w') as f:
    f.writelines(new_lines)

print("Removed drop_table and drop_index from migration")
