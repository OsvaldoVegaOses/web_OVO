# Propuesta de mejora del sitio profesional de Osvaldo Vega Oses

Revisión de diseño, contenido y experiencia de uso · 22 de septiembre de 2026

**Recomendación central:** dar mayor presencia a Osvaldo, las personas y los territorios, y facilitar que un visitante reconozca rápidamente la especialidad, la responsabilidad asumida y el valor de cada experiencia. La base profesional del sitio es sólida; su expresión visual puede comunicar mejor la cercanía y el trabajo territorial que ya aparecen en los relatos.

[Abrir maqueta conceptual](diseno-conceptual.html)

La maqueta explora una dirección visual y una selección editorial. Los espacios para retrato y fotografías pendientes están identificados. La fotografía incorporada procede del caso de Deslindes existente. Los textos propuestos requieren tu revisión editorial antes de publicarse.

## 1. Alcance y hallazgos

Se revisaron `index.html`, las seis páginas de `proyectos/`, `style.css`, `script.js` y las tres imágenes disponibles. Se visualizó el sitio localmente en Chrome de escritorio y se comprobaron las siete páginas a 390 y 320 píxeles de ancho. No se revisaron las fotografías que conservas fuera de esta carpeta, el contenido del CV ni la documentación que respalda los proyectos. Los datos profesionales se toman de las páginas actuales; no constituyen una verificación documental independiente.

| Hallazgo comprobado | Implicación |
| --- | --- |
| La portada contiene nueve tarjetas de experiencia, seis con enlace a una página de caso. | Unificar su estructura. Bollenar, Río Teno y la experiencia de catastros del Maule necesitan desarrollo editorial para convertirse en casos navegables. |
| La portada no contiene imágenes. El nombre completo aparece en el título del navegador y el pie, pero no en el bloque inicial visible. | Presentar nombre, especialidad y rostro desde el primer contacto. |
| Deslindes incluye una fotografía; La Florida incluye dos afiches; los otros cuatro casos no muestran imágenes. | Introducir fotografías de territorio y trabajo, junto con muestras seleccionadas de productos. |
| San Felipe contiene una referencia a una imagen dentro de un comentario HTML. | Es material visual previsto, no una imagen visible ni un enlace roto activo. |
| Los casos tienen aproximadamente entre 1.150 y 1.650 palabras en su contenido principal. | Ofrecer una lectura breve inicial y otra más profunda. Revisar también la repetición de bloques y diagramas. |
| La portada alcanza unos 7.500 px de alto en la prueba de escritorio y 13.700 px a 390 px de ancho. | Acercar casos e identidad personal al comienzo y compactar la lista de proyectos. Estas alturas dependen de ventana, fuentes y navegador. |
| San Felipe alcanza un ancho de documento de 648 px en una pantalla de 390 px: sus cronologías desbordan. | Convertir las cronologías a una secuencia vertical en móvil. |
| A 320 px también desbordan elementos de la portada, Desaladora Arica y Arenillas Negras. | Revisar anchos mínimos y márgenes interiores. |
| Hay un PDF de CV en la raíz, sin enlace desde la portada. | Ofrecer una descarga secundaria desde «Sobre mí», previa revisión de su versión y contenido publicable. |

Los archivos del sitio se conservan. Los entregables de esta revisión se encuentran en `propuesta/`.

## 2. Qué conservar y potenciar

La especialización está clara: Medio Humano, Participación Ciudadana e investigación cualitativa aplicada a infraestructura. Los casos distinguen participación profesional, contexto institucional, productos y aprendizajes. Ese cuidado aporta credibilidad.

Hay contenido humano especialmente valioso: la adaptación metodológica en Arenillas Negras, los liderazgos comunitarios en La Florida, los aprendizajes de la Desaladora de Arica y el inicio de una línea profesional en San Felipe. Conviene acercar estos pasajes a fotografías y ejemplos concretos.

