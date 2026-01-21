import pyodbc
import pandas as pd
import os
import time

# ===============================
# CONFIGURACIÓN
# ===============================
DB_HOST = os.getenv("DB_HOST", "localhost,1434")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASS = os.getenv("DB_PASS", "ContraseñaFuerte123!")
DB_NAME = "RetoSQL"

# Ruta del CSV (relativa al directorio raíz del proyecto)
CSV_PATH = os.path.join(os.path.dirname(__file__), "../../01_data/raw/raw_sales_dump.csv")

# ===============================
# CONEXIÓN SQL SERVER
# ===============================
def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={DB_HOST};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASS};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str, autocommit=True)

# ===============================
# PROCESO ELT
# ===============================
def run_elt():
    print("🚀 INICIANDO ELT")

    # ---------------------------
    # EXTRACT
    # ---------------------------
    print("📂 Leyendo CSV...")
    df = pd.read_csv(CSV_PATH)

    print(f"✅ Filas leídas: {len(df)}")

    # ---------------------------
    # TRANSFORM
    # ---------------------------
    print("🧹 Normalizando datos...")

    df["Cliente_Email"] = df["Cliente_Email"].str.lower().str.strip()
    df["Cliente_Nombre"] = df["Cliente_Nombre"].str.title().str.strip()

    df["Producto"] = df["Producto"].str.strip()
    df["Categoria"] = df["Categoria"].str.strip()

    df["Sucursal"] = df["Sucursal"].str.strip()
    df["Ciudad_Sucursal"] = df["Ciudad_Sucursal"].str.strip()

    # ---------------------------
    # LOAD
    # ---------------------------
    conn = get_connection()
    cursor = conn.cursor()

    # ===========================
    # CLIENTES
    # ===========================
    print("👥 Cargando Clientes...")
    clientes = df[["Cliente_Nombre", "Cliente_Email"]].drop_duplicates()

    for _, row in clientes.iterrows():
        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM Clientes WHERE Email = ?
            )
            INSERT INTO Clientes (Nombre, Email)
            VALUES (?, ?)
        """, row.Cliente_Email, row.Cliente_Nombre, row.Cliente_Email)

    # ===========================
    # PRODUCTOS
    # ===========================
    print("📦 Cargando Productos...")
    productos = df[["Producto", "Categoria"]].drop_duplicates()

    for _, row in productos.iterrows():
        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM Productos 
                WHERE NombreProducto = ? AND Categoria = ?
            )
            INSERT INTO Productos (NombreProducto, Categoria)
            VALUES (?, ?)
        """, row.Producto, row.Categoria, row.Producto, row.Categoria)

    # ===========================
    # SUCURSALES
    # ===========================
    print("🏬 Cargando Sucursales...")
    sucursales = df[["Sucursal", "Ciudad_Sucursal"]].drop_duplicates()

    for _, row in sucursales.iterrows():
        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM Sucursales 
                WHERE NombreSucursal = ? AND Ciudad = ?
            )
            INSERT INTO Sucursales (NombreSucursal, Ciudad)
            VALUES (?, ?)
        """, row.Sucursal, row.Ciudad_Sucursal, row.Sucursal, row.Ciudad_Sucursal)

    # ===========================
    # VENTAS
    # ===========================
    print("🧾 Cargando Ventas...")
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO Ventas (
                TransaccionID,
                ClienteID,
                ProductoID,
                SucursalID,
                FechaVenta,
                Cantidad,
                PrecioUnitario
            )
            SELECT
                ?,
                c.ClienteID,
                p.ProductoID,
                s.SucursalID,
                ?,
                ?,
                ?
            FROM Clientes c
            JOIN Productos p 
                ON p.NombreProducto = ? AND p.Categoria = ?
            JOIN Sucursales s
                ON s.NombreSucursal = ? AND s.Ciudad = ?
            WHERE c.Email = ?
        """,
        row.Transaccion_ID,
        row.Fecha_Venta,
        row.Cantidad,
        row.Precio_Unitario,
        row.Producto,
        row.Categoria,
        row.Sucursal,
        row.Ciudad_Sucursal,
        row.Cliente_Email
        )

    conn.close()
    print("✅ ELT FINALIZADO CORRECTAMENTE")

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    time.sleep(5)  # espera SQL Server
    run_elt()
