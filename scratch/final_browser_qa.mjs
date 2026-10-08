import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const root = process.cwd();
const outDir = path.join(root, 'scratch', 'final-qa');
fs.mkdirSync(outDir, { recursive: true });

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const profileDir = path.join('C:\\Windows\\Temp', `ovo-cdp-${process.pid}`);
const chrome = spawn(chromePath, [
  '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  '--remote-debugging-port=0', `--user-data-dir=${profileDir}`, 'about:blank'
], { stdio: ['ignore', 'ignore', 'pipe'], windowsHide: true });

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

async function browserEndpoint() {
  let buffer = '';
  return await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('Chrome DevTools endpoint timeout')), 15000);
    chrome.stderr.on('data', chunk => {
      buffer += chunk.toString();
      const match = buffer.match(/DevTools listening on (ws:\/\/[^\s]+)/);
      if (match) {
        clearTimeout(timer);
        resolve(match[1]);
      }
    });
    chrome.on('exit', code => reject(new Error(`Chrome exited early: ${code}`)));
  });
}

class CDP {
  constructor(url) {
    this.url = url;
    this.nextId = 1;
    this.pending = new Map();
    this.listeners = new Map();
  }
  async connect() {
    this.ws = new WebSocket(this.url);
    await new Promise((resolve, reject) => {
      this.ws.addEventListener('open', resolve, { once: true });
      this.ws.addEventListener('error', reject, { once: true });
    });
    this.ws.addEventListener('message', event => {
      const msg = JSON.parse(event.data);
      if (msg.id) {
        const pending = this.pending.get(msg.id);
        if (!pending) return;
        this.pending.delete(msg.id);
        if (msg.error) pending.reject(new Error(`${pending.method}: ${msg.error.message}`));
        else pending.resolve(msg.result);
        return;
      }
      const handlers = this.listeners.get(msg.method) || [];
      handlers.forEach(handler => handler(msg.params));
    });
  }
  send(method, params = {}) {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject, method });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }
  on(method, handler) {
    const handlers = this.listeners.get(method) || [];
    handlers.push(handler);
    this.listeners.set(method, handlers);
  }
  once(method, timeout = 15000) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error(`${method} timeout`)), timeout);
      const handler = params => {
        clearTimeout(timer);
        const handlers = this.listeners.get(method) || [];
        this.listeners.set(method, handlers.filter(item => item !== handler));
        resolve(params);
      };
      this.on(method, handler);
    });
  }
}

const viewports = [320, 375, 390, 768, 1024, 1200, 1440];
const pages = [
  'index.html',
  'proyectos/pac-arenillas-negras.html',
  'proyectos/medio-humano-horcon.html',
  'proyectos/plan-maestro-san-felipe.html',
  'proyectos/pac-la-florida.html',
  'proyectos/medio-humano-desaladora-arica.html',
  'proyectos/deslindes-rios-valparaiso.html'
];

