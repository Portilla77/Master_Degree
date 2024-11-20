## Funciones escalares
CREATE FUNCTION dbo.CalcularSaldoRestante (
    @SaldoActual DECIMAL(15, 2),
    @Retiro DECIMAL(15, 2)
)
RETURNS DECIMAL(15, 2)
AS
BEGIN
    RETURN @SaldoActual - @Retiro;
END;

- Calcula el saldo restante en cuentas despues de retiros
SELECT dbo.CalcularSaldoRestante(SALDO, 5000) AS SaldoRestante
FROM CUENTAS
WHERE NUMERO_CUENTA = 1;

- Calcula la antiguedad de empleados en años
CREATE FUNCTION dbo.CalcularAntiguedad (@FechaContrato DATE)
RETURNS INT
AS
BEGIN
    RETURN DATEDIFF(YEAR, @FechaContrato, GETDATE());
END;

- Haciendo uso de lo anterior:
SELECT NOMBRE, dbo.CalcularAntiguedad(FECHA_CONTRATO) AS Antiguedad
FROM EMPLEADOS;



## Funciones tabulares
- Funcion para obtener un saldo superior a un valor dado
CREATE FUNCTION dbo.CuentasConSaldoSuperior (@SaldoMinimo DECIMAL(15, 2))
RETURNS TABLE
AS
RETURN (
    SELECT NUMERO_CUENTA, SALDO
    FROM CUENTAS
    WHERE SALDO > @SaldoMinimo
);

SELECT * 
FROM dbo.CuentasConSaldoSuperior(20000);

- Funcion para listas clientes asociados con un banco particular
CREATE FUNCTION dbo.ClientesDeBanco (@SucursalID INT)
RETURNS TABLE
AS
RETURN (
    SELECT C.ID_CLIENTE, C.NOMBRE
    FROM CLIENTES C
    JOIN PRESTAMO_CLIENTE PC ON C.ID_CLIENTE = PC.ID_CLIENTE
    JOIN PRESTAMOS P ON PC.ID_PRESTAMO = P.ID_PRESTAMO
    WHERE P.ID_SUCURSAL = @SucursalID
);

SELECT * 
FROM dbo.ClientesDeBanco(1);