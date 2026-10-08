# Registro de Experimentos Editoriales V1 / V2 — Sitio Profesional OVO

**Proyecto:** Portafolio Profesional de Osvaldo Vega Oses · Sociólogo  
**Fecha de registro:** 8 de octubre de 2026  
**Ámbito:** Arquitectura de versiones paralelas y experimentación editorial controlada  

---

## Estado Actual del Sistema

```text
V1 = REFERENCIA ORIGINAL

V2 = EXPERIMENTO EDITORIAL

PUBLICACIÓN V2 = PENDIENTE DE AUTORIZACIÓN

COMPARACIÓN = NO INICIADA

DECISIÓN DE PROMOCIÓN = NO TOMADA
```

> **Aviso de alcance:** Este documento describe una arquitectura técnica y editorial preparada en el repositorio local. Nada de lo aquí registrado se encuentra publicado en producción ni accesible a tráfico externo en esta fase.

---

## 1. Propósito de V1 y V2

El sitio web profesional presenta la trayectoria y capacidades de Osvaldo Vega Oses en Medio Humano, Participación Ciudadana y análisis socio-territorial para proyectos de infraestructura y evaluación ambiental.

- **V1 (Referencia Original):** Es la versión oficial actual de producción. Mantiene una estética técnica y oscura, estructurada en torno a `index.html` y seis casos de proyectos desarrollados en profundidad. Representa la línea base de presentación y validación profesional.
- **V2 (Experimento Editorial):** Es una variante alternativa desarrollada para explorar una narrativa editorial clara y humana, con mayor protagonismo de la identidad profesional, los territorios y la estructura de servicios. Organiza la portada en diez bloques funcionales (Hero profesional, Servicios, Mapa de experiencia, Tres casos destacados, Tres casos secundarios, Trabajo actual, Mi forma de trabajar, Trayectoria, Innovación aplicada y Contacto).

**Principio de diseño:** Construir una infraestructura de experimentación editorial controlada, reversible, reproducible y verificable, donde **ningún cambio en V2 modifique visual, funcional o editorialmente a V1**.

---

## 2. Archivos Pertenecientes a Cada Versión

### Versión 1 (V1 — Referencia Original)
- **Portada:** `index.html`
- **Páginas de proyectos:**
  - `proyectos/pac-arenillas-negras.html`
  - `proyectos/medio-humano-desaladora-arica.html`
  - `proyectos/deslindes-rios-valparaiso.html`
  - `proyectos/pac-la-florida.html`
  - `proyectos/plan-maestro-san-felipe.html`
  - `proyectos/medio-humano-horcon.html`
- **Estilos y lógica:** `style.css`, `script.js`

### Versión 2 (V2 — Experimento Editorial)
- **Portada:** `index2.html`
- **Páginas de proyectos:**
  - `proyectos/pac-arenillas-negras-v2.html`
  - `proyectos/medio-humano-desaladora-arica-v2.html`
  - `proyectos/deslindes-rios-valparaiso-v2.html`
  - `proyectos/pac-la-florida-v2.html`
  - `proyectos/plan-maestro-san-felipe-v2.html`
  - `proyectos/medio-humano-horcon-v2.html`
- **Estilos exclusivos V2:** `style-v2.css` (cargado junto a `style.css` únicamente en V2)

### Recursos Compartidos (Sin Duplicación)
- Fotografías y recursos gráficos: `Fotos_proyectos/`, `assets/`
- Tipografías: Google Fonts (Open Sans) y Font Awesome CDN
- Faviconos: `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`
- Analítica: Contenedores Google Tag Manager (`GTM-NN64BQC5`) y Microsoft Clarity (`ypzia0e866`)

---

## 3. Relación entre Portada y Páginas de Proyectos (Aislamiento de Navegación)

Los recorridos de navegación se encuentran 100% aislados e impermeables entre sí:

```text
[ Recorrido Oficial V1 ]
index.html ───► proyectos/caso.html ───► index.html#seccion

[ Recorrido Experimental V2 ]
index2.html ───► proyectos/caso-v2.html ───► index2.html#seccion
```

### Reglas de Enlace Implementadas
1. **Desde `index2.html`:** Todos los enlaces a proyectos apuntan exclusivamente a las variantes `-v2.html` (tanto en casos destacados, casos secundarios como en enlaces cruzados de servicios). Ningún enlace apunta a las páginas originales V1.
2. **Desde las páginas `*-v2.html`:** Todos los enlaces de retorno (`logo`, barra de navegación, CTA inferior) apuntan exclusivamente a `../index2.html`, conservando intactos sus destinos por ancla (`#inicio`, `#proyectos`, `#que-hago`, `#metodologia`, `#sobre-mi`, `#innovacion`, `#contacto`).
3. **Navegación interna de caso:** Las anclas locales (`#resumen`, `#territorio`, `#proceso`, etc.) y controles interactivos (acordeones, botones colapsar/expandir) operan autónomamente dentro de cada documento.

---

## 4. Política de Modificaciones

