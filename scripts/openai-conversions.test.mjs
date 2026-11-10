import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';

const root = fileURLToPath(new URL('../', import.meta.url));
const source = fs.readFileSync(path.join(root, 'openai-conversions.js'), 'utf8');
const trackingSource = fs.readFileSync(path.join(root, 'contact-tracking.js'), 'utf8');

function browser({ hostname = 'osvaldovega.cl', navigator = {}, existingPixel = false, pathname = '/proyectos/pac-la-florida.html' } = {}) {
    const scripts = [];
    const listeners = new Map();
    const existingCalls = [];
    const window = { location: { hostname, pathname }, navigator };
    if (existingPixel) window.oaiq = (...args) => existingCalls.push(args);
    const document = {
        createElement: () => ({}),
        head: { appendChild: script => scripts.push(script) },
        addEventListener: (name, handler) => listeners.set(name, [...(listeners.get(name) || []), handler])
    };
    const context = vm.createContext({ window, document });
    const run = () => { vm.runInContext(trackingSource, context); vm.runInContext(source, context); };
    run();
    const calls = () => JSON.parse(JSON.stringify(Array.from(existingPixel ? existingCalls : (window.oaiq?.q || []), args => Array.from(args))));
    const click = (id, overrides = {}, target = null, dataset = undefined) => {
        const link = { id, dataset: dataset || {}, getAttribute: () => id === 'footer-linkedin' ? 'https://www.linkedin.com/' : 'mailto:contacto@osvaldovega.cl', closest: () => link };
        for (const handler of listeners.get('click') || []) handler({
            isTrusted: true, button: 0, defaultPrevented: false,
            target: target || link,
            preventDefault: () => { throw new Error('Contact navigation must remain available'); },
            ...overrides
        });
    };
    return { window, scripts, listeners, calls, click, run };
}

test('las 14 páginas cargan una sola integración diferida en head, con ruta válida', () => {
    const pages = ['index.html', 'index2.html', ...fs.readdirSync(path.join(root, 'proyectos'))
        .filter(name => name.endsWith('.html')).map(name => `proyectos/${name}`)];
    assert.equal(pages.length, 14);
    for (const page of pages) {
        const html = fs.readFileSync(path.join(root, page), 'utf8');
        const head = html.match(/<head>([\s\S]*?)<\/head>/i)?.[1];
        const tags = [...html.matchAll(/<script\b[^>]*src="([^"]*openai-conversions\.js)"[^>]*><\/script>/g)];
        assert.equal(tags.length, 1, page);
        assert.match(tags[0][0], /\bdefer\b/, page);
        assert.ok(head.includes(tags[0][0]), page);
        assert.equal(path.resolve(root, path.dirname(page), tags[0][1]), path.join(root, 'openai-conversions.js'));
    }
});

test('un clic de servicio emite una conversión y contexto sin datos personales', () => {
    const b = browser({ pathname: '/index2.html' });
    b.click('', {}, null, { contactService: 'pac', contactSource: 'servicios' });
    assert.equal(b.calls().filter(c => c[3]?.custom_event_name === 'contact_email_clicked').length, 1);
    assert.deepEqual(JSON.parse(JSON.stringify(b.window.dataLayer)), [{
        event: 'ovo_contact_context', contact_service: 'pac', contact_source: 'servicios',
        contact_version: 'v2', contact_case: ''
    }]);
});

test('una ficha V2 identifica caso y limita los datos permitidos', () => {
    const b = browser({ pathname: '/proyectos/pac-la-florida-v2.html' });
    b.click('', {}, null, { contactService: 'pac', contactSource: 'caso', contactCase: 'pac-la-florida' });
    const context = JSON.parse(JSON.stringify(b.window.dataLayer[0]));
    assert.equal(context.contact_version, 'v2');
    assert.equal(context.contact_case, 'pac-la-florida');
    b.click('', {}, null, { contactService: 'dato-personal', contactSource: 'caso', contactCase: 'dato-personal' });
    assert.equal(b.window.dataLayer[1].contact_service, 'general');
    assert.equal(b.window.dataLayer[1].contact_case, '');
});

test('las pruebas locales y los dominios ajenos no cargan el SDK ni registran eventos', () => {
    for (const hostname of ['localhost', '127.0.0.1', '', 'preview.example', 'osvaldovega.cl.example']) {
        const b = browser({ hostname });
        assert.equal(b.scripts.length, 0, hostname);
        assert.equal(b.listeners.size, 0, hostname);
        assert.equal(b.window.oaiq, undefined, hostname);
    }
});

