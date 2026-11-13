const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync('contact-tracking.js', 'utf8');
function setup(host, path) {
  const calls = [], listeners = [];
  const window = { location: { hostname: host, pathname: path }, clarity: (...args) => calls.push(args) };
  const document = { addEventListener: (name, callback) => listeners.push(callback) };
  vm.runInNewContext(source, { window, document });
  return { calls, listeners, window };
}
test('versiones se etiquetan y clic real de correo registra un solo evento por servicio', () => {
  const { calls, listeners, window } = setup('osvaldovega.cl', '/index2.html');
  const link = { dataset: { contactSource: 'servicios', contactService: 'pac' }, getAttribute: () => 'mailto:contacto@osvaldovega.cl?subject=PAC' };
  listeners[0]({ isTrusted: true, button: 0, defaultPrevented: false, target: { closest: () => link } });
  assert.deepEqual(calls, [['set', 'ovo_version', 'v2'], ['event', 'ovo_correo_pac']]);
  assert.equal(window.dataLayer.length, 1);
});
test('no se registra fallback, enlaces internos ni eventos sintéticos', () => {
  const { calls, listeners } = setup('www.osvaldovega.cl', '/');
  for (const [href, data, trusted] of [['mailto:contacto@osvaldovega.cl', {}, true], ['#contacto', {contactSource:'hero'}, true], ['mailto:contacto@osvaldovega.cl', {contactSource:'hero'}, false]]) {
    const link = { dataset: data, getAttribute: () => href };
    listeners[0]({isTrusted: trusted, button: 0, defaultPrevented: false, target: {closest: () => link}});
  }
  assert.deepEqual(calls, [['set', 'ovo_version', 'v1']]);
});
test('no se registra en localhost', () => {
  const {calls, listeners} = setup('localhost', '/');
  assert.equal(calls.length, 0); assert.equal(listeners.length, 0);
});
