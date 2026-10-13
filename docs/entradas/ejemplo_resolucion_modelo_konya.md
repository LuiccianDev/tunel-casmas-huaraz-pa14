Profesor: Daniel Zurita Vilca.

Guía de Ejercicios Extracción Mina I - Evaluación Nº 3

2. En una operación minera a rajo abierto se iniciará una nueva fase de expansión donde se
requiere un ritmo de producción de 70 KTPD desde bancos que miden 15 metros de altura. El
macizo rocoso posee una densidad de 2,4 ton/m3, una resistencia a la compresión de 230 MPa
y   una   resistencia   a   la   tracción   de   23   MPa,   además  se   identifican   estratificaciones   en   la
profundidad de los cortes a volar y familias de diaclasas con capas cementadas y bien unidas.
Los equipos seleccionados para la perforación de los pozos de producción son perforadoras
rotativas con triconos de 9 pulgadas de diámetro, las cuales trabajarán 2 turnos al día de 12
horas por turno, ejerciendo velocidades de rotación de 90 RPM.
Además, se consideran los siguientes datos:

PRODUCCIÓN

BUFFER

PRECORTE

Explosivo: Anfo a granel W: 205 Kg.

φPerf: 6 Pulg.

J: 0,22*B

φPerf: 7 3/8 Pulg.

Pb: 210 MPa

ρexp: 0,77 gr/cc

Sin pasadura

Ángulo β: 20°

FC: 300 gr/ton

Explosivo: Anfo Liviano

Explosivo: Enaline

Calcule:

a) El diseño de tronadura aplicando el modelo matemático de Konya.
b) La plantilla de barrenación, indicando el número total de pozos para un polígono de 60

mts. de ancho y 100 mts. de largo. Considere 2 filas de buffer.

Solución:

A)

Pozos de producción

- Primero hay que fijarse en el modelo matemático que indica el problema para diseñar la malla, en
este caso se señala que se debe usar el Modelo matemático de Konya.
- Seguido de eso, se debe comenzar con el diseño, estableciendo primero el Burden y el Espaciamiento
de los pozos de producción.
- Para lo anterior se recurre a la fórmula planteada por Konya para el cálculo de Burden:

B=( 2∗ρexp

ρrx

+1,5)∗d exp

Donde:
B = Burden (pies)
ρexp = Densidad del explosivo (gr/cc)
ρrx = Densidad de la roca (gr/cc)
dexp = Diámetro de la carga explosiva (pulg)

- Según el enunciado la densidad de la roca es de 2,4 gr/cc. En cuanto al explosivo, se indica que para
los pozos de producción se usará Anfo a granel, el cual tiene una densidad de 0,77 gr/cc, mientras que
su diámetro será igual al del diámetro de perforación (9 pulgadas). Lo que sigue es calcular el Burden
con los datos entregados:

Profesor: Daniel Zurita Vilca.

B=( 2∗0,77

2,4

gr
cc

+ 1,5)∗9 pulgadas

gr
cc
B=19,275 ft

- Como el Burden quedó en pies (ft), este se debe transformar a metros:

B=19,275

ft∗1m
3,28084 ft

B=5,875 m

-   La   fórmula   de   Konya   involucra   un   Burden   corregido,   el   cual   considera   factores   del   diseño   de
tronadura, así como también factores geomecánicos.

BC=B∗Kr∗Kd∗Ks

Donde:
B = Burden (m)
Kr = Corrección por número de líneas
Kd = Corrección por depositación de la roca
Ks = Corrección por estructuras geológicas

- Los parámetros de corrección vienen dados por las siguientes tablas:

- La corrección por número de líneas tiene que ver con la cantidad de filas que vaya a tener el diseño
de tronadura. En la enorme mayoría de casos, las mallas tienen 3 o más filas (líneas) de pozos, por lo
que en este caso Kr es 0,9:

- La corrección por depositación de la roca considera la ubicación de los estratos del macizo rocoso en
relación   a   los   cortes   del   banco.   En   este   caso   se   señala   textualmente   que   “se   identifican
estratificaciones en la profundidad de los cortes a volar” por lo que el factor Kd es igual a 1,18:

