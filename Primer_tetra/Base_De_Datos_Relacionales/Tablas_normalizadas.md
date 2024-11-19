# Tablas sin normalización:
USE DATA_BANK_JL;

-- Creacion de tablas Banco DATA_BANK_JL | En Orden de Dependencias

CREATE TABLE SUCURSALES (
    ID_SUCURSAL INT PRIMARY KEY,
    NOMBRE VARCHAR(100) NOT NULL,
    DIRECCION VARCHAR(200) NOT NULL,
    TELEFONO VARCHAR(15)
);

CREATE TABLE TIPOS_CUENTA (
    ID_TIPOCUENTA INT PRIMARY KEY,
    DESCRIPCION VARCHAR(200) NOT NULL,
    ESTADO_TIPO_CUENTA VARCHAR(10) NOT NULL,
    TIPO_CUENTA VARCHAR(10) NOT NULL,
    CHECK (ESTADO_TIPO_CUENTA in ('ACTIVO','INACTIVO')),
    CHECK (TIPO_CUENTA in ('DEBITO','CREDITO','AHORRO'))
);

CREATE TABLE TIPOS_PRESTAMO (
    ID_TIPOPRESTAMO INT PRIMARY KEY,
    DESCRIPCION VARCHAR(200) NOT NULL,
    TIPO_PRESTAMO VARCHAR(20) NOT NULL,
    CHECK (TIPO_PRESTAMO in ('HIPOTECARIO', 'AUTOMOVILISTICO','BANCARIO'))
);

CREATE TABLE DIRECCION_CLIENTE (
    ID_DIRECCION INT PRIMARY KEY,
    ID_CLIENTE INT NOT NULL,
    CALLE VARCHAR(40) NOT NULL,
    NUMERO INT NOT NULL,
    COLONIA VARCHAR(40) NOT NULL
);

CREATE TABLE CLIENTES (
    ID_CLIENTE INT PRIMARY KEY,
    NOMBRE VARCHAR(100) NOT NULL,
    TELEFONO VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL,
    ID_DIRECCION INT NOT NULL,
    FOREIGN KEY (ID_DIRECCION) REFERENCES DIRECCION_CLIENTE(ID_DIRECCION)
);

CREATE TABLE COLABORADOR (
    ID_COLABORADOR INT PRIMARY KEY,
    NOMBRE VARCHAR(100) NOT NULL,
    TELEFONO VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL,
    ID_SUCURSAL INT NOT NULL,
    FOREIGN KEY (ID_SUCURSAL) REFERENCES SUCURSALES(ID_SUCURSAL)
);

CREATE TABLE PRODUCTO_BANCARIO (
    ID_PRODUCTO_BANCARIO INT PRIMARY KEY,
    NOMBRE_PRODUCTO VARCHAR(200) NOT NULL,
    TIPO_PRODUCTO VARCHAR(50) NOT NULL,
    ESTADO_PRODUCTO VARCHAR(50) NOT NULL,
    ID_COLABORADOR INT NOT NULL,
    FOREIGN KEY (ID_COLABORADOR) REFERENCES COLABORADOR(ID_COLABORADOR),
    CHECK (TIPO_PRODUCTO in ('PRESTAMOS','TRANSACCION')),
    CHECK (ESTADO_PRODUCTO in ('TRUE','FALSE'))
);

CREATE TABLE CUENTA (
    NUMERO_CUENTA INT PRIMARY KEY,
    ID_CLIENTE INT NOT NULL,
    ID_TIPOCUENTA INT NOT NULL,
    ID_PRODUCTO_BANCARIO INT NOT NULL,
    SALDO DECIMAL(15, 2) NOT NULL,
    FECHA_APERTURA DATE NOT NULL,
    TIPO_CLIENTE VARCHAR(50) NOT NULL,
    FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID_CLIENTE),
    FOREIGN KEY (ID_TIPOCUENTA) REFERENCES TIPOS_CUENTA(ID_TIPOCUENTA),
    FOREIGN KEY (ID_PRODUCTO_BANCARIO) REFERENCES PRODUCTO_BANCARIO(ID_PRODUCTO_BANCARIO),
    CHECK (TIPO_CLIENTE in ('EMPRESARIAL', 'PERSONAL'))
);

