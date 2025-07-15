<h1 align="center">Reporte de Estrategia con enfoque a teoría de Juegos aplicado a Conecta 4</h1>

<p align="center">
  Alumno: Jorge Ramón Flores Portilla<br>
  Matrícula: 1550162<br>
  Maestro: Jose Anastacio Hernandez Saldaña<br>
  Materia: Inteligencia Artificial
</p>

<h3 align="center">Introducción</h3>

Conecta 4 es un juego de estrategia abstracta para dos jugadores que combina análisis táctico, planificación secuencial y anticipación de movimientos adversarios. Su dinámica consiste en alinear cuatro fichas del mismo color de forma consecutiva, ya sea en línea horizontal, vertical o diagonal, dentro de una cuadrícula de 7 columnas por 6 filas.

Cada jugador, en su turno, deja caer una ficha desde la parte superior de una de las columnas. La ficha se desliza hacia abajo ocupando la celda vacía más baja de esa columna. Esta simple mecánica introduce una dimensión estratégica profunda: los movimientos no solo afectan el turno actual, sino que también condicionan las posibilidades futuras del oponente y del propio jugador.

Aunque el juego parece sencillo en apariencia, es matemáticamente complejo y ha sido completamente resuelto por computadoras. Se ha demostrado que, con juego perfecto, el primer jugador (jugador inicial) puede forzar una victoria, lo que convierte a Conecta 4 en un referente clásico dentro de los juegos deterministas de suma cero.

---

#### La primera jugada podría garantizar victoria

En 1988, el investigador James D. Allen, y posteriormente Victor Allis, desarrollaron algoritmos de búsqueda y poda del árbol de decisiones de Conecta 4, demostrando que:

Si el primer jugador coloca su ficha en la columna central (columna 4) y ambos jugadores juegan de forma óptima, el primer jugador puede forzar una victoria.

Esta conclusión se basa en el hecho de que Conecta 4 es un juego finito, es decir, tiene un número limitado de posiciones posibles (aunque bastante grande: más de 4 billones). Esto permitió a las computadoras explorar exhaustivamente todas las secuencias de movimientos posibles (búsqueda completa en el árbol de juego). Al analizar todas las posiciones posibles desde la jugada inicial en la columna central, los investigadores encontraron que:

- El control temprano del centro del tablero maximiza las posibilidades de construir alineaciones de 4 en todas las direcciones: vertical, horizontal y ambas diagonales.
- Jugar en la columna 4 crea múltiples amenazas dobles (dos oportunidades de ganar en turnos consecutivos), lo que pone al oponente en una posición de defensa constante.
- Muchas respuestas del oponente pueden ser neutralizadas con contraataques que restablecen la ventaja estructural.

De este modo, se determinó que si el primer jugador comienza correctamente y nunca comete errores, puede obligar al segundo jugador a perder, sin importar cuán bien juegue este último.

Este resultado clasifica a Conecta 4 como un juego resuelto: se conoce el resultado óptimo desde el estado inicial si ambos jugadores juegan perfectamente.

---

#### Juegos deterministas de suma cero

Conecta 4 es un excelente ejemplo de un juego determinista de suma cero con información perfecta. Vamos a desglosar lo anterior:

- Determinista
Un juego es determinista cuando no existe ningún elemento de azar. Es decir, no hay tiradas de dados, cartas al azar o eventos aleatorios. Cada acción lleva directamente a un resultado que depende exclusivamente de las decisiones de los jugadores.

En Conecta 4, cada jugada produce un resultado 100% predecible.

- Suma cero
Un juego es de suma cero cuando la ganancia de un jugador implica exactamente la pérdida del otro. Es decir:

Utilidad del Jugador $A$ + Utilidad del Jugador $B = 0$

Si un jugador gana (+1), el otro necesariamente pierde (-1). No hay escenarios de ganancia mutua ni empates si se juega hasta el final.

Este tipo de estructura es típica en juegos competitivos donde el éxito de un participante depende directamente del fracaso del otro, como ajedrez, damas o Conecta 4.

$Ganancia Jugador_1 + Ganancia Jugador_2 = 0$

Conecta 4 ha sido utilizado en investigaciones de inteligencia artificial, teoría de juegos y educación matemática, debido a su:

- Estructura claramente definida
- Representación visual directa
- Existencia de soluciones óptimas

En el ámbito académico, Conecta 4 representa un excelente ejemplo de un juego de información perfecta, donde ambos jugadores conocen el estado completo del tablero en todo momento, sin elementos ocultos ni azar.

Esto lo convierte en un campo ideal para explorar conceptos como:

- **Estrategias dominantes**
- **Árboles de decisión**
- **Equilibrio de Nash**
- **Algoritmos como Minimax con poda Alpha-Beta**

Además, su estructura lo convierte en un modelo ideal para enseñar:

- **Pensamiento estratégico**
- **Previsión**
- **Toma de decisiones secuenciales**
- **Resolución de conflictos bajo presión adversarial**

Es un juego adversarial: los intereses de los jugadores están enfrentados, lo que lo convierte en un excelente caso para analizar con teoría de juegos.

---

<h3 align="center">Historia del juego</h3>

