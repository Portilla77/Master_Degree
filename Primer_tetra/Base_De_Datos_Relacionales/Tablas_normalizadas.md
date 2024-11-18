
## Tablas sin normalización:
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

# Recordemos que los criterios de normalizacion son:
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
No se realizaron cambios en esta tabla ya que cumple con FN1, FN2, y FN3. Todos los atributos son atómicos, y no hay dependencias parciales o transitivas

-
CREATE TABLE TIPOS_CUENTA (
    ID_TIPOCUENTA INT PRIMARY KEY,
    DESCRIPCION VARCHAR(200) NOT NULL,
    TIPO_CUENTA VARCHAR(10) NOT NULL,
	CHECK (TIPO_CUENTA in ('DEBITO','CREDITO','AHORRO'))
);

 Se eliminó el atributo ESTADO_TIPO_CUENTA de esta tabla y lo indexamos a una tabla nueva llamada SUCURSAL_TIPO_CUENTA para evitar redundancias y cumplir con FN3, ya que el estado puede depender de la relación entre sucursal y tipo de cuenta. De esta manera, se eliminan dependencias parciales y transitivas.

-
CREATE TABLE SUCURSAL_TIPO_CUENTA (
    ID_SUCURSAL INT NOT NULL,
    ID_TIPOCUENTA INT NOT NULL,
    ESTADO_TIPO_CUENTA VARCHAR(10) NOT NULL,
    PRIMARY KEY (ID_SUCURSAL, ID_TIPOCUENTA),
    FOREIGN KEY (ID_SUCURSAL) REFERENCES SUCURSALES(ID_SUCURSAL),
    FOREIGN KEY (ID_TIPOCUENTA) REFERENCES TIPOS_CUENTA(ID_TIPOCUENTA),
	CHECK (ESTADO_TIPO_CUENTA in ('ACTIVO','INACTIVO'))
);

Aplicamos FN4 al crear esta tabla para manejar la relación entre sucursales y tipos de cuenta y así evitar dependencias multivaluadas. Ahora, el estado se define en función de la combinación de sucursal y tipo de cuenta mejorando la integridad y eficiencia en el diseño de la base de datos.

-
CREATE TABLE TIPOS_PRESTAMO (
    ID_TIPOPRESTAMO INT PRIMARY KEY,
    DESCRIPCION VARCHAR(200) NOT NULL,
    TIPO_PRESTAMO VARCHAR(20) NOT NULL,
	CHECK (TIPO_PRESTAMO in ('HIPOTECARIO', 'AUTOMOVILISTICO','BANCARIO'))
);

No se realizaron cambios en esta tabla ya que TIPOS_PRESTAMO ya cumple con todos los criterios de normalización. Los datos son atómicos, sin dependencias parciales ni transitivas.

-

CREATE TABLE DIRECCION_CLIENTE (
    ID_DIRECCION INT PRIMARY KEY,
    CALLE VARCHAR(40) NOT NULL,
    NUMERO INT NOT NULL,
    COLONIA VARCHAR(40) NOT NULL
);

Aplicamos FN2 al separar la información de dirección en una tabla independiente para evitar redundancias. Ahora DIRECCION_CLIENTE es una entidad independiente que se relaciona con CLIENTES, eliminando dependencias parciales.
-

CREATE TABLE CLIENTES (
    ID_CLIENTE INT PRIMARY KEY,
    NOMBRE VARCHAR(100) NOT NULL,
    TELEFONO VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL,
    ID_DIRECCION INT NOT NULL,
    FOREIGN KEY (ID_DIRECCION) REFERENCES DIRECCION_CLIENTE(ID_DIRECCION)
);

Aplicamos FN2 y FN3 al mover la dirección a la tabla DIRECCION_CLIENTE, eliminando así las dependencias transitivas. Esto asegura que nuestra tabla cumpla con los criterios de normalización.

-
CREATE TABLE COLABORADOR (
    ID_COLABORADOR INT PRIMARY KEY,
    NOMBRE VARCHAR(100) NOT NULL,
    TELEFONO VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL,
    ID_SUCURSAL INT NOT NULL,
    FOREIGN KEY (ID_SUCURSAL) REFERENCES SUCURSALES(ID_SUCURSAL)
);

 No se realizaron cambios en esta tabla ya que nuestra tabla COLABORADOR ya cumple con normaliación. Todos los datos son atómicos, y no existen dependencias parciales ni transitivas.