CREATE TABLE PRESTAMOS (
    ID_PRESTAMO INT PRIMARY KEY,
    ID_TIPOPRESTAMO INT NOT NULL,
    ID_CLIENTE INT NOT NULL,
    TASA_INTERES DECIMAL (2,2) NOT NULL,
    MONTO DECIMAL(10,2) NOT NULL,
    FECHA_INICIO DATE,
    FECHA_FIN DATE,
    FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID_CLIENTE),
    FOREIGN KEY (ID_TIPOPRESTAMO) REFERENCES TIPOS_PRESTAMO(ID_TIPOPRESTAMO)
);

CREATE TABLE OPERACION_BANCARIA (
    ID_OPERACION INT PRIMARY KEY,
    NUMERO_CUENTA INT NOT NULL,
    TIPO_OPERACION VARCHAR(50) NOT NULL,
    IMPORTE DECIMAL(10,2) NOT NULL,
    FECHA_OPERACION DATETIME,
    CHECK (TIPO_OPERACION in ('DEPOSITO', 'RETIRO','PAGO','TRANSACCION'))
);

CREATE TABLE CUENTA_PRODUCTO (
    NUMERO_CUENTA INT NOT NULL,
    ID_PRODUCTO_BANCARIO INT NOT NULL,
    FOREIGN KEY (NUMERO_CUENTA) REFERENCES CUENTA(NUMERO_CUENTA),
    FOREIGN KEY (ID_PRODUCTO_BANCARIO) REFERENCES PRODUCTO_BANCARIO(ID_PRODUCTO_BANCARIO),
    PRIMARY KEY (NUMERO_CUENTA, ID_PRODUCTO_BANCARIO)
);

## Recordemos que los criterios de normalizacion son:
- Primera Forma Normal (FN1):

Una relación está en la Primera Forma Normal (FN1) si, y solo si, todos los atributos de la relación contienen valores atómicos. Esto significa que no deben existir conjuntos de datos repetitivos o múltiples valores en una sola celda de una tabla. Cada columna debe contener un único valor indivisible.

- Segunda Forma Normal (FN2):

Una relación está en la Segunda Forma Normal (FN2) si, y solo si, está en FN1 y todos los atributos no clave dependen completamente de la clave primaria, es decir, no deben existir dependencias parciales. Esto se aplica principalmente a tablas con claves primarias compuestas.

- Tercera Forma Normal (FN3):

Una relación está en la Tercera Forma Normal (FN3) si, y solo si, está en FN2 y no hay dependencias transitivas entre los atributos no clave y la clave primaria. En otras palabras, ningún atributo no clave debe depender de otro atributo no clave.

- Cuarta Forma Normal (FN4):

Una relación está en la Cuarta Forma Normal (FN4) si, y solo si, está en FN3 y no contiene dependencias multivaluadas. Las dependencias multivaluadas ocurren cuando un atributo no clave depende de un conjunto de valores de otro atributo no clave, lo que puede dar lugar a redundancias.

- Quinta Forma Normal (FN5):

Una relación está en la Quinta Forma Normal (FN5) si, y solo si, está en FN4 y no contiene dependencias de reunión (o "join dependencies") no triviales. Esto significa que no debe ser posible dividir la tabla en dos o más tablas que se puedan unir nuevamente para formar la tabla original sin pérdida de información. La FN5 se aplica cuando hay relaciones complejas entre varios atributos y es poco común en la práctica.

# Aplicación de los criterios de normalización a nuestras tablas:


CREATE TABLE SUCURSALES (
    ID_SUCURSAL INT PRIMARY KEY,
    NOMBRE VARCHAR(100) NOT NULL,
    DIRECCION VARCHAR(200) NOT NULL,
    TELEFONO VARCHAR(15)
);

- Justificación: Como ya cumple con FN1, FN2, y FN3. Todos los atributos son atómicos, y no hay dependencias parciales o transitivas no aplicamos cambios.


CREATE TABLE TIPOS_CUENTA (
    ID_TIPOCUENTA INT PRIMARY KEY,
    DESCRIPCION VARCHAR(200) NOT NULL,
    TIPO_CUENTA VARCHAR(10) NOT NULL CHECK (TIPO_CUENTA IN ('DEBITO', 'CREDITO', 'AHORRO'))
);