También son útiles la estructura semántica básica, los títulos y descripciones de página, los enlaces institucionales presentes y el foco de teclado ya definido. La propuesta evoluciona sobre esta base.

## 3. Posicionamiento profesional y humano

El público principal ya declarado —consultoras, empresas de ingeniería, organismos públicos y equipos interdisciplinarios— necesita reconocer en qué puedes ayudar, qué responsabilidad has asumido y cómo te relacionas con las personas involucradas.

| Cualidad | Cómo expresarla |
| --- | --- |
| Rigor profesional | Rol específico, método, entregable y ejemplo verificable. |
| Escucha y presencia territorial | Fotografías de conversaciones, recorridos y trabajo colectivo; relatos de adaptación metodológica. |
| Criterio y aprendizaje | Qué aprendiste, cómo revisaste una interpretación y cómo delimitaste lo que el estudio podía responder. |

La dimensión humana puede expresarse desde tu práctica y tu vinculación con la sociedad civil. Una presentación personal, un retrato natural y un ejemplo de trabajo comunitario de ONG Tren Ciudadano darían más espesor a la trayectoria. Los hitos y fechas deben seleccionarse contigo.

**Texto propuesto para la portada:**

> Osvaldo Vega Oses · Sociólogo
>
> Escuchar a las personas. Comprender el territorio.
>
> Acompaño proyectos de infraestructura y evaluación ambiental con participación ciudadana, estudios de Medio Humano y evidencia cualitativa para decisiones mejor informadas.

Acciones: **Ver proyectos** y **Conversemos**. La frase actual «Construir evidencia para mejores decisiones» puede mantenerse como remate del bloque metodológico.

**Texto propuesto para «Mi forma de trabajar»:**

> Mi trabajo comienza escuchando cómo las personas viven y utilizan su territorio. Combino esas conversaciones con observación en terreno y análisis documental para producir evidencia útil, conservando el contexto, las diferencias y las preguntas que permanecen abiertas.

Son propuestas editoriales basadas en el contenido actual, no citas personales ya aprobadas.

## 4. Dirección visual

Sugiero una estética editorial sobria, con fotografía documental protagonista. La paleta oscura, los degradados eléctricos y las tarjetas translúcidas actuales evocan un producto tecnológico; mi lectura de diseño es que dejan menos visible tu práctica social y territorial.

| Elemento | Propuesta |
| --- | --- |
| Fondos | Marfil cálido `#F5F2EB` y blanco para contenidos extensos. |
| Texto | Tinta `#203331`, con pocas variaciones de gris. |
| Identidad y enlaces | Azul petróleo / verde profundo `#174C4F`. |
| Acentos | Terracota `#A64F32` para detalles y numeración. |
| Tipografía | Sans serif legible para texto y navegación; serif editorial moderada para titulares personales. También es viable conservar Inter y simplificar el tratamiento actual. |
| Composición | Menos contenedores anidados, superficies amplias de fotografía y columna de lectura de aproximadamente 60–75 caracteres. |
| Movimiento | Transiciones discretas y respeto de movimiento reducido. |

La maqueta usa fuentes del sistema para abrirse localmente sin dependencias externas. La paleta es una hipótesis de diseño; las fotografías finales ayudarán a ajustar el balance de color. Si prefieres mantener la identidad oscura, puede reservarse para cabecera y contacto, utilizando superficies claras en los relatos.

## 5. Estructura propuesta de portada

