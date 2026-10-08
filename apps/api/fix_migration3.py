import os

migration_file = "d:/SEVA/apps/api/alembic/versions/782cef6d998b_sensor_abstraction_expansion.py"

with open(migration_file, "r") as f:
    lines = f.readlines()

new_lines = []
in_upgrade = False
for line in lines:
    if "def upgrade()" in line:
        in_upgrade = True
    elif "def downgrade()" in line:
        in_upgrade = False

    if "op.drop_table" in line or "op.drop_index" in line:
        # Ignore all drop tables in upgrade, as they are PostGIS tiger tables
        # But wait, wait! The script must also not drop our new columns in downgrade?
        # Let's just comment out all drops that relate to tiger/postgis
        if any(x in line for x in ['place', 'tabblock', 'zip_state', 'addr', 'loader_lookuptables', 'street_type_lookup', 'cousub', 'tabblock20']):
            new_lines.append(f"    # {line.strip()}\n")
            continue
            
    # For enum creation
    if "sa.Column('observation_type', sa.Enum" in line:
        new_lines.append("    observation_type = postgresql.ENUM('DETECTION', 'POSITION', 'VELOCITY', 'SIGNAL', 'THERMAL', 'ACOUSTIC', 'IDENTIFICATION', 'STATUS', name='observationtype')\n")
        new_lines.append("    observation_type.create(op.get_bind())\n")
        line = line.replace("sa.Enum('DETECTION', 'POSITION', 'VELOCITY', 'SIGNAL', 'THERMAL', 'ACOUSTIC', 'IDENTIFICATION', 'STATUS', name='observationtype')", "postgresql.ENUM('DETECTION', 'POSITION', 'VELOCITY', 'SIGNAL', 'THERMAL', 'ACOUSTIC', 'IDENTIFICATION', 'STATUS', name='observationtype', create_type=False)")
    
    if "sa.Column('operational_status', sa.Enum" in line:
        new_lines.append("    sensor_status = postgresql.ENUM('ACTIVE', 'INACTIVE', 'DEGRADED', 'MAINTENANCE', 'OFFLINE', 'UNKNOWN', name='sensorstatus')\n")
        new_lines.append("    sensor_status.create(op.get_bind())\n")
        line = line.replace("sa.Enum('ACTIVE', 'INACTIVE', 'DEGRADED', 'MAINTENANCE', 'OFFLINE', 'UNKNOWN', name='sensorstatus')", "postgresql.ENUM('ACTIVE', 'INACTIVE', 'DEGRADED', 'MAINTENANCE', 'OFFLINE', 'UNKNOWN', name='sensorstatus', create_type=False)")
        
    if "sa.Column('health_status', sa.Enum" in line:
        new_lines.append("    health_status = postgresql.ENUM('HEALTHY', 'WARNING', 'CRITICAL', 'UNKNOWN', name='sensorhealthstatus')\n")
        new_lines.append("    health_status.create(op.get_bind())\n")
        line = line.replace("sa.Enum('HEALTHY', 'WARNING', 'CRITICAL', 'UNKNOWN', name='sensorhealthstatus')", "postgresql.ENUM('HEALTHY', 'WARNING', 'CRITICAL', 'UNKNOWN', name='sensorhealthstatus', create_type=False)")

    new_lines.append(line)
    
    if "from alembic import op" in line:
        new_lines.append("from sqlalchemy.dialects import postgresql\n")

with open(migration_file, "w") as f:
    f.writelines(new_lines)
    
print("Migration fixed.")