- Justificación: Se eliminó el atributo ESTADO_TIPO_CUENTA de esta tabla ya que el estado puede depender de la relación entre sucursal y tipo de cuenta. De esta manera, se eliminan dependencias parciales y transitivas.


CREATE TABLE TIPOS_PRESTAMO (
    ID_TIPOPRESTAMO INT PRIMARY KEY,
    DESCRIPCION VARCHAR(200) NOT NULL,
    TIPO_PRESTAMO VARCHAR(20) NOT NULL,
	CHECK (TIPO_PRESTAMO in ('HIPOTECARIO', 'AUTOMOVILISTICO','BANCARIO'))
);

- Justificación: No se realizaron cambios en esta tabla ya que TIPOS_PRESTAMO ya cumple con todos los criterios de normalización. Los datos son atómicos, sin dependencias parciales ni transitivas.


CREATE TABLE DIRECCION_CLIENTE (
    ID_DIRECCION INT PRIMARY KEY,
    CALLE VARCHAR(40) NOT NULL,
    NUMERO INT NOT NULL,
    COLONIA VARCHAR(40) NOT NULL
);

- Justificación: Aplicamos FN2 al separar la información de dirección en una tabla independiente para evitar redundancias. Ahora DIRECCION_CLIENTE es una entidad independiente que se relaciona con CLIENTES, eliminando dependencias parciales.


CREATE TABLE CLIENTES (
    ID_CLIENTE INT PRIMARY KEY,
    NOMBRE VARCHAR(100) NOT NULL,
    TELEFONO VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL,
    ID_DIRECCION INT NOT NULL,
    FOREIGN KEY (ID_DIRECCION) REFERENCES DIRECCION_CLIENTE(ID_DIRECCION)
);


- Justificación: Aplicamos FN2 y FN3 al mover la dirección a la tabla DIRECCION_CLIENTE, eliminando así las dependencias transitivas. Esto asegura que nuestra tabla cumpla con los criterios de normalización.


CREATE TABLE COLABORADOR (
    ID_COLABORADOR INT PRIMARY KEY,
    NOMBRE VARCHAR(100) NOT NULL,
    TELEFONO VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL,
    ID_SUCURSAL INT NOT NULL,
    FOREIGN KEY (ID_SUCURSAL) REFERENCES SUCURSALES(ID_SUCURSAL)
);

- Justificación: No se realizaron cambios en esta tabla ya que nuestra tabla COLABORADOR ya cumple con normaliación. Todos los datos son atómicos, y no existen dependencias parciales ni transitivas.


CREATE TABLE PRODUCTO_BANCARIO (
    ID_PRODUCTO_BANCARIO INT PRIMARY KEY,
    NOMBRE_PRODUCTO VARCHAR(200) NOT NULL,
    TIPO_PRODUCTO VARCHAR(50) NOT NULL CHECK (TIPO_PRODUCTO IN ('PRESTAMOS', 'TRANSACCION')),
    ESTADO_PRODUCTO VARCHAR(10) NOT NULL CHECK (ESTADO_PRODUCTO IN ('ACTIVO', 'INACTIVO')),
    ID_COLABORADOR INT NOT NULL,
    FOREIGN KEY (ID_COLABORADOR) REFERENCES COLABORADOR(ID_COLABORADOR)
);

- Justificación: Aplicamos FN3 al estructurar ID_COLABORADOR como clave externa, asegurando que todos los atributos no clave dependan únicamente de la clave primaria. Esto elimina dependencias transitivas y asi, con normalización.


CREATE TABLE TIPO_CLIENTE (
    ID_TIPO_CLIENTE INT PRIMARY KEY,
    TIPO VARCHAR(50) NOT NULL CHECK (TIPO in ('EMPRESARIAL', 'PERSONAL'))
);

- Justificación: Aplicamos FN3 al crear la tabla TIPO_CLIENTE, lo cual permite que CUENTA se refiera a esta tabla para definir el tipo de cliente. Esto elimina dependencias transitivas en la tabla CUENTA y nuestra tabla cumple con normalización.


