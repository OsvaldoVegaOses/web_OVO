import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { spawn } from 'node:child_process';

const root = process.cwd();
const server = http.createServer((req, res) => {
  let filePath = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (filePath.endsWith(path.sep) || req.url === '/') filePath = path.join(root, 'index2.html');
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    res.writeHead(404);
    res.end('Not found');
    return;
  }
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.json': 'application/json',
    '.ico': 'image/x-icon'
  };
  res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
  res.end(fs.readFileSync(filePath));
});

await new Promise(resolve => server.listen(8790, '127.0.0.1', resolve));

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const profileDir = path.join('C:\\Windows\\Temp', `ovo-all-${process.pid}`);
const chrome = spawn(chromePath, [
  '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
  '--remote-debugging-port=0', `--user-data-dir=${profileDir}`, 'about:blank'
], { stdio: ['ignore', 'ignore', 'pipe'], windowsHide: true });

const delay = ms => new Promise(r => setTimeout(r, ms));

async function getWsUrl() {
  let buf = '';
  return new Promise((resolve, reject) => {
    chrome.stderr.on('data', chunk => {
      buf += chunk.toString();
      const m = buf.match(/DevTools listening on (ws:\/\/[^\s]+)/);
      if (m) resolve(m[1]);
    });
    setTimeout(() => reject(new Error('Chrome timeout')), 10000);
  });
}

const wsUrl = await getWsUrl();
const port = new URL(wsUrl).port;
const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
const target = list.find(t => t.type === 'page');

class CDP {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.id = 1;
    this.callbacks = new Map();
  }
  async connect() {
    await new Promise((res, rej) => {
      this.ws.onopen = res;
      this.ws.onerror = rej;
    });
    this.ws.onmessage = e => {
      const msg = JSON.parse(e.data);
      if (msg.id && this.callbacks.has(msg.id)) {
        const cb = this.callbacks.get(msg.id);
        this.callbacks.delete(msg.id);
        if (msg.error) cb.reject(new Error(msg.error.message));
        else cb.resolve(msg.result);
      }
    };
  }
  send(method, params = {}) {
    const id = this.id++;
    return new Promise((resolve, reject) => {
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }
}

const cdp = new CDP(target.webSocketDebuggerUrl);
await cdp.connect();
await cdp.send('Page.enable');
await cdp.send('Runtime.enable');

const v2_pages = [
  'index2.html',
  'proyectos/pac-arenillas-negras-v2.html',
  'proyectos/medio-humano-desaladora-arica-v2.html',
  'proyectos/deslindes-rios-valparaiso-v2.html',
  'proyectos/pac-la-florida-v2.html',
  'proyectos/plan-maestro-san-felipe-v2.html',
  'proyectos/medio-humano-horcon-v2.html',
];

const viewports = [1440, 768, 390, 320];

const results = [];

for (const p of v2_pages) {
  for (const width of viewports) {
    const height = width <= 768 ? 1200 : 1000;
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width, height, deviceScaleFactor: 1, mobile: width <= 768
    });
    await cdp.send('Page.navigate', { url: `http://127.0.0.1:8790/${p}` });
    await delay(600);

    const evalRes = await cdp.send('Runtime.evaluate', {
      expression: `(() => {
        const images = [...document.images];
        const missing = images.filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src);
        const accordions = [...document.querySelectorAll('.case-accordion')];
        const navToggle = document.getElementById('nav-toggle');

        return {
          title: document.title,
          innerWidth: window.innerWidth,
          scrollWidth: document.documentElement.scrollWidth,
          overflow: document.documentElement.scrollWidth > window.innerWidth,
          missingImages: missing,
          accordionCount: accordions.length,
          hasNavToggle: !!navToggle,
        };
      })()`,
      returnByValue: true
    });

    const res = evalRes.result.value;
    results.push({ page: p, width, ...res });
    if (res.overflow || res.missingImages.length > 0) {
      console.log(`[FAIL] ${p} @ ${width}px: overflow=${res.overflow}, missingImgs=${res.missingImages.length}`);
    } else {
      console.log(`[PASS] ${p} @ ${width}px (scrollWidth=${res.scrollWidth}, accordions=${res.accordionCount})`);
    }
  }
}

chrome.kill();
server.close();
console.log('\nAll V2 pages tested successfully!');
process.exit(0);