1. **Presentación personal:** nombre, especialidad, promesa breve, retrato en contexto y dos acciones claras.
2. **Tres casos destacados:** Arenillas Negras por participación inclusiva, Horcón por análisis cualitativo y Deslindes por coordinación territorial. La selección muestra capacidades complementarias y puede cambiar al completar Bollenar y Teno.
3. **En qué puedo aportar:** las tres especialidades resumidas como necesidad que atiendes, trabajo que realizas y producto que entregas.
4. **Mi forma de trabajar:** cuatro pasos breves, una escena de terreno y una muestra de producto. Los pasos actuales sirven de base.
5. **Sobre mí y trayectoria:** retrato, presentación de 80–120 palabras, tres o cuatro hitos y acceso al CV. Dar espacio a ONG Tren Ciudadano con un ejemplo específico.
6. **Innovación aplicada:** conectar TrazaClara con la necesidad de revisar de dónde proviene una interpretación. Incorporar una captura publicable cuando exista e indicar su estado con precisión.
7. **Contacto:** correo visible y copiable, LinkedIn e invitación concreta a conversar sobre un proyecto.

Reunir las demás experiencias en «Todos los proyectos», con imágenes, dos líneas de resumen y etiquetas consistentes. Con nueve experiencias, una agrupación por especialidad puede ser suficiente; no hace falta introducir un buscador.

Cambiar «Proyectos recientes» por «Experiencia seleccionada» o «Proyectos destacados»: la colección incluye participación desde 2021. La navegación puede simplificarse a Proyectos · Especialidades · Sobre mí · Contacto.

## 6. Plantilla de caso

**Lectura inicial de menos de un minuto:** título corto, foto principal, ubicación, período de participación, rol, contexto institucional, reto y contribución concreta. Mantener el nombre administrativo completo como subtítulo o ficha técnica.

**Lectura de evaluación profesional:** contexto, decisiones metodológicas, escenas de trabajo, productos, aprendizajes y referencias. Un índice breve facilita ir a cada sección.

Orden sugerido:

1. Título editorial + nombre oficial + fotografía de contexto.
2. Ficha: territorio, período de participación, organización, contraparte y rol.
3. El desafío: qué había que comprender o coordinar.
4. Mi contribución: tareas y decisiones bajo tu responsabilidad.
5. Trabajo en terreno: fotografías y pies explicativos.
6. Productos y aportes: muestra legible de mapa, matriz o síntesis publicable.
7. Aprendizaje específico y breve.
8. Proyecto relacionado y contacto.

Como objetivo editorial inicial, apuntaría a 700–1.000 palabras visibles por caso cuando el contenido lo permita, con detalles complementarios en apartados desplegables o anexos. Quitar repeticiones y conservar la precisión del alcance profesional.

Varios diagramas actuales convierten listas de actividades en largas cadenas verticales. Mantendría uno o dos gráficos por caso cuando expliquen una relación: por ejemplo, cómo una inquietud se transforma en un insumo de diseño. Los pasos simples pueden presentarse como una lista breve.

**Ejemplo de resumen para Arenillas Negras:**

> Participación adaptada a distintas formas de habitar el borde costero.
>
> Como encargado de Participación Ciudadana de GSI Ingeniería, coordiné la primera etapa participativa del estudio. Se utilizaron metodologías diferenciadas con comunidad, establecimientos educacionales, usuarios de Teletón, actores del borde costero y servicios públicos para sistematizar necesidades e inquietudes relevantes para el diseño.

El alcance «primera etapa» debe permanecer visible. Distinguir entregables propios de resultados del equipo, período de participación de estado actual del proyecto y asistencias de personas únicas. Las cifras de participación o satisfacción deben conservar contexto, fecha y base; por sí solas no equivalen a impacto social.

## 7. Plan de imágenes por proyecto

Orientaciones para seleccionar tu archivo fotográfico. No se asume que dispongas de cada toma ni que una imagen de un proyecto pueda representar otro.

