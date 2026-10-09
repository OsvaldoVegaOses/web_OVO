/**
 * test_responsive_index2.mjs — QA responsive de index2.html
 *
 * Evalua index2.html en 5 resoluciones.
 * Inspecciona: overflow, elementos fuera de borde, columnas de grid principales.
 * Resultado global: PASS si ninguna resolucion tiene overflow ni elementos fuera de borde.
 * Exit code distinto de cero en FAIL e INCOMPLETE.
 *
 * Limpieza: chrome.kill() + server.close() en finally (siempre ejecuta).
 */

import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { spawn } from 'node:child_process';

const ROOT = process.cwd();
const PORT = 8792;
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

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
console.log(`HTTP test server running on http://127.0.0.1:${PORT}`);

const profileDir = path.join('C:\\Windows\\Temp', `ovo-resp2-${process.pid}`);
const chrome = spawn(CHROME_PATH, [
  '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  '--remote-debugging-port=0', `--user-data-dir=${profileDir}`, 'about:blank'
], { stdio: ['ignore', 'ignore', 'pipe'], windowsHide: true });

const delay = ms => new Promise(r => setTimeout(r, ms));

function cleanup() {
  try { chrome.kill(); } catch (_) {}
  try { server.close(); } catch (_) {}
}

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

const VIEWPORTS = [1440, 1024, 768, 390, 320];
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

  console.log('\n================================================================================');
  console.log('RESPONSIVE QA — index2.html');
  console.log(`Resoluciones: ${VIEWPORTS.join(', ')}px`);
  console.log('================================================================================');

  for (const width of VIEWPORTS) {
    const height = width <= 768 ? 1200 : 1000;
    const tag = `index2.html @ ${width}px`;

    try {
      await cdp.send('Emulation.setDeviceMetricsOverride', {
        width, height, deviceScaleFactor: 1, mobile: width <= 768
      });
      await cdp.send('Page.navigate', { url: `http://127.0.0.1:${PORT}/index2.html` });
      await delay(1200);

      const evalRes = await cdp.send('Runtime.evaluate', {
        expression: `(() => {
          const outOfBounds = [...document.querySelectorAll('*')].filter(el => {
            const cs = getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'fixed') return false;
            const r = el.getBoundingClientRect();
            return r.width > 0 && r.height > 0 && (r.left < -1 || r.right > window.innerWidth + 1);
          }).slice(0, 10).map(el => ({
            tag: el.tagName, cls: el.className ? el.className.toString().slice(0,60) : '',
            id: el.id, left: Math.round(el.getBoundingClientRect().left),
            right: Math.round(el.getBoundingClientRect().right)
          }));

          const expMap = document.querySelector('.experience-map');
          const featProj = document.querySelector('.featured-projects');
          const pubRows = [...document.querySelectorAll('.published-project-row')];
          const curGrid = document.querySelector('.current-project-grid');

          return {
            innerWidth: window.innerWidth,
            scrollWidth: document.documentElement.scrollWidth,
            overflow: document.documentElement.scrollWidth > window.innerWidth + 2,
            outOfBoundsCount: outOfBounds.length,
            outOfBounds: outOfBounds,
            expMapCols: expMap ? getComputedStyle(expMap).gridTemplateColumns : 'N/A',
            featProjCols: featProj ? getComputedStyle(featProj).gridTemplateColumns : 'N/A',
            pubRowsCount: pubRows.length,
            pubRowCols: pubRows[0] ? getComputedStyle(pubRows[0]).gridTemplateColumns : 'N/A',
            curGridCols: curGrid ? getComputedStyle(curGrid).gridTemplateColumns : 'N/A',
          };
        })()`,
        returnByValue: true
      });

      const r = evalRes.result.value;
      console.log(`\n=== VIEWPORT ${width}px (innerWidth=${r.innerWidth}, scrollWidth=${r.scrollWidth}) ===`);
      console.log(`  overflow:        ${r.overflow}`);
      console.log(`  outOfBounds:     ${r.outOfBoundsCount} elemento(s)`);
      console.log(`  expMap cols:     ${r.expMapCols}`);
      console.log(`  featProj cols:   ${r.featProjCols}`);
      console.log(`  pubRow cols:     ${r.pubRowCols}`);
      console.log(`  curGrid cols:    ${r.curGridCols}`);
      console.log(`  pubRowsCount:    ${r.pubRowsCount}`);

      const issues = [];
      if (r.overflow) issues.push('overflow horizontal');
      if (r.outOfBoundsCount > 0) {
        issues.push(`${r.outOfBoundsCount} elemento(s) fuera de borde`);
        r.outOfBounds.forEach(el => console.log(`    OOB: <${el.tag}> .${el.cls} #${el.id} left=${el.left} right=${el.right}`));
      }

      if (issues.length === 0) {
        passCount++;
        console.log(`  -> [PASS]`);
      } else {
        failCount++;
        const detail = `[FAIL] ${tag}: ${issues.join(' | ')}`;
        console.log(`  -> ${detail}`);
        failDetails.push(detail);
      }
    } catch (err) {
      incompleteCount++;
      const detail = `[INCOMPLETE] ${tag}: ${err.message}`;
      console.log(detail);
      failDetails.push(detail);
    }
  }
} catch (outerErr) {
  incompleteCount++;
  failDetails.push(`[INCOMPLETE] Error de configuracion: ${outerErr.message}`);
  console.error(`Error critico: ${outerErr.message}`);
} finally {
  cleanup();
}

const executed = passCount + failCount + incompleteCount;
let globalResult, exitCode;
if (incompleteCount > 0 && failCount === 0) {
  globalResult = 'INCOMPLETE'; exitCode = 2;
} else if (failCount > 0 || executed < VIEWPORTS.length) {
  globalResult = 'FAIL'; exitCode = 1;
} else {
  globalResult = 'PASS'; exitCode = 0;
}

console.log('\n================================================================================');
console.log('RESUMEN RESPONSIVE QA');
console.log('================================================================================');
console.log(`Resoluciones previstas:  ${VIEWPORTS.length}`);
console.log(`Ejecutadas:              ${executed}`);
console.log(`PASS:                    ${passCount}`);
console.log(`FAIL:                    ${failCount}`);
console.log(`INCOMPLETE:              ${incompleteCount}`);
console.log(`Resultado global:        ${globalResult}`);
console.log(`Exit code:               ${exitCode}`);
console.log('================================================================================');

if (failDetails.length > 0) {
  console.log('\nDETALLE DE FALLOS:');
  failDetails.forEach(d => console.log(`  ${d}`));
}

process.exit(exitCode);
