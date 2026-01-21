/*
RETO PARTE B: LABORATORIO DE PERFORMANCE
Objetivo: Comparar CROSS JOIN vs INNER JOIN
*/

-- PASO 0: PREPARACIÓN
-- Activa las estadísticas para ver la "sangre" del servidor
SET STATISTICS IO ON;   -- Muestra lecturas de disco
SET STATISTICS TIME ON; -- Muestra tiempo de CPU

PRINT '>>> INICIO DEL BENCHMARK <<<';

-- =======================================================
-- ESCENARIO 1: LA CONSULTA TÓXICA (CROSS JOIN)
-- =======================================================
PRINT '--- EJECUTANDO CROSS JOIN (Producto Cartesiano) ---';

-- Esta consulta combina TODOS los clientes con TODOS los productos.
-- Si tienes 5 clientes y 5 productos, traerá 25 filas.
-- Si tienes 1 millón de clientes... bueno, ya sabes.
USE RetoSQL;
GO

SELECT
    c.Nombre AS Cliente,
    p.NombreProducto AS Producto
FROM Clientes c
CROSS JOIN Productos p;

-- PREGUNTA DE ANÁLISIS:
-- ¿Cuántos "Logical Reads" muestra la pestaña Messages?
-- SQL Server tuvo 30 logical reads para generar el resultado de la consulta CROSS JOIN.
-- ¿Por qué el número de filas es Mayor que la tabla de ventas real?
-- La tabla ventas solo contiene las ventas reales, mientras que el CROSS JOIN genera todas 
-- las combinaciones posibles entre clientes y productos, resultando en un número mucho mayor de filas.

-- =======================================================
-- ESCENARIO 2: LA CONSULTA EFICIENTE (INNER JOIN)
-- =======================================================
PRINT '--- EJECUTANDO INNER JOIN (Ventas Reales) ---';

-- Esta consulta usa la FK para unir solo lo que existe.

SELECT
    c.Nombre AS Cliente,
    p.NombreProducto AS Producto,
    v.FechaVenta,
    v.Cantidad,
    v.PrecioUnitario
FROM Ventas v
INNER JOIN Clientes c 
    ON v.ClienteID = c.ClienteID
INNER JOIN Productos p 
    ON v.ProductoID = p.ProductoID;

-- COMPARACIÓN:
-- Mira los Logical Reads aquí. Deberían ser drásticamente menores.
-- Si son mucho menores con un total de 9 logical reads para la consulta INNER JOIN.
SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
