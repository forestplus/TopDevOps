// Verify the Projects section is gone and the rest of the page still works.
const { spawn } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = 9345;
const URL = process.env.SHOT_URL || 'http://127.0.0.1:8765/index.html';
const profileDir = path.join(os.tmpdir(), 'dsh-check-' + Date.now());
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
  '--no-default-browser-check', '--disable-extensions',
  '--remote-debugging-port=' + PORT, '--user-data-dir=' + profileDir, 'about:blank',
], { stdio: 'ignore', windowsHide: true });

async function getWs() {
  for (let i = 0; i < 80; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json();
      const page = list.find((t) => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(250);
  }
  throw new Error('no devtools');
}

(async () => {
  const ws = new WebSocket(await getWs());
  let id = 0;
  const pending = new Map();
  const errors = [];
  const failed = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text);
    if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push('console: ' + m.params.args.map((a) => a.value || a.description).join(' '));
    if (m.method === 'Network.loadingFailed') failed.push(m.params.errorText);
    if (m.id && pending.has(m.id)) {
      const p = pending.get(m.id); pending.delete(m.id);
      m.error ? p.reject(new Error(JSON.stringify(m.error))) : p.resolve(m.result);
    }
  };
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    const mid = ++id; pending.set(mid, { resolve, reject });
    ws.send(JSON.stringify({ id: mid, method, params }));
  });
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1050, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: URL });
  await sleep(5000);

  const js = async (expr) => {
    const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.text);
    return r.result.value;
  };

  const info = await js(`({
    projectsSection: !!document.getElementById('projects'),
    navLinks: [...document.querySelectorAll('header nav a')].map(a => a.textContent.trim()),
    notesGroups: document.querySelectorAll('#notes .notes-group').length,
    notesCollapsed: [...document.querySelectorAll('#notes .notes-group')].every(g => !g.classList.contains('open')),
    githubIcon: !!document.querySelector('.social-icon.github-icon'),
    height: Math.round(document.documentElement.scrollHeight)
  })`);
  console.log('STATE', JSON.stringify(info, null, 1));

  // accordion still works
  await js(`document.querySelectorAll('#notes .notes-toggle')[0].click(); true`);
  await sleep(600);
  const acc = await js(`({
    open: document.querySelectorAll('#notes .notes-group')[0].classList.contains('open'),
    height: Math.round(document.querySelectorAll('#notes .notes-group-body')[0].getBoundingClientRect().height)
  })`);
  console.log('ACCORDION', JSON.stringify(acc));

  await js(`document.getElementById('notes').scrollIntoView({block:'start'}); window.scrollBy(0,-70); true`);
  await sleep(600);
  const shot = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('_check_notes.png', Buffer.from(shot.data, 'base64'));

  console.log('ERRORS', JSON.stringify(errors));
  console.log('FAILED_REQUESTS', JSON.stringify(failed));
  ws.close(); chrome.kill(); process.exit(0);
})().catch((e) => { console.error('FAILED', e.message); try { chrome.kill(); } catch {} process.exit(1); });
