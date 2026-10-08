# Sitio Profesional de Osvaldo Vega Oses
### Sociólogo · Medio Humano · Participación Ciudadana · osvaldovega.cl

Repositorio oficial del sitio web profesional de **Osvaldo Vega Oses**, sociólogo especializado en estudios de Medio Humano, diseño y conducción de Participación Ciudadana (PAC) y análisis socio-territorial para proyectos de infraestructura y evaluación ambiental (SEIA).

---

## Arquitectura del Sitio (Versiones V1 / V2)

El repositorio incorpora una arquitectura de publicación paralela y experimentación controlada que mantiene simultáneamente dos versiones del portafolio:

### 1. Versión 1 — Producción Oficial (V1)
- **Portada:** [`index.html`](index.html)
- **Casos de estudio (`proyectos/`):**
  - `pac-arenillas-negras.html`
  - `medio-humano-desaladora-arica.html`
  - `deslindes-rios-valparaiso.html`
  - `pac-la-florida.html`
  - `plan-maestro-san-felipe.html`
  - `medio-humano-horcon.html`
- **Estilos y Scripts:** `style.css`, `script.js`
- **SEO:** Indexable (`index, follow`), canónicos autorreferenciales e indexado en `sitemap.xml`.

### 2. Versión 2 — Experimento Editorial (V2)
- **Portada:** [`index2.html`](index2.html)
- **Casos de estudio (`proyectos/`):**
  - `pac-arenillas-negras-v2.html`
  - `medio-humano-desaladora-arica-v2.html`
  - `deslindes-rios-valparaiso-v2.html`
  - `pac-la-florida-v2.html`
  - `plan-maestro-san-felipe-v2.html`
  - `medio-humano-horcon-v2.html`
- **Estilos exclusivos:** `style-v2.css` (reglas responsive para componentes editoriales).
- **SEO:** No indexable en fase experimental (`noindex, follow`), canónicos hacia sus equivalentes V1 y `og:url` propio de variante.

Documentación detallada sobre esta arquitectura en [`docs/experimentos-editoriales-v1-v2.md`](docs/experimentos-editoriales-v1-v2.md).

---

## Estructura de Directorios

```text
/
├── index.html                           # Portada oficial V1
├── index2.html                          # Portada experimental V2
├── style.css                            # Hoja de estilos principal
├── style-v2.css                         # Reglas responsive exclusivas V2
├── script.js                            # Lógica interactiva (menú, acordeones)
├── CV_Sociologo_Osvaldo Vega Oses.pdf   # Currículum profesional
├── robots.txt                           # Directivas para rastreadores
├── sitemap.xml                          # Mapa del sitio oficial (7 URLs canónicas)
│
├── proyectos/                           # Casos de estudio en profundidad
│   ├── *-v2.html                        # Variantes experimentales V2
│   └── *.html                           # Páginas originales V1
│
├── Fotos_proyectos/                     # Registro fotográfico y territorial
├── assets/                              # Recursos gráficos y Open Graph
├── docs/                                # Documentación de arquitectura y experimentos
├── propuesta/                           # Diseños conceptuales y propuestas editoriales
└── scripts/                             # Utilidades de mantenimiento y SEO (IndexNow)
```

---

## Contacto

- **Correo electrónico:** [contacto@osvaldovega.cl](mailto:contacto@osvaldovega.cl)
- **LinkedIn:** [linkedin.com/in/osvaldovegaoses](https://www.linkedin.com/in/osvaldovegaoses)
- **Sitio web:** [osvaldovega.cl](https://osvaldovega.cl)
