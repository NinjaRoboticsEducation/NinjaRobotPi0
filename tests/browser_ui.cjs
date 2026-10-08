// Static built-UI contract tests: no robot backend, external sockets, speech, or shutdown.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const build = path.resolve(process.argv[2]);
const shots = process.env.UI_SCREENSHOTS;
(async () => {
  const server = http.createServer((req, res) => {
    let route = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    if (!path.extname(route)) route = '/index.html';
    const file = path.resolve(build, '.' + route);
    if (!file.startsWith(build + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
      res.writeHead(404); res.end(); return;
    }
    const mime = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.png': 'image/png' };
    res.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  let checks = 0;
  const requests = [];
  try {
    browser = await chromium.launch({ headless: true });
    const base = `http://127.0.0.1:${server.address().port}`;
    for (const viewport of [{width:360,height:800},{width:390,height:844},{width:844,height:390},{width:1280,height:900}]) {
      const context = await browser.newContext({ viewport, locale: 'en-US', reducedMotion: 'reduce' });
      await context.addInitScript(() => {
        window.__sockets = [];
        window.WebSocket = class { constructor(url) { this.url = url; window.__sockets.push(this); } close() {} };
        window.confirm = () => false;
        window.SpeechRecognition = class { start() { throw new Error('Live speech is forbidden in fixtures'); } };
      });
      await context.route('**/*', async route => {
        const request = route.request(); const url = new URL(request.url());
        if (url.origin !== base) return route.abort();
        if (!url.pathname.startsWith('/api/')) return route.continue();
        requests.push({method:request.method(), path:url.pathname, body:request.postData()});
        assert.notEqual(url.pathname, '/api/system/shutdown');
        let body = { advertising: true };
        if (url.pathname === '/api/display/expressions') body = { expressions: ['happy'] };
        if (url.pathname === '/api/sound/emotions') body = { emotions: ['joy'] };
        if (url.pathname === '/api/servos/movements') body = { movements: ['greeting'] };
        if (url.pathname === '/api/agent/chat') body = { response: 'Fixture reply' };
        await route.fulfill({status:200, contentType:'application/json', body:JSON.stringify(body)});
      });
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.goto(base + '/agent'); await page.waitForLoadState('networkidle');
      assert.ok(await page.getByText('BLE advertising').isVisible()); checks++;
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true); checks++;
      assert.deepEqual(await page.evaluate(() => window.__sockets.map(s => new URL(s.url).pathname).sort()), ['/ws/distance','/ws/events']); checks++;
      await page.evaluate(() => window.__sockets.find(s => s.url.endsWith('/ws/distance')).onmessage({data:'{"distance_mm":123}'}));
      await page.getByText('123 mm').waitFor(); checks++;
      await page.getByRole('textbox').fill('Fixture message');
      await page.getByRole('button', {name:'Send', exact:true}).click();
      await page.getByText('Fixture reply', {exact:true}).waitFor();
      const chat = requests.filter(r => r.path === '/api/agent/chat').at(-1);
      assert.equal(chat.method, 'POST'); assert.deepEqual(JSON.parse(chat.body), {message:'Fixture message',language:'en'}); checks++;
      for (const name of ['Run expression','Play sound','Run movement']) await page.getByRole('button',{name,exact:true}).click();
      for (const endpoint of ['/api/display/expressions/happy','/api/sound/emotions/joy','/api/servos/movements/greeting/execute']) assert.ok(requests.some(r => r.path===endpoint && r.method==='POST')); checks++;
      await page.getByRole('button', {name:/System activity/}).click(); checks++;
      await page.getByRole('button', {name:'Open robot menu'}).click();
      await page.getByRole('dialog').waitFor();
      await page.keyboard.press('Escape');
      assert.equal(await page.getByRole('button', {name:'Open robot menu'}).evaluate(el => el===document.activeElement), true); checks++;
      if (shots) {fs.mkdirSync(shots,{recursive:true});await page.screenshot({path:path.join(shots,`agent-${viewport.width}.png`),fullPage:true});}
      // Localization and navigation can only issue read requests.
      for (const lang of ['ja','zh-TW','zh-CN','en']) {
        await page.getByRole('button').filter({hasText:'☰'}).click();
        await page.getByRole('dialog').locator('select').selectOption(lang);
        await page.keyboard.press('Escape');
        const text = await page.locator('body').innerText();
        assert.ok(!/home\.(sliderText|systemTitle)|agent\.(welcome|systemLog)|header\.(openMenu|advertising)/.test(text)); checks++;
      }
      await page.goto(base + '/'); await page.waitForLoadState('networkidle');
      assert.ok(await page.getByText('Slide to power off').isVisible()); checks++;
      const power = page.getByRole('slider');
      await power.focus();
      for (let i=0;i<10;i++) await page.keyboard.press('ArrowRight');
      await page.keyboard.press('Enter');
      assert.equal(await power.getAttribute('aria-valuenow'), '0'); checks++;
      if (shots) await page.screenshot({path:path.join(shots,`home-${viewport.width}.png`),fullPage:true});
      await page.goto(base+'/help');await page.waitForLoadState('networkidle');
      assert.ok(await page.getByRole('heading',{name:'Help & Documentation'}).isVisible()); checks++;
      assert.deepEqual(errors,[]); checks++;
      await context.close();
    }
    console.log(`PASS: ${checks} mocked browser contract, locale, responsive, and navigation assertions.`);
  } finally { if(browser)await browser.close(); await new Promise(resolve=>server.close(resolve)); }
})().catch(error=>{console.error(error);process.exitCode=1;});
