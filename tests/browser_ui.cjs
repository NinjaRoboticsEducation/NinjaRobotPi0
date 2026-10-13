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
    browser = await chromium.launch({ headless: true, ...(process.env.PLAYWRIGHT_EXECUTABLE_PATH ? { executablePath: process.env.PLAYWRIGHT_EXECUTABLE_PATH } : {}) });
    const base = `http://127.0.0.1:${server.address().port}`;
    for (const viewport of [{width:390,height:670},{width:390,height:740},{width:390,height:844},{width:320,height:568},{width:360,height:640},{width:360,height:800},{width:430,height:932},{width:568,height:320},{width:844,height:390},{width:768,height:1024},{width:1280,height:900}]) {
      const mobile = viewport.width < 1000;
      const context = await browser.newContext({ viewport, isMobile:mobile, hasTouch:mobile, locale: 'en-US', reducedMotion: 'reduce' });
      await context.addInitScript(() => {
        window.__sockets = []; window.__recognizers = []; window.__fullscreenRequests = 0;
        Object.defineProperty(document, 'fullscreenEnabled', { configurable:true, value:true });
        Object.defineProperty(document, 'webkitFullscreenEnabled', { configurable:true, value:false });
        Element.prototype.requestFullscreen = () => {window.__fullscreenRequests++;return Promise.reject(new Error('Fixture denied fullscreen'));};
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
        if (url.pathname === '/api/robot/status') body = { robot_type: 'spider' };
        if (url.pathname === '/api/display/expressions') body = { expressions: ['idle'] };
        if (url.pathname === '/api/sound/emotions') body = { emotions: ['happy'] };
        if (url.pathname === '/api/servos/movements') body = { movements: ['spider_dance','spider_run_forward','spider_run_backward','spider_turn_left','spider_turn_right','spider_home'] };
        if (/^\/api\/servos\/movements\/.+\/execute$/.test(url.pathname)) body = { status: 'executed' };
        if (url.pathname === '/api/agent/chat') body = { response: 'Fixture reply' };
        await route.fulfill({status:200, contentType:'application/json', body:JSON.stringify(body)});
      });
      const page = await context.newPage(), errors = [];
      page.on('pageerror', error => errors.push(error.message));
      const fits = async () => {
        assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth && document.documentElement.scrollHeight <= innerHeight));
        assert.equal(await page.evaluate(() => { window.scrollTo(0,100); return scrollY; }),0);
        // Every control stays reachable inside its own scroll region, above the folded drawer.
        for (const control of await page.locator('main a, main button, main select, main textarea, main [role="slider"]').all()) {
          if (!await control.isVisible()) continue;
          await control.scrollIntoViewIfNeeded();
          const box = await control.boundingBox();
          assert.ok(box && box.x >= -1 && box.x + box.width <= viewport.width + 1 && box.y >= -1 && box.y + box.height <= viewport.height + 1, `Unreachable control: ${await control.getAttribute('aria-label')}`);
          assert.ok(await control.evaluate(el=>{const b=el.getBoundingClientRect();return el.contains(document.elementFromPoint(b.x+b.width/2,b.y+b.height/2));}),`Covered control: ${await control.getAttribute('aria-label')}`);
        }
        await page.evaluate(()=>document.querySelector('main > div')?.scrollTo(0,0));
        checks++;
      };
      const snapshot = async name => {
        if (shots) {
          fs.mkdirSync(shots,{recursive:true});
          await page.evaluate(()=>document.fonts.ready);
          await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
          await page.screenshot({path:path.join(shots,`${name}-${viewport.width}x${viewport.height}.png`),fullPage:true,animations:'disabled'});
        }
      };
      const sliderLabelFits = async () => {
        const geometry = await page.getByRole('slider').evaluate(thumb=>{
          const container=thumb.parentElement, text=container.querySelector('span');
          const box=container.getBoundingClientRect(), label=text.getBoundingClientRect(), style=getComputedStyle(text);
          return {dx:Math.abs(label.x+label.width/2-box.x-box.width/2),dy:Math.abs(label.y+label.height/2-box.y-box.height/2),font:parseFloat(style.fontSize),height:label.height,trackHeight:box.height};
        });
        assert.ok(geometry.dx<=1 && geometry.dy<=1,'Power label must share the track center');
        assert.ok(geometry.font>=16 && geometry.height<=geometry.trackHeight-2,'Power label must remain readable within its track');checks++;
      };
      const distributedCards = async activitySpace => {
        if(viewport.width!==390) return;
        const layout=await page.locator('main > div').evaluate(el=>{
          const box=el.getBoundingClientRect(), cards=[...el.querySelectorAll(':scope > section')].map(card=>card.getBoundingClientRect());
          return {overflow:el.scrollHeight-el.clientHeight,bottomSpace:box.bottom-cards.at(-1).bottom,gaps:cards.slice(1).map((card,i)=>card.top-cards[i].bottom),lineRatios:[...el.querySelectorAll('p')].map(p=>parseFloat(getComputedStyle(p).lineHeight)/parseFloat(getComputedStyle(p).fontSize))};
        });
        assert.ok(layout.overflow<=1,`Phone-sized pages should fit without internal overflow: ${JSON.stringify(layout)}`);
        assert.ok(layout.bottomSpace<=activitySpace+24,'Cards must use the lower page area');
        assert.ok(layout.gaps.every(gap=>gap>=10) && Math.max(...layout.gaps)-Math.min(...layout.gaps)<=1,'Card gaps must be even and deliberate');
        assert.ok(layout.lineRatios.every(ratio=>ratio>=1.4),'Descriptions need readable line spacing');checks++;
      };
      const event = (endpoint, data) => page.evaluate(({endpoint,data}) => window.__sockets.find(s=>s.readyState===1 && s.url.endsWith(endpoint)).onmessage({data:JSON.stringify(data)}),{endpoint,data});
      await page.goto(base);
      try { await page.getByRole('link',{name:'Movement Tool'}).waitFor(); }
      catch(error) { console.error({errors,body:await page.locator('body').innerText()}); throw error; }
      await fits();await snapshot('home');
      await sliderLabelFits();await distributedCards(0);
      assert.equal(await page.locator('main > div').evaluate(el=>getComputedStyle(el).borderTopColor),'rgba(0, 163, 255, 0.25)');checks++;
      assert.equal(await page.getByRole('slider').evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(255, 138, 0)');checks++;
      if(viewport.width===390 && viewport.height===844) {
        // Browser chrome can reduce only the visual viewport, leaving media-query height tall.
        for(const height of [670,740]) {
          await page.evaluate(height=>{Object.defineProperty(visualViewport,'height',{configurable:true,value:height});visualViewport.dispatchEvent(new Event('resize'));},height);
          await distributedCards(0);await sliderLabelFits();
        }
        await page.evaluate(()=>{delete visualViewport.height;visualViewport.dispatchEvent(new Event('resize'));});
      }
      assert.ok(await page.evaluate(()=>document.querySelector('meta[name="viewport"]').content.includes('user-scalable=no') && getComputedStyle(document.documentElement).touchAction==='pan-x pan-y'));checks++;
      const selection = async expected => {
        for(const [label,route] of [['Movement Tool','/movement'],['Chat with Robot','/agent']]) {
          const link=page.getByRole('link',{name:label,exact:true});
          assert.equal(await link.getAttribute('aria-current'),expected===route?'true':null);
          assert.equal(await link.evaluate(el=>getComputedStyle(el).backgroundColor),expected===route?'rgb(255, 138, 0)':'rgb(6, 71, 128)');
        }
        checks++;
      };
      await selection(null);assert.equal(await page.evaluate(()=>window.__fullscreenRequests),0);checks++;
      await page.evaluate(() => {window.__primarySession=window.__sockets.find(s=>s.url.endsWith('/ws/session'));});
      const power = page.getByRole('slider');await power.focus();
      for (let i=0;i<10;i++) await page.keyboard.press('ArrowRight');
      await page.keyboard.press('Enter');assert.equal(await power.getAttribute('aria-valuenow'),'0');checks++;
      if(mobile) await page.getByRole('link',{name:'Movement Tool'}).tap();
      else await page.getByRole('link',{name:'Movement Tool'}).click();
      await page.getByRole('option',{name:'spider_dance'}).waitFor({state:'attached'});
      await page.getByRole('link',{name:'NINJA ROBOT Pi0 - Spider',exact:true}).waitFor();checks++;
      assert.equal(await page.evaluate(()=>window.__fullscreenRequests),1);checks++;
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
      assert.equal(await activity.evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(255, 138, 0)');checks++;
      await page.keyboard.press('Escape');assert.equal(await activity.getAttribute('aria-expanded'),'false');checks++;
      assert.equal(await activity.evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(6, 71, 128)');checks++;
      await event('/ws/distance',{distance_mm:125});await fits();await distributedCards(56);
      for (const button of await page.locator('[data-direction]').all()) {
        const box=await button.boundingBox();assert.ok(box.width>=44 && box.height>=44);
      } checks++;
      assert.equal(await page.locator('main section').last().evaluate(el=>getComputedStyle(el).borderTopColor),'rgba(0, 163, 255, 0.25)');checks++;
      const readout=await page.getByRole('status',{name:'Distance Detection: 125 mm'}).boundingBox();
      assert.ok(readout.x<viewport.width/3);checks++;
      await snapshot('movement');
      await page.getByRole('link',{name:'Open robot menu'}).click();await page.getByRole('link',{name:'Movement Tool',exact:true}).waitFor();await selection('/movement');
      await page.getByRole('link',{name:'Chat with Robot'}).click();await page.getByRole('heading',{name:'Conversation',exact:true}).waitFor();
      assert.equal(await page.getByRole('combobox').count(),0);checks++;
      const voice = page.getByRole('button',{name:'Voice Input',exact:true});
      assert.equal(await voice.evaluate(el=>getComputedStyle(el).backgroundColor),'rgb(6, 71, 128)');checks++;
      assert.equal(await page.locator('section').evaluate(el=>getComputedStyle(el).borderTopColor),'rgba(0, 163, 255, 0.25)');checks++;
      assert.equal(await page.getByText('Hello, NinjaRobot Agent is ready.',{exact:true}).evaluate(el=>getComputedStyle(el).borderTopColor),'rgba(189, 196, 202, 0.25)');checks++;
      await voice.click();
      assert.equal(await voice.getAttribute('aria-pressed'),'true');checks++;await snapshot('voice-on');
      await page.evaluate(()=>window.__recognizers.at(-1).onresult({results:[[{transcript:'Fixture speech'}]]}));
      await page.waitForFunction(()=>document.querySelector('textarea').value==='Fixture speech');
      await voice.click();assert.equal(await page.evaluate(()=>window.__recognizers.at(-1).stopped),true);checks++;
      await Promise.all([page.waitForResponse(r=>new URL(r.url()).pathname==='/api/agent/chat'),page.getByRole('button',{name:'Send',exact:true}).click()]);
      await page.getByText('Fixture reply',{exact:true}).waitFor();
      assert.equal(await page.getByText('Fixture speech',{exact:true}).evaluate(el=>getComputedStyle(el).borderTopColor),'rgba(0, 163, 255, 0.25)');checks++;
      await event('/ws/events',{type:'execute_received',full_code:'Fixture system code',code_length:19});
      await page.getByText('Fixture system code',{exact:true}).waitFor();
      assert.equal(await page.getByText('Fixture system code',{exact:true}).evaluate(el=>getComputedStyle(el.parentElement).borderTopColor),'rgba(0, 163, 255, 0.25)');checks++;
      assert.deepEqual(JSON.parse(requests.at(-1).body),{message:'Fixture speech',language:'en'});checks++;
      await page.locator('section').getByRole('button',{name:'Clear Messages'}).click();
      assert.equal(await page.getByText('Fixture reply',{exact:true}).count(),0);checks++;
      await fits();await snapshot('chat');
      await page.getByRole('button',{name:/System activity/}).click();await snapshot('chat-log');
      await page.keyboard.press('Escape');await voice.click();await page.getByRole('link',{name:'Open robot menu'}).click();
      await page.waitForFunction(()=>window.__recognizers.at(-1).aborted);checks++;
      await page.getByRole('link',{name:'Movement Tool',exact:true}).waitFor();await selection('/agent');
      await snapshot('home-selected');
      assert.equal(await page.evaluate(()=>window.__primarySession===window.__sockets.find(s=>s.readyState===1 && s.url.endsWith('/ws/session'))),true);checks++;
      await page.reload();await page.getByRole('link',{name:'Movement Tool',exact:true}).waitFor();await selection(null);
      // No Fullscreen API is a supported fallback, and must not block navigation.
      await page.evaluate(()=>{Object.defineProperty(document,'fullscreenEnabled',{value:false});delete Element.prototype.requestFullscreen;});
      for(const [locale,file] of [['ja','ja'],['zh-TW','zh-tw'],['zh-CN','zh-cn'],['en','en']]) {
        const labels=JSON.parse(fs.readFileSync(path.join(__dirname,'../ninja_webapp/src/locales',file+'.json'),'utf8'));
        await page.getByRole('combobox').selectOption(locale);
        await page.waitForFunction(locale=>document.documentElement.lang===locale,locale);checks++;await fits();
        await sliderLabelFits();
        await page.getByRole('link',{name:labels.home.movementButton}).click();
        await page.getByRole('heading',{name:labels.agent.distance}).waitFor();checks++;await fits();
        for(const direction of ['up','down','left','right','center']) await page.getByRole('button',{name:labels.gamepad[direction],exact:true}).waitFor();checks++;
        if(viewport.width===390 && viewport.height===740) {
          await page.evaluate(()=>{window.__fontOriginals=[...document.querySelectorAll('main h1, main h2, main p, main select')].map(el=>[el,el.style.fontSize]);for(const [el] of window.__fontOriginals)el.style.fontSize=`${parseFloat(getComputedStyle(el).fontSize)*1.5}px`;});
          await fits();checks++;await snapshot(`movement-enlarged-${locale}`);
          await page.evaluate(()=>{for(const [el,size] of window.__fontOriginals)el.style.fontSize=size;delete window.__fontOriginals;});
        }
        assert.equal(await page.getByText(labels.movement.movementsDescription,{exact:true}).count(),0);checks++;
        await page.getByRole('link',{name:`NINJA ROBOT Pi0 - ${labels.robotType.spider}`,exact:true}).waitFor();checks++;
        await page.getByRole('link',{name:labels.header.openMenu}).click();await page.getByRole('link',{name:labels.home.chatButton}).click();
        await page.getByRole('heading',{name:labels.agent.conversation}).waitFor();checks++;await fits();
        await page.getByRole('button',{name:labels.agent.voice,exact:true}).click();
        assert.equal(await page.evaluate(()=>window.__recognizers.at(-1).lang),{en:'en-US',ja:'ja-JP','zh-TW':'zh-TW','zh-CN':'zh-CN'}[locale]);checks++;
        await page.getByRole('link',{name:labels.header.openMenu}).click();
      }
      // Emulate the visual viewport shrinking/panning above the keyboard without navigating.
      await page.getByRole('link',{name:'Chat with Robot'}).click();await page.getByRole('heading',{name:'Conversation',exact:true}).waitFor();
      await page.evaluate(()=>{
        Object.defineProperty(visualViewport,'height',{configurable:true,value:300});
        Object.defineProperty(visualViewport,'offsetTop',{configurable:true,value:20});
        visualViewport.dispatchEvent(new Event('resize'));
      });
      assert.equal(await page.locator('main').evaluate(el=>el.parentElement.getBoundingClientRect().height),300);checks++;
      assert.equal(await page.locator('main').evaluate(el=>el.parentElement.getBoundingClientRect().top),20);checks++;
      await page.evaluate(()=>{delete visualViewport.height;delete visualViewport.offsetTop;visualViewport.dispatchEvent(new Event('resize'));});
      await page.getByRole('button',{name:/System activity/}).click();
      for(let i=0;i<60;i++) await event('/ws/events',{type:'log',message:`Fixture long activity ${i} ${'long '.repeat(30)}`});
      assert.equal(await page.locator('#robot-activity-log time').count(),50);checks++;
      assert.ok(await page.getByRole('log').last().evaluate(el=>el.scrollHeight>el.clientHeight));checks++;
      const menu=page.getByRole('link',{name:'Open robot menu'});
      assert.ok(await menu.evaluate(el=>{const b=el.getBoundingClientRect();return el.contains(document.elementFromPoint(b.x+b.width/2,b.y+b.height/2));}));checks++;
      await snapshot('long-log');
      await page.keyboard.press('Escape');
      // A successful fullscreen request is made directly by the selection gesture.
      await menu.click();await page.getByRole('link',{name:'Movement Tool',exact:true}).waitFor();
      await page.evaluate(()=>{
        Object.defineProperty(document,'fullscreenEnabled',{value:true});
        Element.prototype.requestFullscreen=function(options){window.__fullscreenOptions=options;return Promise.resolve();};
      });
      await page.getByRole('link',{name:'Movement Tool',exact:true}).click();
      await page.getByRole('heading',{name:'Distance Detection',exact:true}).waitFor();
      assert.deepEqual(await page.evaluate(()=>window.__fullscreenOptions),{navigationUI:'hide'});checks++;
      await page.getByRole('link',{name:'Open robot menu'}).click();await page.getByRole('link',{name:'Chat with Robot',exact:true}).waitFor();
      await page.evaluate(()=>{
        Object.defineProperty(document,'fullscreenEnabled',{value:false});
        Object.defineProperty(document,'webkitFullscreenEnabled',{value:true});
        Element.prototype.webkitRequestFullscreen=()=>{window.__prefixedFullscreen=true;};
      });
      await page.getByRole('link',{name:'Chat with Robot',exact:true}).click();await page.getByRole('heading',{name:'Conversation',exact:true}).waitFor();
      assert.equal(await page.evaluate(()=>window.__prefixedFullscreen),true);checks++;
      if(viewport.width===390 && viewport.height===740) {
        await page.evaluate(()=>{for(const el of document.querySelectorAll('main h1, main h2, main p, main button, main select, main textarea')) el.style.fontSize=`${parseFloat(getComputedStyle(el).fontSize)*1.5}px`;});
        await fits();checks++;await snapshot('chat-enlarged');
      }
      await page.goto(base+'/help');await page.getByRole('heading',{name:'Welcome to NinjaRobot'}).waitFor();assert.equal(new URL(page.url()).pathname,'/');checks++;
      assert.deepEqual(errors,[]);checks++;await context.close();
    }
    console.log(`PASS: ${checks} mocked browser contract, locale, responsive, and navigation assertions.`);
  } finally { if(browser)await browser.close();await new Promise(resolve=>server.close(resolve)); }
})().catch(error=>{console.error(error);process.exitCode=1;});