Profesor: Daniel Zurita Vilca.

- La corrección por estructuras geológicas toma en cuenta el estado en el que se encuentra el material
rocoso del macizo y las estructuras asociadas a él. En este caso se indica que el macizo tiene “familias
de diaclasas con capas cementadas y bien unidas”, por lo que Ks es 1,10:

-   Habiendo   determinado   todos   los   factores   de   corrección,   ya   es   posible   determinar   el   Burden
corregido:

BC=5,875 m∗0,9∗1,18∗1,10
BC=6,863 m ≈7 m

- El espaciamiento se va a determinar considerando si los pozos detonan de forma instantánea o de
forma secuenciada. En la mayoría de los diseños, se opta por una detonación secuenciada, por lo que
el espaciamiento pasa a depender de la relación entre la altura de banco y el Burden. Si la altura de
banco es menor que el Burden multiplicado por 4, entonces se usará la siguiente fórmula para el
espaciamiento:

H b<(4∗B)E=

H b+(7∗B)
8

- Por otra parte, si la altura de banco es mayor o igual al Burden multiplicado por 4, entonces el
espaciamiento quedará determinado por la siguiente fórmula:

H b ≥(4∗B)E=(1,4∗B)

- La altura del banco en este caso es de 15 m, mientras que el Burden (corregido) multiplicado por 4 da
igual a 27,452. Con este cálculo, queda en evidencia que la altura del banco es menor al Burden
multiplicado por 4, por lo que se procede a utilizar la primera fórmula mostrada:

E=

H b+(7∗B)
8
15 m+(7∗6,863 m)
8

E=

E=7,880 m≈ 8 m

- El diseño de los pozos de producción concluye con el cálculo de la longitud de los pozos, lo cual se
logra sumando la altura de banco con la pasadura.

- Se señala que el banco tiene una altura de 15 m, mientras que la pasadura es de 0,22 veces el Burden,
por lo que la fórmula para determinar la longitud de los pozos queda así:

L=H B+J

L=15 m+(0,22∗B)
L=15 m+(0,22∗6,863 m)
L=16,510 m

Profesor: Daniel Zurita Vilca.

Pozos de Buffer

- Para diseñar la malla de Buffer, en este curso de Extracción Mina I, se utilizará siempre el mismo
modelo matemático, el cual indica que el Burden del Buffer se calcula de la siguiente manera:

BB=(

W ∗1000

FC∗K BP∗H B∗ρrx∗SBR)1

2

Donde:

Bb = Burden buffer (m)
W = Explosivo en buffer (Kg)
Fc = Factor de carga de pozos de producción (gr/ton)
KBP = Relación Factor de carga Buffer/Producción “1”
Hb = Altura del banco (m)
ρrx = Densidad de la roca (Ton/m3)
SBR = Relación Espaciamiento/Burden

-   En   la   tabla   de   datos   se   indica   que   W   es   de   205   kg   y   que   el   FC   es   de   300   gr/ton.   La   relación
Espaciamiento/Burden se debe calcular dividiendo el Espaciamiento y el Burden (corregido) calculados
anteriormente.

SBR=

Espaciamiento
Burden (Corregido)
7,880 m
6,863 m
SBR=1,148

SBR=

- Con estos datos se procede a utilizar la ecuación antes mencionada:

BB=(

300

gr
ton

205 kg∗1000

∗1∗15 m∗2,4

Ton
m3

∗1,148)1

2

BB=4,066 m ≈ 4 m

-   Ya   habiendo   determinado   el   Burden   de   los   pozos   de   Buffer,   se   prosigue   con   el   cálculo   del
espaciamiento de dichos pozos utilizando la siguiente fórmula:

E B=BB∗SBR

- El Burden del Buffer es de 4,066 m, mientras que la relación Espaciamiento/Burden es de 1,148 tal
como indica el cálculo realizado con anterioridad. Así se calcula el espaciamiento de los pozos de
Buffer:

