/* ChatGPT Ads Measurement Pixel: https://developers.openai.com/ads/measurement-pixel */
(function (window, document) {
    'use strict';

    // Las previsualizaciones y pruebas locales no envían eventos a la cuenta real.
    if (!['osvaldovega.cl', 'www.osvaldovega.cl'].includes(window.location.hostname)) return;
    if (window.__ovoOpenAIConversionsLoaded) return;
    window.__ovoOpenAIConversionsLoaded = true;

    if (!window.oaiq) {
        const queue = function () { queue.q.push(arguments); };
        queue.q = [];
        window.oaiq = queue;

        const sdk = document.createElement('script');
        sdk.async = true;
        sdk.src = 'https://bzrcdn.openai.com/sdk/oaiq.min.js';
        document.head.appendChild(sdk);
    }

    // Respetar las señales de privacidad antes de inicializar la medición.
    if (window.navigator.globalPrivacyControl === true || window.navigator.doNotTrack === '1') {
        window.oaiq('consent', false);
    }

    window.oaiq('init', { pixelId: 'E33Ne9Y7pSoTiwvskgLnnE' });
    window.oaiq('measure', 'page_viewed', {
        type: 'contents',
        contents: [{ id: window.location.pathname, content_type: 'page' }]
    }, { opt_out: true });

    // Un clic indica intención de contacto; no confirma un correo ni una cita.
    document.addEventListener('click', function (event) {
        if (!event.isTrusted || event.defaultPrevented || event.button !== 0) return;
        const target = event.target && (event.target.closest ? event.target : event.target.parentElement);
        const link = target && target.closest('a[href]');
        if (!link) return;

        let name;
        if ((link.id === 'footer-email' || (link.dataset && link.dataset.contactSource)) && /^mailto:contacto@osvaldovega\.cl(?:\?|$)/i.test(link.getAttribute('href') || '')) name = 'contact_email_clicked';
        if (link.id === 'footer-linkedin') name = 'contact_linkedin_clicked';
        if (!name) return;

        window.oaiq('measure', 'custom', { type: 'custom' }, {
            custom_event_name: name,
            opt_out: true
        });

    });
})(window, document);