const auditExpression = `(() => {
  const visible = el => {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    return cs.display !== 'none' && cs.visibility !== 'hidden' && r.width > 0 && r.height > 0;
  };
  const icons = [...document.querySelectorAll('i[class*="fa-"]')].filter(visible).map(el => {
    const cs = getComputedStyle(el);
    const before = getComputedStyle(el, '::before');
    return { cls: el.className, family: before.fontFamily || cs.fontFamily, content: before.content };
  });
  const images = [...document.images];
  const focusable = [...document.querySelectorAll('a[href], button, summary, input, select, textarea, [tabindex]:not([tabindex="-1"])')].filter(visible);
  const outOfBounds = [...document.body.querySelectorAll('*')].filter(el => {
    if (!visible(el)) return false;
    const cs = getComputedStyle(el);
    if (cs.position === 'fixed') return false;
    const r = el.getBoundingClientRect();
    return r.left < -1 || r.right > window.innerWidth + 1;
  }).map(el => ({ tag: el.tagName, cls: el.className || '', left: Math.round(el.getBoundingClientRect().left), right: Math.round(el.getBoundingClientRect().right) })).slice(0,20);
  const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(el => ({ level: Number(el.tagName[1]), text: el.textContent.trim().replace(/\\s+/g,' ').slice(0,120) }));
  const hero = document.querySelector('.hero-photo');
  const heroRect = hero?.getBoundingClientRect();
  return {
    title: document.title,
    innerWidth: window.innerWidth,
    scrollWidth: document.documentElement.scrollWidth,
    overflowPass: document.documentElement.scrollWidth === window.innerWidth,
    h1Count: document.querySelectorAll('h1').length,
    headings,
    landmarks: { header: !!document.querySelector('header'), nav: document.querySelectorAll('nav').length, main: !!document.querySelector('main'), footer: !!document.querySelector('footer') },
    images: { total: images.length, missing: images.filter(img => !img.complete || img.naturalWidth === 0).map(img => img.currentSrc || img.src), missingAlt: images.filter(img => !img.hasAttribute('alt')).map(img => img.currentSrc || img.src) },
    icons: { total: icons.length, broken: icons.filter(i => !/Font Awesome/i.test(i.family) || !i.content || i.content === 'none' || i.content === 'normal') },
    fonts: { openSans: document.fonts.check('16px "Open Sans"'), faFree: document.fonts.check('16px "Font Awesome 6 Free"'), bodyFamily: getComputedStyle(document.body).fontFamily },
    focusableCount: focusable.length,
    outOfBounds,
    hero: hero ? { src: hero.getAttribute('src'), alt: hero.getAttribute('alt'), loading: hero.getAttribute('loading'), fetchpriority: hero.getAttribute('fetchpriority'), decoding: hero.getAttribute('decoding'), width: Math.round(heroRect.width), height: Math.round(heroRect.height), objectFit: getComputedStyle(hero).objectFit, objectPosition: getComputedStyle(hero).objectPosition } : null,
    trazaclara: document.body.textContent.includes('TrazaClara'),
    favicon: [...document.querySelectorAll('link[rel~="icon"]')].map(el => el.getAttribute('href')),
    verCasoCount: [...document.querySelectorAll('a')].filter(a => a.textContent.trim().startsWith('Ver caso')).length,
    verProyectoCount: [...document.querySelectorAll('a')].filter(a => a.textContent.trim().startsWith('Ver proyecto')).length
  };
})()`;