test('ambos dominios públicos usan el píxel verificado y el transporte oficial asíncrono', () => {
    for (const hostname of ['osvaldovega.cl', 'www.osvaldovega.cl']) {
        const b = browser({ hostname });
        assert.equal(b.scripts.length, 1);
        assert.equal(b.scripts[0].src, 'https://bzrcdn.openai.com/sdk/oaiq.min.js');
        assert.equal(b.scripts[0].async, true);
        assert.deepEqual(b.calls()[0], ['init', { pixelId: 'E33Ne9Y7pSoTiwvskgLnnE' }]);
    }
});

test('una visita envía únicamente la ruta y excluye datos de usuario y valor comercial', () => {
    const b = browser();
    assert.deepEqual(b.calls()[1], ['measure', 'page_viewed', {
        type: 'contents', contents: [{ id: '/proyectos/pac-la-florida.html', content_type: 'page' }]
    }, { opt_out: true }]);
});

test('correo y LinkedIn registran intención, sin impedir enlaces ni inventar citas o leads', () => {
    const b = browser();
    b.click('footer-email');
    b.click('footer-linkedin');
    const events = b.calls().slice(2);
    assert.deepEqual(events.map(c => c[3].custom_event_name), ['contact_email_clicked', 'contact_linkedin_clicked']);
    for (const event of events) {
        assert.deepEqual(event.slice(0, 3), ['measure', 'custom', { type: 'custom' }]);
        assert.equal(event[3].opt_out, true);
    }
    assert.ok(!b.calls().some(c => ['appointment_scheduled', 'lead_created'].includes(c[1])));
});

test('navegación, clics cancelados, botones secundarios y eventos sintéticos no cuentan como contacto', () => {
    const b = browser();
    b.click('hero-cta-contacto');
    b.click('link-arenillas');
    b.click('footer-email', { isTrusted: false });
    b.click('footer-email', { defaultPrevented: true });
    b.click('footer-email', { button: 1 });
    b.click('footer-email', {}, { closest: () => null });
    assert.equal(b.calls().length, 2);
});

test('también reconoce clics en el icono o texto interior del enlace', () => {
    const b = browser();
    const link = { id: 'footer-email', dataset: {}, getAttribute: () => 'mailto:contacto@osvaldovega.cl' };
    b.click(null, {}, { parentElement: { closest: () => link } });
    assert.equal(b.calls().at(-1)[3].custom_event_name, 'contact_email_clicked');
});

test('respeta GPC y Do Not Track antes de inicializar, sin forzar aceptación', () => {
    for (const navigator of [{ globalPrivacyControl: true }, { doNotTrack: '1' }]) {
        const b = browser({ navigator });
        assert.deepEqual(b.calls()[0], ['consent', false]);
        assert.equal(b.calls()[1][0], 'init');
        assert.ok(!b.calls().some(c => c[0] === 'consent' && c[1] === true));
    }
});

test('recargar la integración no duplica inicialización, visitas ni el SDK', () => {
    const b = browser();
    b.run();
    assert.equal(b.scripts.length, 1);
    assert.equal(b.calls().length, 2);
});

test('un SDK existente conserva su función y no se vuelve a descargar', () => {
    const b = browser({ existingPixel: true });
    assert.equal(b.scripts.length, 0);
    assert.equal(b.calls()[0][0], 'init');
    b.click('footer-email');
    assert.equal(b.calls().at(-1)[3].custom_event_name, 'contact_email_clicked');
});

test('un enlace interno no es una conversión aunque tenga atributos de contacto', () => {
    const b = browser();
    const link = { id: '', dataset: { contactSource: 'servicios', contactService: 'pac' }, getAttribute: () => '#contacto' };
    b.click('', {}, { closest: () => link });
    assert.equal(b.calls().length, 2);
    assert.equal(b.window.dataLayer, undefined);
});

test('el hero registra navegación sin convertirla en correo', () => {
    const b = browser();
    b.click('hero-cta-contacto', {}, null, { ovoSource: 'hero', ovoAction: 'ir_contacto' });
    assert.equal(b.calls().length, 2);
    assert.equal(b.window.dataLayer[0].event, 'ovo_navigation');
    assert.equal(b.window.dataLayer[0].navigation_action, 'ir_contacto');
});

test('el contexto permanece registrado si el SDK de publicidad falla', () => {
    const b = browser({ existingPixel: true });
    b.window.oaiq = () => { throw new Error('SDK failure'); };
    assert.throws(() => b.click('', {}, null, { contactSource: 'servicios', contactService: 'pac' }));
    assert.equal(b.window.dataLayer.length, 1);
    assert.equal(b.window.dataLayer[0].contact_service, 'pac');
});
