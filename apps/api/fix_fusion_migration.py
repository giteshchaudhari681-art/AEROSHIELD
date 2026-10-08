import re
import sys

def fix_migration(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Find upgrade function
    upgrade_match = re.search(r"def upgrade\(\) -> None:(.*?)(?=def downgrade\(\) -> None:)", content, re.DOTALL)
    downgrade_match = re.search(r"def downgrade\(\) -> None:(.*)", content, re.DOTALL)
    
    if not upgrade_match or not downgrade_match:
        print("Could not find upgrade or downgrade functions.")
        return

    upgrade_body = upgrade_match.group(1)
    downgrade_body = downgrade_match.group(1)

    # Filter out op.drop_table and op.drop_index lines from upgrade that are related to PostGIS
    new_upgrade_lines = []
    for line in upgrade_body.split("\n"):
        if "op.drop_table" in line or "op.drop_index" in line:
            continue
        new_upgrade_lines.append(line)

    # Filter out op.create_table and op.create_index lines from downgrade that are related to PostGIS
    new_downgrade_lines = []
    for line in downgrade_body.split("\n"):
        if "op.create_table" in line or "op.create_index" in line:
            if "fused_" not in line:
                continue
        new_downgrade_lines.append(line)

    new_content = content[:upgrade_match.start()] + \
                  "def upgrade() -> None:\n" + "\n".join(new_upgrade_lines) + \
                  "def downgrade() -> None:\n" + "\n".join(new_downgrade_lines)

    with open(filepath, "w") as f:
        f.write(new_content)
    print("Migration fixed.")

if __name__ == "__main__":
    fix_migration(sys.argv[1])