Aunque es un juego simple, tiene una estructura suficientemente rica como para ser analizada con técnicas de inteligencia artificial y teoría matemática, como:

- Algoritmos minimax
- Alpha-beta pruning
- Modelos de equilibrio de Nash

---

#### Reglas

- Dos jugadores (uno con fichas rojas y otro con amarillas, típicamente).
- El tablero tiene 7 columnas y 6 filas.
- Las fichas caen desde arriba y ocupan la celda más baja disponible.
- El primero en alinear 4 fichas en cualquier dirección gana.
- Si el tablero se llena sin una conexión, hay empate.


<h3 align="center">Registro de Jugadas</h3>

| Turno | Jugador               | Columna | Descripción                           |
|-------|------------------------|---------|----------------------------------------|
| 1     | (Roja) Jorge Portilla | 4       | Primera ficha al centro                |
| 2     | (Amarilla) Luis Lerma | 3       | Contrajugada lateral                   |
| 3     | (Roja) Jorge Portilla | 2       | Expansión hacia la izquierda           |
| 4     | (Amarilla) Luis Lerma | 5       | Control lateral derecho                |
| 5     | (Roja) Jorge Portilla | 3       | Segunda ficha sobre amarilla           |
| 6     | (Amarilla) Luis Lerma | 6       | Control de extremo derecho             |
| 7     | (Roja) Jorge Portilla | 4       | Avanza hacia conexión vertical         |
| 8     | (Amarilla) Luis Lerma | 7       | Sigue por los extremos                 |
| 9     | (Roja) Jorge Portilla | 4       | Tercer nivel en columna 4              |
| 10    | (Amarilla) Luis Lerma | 4       | Bloquea conexión vertical              |
| 11    | (Roja) Jorge Portilla | 3       | Tercera ficha en columna 3             |
| 12    | (Amarilla) Luis Lerma | 1       | Ocupa el extremo izquierdo             |
|13     | (Roja) Jorge Portilla | 3       | Cuarta ficha en columna 3              |
|14     | (Amarilla) Luis Lerma | 2       | Ficha columna 2 sin prevenir anticipo  |
|15     | (Roja) Jorge Portilla | 3       | Cuarta ficha consecutiva (fila 2)  Gana|
---

#### Estrategias usadas

- **Control del centro:** Iniciar en la columna 4 permite acceso simétrico y conexión vertical.
- **Expansión lateral:** Movimientos hacia columnas 3 y 5 como extensión defensiva y ofensiva.
- **Juego en extremos:** Intento del oponente de reducir posibilidades bloqueando desde las orillas.


<h3 align="center">Aplicación de la Teoría de Juegos</h3>

Conecta 4 puede modelarse como un juego de dos jugadores con información perfecta, y se puede analizar usando:

- **Equilibrio de Nash:** Si ambos jugadores conocen la estrategia del otro, ninguno tiene incentivo para cambiar su jugada.
- **Minimax:** Técnica para minimizar la pérdida máxima posible. Se usa en agentes que juegan contra un oponente óptimo.
- **Árboles de decisión:** Donde cada nodo representa un estado del tablero y se busca el camino con mayor utilidad.

---

#### Ejemplo matemático sencillo de equilibrio:

Sea:

$U_J(c)$ mi utilidad (Jorge) al elegir columna $c=4$

$U_L(c)$ la utilidad de mi oponente al elegir columna $c=3$

Si para mí (Jorge Portilla):

$$U_J(4) > U_J(c)$$

Y para Luis Lerma:

$$U_L(3) > U_L(c)$$

Entonces, ninguno de los dos jugadores tiene incentivo para cambiar su estrategia,
dado que cada uno está maximizando su utilidad en respuesta a la elección del
otro.
Esto constituye un equilibrio de Nash, ya que: - Dado que cada jugador conoce
la estrategia del otro, ninguno mejora su resultado al cambiar unilateralmente
nuestra elección.

---

### Algoritmos con posible aplicación

- Minimax: algoritmo para decidir el mejor movimiento asumiendo que el
oponente juega óptimamente.
- Dominancia: columna 4 fue dominante en esta partida.
- Zonas críticas: control del centro → mayor conectividad.
- Jugada forzada: se vio cuando Luis tuvo que bloquear vertical en turno

<h3 align="center">Conclusión</h3>

En esta partida, mi estrategia fue enfocarme en la columna central desde el
principio, creando una cadena vertical difícil de bloquear. Mi oponente no pudo
anticipar la jugada dominada, y eso me permitió aprovechar la estructura del
tablero.
Este juego ejemplifica muy bien los conceptos de la teoría de juegos, como
conflicto de intereses, análisis secuencial, estrategia dominante y equilibrio. Fue
bastante interesante jugar como comunmente se hace, pero con los principios
y jugadas previamente investigadas, ya que te permitia además de anticiparme
por los movimientos de mi oponente, tener un objetivo o jugada al que llegar.

---

<h3 align="center">Bibliografia</h3>

- Allis, L. V. (1994). *Searching for Solutions in Games and Artificial Intelligence*. PhD Thesis.
- Allen, J. D. (1988). *Connect Four Solver*.
- Fogel, D. B. (2004). *Blondie24: Playing at the Edge of AI*.
