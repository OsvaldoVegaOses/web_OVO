# Registro de Experimentos Editoriales V1 / V2 - Sitio Profesional OVO

**Proyecto:** Portafolio Profesional de Osvaldo Vega Oses - Sociologo
**Fecha de creacion del registro:** 8 de octubre de 2026
**Ultima actualizacion:** 8 de octubre de 2026 (auditoria tecnica)
**Ambito:** Arquitectura de versiones paralelas y experimentacion editorial controlada

---

## Estado Actual del Sistema

`	ext
V1                              PRESERVADA
V2                              PRESERVADA
HASH HISTORICO index.html       CONSERVADO
HASH ACTUAL AUTORIZADO          VERIFICADO
QA PYTHON (4 suites)            EJECUTADO — PASS
QA NAVEGADOR (35 combinaciones) EJECUTADO — PASS
DETECCION DE FALLOS             COMPROBADA
PRODUCCION                      NO VERIFICADO POR HTTP
COMPARACION V1/V2               NO INICIADA
DECISION DE PROMOCION           NO TOMADA
COMMIT                          NO AUTORIZADO
PUSH                            NO AUTORIZADO
DEPLOY                          NO AUTORIZADO
`

---

## Diferenciacion de niveles de estado

### Nivel A - Repositorio GitHub (OsvaldoVegaOses/web_OVO)

Estado confirmado a fecha de auditoria:

- Existe V1 completa (index.html + 6 proyectos + style.css + script.js).
- Existe V2 completa (index2.html + 6 paginas -v2.html + style-v2.css).
- Rama principal: main. Ambas versiones presentes.
- Ultimo commit verificado: 17d6bc0d9eb28c1359ad37d35242d37489385456
  Mensaje: qa: actualizar scripts de verificacion - suite completa PASS (4/4)
  Modifico exclusivamente cuatro scripts de QA.
- Commit anterior: 4a3db796655619d2935a1c47064fb1febf0afc3c
  Mensaje: feat: arquitectura paralela V1/V2, portafolio profesional y actualizacion de contacto

### Nivel B - Publicacion en osvaldovega.cl

**Estado: NO VERIFICADO**

No se realizaron comprobaciones HTTP directas a las URLs publicas durante esta auditoria.
No es valido inferir el estado de despliegue a partir del push al repositorio.

Para verificar el estado real se requiere comprobar directamente:
- https://osvaldovega.cl/ (respuesta HTTP y contenido)
- https://osvaldovega.cl/index2.html (presencia o 404)

### Nivel C - Comparacion editorial V1/V2

**Estado: NO INICIADA**

No se han comparado formalmente las experiencias de navegacion de visitantes reales.
La decision de promover V2 a portada oficial permanece: NO TOMADA.

---

## 1. Proposito de V1 y V2

- **V1 (Referencia Original):** Version oficial actual. Estetica tecnica y oscura. Linea base de validacion profesional.
- **V2 (Experimento Editorial):** Variante alternativa con narrativa editorial clara y humana. Diez bloques funcionales.

Principio: ninggun cambio en V2 modifica visual, funcional o editorialmente a V1.

---

## 2. Archivos de Cada Version

### V1 - Referencia Original
- Portada: index.html
- Proyectos: proyectos/pac-arenillas-negras.html, medio-humano-desaladora-arica.html,
  deslindes-rios-valparaiso.html, pac-la-florida.html, plan-maestro-san-felipe.html,
  medio-humano-horcon.html
- Estilos y logica: style.css, script.js

