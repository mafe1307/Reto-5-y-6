import os
import pandas as pd

CSV_PATH = "01_data/raw/raw_sales_dump.csv"

print("📍 Directorio actual:", os.getcwd())
print("📂 ¿Existe el CSV?:", os.path.exists(CSV_PATH))

df = pd.read_csv(CSV_PATH)
print("📊 Filas leídas:", len(df))
print("🧾 Columnas:", list(df.columns))
df.head()
import pyodbc
import pandas as pd

# 1️⃣ Leer CSV
df = pd.read_csv("../01_data/raw/raw_sales_dump.csv")

# Limpieza básica
df["Cliente_Nombre"] = df["Cliente_Nombre"].str.title().str.strip()
df["Cliente_Email"] = df["Cliente_Email"].str.lower().str.strip()

# 2️⃣ Conexión SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=sqlserver;"
    "DATABASE=RetoSQL;"
    "UID=sa;"
    "PWD=StrongPassword123!;"
    "TrustServerCertificate=yes;",
    autocommit=True
)

cursor = conn.cursor()

# 3️⃣ Insertar clientes (SIN IF NOT EXISTS)
clientes = df[["Cliente_Nombre", "Cliente_Email"]].drop_duplicates()

for _, row in clientes.iterrows():
    cursor.execute("""
        INSERT INTO dbo.Clientes (Nombre, Email)
        VALUES (?, ?)
    """,
    row["Cliente_Nombre"],
    row["Cliente_Email"]
    )

print(f"✅ Clientes insertados: {len(clientes)}")

conn.close()
