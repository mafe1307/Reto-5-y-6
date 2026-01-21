/*
RETO PARTE B: LABORATORIO DE PERFORMANCE
Objetivo: Comparar CROSS JOIN vs INNER JOIN
*/

-- =======================================================
-- PASO 0: PREPARACIÓN
-- =======================================================

SET STATISTICS IO ON;
SET STATISTICS TIME ON;

PRINT '>>> INICIO DEL BENCHMARK DE PERFORMANCE <<<';

-- =======================================================
-- ESCENARIO 1: CONSULTA TÓXICA (CROSS JOIN)
-- =======================================================

PRINT '--- EJECUTANDO CROSS JOIN (PRODUCTO CARTESIANO) ---';

SELECT
    c.Nombre AS Cliente,
    p.Nombre AS Producto
FROM Clientes c
CROSS JOIN Productos p;

-- 🔎 ANÁLISIS:
-- Filas = Clientes × Productos
-- No representa ventas reales
-- Alto consumo de CPU y Logical Reads

-- =======================================================
-- ESCENARIO 2: CONSULTA EFICIENTE (INNER JOIN)
-- =======================================================

PRINT '--- EJECUTANDO INNER JOIN (VENTAS REALES) ---';

SELECT
    c.Nombre  AS Cliente,
    p.Nombre  AS Producto,
    v.Fecha   AS Fecha,
    v.Cantidad
FROM Ventas v
INNER JOIN Clientes c
    ON v.ClienteID = c.ClienteID
INNER JOIN Productos p
    ON v.ProductoID = p.ProductoID;

-- 🔎 COMPARACIÓN:
-- Filas ≈ número real de ventas
-- Logical Reads significativamente menores

-- =======================================================
-- FIN
-- =======================================================

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;

PRINT '>>> FIN DEL BENCHMARK <<<';