### V2 - Experimento Editorial
- Portada: index2.html
- Proyectos: proyectos/*-v2.html (6 archivos)
- Estilos exclusivos: style-v2.css

### Recursos Compartidos
- Fotografias: Fotos_proyectos/, assets/
- Tipografias: Google Fonts + Font Awesome CDN
- Analitica: GTM-NN64BQC5 + Microsoft Clarity ypzia0e866

---

## 3. Aislamiento de Navegacion

Recorridos 100% aislados:
  V1: index.html -> proyectos/caso.html -> index.html#seccion
  V2: index2.html -> proyectos/caso-v2.html -> index2.html#seccion

Verificado mediante scratch/verify_v2_qa.py: 0 errores en 14 paginas.

---

## 4. Tratamiento SEO

| Parametro             | V1 (Referencia)                | V2 (Experimental)              |
|-----------------------|--------------------------------|--------------------------------|
| Directiva Robots      | index, follow                  | noindex, follow                |
| Canonical en Portada  | https://osvaldovega.cl/        | https://osvaldovega.cl/        |
| Canonical Proyectos   | Auto-referencial V1            | Apunta a equivalente V1        |
| og:url                | URL oficial V1                 | URL propia V2                  |
| Sitemap               | Si (7 URLs oficiales)          | No                             |
| IndexNow              | Si (reservado a V1)            | No                             |

---

## 5. Estado de Publicacion

- Repositorio GitHub: Ambas versiones en rama main. CONFIRMADO.
- Servidor osvaldovega.cl: NO VERIFICADO (sin comprobacion HTTP en esta auditoria).
- Autorizacion de publicacion de V2: Pendiente de revision por Osvaldo Vega.

---

## 6. Criterios para Eventual Promocion de V2

V2 sustituira a V1 solo si se cumplen copulativamente:
1. Validacion editorial por Osvaldo Vega.
2. Confirmacion de comportamiento movil.
3. Evidencia de conversion de contacto equivalente o superior.
4. Verificacion tecnica previa (robots, canonicos, sitemap, IndexNow).

---

## 7. Procedimiento de Rollback

V1 permanecio completamente intacta. Rollback es inmediato:
1. Eliminar index2.html, los seis *-v2.html y style-v2.css del servidor.
2. V1 continuara operando sin interrupcion.

---

## 8. Registro de Auditoria Tecnica

### Contexto de la auditoria

- Fecha: 8 de octubre de 2026
- Commit evaluado: 17d6bc0d9eb28c1359ad37d35242d37489385456
- Rama: main
- Working tree al inicio: limpio (sin cambios locales)
- Archivos del sitio modificados durante la auditoria: NINGUNO

### Suites estaticas - Cobertura real

| Suite                  | Archivo                       | Cobertura                                              |
|------------------------|-------------------------------|--------------------------------------------------------|
| SHA-256 V1             | scratch/verify_v1_sha256.py   | Integridad de 9 archivos V1 (hash dual para index.html)|
| Navegacion/aislamiento | scratch/verify_v2_qa.py       | 14 paginas, enlaces, mailto, recursos locales          |
| SEO completo           | verify_seo_final.py           | 14 paginas, sitemap, robots.txt, og:image              |
| Tracking               | verify_tracking.py            | GTM + Clarity en 14 paginas                            |

ACLARACION: 4/4 PASS se refiere a cuatro suites Python estaticas. No representa la totalidad de
pruebas posibles del sitio (no incluye accesibilidad WCAG, Core Web Vitals, comportamiento real).

### Referencias SHA-256 de index.html (trazabilidad dual)

| Referencia           | Hash                                                               | Estado                          |
|----------------------|--------------------------------------------------------------------|---------------------------------|
| Historica            | dead87da88fab4549e7697b9e7600c0f8fa64b18d83af065db5f1dee6bfa01be | Conservada en verify_v1_sha256.py|
| Autorizada actual    | 729fce9acdc6ec3cc38e23fe86999d0a01109e184c868096387ddd0c4107106a | Verificada en disco             |
| Cambio documentado   | Boton Escribeme -> mailto:contacto@osvaldovega.cl                  | Autorizado                      |
| Diff byte a byte     | NO VERIFICADO                                                      | Historico no recuperable desde repo|

Los 8 archivos restantes de V1 conservan sus hashes originales sin cambio alguno.

### Resultados suites Python (exit codes)

`
verify_v1_sha256.py  -> PASS (exit 0)
  PASS identicos a linea base:       8
  PASS cambio autorizado:            1
  FAIL discrepancias no resueltas:   0

verify_v2_qa.py      -> PASS (exit 0)
  Errores encontrados: 0 / 14 paginas

verify_seo_final.py  -> PASS (exit 0)
  Errores encontrados: 0 / 14 paginas

verify_tracking.py   -> PASS (exit 0)
  Errores encontrados: 0 / 14 paginas
`

### Resultados QA de navegador

**test_all_v2_pages.mjs** - Browser QA V2

`
Paginas previstas:       7
Resoluciones previstas:  5  (1440, 1024, 768, 390, 320 px)
Combinaciones previstas: 35
Ejecutadas:              35
PASS:                    35
FAIL:                    0
INCOMPLETE:              0
Resultado global:        PASS
Exit code:               0
`

Detalle por pagina (todas las resoluciones PASS):
- index2.html: 7/7 imgs, sin overflow (1440, 1024, 768, 390, 320 px)
- pac-arenillas-negras-v2.html: 6/6 imgs, sin overflow (todas resoluciones)
- medio-humano-desaladora-arica-v2.html: 3/3 imgs, sin overflow (todas resoluciones)
- deslindes-rios-valparaiso-v2.html: 5/5 imgs, sin overflow (todas resoluciones)
- pac-la-florida-v2.html: 8/8 imgs, sin overflow (todas resoluciones)
- plan-maestro-san-felipe-v2.html: 4/4 imgs, sin overflow (todas resoluciones)
- medio-humano-horcon-v2.html: 2/2 imgs, sin overflow (todas resoluciones)

**test_responsive_index2.mjs** - Responsive QA index2.html

```
Resoluciones previstas:  5 (1440, 1024, 768, 390, 320 px)
Ejecutadas:              5
PASS:                    5
FAIL:                    0
INCOMPLETE:              0
Resultado global:        PASS
Exit code:               0
```

Detalle por resolucion:
- 1440px: overflow=false, outOfBounds=0, grids responsivos conformes -> PASS
- 1024px: overflow=false, outOfBounds=0, grids responsivos conformes -> PASS
- 768px:  overflow=false, outOfBounds=0, grids responsivos conformes -> PASS
- 390px:  overflow=false, outOfBounds=0, grids responsivos conformes -> PASS
- 320px:  overflow=false, outOfBounds=0, grids responsivos conformes -> PASS


### Validacion del mecanismo de deteccion de fallos

El mecanismo de FAIL/exit-code-no-cero fue verificado estructuralmente en el codigo:
- Los scripts corregidos cuentan failCount y incompleteCount por separado.
- process.exit(0) se emite SOLO si passCount == EXPECTED_TOTAL y failCount == 0.
- exit(1) en presencia de cualquier FAIL; exit(2) en presencia de INCOMPLETE.
- Se elimino el process.exit(0) incondicional previo.

Prueba controlada de fallo real (EVIDENCIA OBTENIDA Y DOCUMENTADA):
1. **Python (`verify_v1_sha256.py`):**
   - Inyección temporal de hash no coincidente en un archivo de prueba en memoria.
   - Resultado: salida `RESULTADO GLOBAL: FAIL`, exit code `1`.
2. **Navegador (`test_all_v2_pages.mjs`):**
   - Sustitución temporal de URL por `proyectos/no-existe-v2.html` en ejecución aislada.
   - Resultado: 5 fallos detectados (1 por resolución: título ausente, H1 ausente, body insuficiente), salida `Resultado global: FAIL`, exit code `1`.

Ambas suites comprueban y garantizan detección real de anomalías con códigos de salida estrictamente distintos de cero.

### Limitaciones de las comprobaciones

1. Suites Python son estaticas: no ejecutan JavaScript ni evaluan comportamiento en navegador.
2. QA de navegador corre sobre servidor local; no comprueba CDN externos ni latencia real.
3. Fuentes externas (Google Fonts, Font Awesome) no se clasifican como fallo local.
4. Diff byte a byte de index.html historico vs. autorizado no es verificable desde repo actual.
5. No se realizo auditoria de accesibilidad WCAG ni de rendimiento Core Web Vitals.
6. Estado de produccion (osvaldovega.cl) no fue verificado por HTTP en esta auditoria.

### Incidencias pendientes

Ninguna incidencia requiere modificacion de archivos del sitio web.

---

## 9. Proximos Pasos (Pendientes de Autorizacion)

1. Verificacion HTTP de produccion: confirmar estado real de osvaldovega.cl cuando sea requerido.
2. Commit de auditoria: si se autoriza, registrar scripts corregidos y este documento en Git.
3. Push remoto: enviar cambios a `origin/main` una vez confirmado por Osvaldo Vega.
4. Inicio de comparacion editorial: cuando Osvaldo Vega lo indique.

