import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import assert from 'node:assert/strict';
const root = process.cwd();
const server = http.createServer((req,res) => {
  const file = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!file.startsWith(root) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404).end(); return; }
  const ext = path.extname(file);
  res.setHeader('Content-Type', ({'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css'})[ext] || 'application/octet-stream');
  res.end(fs.readFileSync(file));
});
await new Promise(r => server.listen(0,'127.0.0.1',r));
const port = server.address().port;
const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',['--headless','--no-sandbox','--disable-gpu','--remote-debugging-port=0',`--user-data-dir=${process.env.TEMP}\\ovo-contact-test-${process.pid}`,'about:blank'],{stdio:['ignore','ignore','pipe'],windowsHide:true});
const delay = ms => new Promise(r=>setTimeout(r,ms));
try {
 let log=''; const ws = await new Promise((resolve,reject)=>{chrome.stderr.on('data', b=>{log+=b; const m=log.match(/DevTools listening on (ws:\/\/\S+)/); if(m) resolve(m[1]);}); setTimeout(()=>reject(Error('Chrome timeout')),10000)});
 const pages=await (await fetch(`http://127.0.0.1:${new URL(ws).port}/json/list`)).json();
 const socket=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl); await new Promise(r=>socket.onopen=r);
 let id=0; const pending=new Map(); socket.onmessage=e=>{const x=JSON.parse(e.data);if(pending.has(x.id)){const [resolve,reject]=pending.get(x.id);pending.delete(x.id); x.error?reject(Error(x.error.message)):resolve(x.result)}};
 const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,[resolve,reject]);socket.send(JSON.stringify({id:n,method,params}))});
 await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
 await send('Network.setBlockedURLs',{urls:['*://www.googletagmanager.com/*','*://www.clarity.ms/*','*://*.openai.com/*','*://*.google-analytics.com/*']});
 const files=['index.html','index2.html',...fs.readdirSync('proyectos').filter(x=>x.endsWith('.html')).map(x=>'proyectos/'+x)];
 for (const width of [1440,390]) for (const file of files) {
  await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<500});
  await send('Page.navigate',{url:`http://127.0.0.1:${port}/${file}`}); await delay(500);
  const result=await send('Runtime.evaluate',{returnByValue:true,expression:`(() => {
    const links=[...document.querySelectorAll('a[href^="mailto:contacto@osvaldovega.cl"]')].filter(a=>!a.closest('.contact-notice'));
    let errors=[];
    for (const a of links) {
      const href=a.getAttribute('href');
      if (a.closest('#nav-links') && innerWidth<500) document.querySelector('#nav-toggle').click();
      a.addEventListener('click',e=>e.preventDefault(),{once:true}); a.click();
      const notice=a.closest('#nav-links') ? document.querySelector('#header .contact-notice') : a.nextElementSibling;
      if (!notice || !notice.textContent.includes('Se abrirá tu aplicación de correo.') || !notice.querySelector('a[href="mailto:contacto@osvaldovega.cl"]') || !notice.getClientRects().length || a.getAttribute('href')!==href) errors.push(href);
    }
    return {count:links.length,errors};
  })()`});
  assert.equal(result.result.value.errors.length,0,`${file} ${width}`); console.log(file,width,result.result.value.count);
 }
 socket.close();
} finally {chrome.kill();server.close();}
