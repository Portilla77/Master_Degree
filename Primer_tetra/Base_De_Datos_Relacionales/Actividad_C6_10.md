## Uso de disparadores

- Trigger
CREATE TABLE Auditoria_Cuentas (
    ID INT IDENTITY PRIMARY KEY,
    NUMERO_CUENTA INT NOT NULL,
    SALDO DECIMAL(15, 2),
    FECHA_INSERCION DATETIME DEFAULT GETDATE()
);

CREATE TRIGGER trg_InsertCuentas
ON CUENTAS
AFTER INSERT
AS
BEGIN
    INSERT INTO Auditoria_Cuentas (NUMERO_CUENTA, SALDO)
    SELECT NUMERO_CUENTA, SALDO
    FROM INSERTED;
END;

- Trigger para updatear
CREATE TABLE Auditoria_Actualizaciones (
    ID INT IDENTITY PRIMARY KEY,
    NUMERO_CUENTA INT NOT NULL,
    SALDO_ANTERIOR DECIMAL(15, 2),
    SALDO_NUEVO DECIMAL(15, 2),
    FECHA_ACTUALIZACION DATETIME DEFAULT GETDATE()
);
CREATE TRIGGER trg_UpdateCuentas
ON CUENTAS
AFTER UPDATE
AS
BEGIN
    INSERT INTO Auditoria_Actualizaciones (NUMERO_CUENTA, SALDO_ANTERIOR, SALDO_NUEVO)
    SELECT D.NUMERO_CUENTA, D.SALDO, I.SALDO
    FROM DELETED D
    JOIN INSERTED I ON D.NUMERO_CUENTA = I.NUMERO_CUENTA;
END;

- Trigger para delete
CREATE TABLE Auditoria_Eliminaciones (
    ID INT IDENTITY PRIMARY KEY,
    NUMERO_CUENTA INT NOT NULL,
    SALDO DECIMAL(15, 2),
    FECHA_ELIMINACION DATETIME DEFAULT GETDATE()
);
CREATE TRIGGER trg_DeleteCuentas
ON CUENTAS
AFTER DELETE
AS
BEGIN
    INSERT INTO Auditoria_Eliminaciones (NUMERO_CUENTA, SALDO)
    SELECT NUMERO_CUENTA, SALDO
    FROM DELETED;
END;

- Insert de cuenta
INSERT INTO CUENTAS (NUMERO_CUENTA, SALDO, FECHA_ULTIMO_ACCESO)
VALUES (1001, 5000.00, '2023-11-01');

UPDATE CUENTAS
SET SALDO = 8000.00
WHERE NUMERO_CUENTA = 1001;

DELETE FROM CUENTAS
WHERE NUMERO_CUENTA = 1001;

SELECT * FROM Auditoria_Cuentas;
SELECT * FROM Auditoria_Actualizaciones;
SELECT * FROM Auditoria_Eliminaciones;