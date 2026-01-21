/*
RETO PARTE B: LABORATORIO DE PERFORMANCE
Objetivo: Comparar CROSS JOIN vs INNER JOIN
Estudiante: Maria Fernanda Torres
Fecha: 2026-01-20
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
-- Si tienes 100 clientes y 50 productos → 5.000 filas.
-- No representa ventas reales.

SELECT
    c.Nombre AS Cliente,
    p.NombreProducto AS Producto
FROM Clientes c
CROSS JOIN Productos p;

-- PREGUNTA DE ANÁLISIS:
-- ¿Cuántos "Logical Reads" aparecen?
-- ¿Por qué el número de filas es artificialmente alto?

-- =======================================================
-- ESCENARIO 2: LA CONSULTA EFICIENTE (INNER JOIN)
-- =======================================================
PRINT '--- EJECUTANDO INNER JOIN (Ventas Reales) ---';

-- Esta consulta usa las llaves foráneas reales.

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
-- Los Logical Reads y el tiempo de CPU
-- deberían ser muchísimo menores.

SET STATISTICS IO OFF;
SET STATISTICS TIME OFF;
