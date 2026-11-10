# OVO: recorridos de servicios y contacto v1.1

Publicación en GCP: 10 de noviembre de 2026, operación `20261110T175625Z-0f29ca77`.

Proyecto `helical-analyst-301321`, VM `ovo-web-server`, zona `us-central1-a`, raíz `/var/www/html`. Nginx pasó su comprobación antes de publicar. El publicador verificó los hashes previos, respaldó el estado anterior y comprobó la lectura de los 17 archivos escritos. Respaldo: `/var/backups/ovo-contacto-v11/20261110T175625Z-0f29ca77`.

Las portadas incorporan tres consultas por servicio, correo visible y contacto general. Las doce fichas conservan sus contenidos y navegación propia; su acción final abre un correo con asunto del caso. V1 mantiene proyectos antes de servicios; V2 mantiene servicios antes de proyectos. No se modificaron los destinos de anuncios, los archivos IndexNow ni las imágenes.

`openai-conversions.js` registra una conversión de correo únicamente para los enlaces instrumentados cuyo destino corresponde al correo del sitio. `contact-tracking.js` publica contexto en `dataLayer` de forma independiente del SDK de Ads. `ovo_contact_context` incluye servicio, origen, versión y caso con valores permitidos. `ovo_navigation` identifica las acciones del hero y no representa una conversión de correo. Los eventos no contienen contenido del asunto ni datos personales.

La configuración interna del contenedor GTM no se modificó ni se verificó mediante una sesión administrativa. Crear etiquetas de conversión adicionales en GTM podría duplicar el píxel que ya ejecuta el código del sitio. La presencia de contexto en dataLayer no garantiza que esté disponible en los informes de una herramienta.

Validación: 15 pruebas de seguimiento aprobadas; contacto y SEO correctos en 14 páginas; 70 combinaciones de navegador aprobadas (14 páginas, cinco resoluciones). Estas pruebas de navegador comprueban estructura, imágenes y desbordamiento, sin constituir una auditoría visual completa ni acreditar el envío de un correo. Las 19 URLs de verificación pública respondieron y coincidieron con sus hashes esperados, incluidas las portadas con y sin www.

Evidencia: `recorridos-contacto-v1.1-manifiesto.json`, `contacto-v11-despliegue-gcp.json` y `contacto-v11-verificacion-publica.json`. Las líneas base históricas se conservan; el nuevo manifiesto corresponde al paquete publicado. Las optimizaciones locales previas de imágenes y estilos permanecen fuera de esta publicación.
