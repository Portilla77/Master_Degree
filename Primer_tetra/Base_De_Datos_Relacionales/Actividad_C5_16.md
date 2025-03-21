
## Querys realizadas para la actividad de clase

SELECT C.NOMBRE AS Cliente, CU.NUMERO_CUENTA, CU.SALDO
FROM CLIENTES C
JOIN CUENTA_CLIENTE CC ON C.ID_CLIENTE = CC.ID_CLIENTE
JOIN CUENTAS CU ON CC.NUMERO_CUENTA = CU.NUMERO_CUENTA;

SELECT E.NOMBRE AS Banquero, C.NOMBRE AS Cliente
FROM EMPLEADOS E
JOIN CLIENTE_BANQUERO CB ON E.ID_EMPLEADO = CB.ID_EMPLEADO
JOIN CLIENTES C ON CB.ID_CLIENTE = C.ID_CLIENTE;

SELECT PP.ID_PAGO, PP.IMPORTE AS Pago, P.ID_PRESTAMO, P.IMPORTE AS ImporteTotal
FROM PAGOS_PRESTAMO PP
JOIN PRESTAMOS P ON PP.ID_PRESTAMO = P.ID_PRESTAMO;

- Creacion de vistas*/

INSERT INTO CLIENTES (ID_CLIENTE, NOMBRE, CALLE, CIUDAD)
VALUES 
(3, 'Carlos Hernández', 'Calle 3', 'Ciudad Z');

INSERT INTO CUENTAS (NUMERO_CUENTA, SALDO, FECHA_ULTIMO_ACCESO) 
VALUES 
(3, 150000, '2023-11-01'),
(4, 100000, '2023-11-05');

INSERT INTO CUENTA_CLIENTE (NUMERO_CUENTA, ID_CLIENTE, FECHA_ACCESO) 
VALUES 
(3, 3, '2023-11-01'),
(4, 3, '2023-11-05');

- Consulta anidada
SELECT C.NOMBRE AS Cliente, SUM(CU.SALDO) AS SaldoTotal
FROM CLIENTES C
JOIN CUENTA_CLIENTE CC ON C.ID_CLIENTE = CC.ID_CLIENTE
JOIN CUENTAS CU ON CC.NUMERO_CUENTA = CU.NUMERO_CUENTA
GROUP BY C.NOMBRE
HAVING SUM(CU.SALDO) > 200000;

- Generacion de vista
CREATE VIEW VISTA_CUENTAS_CLIENTES AS
SELECT 
    C.NOMBRE AS Cliente, 
    CU.NUMERO_CUENTA, 
    CU.SALDO
FROM 
    CLIENTES C
JOIN 
    CUENTA_CLIENTE CC ON C.ID_CLIENTE = CC.ID_CLIENTE
JOIN 
    CUENTAS CU ON CC.NUMERO_CUENTA = CU.NUMERO_CUENTA;

SELECT * FROM VISTA_CUENTAS_CLIENTES;

- Reunion de relaciones
SELECT C.NOMBRE AS Cliente, CU.NUMERO_CUENTA, CU.SALDO, P.ID_PRESTAMO, P.IMPORTE AS ImportePrestamo
FROM CLIENTES C
LEFT JOIN CUENTA_CLIENTE CC ON C.ID_CLIENTE = CC.ID_CLIENTE
LEFT JOIN CUENTAS CU ON CC.NUMERO_CUENTA = CU.NUMERO_CUENTA
LEFT JOIN PRESTAMO_CLIENTE PC ON C.ID_CLIENTE = PC.ID_CLIENTE
LEFT JOIN PRESTAMOS P ON PC.ID_PRESTAMO = P.ID_PRESTAMO;