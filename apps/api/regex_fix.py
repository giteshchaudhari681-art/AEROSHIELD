import re
f = 'd:/SEVA/apps/api/alembic/versions/782cef6d998b_sensor_abstraction_expansion.py'
with open(f, 'r') as file: content = file.read()

content = re.sub(r"(sa\.Column\('observation_type'.*?create_type=False\), nullable=False)\)", r"\1, server_default='DETECTION')", content)
content = re.sub(r"(sa\.Column\('received_at'.*?nullable=False)\)", r"\1, server_default=sa.text('now()'))", content)
content = re.sub(r"(sa\.Column\('operational_status'.*?create_type=False\), nullable=False)\)", r"\1, server_default='UNKNOWN')", content)
content = re.sub(r"(sa\.Column\('health_status'.*?create_type=False\), nullable=False)\)", r"\1, server_default='UNKNOWN')", content)
content = re.sub(r"(sa\.Column\('is_enabled'.*?nullable=False)\)", r"\1, server_default='true')", content)

with open(f, 'w') as file: file.write(content)
print('Migration updated')
