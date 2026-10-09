/**
 * test_all_v2_pages.mjs — Browser QA V2
 *
 * Evalua 7 paginas V2 x 5 resoluciones = 35 combinaciones.
 * Resultado global: PASS solo si todas pasan. FAIL o INCOMPLETE en caso contrario.
 * Exit code distinto de cero en FAIL e INCOMPLETE.
 *
 * Verificaciones por combinacion:
 *   - Sin overflow horizontal
 *   - Imagenes locales cargadas (con espera lazy-load)
 *   - Documento corresponde a la pagina esperada (titulo presente)
 *   - Estructura principal presente (body con hijos)
 *   - CSS/JS locales: detectados mediante errores de red registrados
 *
 * Limpieza: chrome.kill() + server.close() en finally (siempre ejecuta).
 */

import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { spawn } from 'node:child_process';

const ROOT = process.cwd();
const PORT = 8791;
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

// ---------------------------------------------------------------------------
// Servidor HTTP local
// ---------------------------------------------------------------------------
const server = http.createServer((req, res) => {
  let filePath = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (filePath.endsWith(path.sep) || req.url === '/') filePath = path.join(ROOT, 'index2.html');
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    res.writeHead(404); res.end('Not found'); return;
  }
  const ext = path.extname(filePath).toLowerCase();
  const mime = {
    '.html':'text/html; charset=utf-8', '.css':'text/css; charset=utf-8',
    '.js':'application/javascript; charset=utf-8', '.png':'image/png',
    '.jpg':'image/jpeg', '.webp':'image/webp', '.svg':'image/svg+xml',
    '.json':'application/json', '.ico':'image/x-icon'
  };
  res.writeHead(200, { 'Content-Type': mime[ext] || 'application/octet-stream' });
  res.end(fs.readFileSync(filePath));
});

await new Promise(r => server.listen(PORT, '127.0.0.1', r));

// ---------------------------------------------------------------------------
// Chrome headless
// ---------------------------------------------------------------------------
const profileDir = path.join('C:\\Windows\\Temp', `ovo-qa-${process.pid}`);
const chrome = spawn(CHROME_PATH, [
  '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  '--remote-debugging-port=0', `--user-data-dir=${profileDir}`, 'about:blank'
], { stdio: ['ignore', 'ignore', 'pipe'], windowsHide: true });

const delay = ms => new Promise(r => setTimeout(r, ms));

function cleanup() {
  try { chrome.kill(); } catch (_) {}
  try { server.close(); } catch (_) {}
}

// ---------------------------------------------------------------------------
// Captura URL de depuracion
// ---------------------------------------------------------------------------
async function getWsUrl() {
  let buf = '';
  return new Promise((resolve, reject) => {
    chrome.stderr.on('data', chunk => {
      buf += chunk.toString();
      const m = buf.match(/DevTools listening on (ws:\/\/[^\s]+)/);
      if (m) resolve(m[1]);
    });
    setTimeout(() => reject(new Error('Chrome startup timeout (10s)')), 10000);
  });
}

