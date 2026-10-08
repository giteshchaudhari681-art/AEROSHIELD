import os

migration_file = "d:/SEVA/apps/api/alembic/versions/782cef6d998b_sensor_abstraction_expansion.py"

with open(migration_file, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "def upgrade()" in line:
        pass
    
    if "op.drop_table" in line or "op.drop_index" in line:
        if any(x in line for x in ['place', 'tabblock', 'zip_state', 'addr', 'loader_lookuptables', 'street_type_lookup', 'cousub', 'tabblock20']):
            new_lines.append(f"    # {line.strip()}\n")
            continue
            
    if "sa.Column('observation_type', sa.Enum" in line:
        new_lines.append("    observation_type = postgresql.ENUM('DETECTION', 'POSITION', 'VELOCITY', 'SIGNAL', 'THERMAL', 'ACOUSTIC', 'IDENTIFICATION', 'STATUS', name='observationtype')\n")
        new_lines.append("    observation_type.create(op.get_bind())\n")
        line = line.replace("sa.Enum('DETECTION', 'POSITION', 'VELOCITY', 'SIGNAL', 'THERMAL', 'ACOUSTIC', 'IDENTIFICATION', 'STATUS', name='observationtype')", "postgresql.ENUM('DETECTION', 'POSITION', 'VELOCITY', 'SIGNAL', 'THERMAL', 'ACOUSTIC', 'IDENTIFICATION', 'STATUS', name='observationtype', create_type=False)")
        line = line.replace("nullable=False)", "nullable=False, server_default='DETECTION')")
    
    elif "sa.Column('operational_status', sa.Enum" in line:
        new_lines.append("    sensor_status = postgresql.ENUM('ACTIVE', 'INACTIVE', 'DEGRADED', 'MAINTENANCE', 'OFFLINE', 'UNKNOWN', name='sensorstatus')\n")
        new_lines.append("    sensor_status.create(op.get_bind())\n")
        line = line.replace("sa.Enum('ACTIVE', 'INACTIVE', 'DEGRADED', 'MAINTENANCE', 'OFFLINE', 'UNKNOWN', name='sensorstatus')", "postgresql.ENUM('ACTIVE', 'INACTIVE', 'DEGRADED', 'MAINTENANCE', 'OFFLINE', 'UNKNOWN', name='sensorstatus', create_type=False)")
        line = line.replace("nullable=False)", "nullable=False, server_default='UNKNOWN')")
        
    elif "sa.Column('health_status', sa.Enum" in line:
        new_lines.append("    health_status = postgresql.ENUM('HEALTHY', 'WARNING', 'CRITICAL', 'UNKNOWN', name='sensorhealthstatus')\n")
        new_lines.append("    health_status.create(op.get_bind())\n")
        line = line.replace("sa.Enum('HEALTHY', 'WARNING', 'CRITICAL', 'UNKNOWN', name='sensorhealthstatus')", "postgresql.ENUM('HEALTHY', 'WARNING', 'CRITICAL', 'UNKNOWN', name='sensorhealthstatus', create_type=False)")
        line = line.replace("nullable=False)", "nullable=False, server_default='UNKNOWN')")

    elif "sa.Column('is_enabled'" in line:
        line = line.replace("nullable=False)", "nullable=False, server_default='true')")

    elif "sa.Column('received_at'" in line:
        line = line.replace("nullable=False)", "nullable=False, server_default=sa.text('now()'))")

    new_lines.append(line)
    
with open(migration_file, "w") as f:
    f.writelines(new_lines)
    
print("Migration fixed again.")
