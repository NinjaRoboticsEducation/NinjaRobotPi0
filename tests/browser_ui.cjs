// Optional built-UI tests for a development host with an existing Playwright browser.
// Inert APIs, sockets and speech only; never starts the robot backend or shuts down the Pi.
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
  let browser, checks = 0;
  try {
    browser = await chromium.launch({ headless: true });
    const base = `http://127.0.0.1:${server.address().port}`;
    for (const viewport of [{width:320,height:568},{width:360,height:800},{width:390,height:844},{width:430,height:932},{width:844,height:390},{width:768,height:1024},{width:1280,height:900}]) {
      const context = await browser.newContext({ viewport, locale: 'en-US', reducedMotion: 'reduce' });
      await context.addInitScript(() => {
        window.__sockets = []; window.__recognizers = [];
        window.WebSocket = class {
          static OPEN = 1;
          constructor(url) {
            this.url = url; this.readyState = 1; window.__sockets.push(this);
            setTimeout(() => {
              this.onopen?.();
              if (url.endsWith('/ws/session')) this.onmessage?.({data:'{"type":"session","status":"connected"}'});
            }, 0);
          }
          send() {}
          close() { this.readyState = 3; }
        };
        window.confirm = () => false;
        window.SpeechRecognition = class {
          constructor() { window.__recognizers.push(this); }
          start() { this.started = true; this.onstart?.(); }
          stop() { this.stopped = true; this.onend?.(); }
          abort() { this.aborted = true; this.onend?.(); }
        };
      });
      const requests = [];
      await context.route('**/*', async route => {
        const request = route.request(), url = new URL(request.url());
        if (url.origin !== base) return route.abort();
        if (!url.pathname.startsWith('/api/')) return route.continue();
        requests.push({method:request.method(), path:url.pathname, body:request.postData()});
        assert.notEqual(url.pathname, '/api/system/shutdown');
        let body = {};
        if (url.pathname === '/api/display/expressions') body = { expressions: ['idle'] };
        if (url.pathname === '/api/sound/emotions') body = { emotions: ['happy'] };
        if (url.pathname === '/api/servos/movements') body = { movements: ['spider_dance'] };
        if (url.pathname === '/api/agent/chat') body = { response: 'Fixture reply' };
        await route.fulfill({status:200, contentType:'application/json', body:JSON.stringify(body)});
      });
      const page = await context.newPage(), errors = [];
      page.on('pageerror', error => errors.push(error.message));
      const fits = async () => { assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)); checks++; };
      const snapshot = async name => {
        if (shots) {fs.mkdirSync(shots,{recursive:true});await page.screenshot({path:path.join(shots,`${name}-${viewport.width}.png`),fullPage:true});}
      };
      const event = (endpoint, data) => page.evaluate(({endpoint,data}) => window.__sockets.find(s=>s.readyState===1 && s.url.endsWith(endpoint)).onmessage({data:JSON.stringify(data)}),{endpoint,data});
      await page.goto(base);await page.getByRole('link',{name:'Movement Tool'}).waitFor();await fits();await snapshot('home');
      await page.evaluate(() => {window.__primarySession=window.__sockets.find(s=>s.url.endsWith('/ws/session'));});
      const power = page.getByRole('slider');await power.focus();
      for (let i=0;i<10;i++) await page.keyboard.press('ArrowRight');
      await page.keyboard.press('Enter');assert.equal(await power.getAttribute('aria-valuenow'),'0');checks++;
      await page.getByRole('link',{name:'Movement Tool'}).click();
      await page.getByRole('option',{name:'spider_dance'}).waitFor({state:'attached'});
      assert.equal(await page.getByRole('textbox').count(),0);checks++;
      await event('/ws/distance',{distance_mm:125});await page.getByRole('status',{name:'Distance Detection: 125 mm'}).waitFor();checks++;
      await event('/ws/distance',{distance_mm:-1});await page.getByRole('status',{name:/Distance Detection: Unavailable/}).waitFor();checks++;
      for (const name of ['Run movement','Run expression','Play sound']) await page.getByRole('button',{name,exact:true}).click();
      for(const endpoint of ['/api/servos/movements/spider_dance/execute','/api/display/expressions/idle','/api/sound/emotions/happy']) assert.ok(requests.some(r=>r.path===endpoint && r.method==='POST'));
      assert.ok(!requests.some(r=>r.path==='/api/agent/chat'));checks++;
      const activity = page.getByRole('button',{name:/System activity/});assert.equal(await activity.getAttribute('aria-expanded'),'false');checks++;
      await event('/ws/events',{type:'log',message:'Fixture live activity'});await activity.click();
      await page.getByText('Fixture live activity',{exact:true}).waitFor();checks++;
      await page.locator('#robot-activity-log').getByRole('button',{name:'Clear Messages'}).click();
      await page.getByText('Events will appear here.').waitFor();checks++;
      await page.keyboard.press('Escape');assert.equal(await activity.getAttribute('aria-expanded'),'false');checks++;
      await fits();await snapshot('movement');
      await page.getByRole('link',{name:'Open robot menu'}).click();await page.getByRole('link',{name:'Chat with Robot'}).click();
      assert.equal(await page.getByRole('combobox').count(),0);checks++;
      const voice = page.getByRole('button',{name:'Voice Input',exact:true});await voice.click();
      assert.equal(await voice.getAttribute('aria-pressed'),'true');checks++;await snapshot('voice-on');
      await page.evaluate(()=>window.__recognizers.at(-1).onresult({results:[[{transcript:'Fixture speech'}]]}));
      await page.waitForFunction(()=>document.querySelector('textarea').value==='Fixture speech');
      await voice.click();assert.equal(await page.evaluate(()=>window.__recognizers.at(-1).stopped),true);checks++;
      await Promise.all([page.waitForResponse(r=>new URL(r.url()).pathname==='/api/agent/chat'),page.getByRole('button',{name:'Send',exact:true}).click()]);
      await page.getByText('Fixture reply',{exact:true}).waitFor();
      assert.deepEqual(JSON.parse(requests.at(-1).body),{message:'Fixture speech',language:'en'});checks++;
      await page.locator('section').getByRole('button',{name:'Clear Messages'}).click();
      assert.equal(await page.getByText('Fixture reply',{exact:true}).count(),0);checks++;
      await fits();await snapshot('chat');
      await page.getByRole('button',{name:/System activity/}).click();await snapshot('chat-log');
      await page.keyboard.press('Escape');await voice.click();await page.getByRole('link',{name:'Open robot menu'}).click();
      await page.waitForFunction(()=>window.__recognizers.at(-1).aborted);checks++;
      assert.equal(await page.evaluate(()=>window.__primarySession===window.__sockets.find(s=>s.readyState===1 && s.url.endsWith('/ws/session'))),true);checks++;
      for(const [locale,file] of [['ja','ja'],['zh-TW','zh-tw'],['zh-CN','zh-cn'],['en','en']]) {
        const labels=JSON.parse(fs.readFileSync(path.join(__dirname,'../ninja_webapp/src/locales',file+'.json'),'utf8'));
        await page.getByRole('combobox').selectOption(locale);
        await page.waitForFunction(locale=>document.documentElement.lang===locale,locale);checks++;await fits();
        await page.getByRole('link',{name:labels.home.movementButton}).click();
        await page.getByRole('heading',{name:labels.agent.distance}).waitFor();checks++;await fits();
        await page.getByRole('link',{name:labels.header.openMenu}).click();await page.getByRole('link',{name:labels.home.chatButton}).click();
        await page.getByRole('heading',{name:labels.agent.conversation}).waitFor();checks++;await fits();
        await page.getByRole('button',{name:labels.agent.voice,exact:true}).click();
        assert.equal(await page.evaluate(()=>window.__recognizers.at(-1).lang),{en:'en-US',ja:'ja-JP','zh-TW':'zh-TW','zh-CN':'zh-CN'}[locale]);checks++;
        await page.getByRole('link',{name:labels.header.openMenu}).click();
      }
      await page.goto(base+'/help');await page.getByRole('heading',{name:'Welcome to NinjaRobot'}).waitFor();assert.equal(new URL(page.url()).pathname,'/');checks++;
      assert.deepEqual(errors,[]);checks++;await context.close();
    }
    console.log(`PASS: ${checks} mocked browser contract, locale, responsive, and navigation assertions.`);
  } finally { if(browser)await browser.close();await new Promise(resolve=>server.close(resolve)); }
})().catch(error=>{console.error(error);process.exitCode=1;});
