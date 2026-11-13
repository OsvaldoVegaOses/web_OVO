# Medición de Clarity y aviso de correo

El desarrollo local incorpora un aviso junto al enlace de correo utilizado. El menú móvil muestra el aviso fuera de la lista que se cierra. Los destinos originales, sus asuntos y los enlaces a secciones se conservan. El aviso utiliza `role="status"` y un enlace de correo seleccionable sin atributos de conversión.

`contact-tracking.js` etiqueta las sesiones mediante `ovo_version=v1|v2` y registra los clics reales en los enlaces originales como `ovo_correo_pac`, `ovo_correo_medio_humano`, `ovo_correo_investigacion` u `ovo_correo_general`. No identifica visitantes ni confirma envío de correo. Si una sesión visita ambas versiones, puede acumular ambos valores de la etiqueta. Los eventos no se emiten en localhost ni desde el enlace del aviso.

La API cliente usa el proyecto Clarity `ypzia0e866`. Las exportaciones requieren un token separado, solicitado de forma oculta por `scripts/exportar_clarity.py` y `scripts/exportar_clarity_ventanas.py`. Estos scripts no guardan el token; los JSON obtenidos deben mantenerse privados. Las ventanas de 24, 48 y 72 horas se superponen y no forman cohortes históricas separadas. Las etiquetas nuevas no se aplican retrospectivamente.

Verificación local:

```powershell
node --test scripts/clarity-contact.test.cjs scripts/openai-conversions.test.mjs
python scripts/verificar_contacto.py
node scripts/qa-aviso-contacto.mjs
```

La prueba de navegador utiliza Chrome headless en Windows y bloquea los rastreadores; intercepta `mailto:` para evitar abrir aplicaciones o enviar mensajes. La apertura efectiva del cliente de correo y la revisión manual completa con teclado y lector de pantalla siguen pendientes.

Esta actualización de GitHub incluye las optimizaciones locales de imágenes, fuentes y estilos, junto con las imágenes nuevas que necesitan las portadas. No constituye un despliegue. Al sincronizar el repositorio el 13 de noviembre de 2026, producción ya tenía el aviso y los enlaces de contacto corregidos, pero aún no estas optimizaciones ni los nuevos eventos de Clarity.
