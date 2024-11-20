## Uso de transacciones usando la DB Bank
BEGIN TRANSACTION;

-- Restar 1000 al saldo de la cuenta 1
UPDATE CUENTAS
SET SALDO = SALDO - 1000
WHERE NUMERO_CUENTA = 1;

-- Agregar 1000 al saldo de la cuenta 2
UPDATE CUENTAS
SET SALDO = SALDO + 1000
WHERE NUMERO_CUENTA = 2;

COMMIT;

--ROLLBACK;