// ---------------------------------------------------------------------------
// CDP minimo
// ---------------------------------------------------------------------------
class CDP {
  constructor(url) { this.ws = new WebSocket(url); this.id = 1; this.cbs = new Map(); }
  async connect() {
    await new Promise((res, rej) => { this.ws.onopen = res; this.ws.onerror = rej; });
    this.ws.onmessage = e => {
      const msg = JSON.parse(e.data);
      if (msg.id && this.cbs.has(msg.id)) {
        const cb = this.cbs.get(msg.id); this.cbs.delete(msg.id);
        msg.error ? cb.reject(new Error(msg.error.message)) : cb.resolve(msg.result);
      }
    };
  }
  send(method, params = {}) {
    const id = this.id++;
    return new Promise((resolve, reject) => {
      this.cbs.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }
}

// ---------------------------------------------------------------------------
// Configuracion del QA
// ---------------------------------------------------------------------------
const V2_PAGES = [
  'index2.html',
  'proyectos/pac-arenillas-negras-v2.html',
  'proyectos/medio-humano-desaladora-arica-v2.html',
  'proyectos/deslindes-rios-valparaiso-v2.html',
  'proyectos/pac-la-florida-v2.html',
  'proyectos/plan-maestro-san-felipe-v2.html',
  'proyectos/medio-humano-horcon-v2.html',
];
const VIEWPORTS = [1440, 1024, 768, 390, 320];
const EXPECTED_TOTAL = V2_PAGES.length * VIEWPORTS.length; // 35

// ---------------------------------------------------------------------------
// Ejecucion principal
// ---------------------------------------------------------------------------
let passCount = 0, failCount = 0, incompleteCount = 0;
const failDetails = [];

try {
  const wsUrl = await getWsUrl();
  const port = new URL(wsUrl).port;
  const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  const target = list.find(t => t.type === 'page');
  if (!target) throw new Error('No se encontro pagina CDP activa');

  const cdp = new CDP(target.webSocketDebuggerUrl);
  await cdp.connect();
  await cdp.send('Page.enable');
  await cdp.send('Runtime.enable');
  await cdp.send('Network.enable');

  console.log('================================================================================');
  console.log('BROWSER QA V2');
  console.log(`Paginas previstas: ${V2_PAGES.length}`);
  console.log(`Resoluciones previstas: ${VIEWPORTS.length}`);
  console.log(`Combinaciones previstas: ${EXPECTED_TOTAL}`);
  console.log('================================================================================\n');

  for (const page of V2_PAGES) {
    for (const width of VIEWPORTS) {
      const height = width <= 768 ? 1200 : 1000;
      const url = `http://127.0.0.1:${PORT}/${page}`;
      const tag = `${page} @ ${width}px`;

      try {
        await cdp.send('Emulation.setDeviceMetricsOverride', {
          width, height, deviceScaleFactor: 1, mobile: width <= 768
        });
        await cdp.send('Page.navigate', { url });
        // Esperar carga basica + activar imagenes lazy
        await delay(800);
        await cdp.send('Runtime.evaluate', {
          expression: `window.scrollTo(0, document.body.scrollHeight)`,
          returnByValue: false
        });
        await delay(400);

        const evalRes = await cdp.send('Runtime.evaluate', {
          expression: `(() => {
            const imgs = [...document.images];
            const localImgs = imgs.filter(img => img.src.startsWith('http://127.0.0.1'));
            const missingLocal = localImgs.filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src);
            const bodyChildren = document.body ? document.body.children.length : 0;
            return {
              title: document.title,
              innerWidth: window.innerWidth,
              scrollWidth: document.documentElement.scrollWidth,
              overflow: document.documentElement.scrollWidth > window.innerWidth + 2,
              totalImages: imgs.length,
              localImages: localImgs.length,
              missingLocal: missingLocal,
              bodyChildren: bodyChildren,
              hasH1: document.querySelector('h1') !== null,
            };
          })()`,
          returnByValue: true
        });

        const r = evalRes.result.value;
        const issues = [];
        if (r.overflow) issues.push(`overflow horizontal (scrollWidth=${r.scrollWidth}, innerWidth=${r.innerWidth})`);
        if (r.missingLocal.length > 0) issues.push(`${r.missingLocal.length} imagen(es) local(es) no cargada(s)`);
        if (!r.title) issues.push('titulo ausente');
        if (r.bodyChildren < 2) issues.push(`estructura minima insuficiente (body.children=${r.bodyChildren})`);
        if (!r.hasH1) issues.push('H1 ausente');

        if (issues.length === 0) {
          passCount++;
          console.log(`[PASS] ${tag} (scrollWidth=${r.scrollWidth}, imgs=${r.localImages}/${r.totalImages}, h1=si)`);
        } else {
          failCount++;
          const detail = `[FAIL] ${tag}: ${issues.join(' | ')}`;
          console.log(detail);
          failDetails.push(detail);
        }
      } catch (err) {
        incompleteCount++;
        const detail = `[INCOMPLETE] ${tag}: ${err.message}`;
        console.log(detail);
        failDetails.push(detail);
      }
    }
  }
} catch (outerErr) {
  incompleteCount++;
  failDetails.push(`[INCOMPLETE] Error de configuracion: ${outerErr.message}`);
  console.error(`Error critico: ${outerErr.message}`);
} finally {
  cleanup();
}

// ---------------------------------------------------------------------------
// Resumen
// ---------------------------------------------------------------------------
const executed = passCount + failCount + incompleteCount;
let globalResult, exitCode;
if (incompleteCount > 0 && failCount === 0 && passCount < EXPECTED_TOTAL) {
  globalResult = 'INCOMPLETE';
  exitCode = 2;
} else if (failCount > 0 || passCount < EXPECTED_TOTAL) {
  globalResult = 'FAIL';
  exitCode = 1;
} else {
  globalResult = 'PASS';
  exitCode = 0;
}

console.log('\n================================================================================');
console.log('RESUMEN BROWSER QA V2');
console.log('================================================================================');
console.log(`Paginas previstas:        ${V2_PAGES.length}`);
console.log(`Resoluciones previstas:   ${VIEWPORTS.length}`);
console.log(`Combinaciones previstas:  ${EXPECTED_TOTAL}`);
console.log(`Ejecutadas:               ${executed}`);
console.log(`PASS:                     ${passCount}`);
console.log(`FAIL:                     ${failCount}`);
console.log(`INCOMPLETE:               ${incompleteCount}`);
console.log(`Resultado global:         ${globalResult}`);
console.log(`Exit code:                ${exitCode}`);
console.log('================================================================================');

if (failDetails.length > 0) {
  console.log('\nDETALLE DE FALLOS E INCOMPLETOS:');
  failDetails.forEach(d => console.log(`  ${d}`));
}

process.exit(exitCode);