CREATE TABLE CUENTA (
    NUMERO_CUENTA INT PRIMARY KEY,
    ID_CLIENTE INT NOT NULL,
    ID_TIPOCUENTA INT NOT NULL,
    ID_PRODUCTO_BANCARIO INT NOT NULL,
    SALDO DECIMAL(15, 2) NOT NULL,
    FECHA_APERTURA DATE NOT NULL,
    ESTADO_CUENTA VARCHAR(10) NOT NULL CHECK (ESTADO_CUENTA IN ('ACTIVO', 'INACTIVO')),
    FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID_CLIENTE),
    FOREIGN KEY (ID_TIPOCUENTA) REFERENCES TIPOS_CUENTA(ID_TIPOCUENTA),
    FOREIGN KEY (ID_PRODUCTO_BANCARIO) REFERENCES PRODUCTO_BANCARIO(ID_PRODUCTO_BANCARIO)
);

- Justificacion: Aplicamos FN3 al referenciar el tipo de cliente mediante ID_TIPO_CLIENTE, evitando dependencias transitivas. Esto asegura que los atributos dependan únicamente de la clave primaria.


CREATE TABLE PRESTAMOS (
    ID_PRESTAMO INT PRIMARY KEY,
    ID_TIPOPRESTAMO INT NOT NULL,
    ID_CLIENTE INT NOT NULL,
    TASA_INTERES DECIMAL(5,2) NOT NULL,
    MONTO DECIMAL(10,2) NOT NULL,
    FECHA_INICIO DATE NOT NULL,
    FECHA_FIN DATE NOT NULL,
    FOREIGN KEY (ID_TIPOPRESTAMO) REFERENCES TIPO_PRESTAMO(ID_TIPOPRESTAMO),
    FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID_CLIENTE)
);

- Justificacion: Cumple con normalización ya que sus atributos son atómicos y dependen solo de la clave primaria sin dependencias transitivas.


CREATE TABLE TIPO_PRESTAMO (
    ID_TIPOPRESTAMO INT PRIMARY KEY,
    TIPO_PRESTAMO VARCHAR(20) NOT NULL,
    DESCRIPCION VARCHAR(200) NOT NULL
);

- Justificación: Maneja los diferentes tipos de préstamos evitando redudancias y cumpliendo con los criterios de normalizacion, ya que sin ella, no se cumplia FN1


CREATE TABLE SUCURSALES (
    ID_SUCURSAL INT PRIMARY KEY,
    NOMBRE VARCHAR(100) NOT NULL,
    DIRECCION VARCHAR(200) NOT NULL,
    TELEFONO VARCHAR(15)
);

- Justificación: Esta tabla cumple con FN1, FN2, y FN3. No se realizaron cambios, ya que no tiene dependencias parciales ni transitivas. Mantiene una relación 1
con COLABORADOR.


CREATE TABLE TIPOS_CUENTA (
    ID_TIPOCUENTA INT PRIMARY KEY,
    DESCRIPCION VARCHAR(200) NOT NULL,
    TIPO_CUENTA VARCHAR(10) NOT NULL CHECK (TIPO_CUENTA IN ('DEBITO', 'CREDITO', 'AHORRO'))
);

- Justificación: Se eliminó el atributo ESTADO_TIPO_CUENTA, ya que su estado puede gestionarse en otras tablas relacionadas. Relación 1
con CUENTA.


CREATE TABLE CLIENTES (
    ID_CLIENTE INT PRIMARY KEY,
    NOMBRE VARCHAR(100) NOT NULL,
    TELEFONO VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL,
    ID_DIRECCION INT NOT NULL,
    FOREIGN KEY (ID_DIRECCION) REFERENCES DIRECCION_CLIENTE(ID_DIRECCION)
);

- Justificación: Relación 1
con CUENTA. Se movió la dirección a una tabla independiente (DIRECCION_CLIENTE) para evitar redundancia y cumplir con FN2.


CREATE TABLE DIRECCION_CLIENTE (
    ID_DIRECCION INT PRIMARY KEY,
    CALLE VARCHAR(40) NOT NULL,
    NUMERO INT NOT NULL,
    COLONIA VARCHAR(40) NOT NULL
);

- Justificación: Esta tabla permite manejar direcciones de clientes. Cumple con FN2 y FN3 al separar atributos dependientes de la dirección en una tabla independiente.


