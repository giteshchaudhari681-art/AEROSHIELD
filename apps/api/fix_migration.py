import re

file_path = "alembic/versions/7704418c1da7_add_event_outbox.py"
with open(file_path, "r") as f:
    content = f.read()

upgrade_match = re.search(r"def upgrade\(\) -> None:(.*?)\n    # ### end Alembic commands ###", content, re.DOTALL)
downgrade_match = re.search(r"def downgrade\(\) -> None:(.*?)\n    # ### end Alembic commands ###", content, re.DOTALL)

if upgrade_match:
    upgrade_body = upgrade_match.group(1)
    kept_upgrade = "\n".join([line for line in upgrade_body.split("\n") if "event_outbox" in line or not line.strip() or "sa.Column" in line or "sa.PrimaryKeyConstraint" in line])
    # Add back the table and indices carefully
    content = content.replace(upgrade_body, kept_upgrade)

if downgrade_match:
    downgrade_body = downgrade_match.group(1)
    kept_downgrade = "\n".join([line for line in downgrade_body.split("\n") if "event_outbox" in line or not line.strip()])
    content = content.replace(downgrade_body, kept_downgrade)

with open(file_path, "w") as f:
    f.write(content)
