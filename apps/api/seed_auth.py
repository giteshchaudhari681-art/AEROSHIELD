import uuid
from sqlalchemy.orm import Session
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.models import Operator, Role, Permission
from app.core.security import get_password_hash
from app.core.config import settings

def seed_auth():
    db = SessionLocal()
    
    # 1. Define Permissions
    perms = [
        "site:read", "site:write",
        "asset:read", "asset:write",
        "zone:read", "zone:write",
        "sensor:read", "sensor:write",
        "observation:read", "observation:write",
        "track:read", "track:write",
        "behaviour:read", "behaviour:write",
        "threat:read", "threat:write",
        "alert:read", "alert:acknowledge", "alert:write",
        "incident:read", "incident:write",
        "evidence:read", "evidence:write",
        "operator:read", "operator:write",
        "admin:manage"
    ]
    
    db_perms = []
    for p_name in perms:
        p = db.query(Permission).filter_by(name=p_name).first()
        if not p:
            p = Permission(id=str(uuid.uuid4()), name=p_name)
            db.add(p)
        db_perms.append(p)
    db.commit()
    
    # 2. Define Roles
    roles = {
        "ADMIN": perms,
        "OPERATOR": [
            "site:read", "asset:read", "zone:read", "sensor:read", "sensor:write",
            "observation:read", "observation:write", "track:read", "track:write",
            "behaviour:read", "threat:read", "alert:read", "alert:acknowledge",
            "incident:read", "incident:write", "evidence:read"
        ],
        "ANALYST": [
            "site:read", "asset:read", "zone:read", "sensor:read",
            "observation:read", "track:read", "behaviour:read", "threat:read", "evidence:read"
        ],
        "VIEWER": [
            "site:read", "asset:read", "zone:read", "sensor:read", "track:read", "alert:read"
        ]
    }
    
    db_roles = {}
    for r_name, r_perms in roles.items():
        r = db.query(Role).filter_by(name=r_name).first()
        if not r:
            r = Role(id=str(uuid.uuid4()), name=r_name)
            db.add(r)
        
        # assign perms
        r.permissions = [p for p in db_perms if p.name in r_perms]
        db.commit()
        db_roles[r_name] = r

    # 3. Create Admin Operator
    admin = db.query(Operator).filter_by(email=settings.AEROSHIELD_ADMIN_USERNAME).first()
    if not admin:
        admin = Operator(
            id=str(uuid.uuid4()),
            name="System Administrator",
            email=settings.AEROSHIELD_ADMIN_USERNAME,
            password_hash=get_password_hash(settings.AEROSHIELD_ADMIN_PASSWORD),
            active=True
        )
        db.add(admin)
        db.commit()
    
    # assign ADMIN role
    if db_roles["ADMIN"] not in admin.roles:
        admin.roles.append(db_roles["ADMIN"])
        db.commit()
        
    print("Seed Auth completed.")
    db.close()

if __name__ == "__main__":
    seed_auth()