E B=4,066 m∗1,148
E B=4,668 m≈ 5 m

- Con el Burden y el Espaciamiento de los pozos de buffer ya calculados, solamente queda determinar
el   largo   que   tendrán   estos   pozos.   Sin   embargo,   en   la   tabla   de   datos   mostrada   al   inicio   de   este
problema se indica que los pozos de Buffer no tienen pasadura, eso significa que el largo de estos será
igual a la altura del banco, por lo que la longitud de los pozos de Buffer queda en 15 m.

Pozos de Precorte

- Los últimos pozos a diseñar son los de precorte. Ante todo, hay que considerar que la línea de pozos

Profesor: Daniel Zurita Vilca.

de precorte SIEMPRE será una sola, por lo tanto, estos pozos no tienen Burden, solo Espaciamiento:

E Precorte=∅

Perf ∗Pb+ RT
RT

Donde:

RT = Resistencia a la tracción de la roca en MPa.
Pb = Presión de detonación en el barreno en MPa.
ᴓ Perf = Diámetro de perforación en Pulgadas.
Eprecorte = Espaciamiento de precorte en Pulgadas.

- En la tabla de datos se indica que el diámetro de perforación para los pozos de precorte es de 6
pulgadas, también se señala que la presión de detonación (Pb) es de 210 MPa y que la resistencia a la
tracción (RT) es de 23 MPa. Con esto ya se puede calcular el espaciamiento de los pozos de precorte:

E Precorte=6

Pulgadas∗210 MPa+23 MPa
23 MPa

E Precorte=60,783 pulgadas

- El espaciamiento de precorte debe transformarse de pulgadas a metros:

E Precorte=60,783

pulgadas∗0,0254 m
1 pulgada

E Precorte=1,544 m≈ 2 m

- Finalmente, el largo de los pozos de precorte se calcula con la siguiente fórmula:

LPC =

H B
cos β

Donde:

Hb = Altura del banco (m)
β = Ángulo de inclinación de los pozos respecto a la vertical (en Grados)

- Según los datos entregados el banco tiene una altura de 15 m, mientras que el ángulo de inclinación β
es de 20°. Con eso, ya se puede determinar el largo de los pozos de precorte:

15 m
LPC =
cos 20°
LPC =15,963 m

- Los datos obtenidos se resumen en la siguiente tabla:

Pozos de producción Pozos de buffer Pozos de precorte

7 x 8 m
16,510 m

4 x 5 m
15 m

2 m
15,963 m

Malla
Largo de los
pozos

B)

Pozos de Precorte

- Para diseñar la plantilla de barrenación conviene comenzar con los pozos de precorte, luego con los
de Buffer y finalmente con los de producción. Lo primero a determinar es la cantidad de pozos de
precorte que se utilizarán en esta malla, lo cual se determina de la siguiente manera:

Profesor: Daniel Zurita Vilca.

N ° Pozos Precorte=

Largo Polígono−E Precorte
E Precorte

+1

- Para este cálculo conviene aproximar el espaciamiento del precorte a una cifra entera, sin decimales.
Además, se señala en el enunciado que el polígono posee un largo de 100 m. Con esto se determina el
número de pozos de precorte como sigue:

N ° Pozos Precorte=

100 m−2m
2 m

+ 1

N ° Pozos Precorte=5 0 Pozos

- En caso de que el resultado del número de pozos diera decimal, se debe redondear el valor para
dejarlo como un número entero.

Pozos de Buffer

- Según lo señalado por este problema, se deben considerar dos filas de Buffer, por lo que se debe
pasar directamente a calcular el número de pozos por cada fila de Buffer:

N ° Pozos por Fila(Buffer)=

Largo Polígono −EB
E B

+1

-   El   Espaciamiento   del   Buffer   (Eb),   al   igual   que   pasó   con   el   Espaciamiento   del   precorte,   debe
aproximarse a un número entero, en este caso queda en 5 m:

N ° Pozos por Fila(Buffer)=

