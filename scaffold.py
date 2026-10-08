import os

dirs = [
    "apps/api/app/api/v1/endpoints",
    "apps/api/app/core",
    "apps/api/app/domain",
    "apps/api/app/infrastructure",
    "apps/api/app/schemas",
    "apps/api/app/services",
    "apps/api/tests",
    "apps/web",
    "packages/contracts",
    "ml/models",
    "ml/pipelines",
    "ml/inference",
    "ml/tests",
    "simulator",
    "infra/docker",
    "infra/scripts",
    "docs/architecture",
    "docs/adr",
    "docs/api",
    "docs/domain",
    "docs/development",
    "tests/integration",
    ".github/workflows"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

for root, _, files in os.walk("apps/api"):
    with open(os.path.join(root, "__init__.py"), "w") as f:
        pass

print("Directories created.")