async function main() {
  const browserWs = await browserEndpoint();
  const port = new URL(browserWs).port;
  const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  const pageTarget = list.find(item => item.type === 'page');
  const cdp = new CDP(pageTarget.webSocketDebuggerUrl);
  await cdp.connect();
  await Promise.all([cdp.send('Page.enable'), cdp.send('Runtime.enable'), cdp.send('Network.enable'), cdp.send('Log.enable')]);

  let active = null;
  cdp.on('Runtime.exceptionThrown', event => active?.consoleErrors.push(`exception:${event.exceptionDetails.text}`));
  cdp.on('Log.entryAdded', event => {
    if (active && ['error', 'warning'].includes(event.entry.level)) active.consoleErrors.push(`${event.entry.level}:${event.entry.text}`);
  });
  cdp.on('Network.responseReceived', event => {
    if (!active) return;
    const { response } = event;
    if (response.status >= 400) active.networkErrors.push(`${response.status} ${response.url}`);
    if (/cdnjs|fontawesome|fonts\.googleapis|fonts\.gstatic/.test(response.url)) active.fontResources.push({ status: response.status, url: response.url, mimeType: response.mimeType });
  });
  cdp.on('Network.loadingFailed', event => {
    if (active && !event.canceled) active.networkErrors.push(`FAILED ${event.errorText}`);
  });

  const results = [];
  for (const page of pages) {
    for (const width of viewports) {
      const height = width <= 390 ? 1200 : width <= 768 ? 1200 : 1000;
      active = { page, width, consoleErrors: [], networkErrors: [], fontResources: [] };
      await cdp.send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: width <= 768 });
      const loaded = cdp.once('Page.loadEventFired');
      await cdp.send('Page.navigate', { url: `http://127.0.0.1:8765/${page}` });
      await loaded;
      await delay(900);
      const evaluation = await cdp.send('Runtime.evaluate', { expression: auditExpression, returnByValue: true });
      const metrics = evaluation.result.value;

      let interaction = null;
      if (page === 'index.html' && width <= 390) {
        interaction = (await cdp.send('Runtime.evaluate', { expression: `(() => { const b=document.getElementById('nav-toggle'); b.click(); const open={expanded:b.getAttribute('aria-expanded'), active:document.getElementById('nav-links').classList.contains('active')}; b.click(); return open; })()`, returnByValue: true })).result.value;
      }
      if (page.startsWith('proyectos/')) {
        interaction = (await cdp.send('Runtime.evaluate', { expression: `(() => { const all=[...document.querySelectorAll('.case-accordion')]; const before=all.filter(x=>x.open).length; document.getElementById('btn-expand-all')?.click(); const expanded=all.filter(x=>x.open).length; document.getElementById('btn-collapse-all')?.click(); const collapsed=all.filter(x=>x.open).length; return { total:all.length, before, expanded, collapsed }; })()`, returnByValue: true })).result.value;
      }

      let focusAudit = null;
      if (width === 390) {
        await cdp.send('Runtime.evaluate', { expression: `document.activeElement?.blur(); document.body.focus();` });
        const samples = [];
        for (let i = 0; i < 12; i++) {
          await cdp.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
          await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
          const sample = (await cdp.send('Runtime.evaluate', { expression: `(() => { const el=document.activeElement; const cs=getComputedStyle(el); return { tag:el.tagName, id:el.id, cls:el.className || '', text:(el.textContent||el.getAttribute('aria-label')||'').trim().replace(/\\s+/g,' ').slice(0,80), outlineStyle:cs.outlineStyle, outlineWidth:cs.outlineWidth, outlineColor:cs.outlineColor, boxShadow:cs.boxShadow }; })()`, returnByValue: true })).result.value;
          samples.push(sample);
        }
        focusAudit = { samples, failures: samples.filter(s => (s.outlineStyle === 'none' || parseFloat(s.outlineWidth) === 0) && s.boxShadow === 'none') };
      }

      const capture = page === 'index.html' || width === 390 || width === 1440;
      let screenshot = null;
      if (capture) {
        await cdp.send('Runtime.evaluate', { expression: `window.scrollTo(0, 0)` });
        await delay(100);
        const shot = await cdp.send('Page.captureScreenshot', { format: 'png', fromSurface: true, captureBeyondViewport: false });
        const safe = page.replace(/\.html$/, '').replace(/[\\/]/g, '-');
        screenshot = `${safe}-${width}.png`;
        fs.writeFileSync(path.join(outDir, screenshot), Buffer.from(shot.data, 'base64'));
      }
      results.push({ ...active, metrics, interaction, focusAudit, screenshot });
    }
  }

  fs.writeFileSync(path.join(outDir, 'browser-results.json'), JSON.stringify(results, null, 2));
  const summary = {
    runs: results.length,
    overflowFailures: results.filter(r => !r.metrics.overflowPass).map(r => `${r.page}@${r.width}:${r.metrics.scrollWidth}/${r.metrics.innerWidth}`),
    missingImages: results.flatMap(r => r.metrics.images.missing.map(src => `${r.page}@${r.width}:${src}`)),
    missingAlt: results.flatMap(r => r.metrics.images.missingAlt.map(src => `${r.page}:${src}`)),
    brokenIcons: results.reduce((sum, r) => sum + r.metrics.icons.broken.length, 0),
    consoleErrors: [...new Set(results.flatMap(r => r.consoleErrors))],
    networkErrors: [...new Set(results.flatMap(r => r.networkErrors))],
    h1Failures: results.filter(r => r.metrics.h1Count !== 1).map(r => `${r.page}@${r.width}:${r.metrics.h1Count}`),
    outOfBoundsFailures: results.filter(r => r.metrics.outOfBounds.length).map(r => `${r.page}@${r.width}:${r.metrics.outOfBounds.length}`),
    openSansFailures: results.filter(r => !r.metrics.fonts.openSans).map(r => `${r.page}@${r.width}`),
    fontAwesomeFailures: results.filter(r => r.metrics.icons.broken.length).map(r => `${r.page}@${r.width}`),
    focusFailures: results.filter(r => r.focusAudit?.failures.length).map(r => `${r.page}@${r.width}:${r.focusAudit.failures.length}`),
    interactionFailures: results.filter(r => {
      if (r.page === 'index.html' && r.width <= 390) return r.interaction?.expanded !== 'true' || !r.interaction?.active;
      if (r.page.startsWith('proyectos/')) return r.interaction?.expanded !== r.interaction?.total || r.interaction?.collapsed !== 0;
      return false;
    }).map(r => `${r.page}@${r.width}`)
  };
  fs.writeFileSync(path.join(outDir, 'browser-summary.json'), JSON.stringify(summary, null, 2));
  console.log(JSON.stringify(summary, null, 2));
}

try {
  await main();
} finally {
  chrome.kill();
}
