import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine, text
import urllib
import time
import os

# ===============================
# CONEXIÓN
# ===============================
params = urllib.parse.quote_plus(
    "DRIVER=ODBC Driver 18 for SQL Server;"
    "SERVER=localhost,1434;"
    "DATABASE=RetoSQL;"
    "UID=sa;"
    "PWD=ContraseñaFuerte123!;"
    "TrustServerCertificate=yes;"
)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}",
    fast_executemany=True
)

# ===============================
# ELT
# ===============================
def run_elt():
    print("🚀 INICIANDO ELT CON SQLALCHEMY")

    # -------- EXTRACT --------
    csv_path = os.path.join(os.path.dirname(__file__), "../../01_data/raw/raw_sales_dump.csv")
    df = pd.read_csv(csv_path)
    print(f"Filas leídas: {len(df)}")

    # -------- TRANSFORM (ligero) --------
    df["Cliente_Email"] = df["Cliente_Email"].str.lower().str.strip()
    df["Cliente_Nombre"] = df["Cliente_Nombre"].str.title().str.strip()

    # -------- LOAD (STAGING) --------
    print("📥 Cargando tabla STG_VentasRaw...")

    with engine.begin() as conn:
        conn.execute(text("IF OBJECT_ID('STG_VentasRaw','U') IS NOT NULL DROP TABLE STG_VentasRaw"))

    df.to_sql(
        "STG_VentasRaw",
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=10000
    )

    print("✅ Staging cargado")

    # -------- TRANSFORM EN SQL --------
    with engine.begin() as conn:

        print("👥 Poblando Clientes...")
        conn.execute(text("""
            INSERT INTO Clientes (Nombre, Email)
            SELECT DISTINCT
                Cliente_Nombre,
                Cliente_Email
            FROM STG_VentasRaw
            WHERE Cliente_Email NOT IN (
                SELECT Email FROM Clientes
            )
        """))

        print("📦 Poblando Productos...")
        conn.execute(text("""
            INSERT INTO Productos (NombreProducto, Categoria)
            SELECT DISTINCT
                Producto,
                Categoria
            FROM STG_VentasRaw
            WHERE NOT EXISTS (
                SELECT 1 FROM Productos p
                WHERE p.NombreProducto = STG_VentasRaw.Producto
                AND p.Categoria = STG_VentasRaw.Categoria
            )
        """))

        print("🏬 Poblando Sucursales...")
        conn.execute(text("""
            INSERT INTO Sucursales (NombreSucursal, Ciudad)
            SELECT DISTINCT
                Sucursal,
                Ciudad_Sucursal
            FROM STG_VentasRaw
            WHERE NOT EXISTS (
                SELECT 1 FROM Sucursales s
                WHERE s.NombreSucursal = STG_VentasRaw.Sucursal
                AND s.Ciudad = STG_VentasRaw.Ciudad_Sucursal
            )
        """))

        print("🧾 Poblando Ventas...")
        conn.execute(text("""
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
                r.Transaccion_ID,
                c.ClienteID,
                p.ProductoID,
                s.SucursalID,
                r.Fecha_Venta,
                r.Cantidad,
                r.Precio_Unitario
            FROM STG_VentasRaw r
            JOIN Clientes c ON r.Cliente_Email = c.Email
            JOIN Productos p ON r.Producto = p.NombreProducto
                            AND r.Categoria = p.Categoria
            JOIN Sucursales s ON r.Sucursal = s.NombreSucursal
                              AND r.Ciudad_Sucursal = s.Ciudad
        """))

    print("🎯 ELT COMPLETADO CON ÉXITO")

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    time.sleep(3)
    run_elt()
