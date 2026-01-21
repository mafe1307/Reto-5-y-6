/*
RETO PARTE A: DISEÑO DEL ESQUEMA RELACIONAL
Estudiante: Maria Fernanda Torres
Fecha: 2026-01-20

INSTRUCCIONES:
1.  Crea la base de datos si no existe.
2.  Define las tablas maestras primero (las que no dependen de nadie).
3.  Define las tablas transaccionales al final.
*/

CREATE DATABASE RetoSQL;
GO
USE RetoSQL;
GO

-- =======================================================
-- 1. TABLAS MAESTRAS (Clientes, Productos, Sucursales)
-- =======================================================

-- Tabla Clientes
CREATE TABLE Clientes (
    ClienteID INT IDENTITY(1,1) PRIMARY KEY,
    Nombre VARCHAR(150) NOT NULL,
    Email VARCHAR(150) UNIQUE NOT NULL
);

-- Tabla Productos
CREATE TABLE Productos (
    ProductoID INT IDENTITY(1,1) PRIMARY KEY,
    NombreProducto VARCHAR(150) NOT NULL,
    Categoria VARCHAR(100) NOT NULL
);

-- Tabla Sucursales
CREATE TABLE Sucursales (
    SucursalID INT IDENTITY(1,1) PRIMARY KEY,
    NombreSucursal VARCHAR(150) NOT NULL,
    Ciudad VARCHAR(100) NOT NULL
);

-- =======================================================
-- 2. TABLA TRANSACCIONAL (Ventas)
-- =======================================================

CREATE TABLE Ventas (
    VentaID INT IDENTITY(1,1) PRIMARY KEY,
    TransaccionID INT NOT NULL,
    FechaVenta DATE NOT NULL,
    Cantidad INT NOT NULL,
    PrecioUnitario FLOAT NOT NULL,

    -- LLAVES FORÁNEAS (La magia de la relación)
    ClienteID INT,
    ProductoID INT,
    SucursalID INT,

    CONSTRAINT FK_Ventas_Clientes 
        FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID),

    CONSTRAINT FK_Ventas_Productos 
        FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID),

    CONSTRAINT FK_Ventas_Sucursales 
        FOREIGN KEY (SucursalID) REFERENCES Sucursales(SucursalID)
);
