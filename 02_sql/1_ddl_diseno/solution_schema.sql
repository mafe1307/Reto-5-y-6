/*
RETO PARTE A: DISEÑO DEL ESQUEMA RELACIONAL
Estudiante: Maria Fernanda Torres
Fecha: 2026-01-18

INSTRUCCIONES:
1.  Crea la base de datos si no existe.
2.  Define las tablas maestras primero (las que no dependen de nadie).
3.  Define las tablas transaccionales al final.
*/


IF DB_ID('RetoSQL') IS NULL
BEGIN
    CREATE DATABASE RetoSQL;
END
GO

USE RetoSQL;
GO

IF OBJECT_ID('dbo.Clientes', 'U') IS NOT NULL
    DROP TABLE dbo.Clientes;
GO

CREATE TABLE dbo.Clientes (
    ClienteID INT IDENTITY(1,1) PRIMARY KEY,
    Nombre VARCHAR(100),
    Email VARCHAR(100),
    Direccion VARCHAR(100)
);
GO

SELECT COUNT(*) AS TotalClientes FROM dbo.Clientes;

SELECT 
    DB_NAME()        AS BaseActual,
    SCHEMA_NAME()    AS EsquemaActual,
    SYSTEM_USER      AS Usuario;