1. **Intangibilidad de V1:** Los 9 archivos constitutivos de V1 (`index.html`, los seis casos originales, `style.css` y `script.js`) tienen prohibición estricta de edición directa durante el desarrollo de experimentos. Su integridad se valida mediante comparación criptográfica SHA-256.
2. **Desarrollo en V2:** Toda mejora de redacción, taxonomía, ordenación o estilo para el experimento debe realizarse en `index2.html`, los archivos `*-v2.html` o la hoja complementaria `style-v2.css`.
3. **Sin conmutador público no autorizado:** No se instalará un selector flotante V1/V2 de cara al visitante general sin previo acuerdo metodológico.
4. **Preservación de contenido sustantivo:** En esta etapa no se alteran roles declarados, períodos, metodologías, evidencias ni resultados técnicos de los proyectos. Las revisiones de contenido se abordan caso a caso con Osvaldo Vega.

---

## 5. Tratamiento SEO: Dos Versiones Públicas, Una Referencia Oficial

Para permitir la publicación simultánea sin generar canibalización, contenido duplicado o señales contradictorias en motores de búsqueda:

| Parámetro | Versión V1 (Referencia) | Versión V2 (Experimental) |
|---|---|---|
| **Directiva Robots** | `index, follow` | `noindex, follow` |
| **Canonical en Portada** | `https://osvaldovega.cl/` | `https://osvaldovega.cl/` |
| **Canonical en Proyectos** | Auto-referencial a V1 (`.../caso.html`) | Apunta a su equivalente original V1 (`.../caso.html`) |
| **Open Graph `og:url`** | `https://osvaldovega.cl/` o `.../caso.html` | URL propia V2 (`.../index2.html` o `.../caso-v2.html`) |
| **Inclusión en Sitemap** | Sí (las 7 URLs oficiales en `sitemap.xml`) | **No** (excluidas para proteger la señal oficial) |
| **Notificación IndexNow** | Sí (reservado a V1) | **No** (prohibido someter URLs experimentales) |
| **Robots.txt** | Permite rastreo general | No se bloquea por ruta para permitir lectura del `noindex` |

---

## 6. Estado de Publicación

- **Archivos locales:** Completamente preparados, verificados en navegación y validados en resolución responsive (1440px, 1024px, 768px, 390px, 320px).
- **Entorno de producción:** Sin despliegue ejecutado. El sitio publicado permanece en su estado anterior.
- **Autorización de publicación:** Pendiente de revisión técnica y editorial por parte de Osvaldo Vega.

---

## 7. Procedimiento de Comparación Futura

Cuando se autorice la publicación paralela de V2, la comparación editorial y de rendimiento se estructurará de forma controlada:

1. **Fase Inicial (Compartición Asistida / Enlaces Directos):**
   - V1 recibe el tráfico orgánico y directo general.
   - V2 se comparte selectivamente con colegas, contrapartes o consultoras de confianza mediante enlaces directos a `https://osvaldovega.cl/index2.html`.
2. **Diferenciación Analítica Propuesta:**
   - Implementar un parámetro de dimensión personalizada en la capa de datos (`dataLayer`):
     ```javascript
     window.dataLayer = window.dataLayer || [];
     window.dataLayer.push({
       'site_version': window.location.pathname.includes('2') || window.location.pathname.includes('-v2') ? 'v2' : 'v1'
     });
     ```
   - Segmentar en Clarity y Google Analytics eventos equivalentes:
     - Tasa de clic a proyectos desde el hero y la sección principal.
     - Exploración de casos secundarios y lectura de trabajo actual.
     - Interacción con enlaces de servicios.
     - Clics en correo de contacto y perfil de LinkedIn.
     - Tasa de rebote y tiempo de permanencia en móvil vs. escritorio.
3. **Fase Posterior (Eventual Prueba A/B):**
   - Si se decide someter ambas variantes a distribución de tráfico aleatorio, se requerirá configurar un middleware en el borde (Cloudflare Worker o rewrite de servidor) antes de activar cualquier redirección.

---

## 8. Criterios para una Eventual Promoción de V2 a Producción Oficial

La variante experimental V2 solo sustituirá a V1 (`index2.html` pasando a ser `index.html`) si se cumplen copulativamente los siguientes criterios:

1. **Validación Editorial:** Aprobación explícita de Osvaldo Vega sobre la narrativa de servicios, la presentación personal y la jerarquía de proyectos.
2. **Comportamiento Móvil:** Confirmación de que el visitante en smartphone encuentra de forma inmediata los casos de interés sin fatiga de scroll.
3. **Conversión de Contacto:** Evidencia de que los accesos a correo y LinkedIn en V2 se mantienen o superan los índices de V1.
4. **Verificación Técnica Previa al Reemplazo:**
   - Promoción segura de `index2.html` a `index.html`.
   - Cambio de directivas robots de `noindex` a `index, follow`.
   - Actualización de canónicos para consolidar la nueva versión.
   - Actualización del sitemap oficial y posterior notificación IndexNow.

---

## 9. Procedimiento de Rollback (Cómo Volver a V1 sin Perder V2)

Dado que V1 ha permanecido completamente intacta durante todo el proceso, el rollback es inmediato y sin riesgo:

1. Si V2 estuviese publicada en el servidor remoto y se decide retirar de inmediato el experimento:
   - Eliminar o despublicar `index2.html`, los seis archivos `proyectos/*-v2.html` y `style-v2.css` del servidor.
   - V1 continuará operando sin interrupción, pues ninguno de sus enlaces o archivos depende de V2.
2. Los archivos V2 pueden archivarse o mantenerse localmente en el repositorio para futuras iteraciones sin generar ningún residuo en producción.