| Experiencia | Fotografía principal sugerida | Material complementario | Mensaje |
| --- | --- | --- | --- |
| Embalse Bollenar | Paisaje habitado o recorrido que relacione asentamientos, actividades y territorio. | Conversación de terreno; mapa territorial; fragmento publicable de matriz de evidencia. | Sistemas de vida y construcción de línea de base. Ficha pendiente de desarrollar. |
| Embalse Río Teno | Reunión o conversación con actores en contexto territorial reconocible. | Recorrido, mesa de trabajo y mapa de actores sin datos de contacto. | Relación territorial y seguimiento de inquietudes. Ficha pendiente de desarrollar. |
| San Felipe | Recorrido urbano o registro de sectores afectados por aguas lluvias, con lugar y fecha. | Actividad participativa, mapa de sectores y antecedente documental. | Experiencia cotidiana, memoria territorial y análisis técnico. |
| Deslindes de ríos de Valparaíso | Recorrido ribereño con presencia del trabajo de campo. | Plano sobre una mesa, difusión territorial o reunión por cauce. | Escala territorial y coordinación. La foto actual sirve como contexto; una toma más cercana al cauce o la actividad explicaría mejor tu aporte. |
| Arenillas Negras | Taller de cartografía social donde se vea el método y la interacción. | Vista del litoral, trabajo sobre planos y síntesis de necesidades. | Participación adaptada, inclusión y relación con el diseño. |
| Desaladora de Arica | Borde costero en uso: pesca, circulación o actividad cotidiana vinculada al estudio. | Reconocimiento territorial, conversación y mapa de usos publicable. | Diversidad de relaciones con el litoral. |
| Horcón y Chocota | Territorio habitado o trabajo participativo sobre planos. | Contexto de entrevista, plano de sectores y ejemplo anonimizado de organización de información. | Vida cotidiana, agua y análisis cualitativo. |
| La Florida | Encuentro comunitario o recorrido con actores territoriales. | Registro urbano, reunión de seguimiento y un afiche como documento secundario. | Continuidad de la relación. Los afiches muestran convocatoria, pero no la interacción. |
| Infraestructura sanitaria y catastros del Maule | Levantamiento de terreno o paisaje de sectores estudiados. | Instrumento en blanco, cartografía agregada y registro de coordinación. | Organización del levantamiento. Precisar proyectos, rol y período antes de convertirlo en caso. |

**Identidad personal:** un retrato con luz natural y mirada cercana, una fotografía tuya trabajando con otras personas y, si corresponde, una escena de tu trayectoria en sociedad civil. Ropa y contexto acordes con tu práctica habitual.

**Selección inicial manejable:** un retrato y tres imágenes finalistas por cada caso desarrollado: territorio, interacción y producto. Son 19 recursos para iniciar. Bollenar, Teno y Maule se incorporan al desarrollar sus fichas.

**Uso editorial:** una foto principal y dos o tres imágenes dentro del relato, junto al contenido que explican. Pies con actividad, lugar, fecha y crédito, completando solo información confirmada. Ejemplo de estructura: «Taller de cartografía social · [lugar] · [mes/año]. Identificación de necesidades sobre el plano del sector. Fotografía: [autor]».

Las fotografías muestran contexto y práctica; la responsabilidad y los resultados se explican en el texto. Un paisaje por sí solo no demuestra una intervención profesional.

Seleccionar imágenes apropiadas para publicación y con autorización de uso, especialmente si aparecen niños, niñas o usuarios de Teletón. Los encuadres de manos y trabajo sobre planos son una alternativa cuando no corresponde mostrar rostros. Las muestras de matrices deben excluir nombres, contactos y datos de entrevistas que no sean públicos.

## 8. Requisitos para la implementación