CREATE TABLE COLABORADOR (
    ID_COLABORADOR INT PRIMARY KEY,
    NOMBRE VARCHAR(100) NOT NULL,
    TELEFONO VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL,
    ID_SUCURSAL INT NOT NULL,
    FOREIGN KEY (ID_SUCURSAL) REFERENCES SUCURSALES(ID_SUCURSAL)
);

- Justificación: Cumple FN3. Relación 1
con PRODUCTO_BANCARIO.


CREATE TABLE PRODUCTO_BANCARIO (
    ID_PRODUCTO_BANCARIO INT PRIMARY KEY,
    NOMBRE_PRODUCTO VARCHAR(200) NOT NULL,
    TIPO_PRODUCTO VARCHAR(50) NOT NULL CHECK (TIPO_PRODUCTO IN ('PRESTAMOS', 'TRANSACCION')),
    ESTADO_PRODUCTO VARCHAR(10) NOT NULL CHECK (ESTADO_PRODUCTO IN ('ACTIVO', 'INACTIVO')),
    ID_COLABORADOR INT NOT NULL,
    FOREIGN KEY (ID_COLABORADOR) REFERENCES COLABORADOR(ID_COLABORADOR)
);

- Justificación: Mantiene relación 1
con CUENTA.


CREATE TABLE CUENTA (
    NUMERO_CUENTA INT PRIMARY KEY,
    ID_CLIENTE INT NOT NULL,
    ID_TIPOCUENTA INT NOT NULL,
    ID_PRODUCTO_BANCARIO INT NOT NULL,
    SALDO DECIMAL(15, 2) NOT NULL,
    FECHA_APERTURA DATE NOT NULL,
    ESTADO_CUENTA VARCHAR(10) NOT NULL CHECK (ESTADO_CUENTA IN ('ACTIVO', 'INACTIVO')),
    FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID_CLIENTE),
    FOREIGN KEY (ID_TIPOCUENTA) REFERENCES TIPOS_CUENTA(ID_TIPOCUENTA),
    FOREIGN KEY (ID_PRODUCTO_BANCARIO) REFERENCES PRODUCTO_BANCARIO(ID_PRODUCTO_BANCARIO)
);

- Justificación: Incluye estado de cuenta para simplificar el diseño. Relación 1
con OPERACION_BANCARIA.


CREATE TABLE TIPO_PRESTAMO (
    ID_TIPOPRESTAMO INT PRIMARY KEY,
    TIPO_PRESTAMO VARCHAR(20) NOT NULL,
    DESCRIPCION VARCHAR(200) NOT NULL
);

- Justificación: Maneja los diferentes tipos de préstamos. Relación 1
con PRESTAMOS.


CREATE TABLE PRESTAMOS (
    ID_PRESTAMO INT PRIMARY KEY,
    ID_TIPOPRESTAMO INT NOT NULL,
    ID_CLIENTE INT NOT NULL,
    TASA_INTERES DECIMAL(5,2) NOT NULL,
    MONTO DECIMAL(10,2) NOT NULL,
    FECHA_INICIO DATE NOT NULL,
    FECHA_FIN DATE NOT NULL,
    FOREIGN KEY (ID_TIPOPRESTAMO) REFERENCES TIPO_PRESTAMO(ID_TIPOPRESTAMO),
    FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID_CLIENTE)
);

- Justificación: Relación N:1 con TIPO_PRESTAMO y CLIENTES para cumplir con FN1


CREATE TABLE OPERACION_BANCARIA (
    ID_OPERACION INT PRIMARY KEY,
    NUMERO_CUENTA INT NOT NULL,
    TIPO_OPERACION VARCHAR(50) NOT NULL CHECK (TIPO_OPERACION IN ('DEPOSITO', 'RETIRO', 'PAGO', 'TRANSACCION')),
    IMPORTE DECIMAL(10,2) NOT NULL,
    FECHA_OPERACION DATETIME NOT NULL,
    FOREIGN KEY (NUMERO_CUENTA) REFERENCES CUENTA(NUMERO_CUENTA)
);

- Justificación: Esta tabla ya cumple con normalización, ya que sus datos son atómicos y dependen solo de la clave primaria.