1 00 m−5 m
5 m

+1

N ° Pozos por Fila (Buffer )=20 pozos

- Habiendo determinado el número de pozos por fila de buffer, lo que corresponde hacer ahora es
corregir el Espaciamiento de dichos pozos para que queden alineados correctamente. Para ello se
efectúa el siguiente cálculo:

E B(Corregido)=

Largo Polígono−N ° Pozos por Fila (Buffer)
N ° Pozos por Fila ( Buffer)
10 0 m−20 pozos
2 0 pozos
E B (Corregido )=5 m

+1

E B(Corregido)=

+1

- El Burden no es necesario corregirlo, ya que el enunciado señala que solo debe haber 2 filas de Buffer.

Pozos de Producción

- Para diseñar la malla de pozos de producción hay que tomar en cuenta que el enunciado no indica
cuántas filas debe haber, por lo que estas deben ser calculadas como se muestra a continuación:

N ° Filas( Producción)=

Ancho Disponible−B
B

+1

- El Burden (B) también se trabaja como número entero, mientras que el ancho disponible se refiere al
ancho total del polígono menos el Burden ocupado por los pozos de buffer. Como existen 2 filas de
buffer y el Burden de este último es igual a 4 metros, se puede decir que a los 60 m de ancho del
polígono se le deben restar 8 m, obteniendo así el ancho disponible para los pozos de producción:

N ° Filas( Producción)=

[ Ancho Polígono−(N ° Filas Buffer∗B B)]−B
B

+ 1

Profesor: Daniel Zurita Vilca.

N ° Filas( Producción)=

[60 m−(2∗4 m)]−7 m
7 m

+ 1

N ° Filas( Producción)=7,429

- Debido a que se obtuvo un número decimal este valor debe ser aproximado a un número entero. Por
lo que el número de filas queda en 7.

N ° Filas ( Producción)=7 Filas

- Una vez determinado el número de filas se debe corregir el Burden para que los pozos quepan todos
dentro del ancho disponible en el polígono. Esto se corrige de la siguiente manera:

B(Corregido)=

B(Corregido)=

Ancho Disponible−N ° Filas( Producción)
N ° Filas ( Producción)
[ Ancho Polígono−(N ° Filas Buffer∗B B)]−N ° Filas(Producción)
N ° Filas(Producción)
[60 m−(2∗4 m)]−7 filas
7 filas

B(Corregido)=

+1

+1

+1

B (Corregido )=7,429 m

- El Burden obtenido no se aproxima a un número entero, ya que al hacer eso los pozos quedarían
desalineados respecto al polígono. Ya terminado esto, se procede a determinar el N° de pozos por fila
de producción de la siguiente manera:

N ° Pozos por Fila ( Producción)=

Largo Polígono−E
E

+1

- Donde “E” evidentemente corresponde al espaciamiento de los pozos de producción expresado en
número entero:

N ° Pozos por Fila(Producción)=

10 0−8
8

+1

N ° Pozos por Fila(Producción)=1 2 ,5

- Al haber quedado como número decimal, la cantidad de pozos se redondea hacia arriba:

N ° Pozos por Fila ( Producción)=13 pozos

-   Finalmente   el   espaciamiento   de   los   pozos   de   producción   debe   ser   corregido   para   que   queden
perfectamente alineados. Para ello se realiza la siguiente operación:

E(Corregido)=

Largo Polígono−N ° Pozos por Fila(Producción)
N ° Pozos por Fila (Producción)
1 0 0 m−13 pozos
13 pozos
E (Corregido)=7 ,692 m

E(Corregido)=

+1

+1

- El diseño de la malla se resume en la siguiente tabla:

Pozos de producción Pozos de buffer Pozos de precorte

Malla
N° Filas
N° Pozos por fila
Burden corregido
Espaciamiento Corregido

7 x 8 m
7 filas
13 pozos
7,429 m
7,692 m

4 x 5 m
2 filas
20 pozos
No aplica
5 m

2 m
1 fila
50 pozos
No aplica
No aplica