| Prioridad | Acción | Criterio de aceptación |
| --- | --- | --- |
| Alta | Adaptar cronologías y anchos mínimos. | Texto y controles accesibles a 320, 390 y 768 px, sin contenido recortado. |
| Alta | Incorporar nombre, retrato y presentación breve. | Identificación clara de persona, especialidad y contacto desde el inicio. |
| Alta | Unificar tarjetas. | Imagen, rol, ubicación, resumen y enlace descriptivo. Experiencias sin ficha no ofrecen enlaces vacíos. |
| Alta | Normalizar imágenes y pies. | Alternativa textual para imágenes informativas y contexto en pie o relato. |
| Media | Revisar contraste. | La combinación `#64748b` sobre `#050b14` ofrece aproximadamente 4,15:1, por debajo de 4,5:1 para texto normal. Medir también los fondos efectivos. |
| Media | Optimizar imágenes. | Versiones adaptadas, dimensiones declaradas y carga diferida fuera del primer bloque. |
| Media | Mejorar navegación de casos. | Regreso a proyectos, índice breve y caso relacionado. |
| Media | Completar vistas previas al compartir. | Título, descripción e imagen social por página; URL canónica al conocer el dominio. |
| Media | Revisar movimiento y menú. | Movimiento reducido, foco visible, botón accesible y comprobación con teclado. |
| Media | Reducir estilos dentro del HTML. | Componentes compartidos para fichas, galerías y cronologías. |

La foto de Deslindes pesa aproximadamente 2,14 MB; los afiches de La Florida, 0,68 y 1,34 MB. Son tamaños de archivos locales, no mediciones de carga de una web publicada. Como presupuesto orientativo, buscar fotografías derivadas de 150–350 KB y portadas de hasta unos 500 KB, según detalle y calidad. Mapas y afiches pueden requerir una vista ampliada independiente.

Conservar originales y generar derivados modernos con respaldo compatible, distintos tamaños y recortes revisados para móvil. Priorizar la imagen inicial y reservar carga diferida para las inferiores. El texto importante de los afiches debe tener un equivalente legible en la página. La alternativa textual depende de la función de la imagen: [guía de W3C sobre imágenes](https://www.w3.org/WAI/tutorials/images/).

La comprobación móvil se apoya en la redistribución del contenido a 320 CSS px: [W3C, Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html). Para color, usar como referencia 4,5:1 en texto normal y 3:1 en texto grande: [W3C, contraste mínimo](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Las preferencias de movimiento se detectan con [`prefers-reduced-motion`, MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion).

## 9. Orden de trabajo

**Primera entrega: identidad y acceso.** Corregir desbordamientos, renovar la presentación inicial, seleccionar retrato, acortar tarjetas y destacar tres casos.

**Segunda entrega: caso piloto.** Recomiendo Arenillas Negras por la combinación de método, interacción, inclusión y aprendizaje. Construir la plantilla con fotos reales y comprobarla en móvil. Horcón y Deslindes permiten verificar que funciona para otras especialidades.

**Tercera entrega: portafolio completo.** Aplicar la plantilla a los seis casos existentes y desarrollar Bollenar, Teno y Maule según el material disponible. Completar trayectoria, CV e innovación aplicada.

**Cuarta entrega: preparación para publicación.** Revisar textos, atribuciones, fotografías, enlaces, teclado, contraste, imágenes y vistas previas sociales. Verificar la web publicada cuando se disponga del dominio y alojamiento.

Para evaluar la nueva versión, realizar una prueba breve con tres personas cercanas a tus públicos profesionales: pedirles que expliquen tu especialidad, identifiquen tu rol en un caso y encuentren cómo contactarte. Así se contrasta la claridad sin atribuir mejoras de conversión todavía no medidas.

## 10. Referencias locales

- `index.html:38`: presentación; `index.html:95`: experiencias; `index.html:269`: trayectoria.
- `proyectos/plan-maestro-san-felipe.html:89` y `:220`: cronologías; `:251`: comentario con material visual previsto.
- `proyectos/deslindes-rios-valparaiso.html:196`: foto existente.
- `proyectos/pac-la-florida.html:233` y `:236`: afiches existentes.
- `style.css:265`: ancho mínimo de tarjetas; `style.css:613`: márgenes de figuras; `style.css:866`: reglas adaptables.
- `script.js`: menú, desplazamiento y revelado progresivo; incorporar la preferencia de movimiento reducido.

La propuesta no implica cambiar de plataforma. Con el tamaño actual, una estructura estática bien organizada permite realizar estas mejoras.
