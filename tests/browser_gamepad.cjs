// Hardware-free interaction tests. Static build only; every API/socket is intercepted.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const build = path.resolve(process.argv[2]);
(async () => {
  const server = http.createServer((req,res) => {
    let route = new URL(req.url,'http://localhost').pathname;
    if (!path.extname(route)) route = '/index.html';
    const file = path.resolve(build,'.'+route);
    if (!file.startsWith(build+path.sep) || !fs.existsSync(file)) {res.writeHead(404);res.end();return;}
    res.setHeader('Content-Type',file.endsWith('.js')?'application/javascript':file.endsWith('.css')?'text/css':'text/html');
    fs.createReadStream(file).pipe(res);
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  let browser, checks=0;
  try {
    browser=await chromium.launch({headless:true, ...(process.env.PLAYWRIGHT_EXECUTABLE_PATH ? { executablePath: process.env.PLAYWRIGHT_EXECUTABLE_PATH } : {})});
    const base=`http://127.0.0.1:${server.address().port}`;
    const context=await browser.newContext({viewport:{width:390,height:740},hasTouch:true,isMobile:true});
    await context.addInitScript(()=>{
      window.__sockets=[];
      window.WebSocket=class {
        static OPEN=1;
        constructor(url){this.url=url;this.readyState=1;window.__sockets.push(this);setTimeout(()=>{this.onopen?.();if(url.endsWith('/ws/session'))this.onmessage?.({data:'{"type":"session","status":"connected"}'});},0);}
        send(){} close(){this.readyState=3;}
      };
    });
    let robotType='spider', missing=[], pending=[], calls=[], maxPending=0;
    const errors=[];
    const names=()=>['run_forward','run_backward','turn_left','turn_right','home'].map(s=>`${robotType}_${s}`).filter(n=>!missing.includes(n));
    await context.route('**/*', async route=>{
      const request=route.request(), url=new URL(request.url());
      if(url.origin!==base)return route.abort();
      if(!url.pathname.startsWith('/api/'))return route.continue();
      if(request.method()==='POST') {
        assert.match(url.pathname,/^\/api\/servos\/movements\/[^/]+\/execute$/,'Pad may only invoke native movement');
        assert.equal(request.postData(),null);calls.push(url.pathname);
        await new Promise(resolve=>pending.push({route,resolve}));
        return;
      }
      let body={};
      if(url.pathname==='/api/robot/status')body={robot_type:robotType};
      if(url.pathname==='/api/servos/movements')body={movements:names()};
      if(url.pathname==='/api/display/expressions')body={expressions:['idle']};
      if(url.pathname==='/api/sound/emotions')body={emotions:['happy']};
      await route.fulfill({status:200,contentType:'application/json',body:JSON.stringify(body)});
    });
    const page=await context.newPage();page.on('pageerror',error=>errors.push(error.message));
    const button=direction=>page.locator(`[data-direction="${direction}"]`);
    const waitPending=async()=>{await page.waitForFunction(()=>document.querySelector('[data-direction]').closest('section').textContent.length>0);for(let i=0;i<100&&!pending.length;i++)await new Promise(r=>setTimeout(r,10));assert.equal(pending.length,1);maxPending=Math.max(maxPending,pending.length);checks++;};
    const finish=async(status=200,body={status:'executed'},abort=false)=>{
      const item=pending.shift();assert.ok(item);if(abort)await item.route.abort('failed');else await item.route.fulfill({status,contentType:'application/json',body:JSON.stringify(body)});item.resolve();
      await page.waitForTimeout(40);
    };
    const idle=()=>page.waitForFunction(()=>!document.querySelector('[data-direction="up"]').disabled);
    const open=async()=>{await page.goto(base+'/movement');await button('up').waitFor();if(['spider','humanoid'].includes(robotType)&&!missing.includes(`${robotType}_run_forward`))await idle();};
    const pointer=async(direction,type,id=1,primary=true)=>button(direction).dispatchEvent(type,{pointerId:id,pointerType:'touch',button:0,isPrimary:primary,bubbles:true});
    // Real mouse pointer capture: press, response while held, then release outside the pad.
    await open();
    let box=await button('up').boundingBox();await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();await waitPending();
    assert.equal(await button('up').getAttribute('aria-pressed'),'true');
    const active=await button('up').evaluate(el=>getComputedStyle(el).backgroundImage);
    assert.ok(active.includes('255, 163, 51'));checks++;
    assert.equal(await button('right').isDisabled(),true);assert.equal(await page.getByRole('button',{name:'Run movement',exact:true}).isDisabled(),true);checks++;
    await finish();await waitPending();assert.equal(calls.length,2);checks++;
    await page.mouse.move(5,5);await page.mouse.up();assert.equal(await button('up').getAttribute('aria-pressed'),'false');checks++;
    await finish();await idle();assert.equal(calls.length,2);checks++;
    // Switching focused buttons must not let the old button's blur cancel a new hold.
    box=await button('right').boundingBox();await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();await waitPending();
    assert.equal(await button('right').getAttribute('aria-pressed'),'true');checks++;
    await finish();await waitPending();const beforeSwitchRelease=calls.length;await page.mouse.up();await finish();await idle();assert.equal(calls.length,beforeSwitchRelease);checks++;
    // Real touch tap submits one cycle; a stale pointer release cannot end a different hold.
    await button('up').tap();await waitPending();const beforeTap=calls.length;assert.equal(await button('up').getAttribute('aria-pressed'),'false');await finish();await idle();assert.equal(calls.length,beforeTap);checks++;
    await pointer('up','pointerdown');await waitPending();const beforeWrongRelease=calls.length;
    await pointer('up','pointerup',2);assert.equal(await button('up').getAttribute('aria-pressed'),'true');checks++;
    await pointer('up','pointerup');await finish();await idle();assert.equal(calls.length,beforeWrongRelease);checks++;
    // Selector requests participate in the same lock, including rapid duplicate clicks.
    await page.getByRole('button',{name:'Run movement',exact:true}).click();await waitPending();const beforeSelector=calls.length;
    assert.equal(await button('up').isDisabled(),true);checks++;
    await page.getByRole('button',{name:'Run movement',exact:true}).dispatchEvent('click');assert.equal(calls.length,beforeSelector);checks++;
    await finish();await idle();
    // Both types, all five exact mappings; release prevents repeats; Home once while held.
    for(const type of ['spider','humanoid']) {
      robotType=type;await open();
      for(const [direction,suffix] of Object.entries({up:'run_forward',down:'run_backward',left:'turn_left',right:'turn_right',center:'home'})) {
        const before=calls.length;
        await button(direction).focus();await page.keyboard.down('Space');await waitPending();
        assert.equal(calls.at(-1),`/api/servos/movements/${type}_${suffix}/execute`);checks++;
        await page.keyboard.down('Space');assert.equal(calls.length,before+1);checks++;
        if(direction==='center'){await finish();assert.equal(calls.length,before+1);assert.equal(await button('center').getAttribute('aria-pressed'),'true');checks++;await page.keyboard.up('Space');}
        else {await page.keyboard.up('Space');await finish();}
        await idle();assert.equal(calls.length,before+1);checks++;
      }
    }
    // Pointer cancel, lost capture, page blur, hidden page, overlay, focus change.
    for(const cancel of ['pointercancel','lostpointercapture','blur','hidden','overlay','focus','pagehide']) {
      const before=calls.length;await pointer('up','pointerdown');await waitPending();
      await pointer('right','pointerdown',2,false);assert.equal(calls.length,before+1);checks++;
      if(cancel==='pointercancel'||cancel==='lostpointercapture')await pointer('up',cancel);
      if(cancel==='pagehide')await page.evaluate(()=>window.dispatchEvent(new Event('pagehide')));
      if(cancel==='blur')await page.evaluate(()=>window.dispatchEvent(new Event('blur')));
      if(cancel==='hidden')await page.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));});
      if(cancel==='overlay')await page.getByRole('button',{name:/System activity/}).click();
      if(cancel==='focus')await page.getByRole('combobox').first().focus();
      assert.equal(await button('up').getAttribute('aria-pressed'),'false');checks++;
      await finish();assert.equal(calls.length,before+1);checks++;
      if(cancel==='hidden')await page.evaluate(()=>{delete document.hidden;document.dispatchEvent(new Event('visibilitychange'));});
      if(cancel==='overlay')await page.keyboard.press('Escape');
      await idle();
    }
    // Navigation/unmount cannot unlock the unresolved request or revive a hold.
    await pointer('up','pointerdown');await waitPending();
    if(process.env.UI_SCREENSHOTS){fs.mkdirSync(process.env.UI_SCREENSHOTS,{recursive:true});await page.screenshot({path:path.join(process.env.UI_SCREENSHOTS,'gamepad-pressed.png')});}
    const before=calls.length;
    await page.getByRole('link',{name:'Open robot menu'}).click();await page.getByRole('link',{name:'Movement Tool'}).click();await button('up').waitFor();
    assert.equal(await button('up').isDisabled(),true);checks++;
    await finish();await idle();assert.equal(calls.length,before);checks++;
    // Session loss unmounts controls; reconnect requires a new press.
    await pointer('up','pointerdown');await waitPending();const beforeSession=calls.length;
    await page.evaluate(()=>window.__sockets.find(s=>s.url.endsWith('/ws/session')).onmessage({data:'{"type":"session","status":"busy"}'}));
    await page.locator('main').getByText(/This robot is in use/).waitFor();await finish();
    await page.evaluate(()=>window.__sockets.find(s=>s.url.endsWith('/ws/session')).onmessage({data:'{"type":"session","status":"connected"}'}));await idle();
    assert.equal(calls.length,beforeSession);assert.equal(await button('up').getAttribute('aria-pressed'),'false');checks++;
    // HTTP rejection ends repetition. A subsequent intentional press is allowed for 4xx.
    for(const status of [404,409,422,423]) {
      await pointer('up','pointerdown');await waitPending();const beforeError=calls.length;
      await finish(status,{detail:`Fixture ${status}`});await idle();
      assert.equal(calls.length,beforeError);assert.equal(await button('up').getAttribute('aria-pressed'),'false');checks++;
      await pointer('up','pointerup');
    }
    // Network/5xx/malformed completion is uncertain; lock survives route changes.
    for(const mode of ['503','network','malformed']) {
      await open();await pointer('up','pointerdown');await waitPending();const beforeError=calls.length;
      if(mode==='network')await finish(200,{},true);else await finish(mode==='503'?503:200,{detail:'Fixture uncertain'});
      await page.getByText('Movement status unknown. Check the robot before reloading.',{exact:true}).waitFor();
      assert.equal(await button('up').isDisabled(),true);assert.equal(calls.length,beforeError);checks++;
      await page.getByRole('link',{name:'Open robot menu'}).click();await page.getByRole('link',{name:'Movement Tool'}).click();await button('up').waitFor();assert.equal(await button('up').isDisabled(),true);checks++;
    }
    // Tire and unknown types never invoke a guessed movement. Missing capability disables only its button.
    for(const type of ['tire','unknown']) {
      robotType=type;await open();assert.equal(await page.locator('[data-direction]:disabled').count(),5);checks++;
    }
    robotType='spider';missing=['spider_turn_left'];await open();assert.equal(await button('left').isDisabled(),true);assert.equal(await button('right').isDisabled(),false);checks++;
    // Assistive click is intentionally one cycle; native keyboard has no duplicate click.
    await button('center').dispatchEvent('click',{detail:0});await waitPending();const beforeAssist=calls.length;await finish();await idle();assert.equal(calls.length,beforeAssist);checks++;
    assert.equal(maxPending,1);assert.deepEqual(errors,[]);checks++;
    if(process.env.UI_SCREENSHOTS){fs.mkdirSync(process.env.UI_SCREENSHOTS,{recursive:true});await page.screenshot({path:path.join(process.env.UI_SCREENSHOTS,'gamepad-inert.png')});}
    await context.close();console.log(`PASS: ${checks} delayed-response gamepad mapping, input, cancellation and serialization checks.`);
  } finally {if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);process.exitCode=1;});
