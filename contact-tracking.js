// Contexto de navegación y contacto: independiente del SDK de publicidad.
(function (window, document) {
    'use strict';
    if (!['osvaldovega.cl', 'www.osvaldovega.cl'].includes(window.location.hostname)) return;
    if (window.__ovoContactTrackingLoaded) return;
    window.__ovoContactTrackingLoaded = true;
    const allowed = (value, choices, fallback) => choices.includes(value) ? value : fallback;
    const version = /(?:index2\.html|-v2\.html)$/.test(window.location.pathname) ? 'v2' : 'v1';
    document.addEventListener('click', function (event) {
        if (!event.isTrusted || event.button !== 0 || event.defaultPrevented) return;
        const target = event.target && (event.target.closest ? event.target : event.target.parentElement);
        const link = target && target.closest('a[href]');
        if (!link) return;
        const data = link.dataset;
        let context;
        if (data.contactSource && /^mailto:contacto@osvaldovega\.cl(?:\?|$)/i.test(link.getAttribute('href') || '')) {
            context = { event: 'ovo_contact_context',
                contact_service: allowed(data.contactService, ['pac', 'medio_humano', 'investigacion', 'general'], 'general'),
                contact_source: allowed(data.contactSource, ['hero', 'servicios', 'caso', 'footer'], 'footer'),
                contact_version: version,
                contact_case: allowed(data.contactCase, ['pac-arenillas-negras', 'pac-la-florida', 'deslindes-rios-valparaiso', 'medio-humano-desaladora-arica', 'medio-humano-horcon', 'plan-maestro-san-felipe'], '') };
        } else if (data.ovoAction && data.ovoSource === 'hero') {
            const action = allowed(data.ovoAction, ['ver_proyectos', 'ver_servicios', 'ir_contacto'], '');
            if (action) context = { event: 'ovo_navigation', navigation_action: action, navigation_source: 'hero', site_version: version };
        }
        if (context) {
            window.dataLayer = window.dataLayer || [];
            window.dataLayer.push(context);
        }
    }, true);
})(window, document);