-

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

Aplicamos FN3 al estructurar ID_COLABORADOR como clave externa, asegurando que todos los atributos no clave dependan únicamente de la clave primaria. Esto elimina dependencias transitivas y asi, con normalización.

-

CREATE TABLE TIPO_CLIENTE (
    ID_TIPO_CLIENTE INT PRIMARY KEY,
    TIPO VARCHAR(50) NOT NULL CHECK (TIPO in ('EMPRESARIAL', 'PERSONAL'))
);

Aplicamos FN3 al crear la tabla TIPO_CLIENTE, lo cual permite que CUENTA se refiera a esta tabla para definir el tipo de cliente. Esto elimina dependencias transitivas en la tabla CUENTA y nuestra tabla cumple con normalización.

-

CREATE TABLE CUENTA (
    NUMERO_CUENTA INT PRIMARY KEY,
    ID_CLIENTE INT NOT NULL,
    ID_TIPOCUENTA INT NOT NULL,
    ID_PRODUCTO_BANCARIO INT NOT NULL,
    SALDO DECIMAL(15, 2) NOT NULL,
    FECHA_APERTURA DATE NOT NULL,
    ID_TIPO_CLIENTE INT NOT NULL,
    FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID_CLIENTE),
    FOREIGN KEY (ID_TIPOCUENTA) REFERENCES TIPOS_CUENTA(ID_TIPOCUENTA),
    FOREIGN KEY (ID_PRODUCTO_BANCARIO) REFERENCES PRODUCTO_BANCARIO(ID_PRODUCTO_BANCARIO),
    FOREIGN KEY (ID_TIPO_CLIENTE) REFERENCES TIPO_CLIENTE(ID_TIPO_CLIENTE)
);

Aplicamos FN3 al referenciar el tipo de cliente mediante ID_TIPO_CLIENTE, evitando dependencias transitivas. Esto asegura que los atributos dependan únicamente de la clave primaria.

-

CREATE TABLE PRESTAMOS (
    ID_PRESTAMO INT PRIMARY KEY,
    ID_TIPOPRESTAMO INT NOT NULL,
    ID_CLIENTE INT NOT NULL,
    TASA_INTERES DECIMAL (5,2) NOT NULL,
    MONTO DECIMAL(10,2) NOT NULL,
    FECHA_INICIO DATE,
    FECHA_FIN DATE,
    FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTES(ID_CLIENTE),
    FOREIGN KEY (ID_TIPOPRESTAMO) REFERENCES TIPOS_PRESTAMO(ID_TIPOPRESTAMO)
);

No se realizaron cambios adicionales en esta tabla. PRESTAMOS ya cumple con normalización ya que sus atributos son atómicos y dependen solo de la clave primaria sin dependencias transitivas.

-

CREATE TABLE OPERACION_BANCARIA (
    ID_OPERACION INT PRIMARY KEY,
    NUMERO_CUENTA INT NOT NULL,
    TIPO_OPERACION VARCHAR(50) NOT NULL,
    IMPORTE DECIMAL(10,2) NOT NULL,
    FECHA_OPERACION DATETIME,
    FOREIGN KEY (NUMERO_CUENTA) REFERENCES CUENTA(NUMERO_CUENTA),
	CHECK (TIPO_OPERACION in ('DEPOSITO', 'RETIRO','PAGO','TRANSACCION'))
);

Esta tabla ya cumple con normalización, ya que sus datos son atómicos y dependen solo de la clave primaria.

-

CREATE TABLE CUENTA_PRODUCTO (
    NUMERO_CUENTA INT NOT NULL,
    ID_PRODUCTO_BANCARIO INT NOT NULL,
    PRIMARY KEY (NUMERO_CUENTA, ID_PRODUCTO_BANCARIO),
    FOREIGN KEY (NUMERO_CUENTA) REFERENCES CUENTA(NUMERO_CUENTA),
    FOREIGN KEY (ID_PRODUCTO_BANCARIO) REFERENCES PRODUCTO_BANCARIO(ID_PRODUCTO_BANCARIO)
);

 Aplicamos FN4 al crear esta tabla para manejar la relación entre CUENTA y PRODUCTO_BANCARIO, eliminando dependencias multivaluadas.
