"""Classroom tools for PizarraPad (/tools/...): timer, random name picker, dice, noise meter.
Each is a big, projector-friendly panel at the top of a content page. Nothing is sent anywhere;
lists and settings are kept only in this browser."""

CSS = '''<style>
.tool{background:var(--board);color:var(--chalk);border-radius:22px;padding:56px 22px 22px;margin:8px 0 34px;position:relative;box-shadow:0 14px 34px rgba(16,32,24,.18)}
.tool:fullscreen{border-radius:0;display:flex;flex-direction:column;justify-content:center;padding:4vh 5vw}
.tool .tbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:center;margin-bottom:12px}
.tool button,.tool select{font:inherit;font-weight:700;font-size:16px;border-radius:999px;border:2px solid rgba(242,240,228,.35);background:transparent;color:var(--chalk);padding:8px 16px;cursor:pointer;touch-action:manipulation}
.tool button.on,.tool .go{background:var(--chalk);color:var(--board);border-color:var(--chalk)}
.tool button:disabled{opacity:.4;cursor:default}
.tool .fs{position:absolute;top:12px;right:12px;padding:6px 12px;font-size:14px}
.tool .big{font-family:var(--display);text-align:center;line-height:1.05;margin:8px 0}
.tool textarea{width:100%;min-height:150px;border-radius:12px;border:2px solid rgba(242,240,228,.3);background:rgba(0,0,0,.18);color:var(--chalk);font:16px/1.5 var(--body);padding:10px}
.tool .note{font-size:14px;opacity:.75;text-align:center;margin:8px 0 0}
.tool:fullscreen .ed{display:none}
.tbar label{display:flex;align-items:center;gap:6px;font-size:15px}
.ttiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:18px 0}
.ttiles a{display:block;border:1px solid var(--line);border-radius:14px;padding:18px;background:var(--card);text-decoration:none;color:var(--fg)}
.ttiles b{display:block;font-size:20px;color:var(--accent);margin-bottom:4px}
</style>'''

FS = '<button class="fs" type="button" onclick="const t=this.parentElement;if(document.fullscreenElement)document.exitFullscreen();else if(t.requestFullscreen)t.requestFullscreen();else if(t.webkitRequestFullscreen)t.webkitRequestFullscreen()">⛶ Full screen</button>'

CHIME = '''let AC=null;function chime(){try{AC=AC||new (window.AudioContext||window.webkitAudioContext)();[523,659,784,1047].forEach((f,i)=>{const o=AC.createOscillator(),g=AC.createGain();o.frequency.value=f;o.connect(g);g.connect(AC.destination);const t=AC.currentTime+i*.18;g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.25,t+.02);g.gain.exponentialRampToValueAtTime(.0001,t+.9);o.start(t);o.stop(t+1)})}catch(e){}}
function tick(f){try{AC=AC||new (window.AudioContext||window.webkitAudioContext)();const o=AC.createOscillator(),g=AC.createGain();o.frequency.value=f||880;o.connect(g);g.connect(AC.destination);g.gain.setValueAtTime(.08,AC.currentTime);g.gain.exponentialRampToValueAtTime(.0001,AC.currentTime+.08);o.start();o.stop(AC.currentTime+.1)}catch(e){}}
const store={get:(k,d)=>{try{const v=localStorage.getItem(k);return v===null?d:v}catch(e){return d}},set:(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}}};'''

# ---------------------------------------------------------------- timer
TIMER = '''<div class="tool" id="tm">''' + FS + '''
 <div class="tbar ed" id="tmP"></div>
 <div class="tbar ed"><button type="button" id="tmMinus">− 1 min</button><button type="button" id="tmPlus">+ 1 min</button><label><input type="checkbox" id="tmSnd" checked> Sound at the end</label></div>
 <div class="big" id="tmT" style="font-size:clamp(90px,22vw,260px)">5:00</div>
 <div style="height:12px;background:rgba(242,240,228,.18);border-radius:99px;overflow:hidden;max-width:900px;margin:0 auto 16px"><i id="tmBar" style="display:block;height:100%;width:100%;background:#F2C94C;transition:width .25s linear"></i></div>
 <div class="tbar"><button class="go" type="button" id="tmGo">Start</button><button type="button" id="tmReset">Reset</button></div>
 <p class="note" id="tmMsg">Choose a time, then press Start. Tip: press the space bar to start or pause.</p>
</div>
<script>(()=>{''' + CHIME + '''
const $=i=>document.getElementById(i);let total=+store.get('pp-tm',300),left=total,run=false,end=0,raf=0,last=-1;
[1,2,3,5,10,15,20,30].forEach(m=>{const b=document.createElement('button');b.type='button';b.textContent=m+' min';b.onclick=()=>set(m*60);$('tmP').appendChild(b)});
const fmt=s=>{s=Math.max(0,Math.ceil(s));const m=Math.floor(s/60),r=s%60;return m+':'+String(r).padStart(2,'0')};
function draw(){$('tmT').textContent=fmt(left);$('tmBar').style.width=(total?left/total*100:0)+'%';$('tmBar').style.background=left<=10?'#EB5757':left<=60?'#F2994A':'#F2C94C';
 document.querySelectorAll('#tmP button').forEach(b=>b.classList.toggle('on',parseInt(b.textContent)*60===total))}
function set(s){if(run)return;total=Math.max(10,s);left=total;store.set('pp-tm',total);$('tmMsg').textContent='Ready. Press Start.';draw()}
function loop(){left=(end-performance.now())/1000;const s=Math.ceil(left);if(s!==last&&s<=5&&s>0&&$('tmSnd').checked)tick();last=s;
 if(left<=0){left=0;run=false;draw();$('tmGo').textContent='Start';$('tmMsg').textContent='⏰ Time’s up!';if($('tmSnd').checked)chime();$('tmT').animate([{opacity:1},{opacity:.2},{opacity:1}],{duration:700,iterations:4});return}
 draw();raf=requestAnimationFrame(loop)}
function go(){if(run){run=false;cancelAnimationFrame(raf);$('tmGo').textContent='Resume';$('tmMsg').textContent='Paused.';return}
 if(left<=0)left=total;run=true;end=performance.now()+left*1000;$('tmGo').textContent='Pause';$('tmMsg').textContent='Running…';loop()}
$('tmGo').onclick=go;$('tmReset').onclick=()=>{run=false;cancelAnimationFrame(raf);left=total;$('tmGo').textContent='Start';$('tmMsg').textContent='Ready. Press Start.';draw()};
$('tmPlus').onclick=()=>{if(run){end+=60000}else set(total+60)};$('tmMinus').onclick=()=>{if(run){end=Math.max(performance.now()+1000,end-60000)}else set(total-60)};
document.addEventListener('keydown',e=>{if(e.code==='Space'&&!/INPUT|TEXTAREA|SELECT|BUTTON/.test(document.activeElement.tagName)){e.preventDefault();go()}});draw()})();</script>'''

TIMER_TEXT = '''<h2>How to use the classroom timer</h2>
<ol><li>Choose a time: 1, 2, 3, 5, 10, 15, 20 or 30 minutes. Use <b>+ 1 min</b> and <b>− 1 min</b> for anything in between.</li>
<li>Press <b>Full screen</b> so the whole class can see it on the projector or TV.</li>
<li>Press <b>Start</b>, or the space bar. The bar turns orange in the last minute and red in the last 10 seconds.</li>
<li>When time is up, a short chime plays and the numbers flash. Turn the sound off if you prefer a silent timer.</li></ol>
<p>You can add a minute while the timer is running, which is handy when a group needs “just a little longer”.</p>

<h2>Ways teachers use a visible timer</h2>
<ul><li><b>Think time:</b> “You have 2 minutes to think on your own before we share.” A timer keeps think time honest and calm.</li>
<li><b>Group work:</b> 10 or 15 minutes per task, so groups pace themselves and you don’t have to keep announcing the time.</li>
<li><b>Transitions:</b> 3 minutes to pack up, move desks or clean up. Students know exactly how long they have.</li>
<li><b>Quizzes and quick writes:</b> a 5-minute warm-up quiz or journal entry at the start of class.</li>
<li><b>Stations:</b> rotate every 8 or 10 minutes. The chime tells everyone to move.</li>
<li><b>Breaks:</b> a 5-minute stretch or brain break that ends on time.</li></ul>

<h2>Tips for timers that work</h2>
<ul><li><b>Say the time out loud and show it.</b> Some students rely on hearing it, others on seeing it.</li>
<li><b>Give a 1-minute warning.</b> The color change helps, but a quick “one minute left” prepares everyone.</li>
<li><b>Use slightly less time than you think.</b> Tasks expand to fill the time. You can always add a minute.</li>
<li><b>Keep it visible.</b> On a projector, full screen works best. On a shared screen, put the timer next to your board.</li></ul>

<h2>Use it with the board</h2>
<p>Write the task on the <a href="/board/">PizarraPad board</a>, then open the timer in a second tab and switch between them. On a computer, you can place the two windows side by side.</p>

<h2>Questions</h2>
<p><b>Does it work offline?</b> Yes. Once the page has loaded, the timer keeps running even if the Wi-Fi drops.</p>
<p><b>Does it keep running if I switch tabs?</b> Yes. The timer uses the clock, so it stays accurate even if the page is in the background.</p>
<p><b>Is it free?</b> Yes, with no sign-up. Your last chosen time is remembered on this device.</p>'''

# ---------------------------------------------------------------- random name picker
PICKER = '''<div class="tool" id="np">''' + FS + '''
 <div class="big" id="npName" style="font-size:clamp(54px,11vw,140px);min-height:1.3em">Ready?</div>
 <div class="tbar"><button class="go" type="button" id="npGo">Pick a name</button><label class="ed"><input type="checkbox" id="npRm" checked> Don’t pick the same name twice</label></div>
 <p class="note" id="npInfo"></p>
 <div class="ed" style="margin-top:14px">
  <textarea id="npList" placeholder="Type or paste names, one per line"></textarea>
  <div class="tbar" style="margin-top:10px"><button type="button" id="npReset">Put all names back</button><button type="button" id="npShuf">Shuffle the list</button>
   <label>Groups of <select id="npSize"><option>2</option><option selected>3</option><option>4</option><option>5</option><option>6</option></select></label><button type="button" id="npGroups">Make groups</button></div>
  <div id="npOut" style="margin-top:12px"></div>
 </div>
</div>
<script>(()=>{''' + CHIME + '''
const $=i=>document.getElementById(i);const SAMPLE='Mia\\nNoah\\nWei\\nAva\\nLiam\\nSofia\\nEthan\\nChloe\\nLucas\\nMei\\nOliver\\nGrace';
$('npList').value=store.get('pp-np',SAMPLE);let used=new Set(JSON.parse(store.get('pp-np-used','[]')));let spin=false;
const names=()=>$('npList').value.split('\\n').map(s=>s.trim()).filter(Boolean);
const sh=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
function info(){const n=names(),left=n.filter(x=>!used.has(x));$('npInfo').textContent=n.length?($('npRm').checked?left.length+' of '+n.length+' names left':n.length+' names'):'Add names below to start.'}
function save(){store.set('pp-np',$('npList').value);store.set('pp-np-used',JSON.stringify([...used]))}
$('npList').oninput=()=>{save();info()};$('npRm').onchange=info;
$('npGo').onclick=()=>{if(spin)return;const n=names();let pool=$('npRm').checked?n.filter(x=>!used.has(x)):n;if(!n.length)return info();
 if(!pool.length){used.clear();pool=n;$('npInfo').textContent='Everyone has had a turn, so we started again.'}
 spin=true;const pick=pool[Math.floor(Math.random()*pool.length)];let k=0,steps=16;
 (function step(){$('npName').textContent=n[Math.floor(Math.random()*n.length)];tick(500+k*20);k++;
  if(k<steps)setTimeout(step,40+k*k*1.4);else{$('npName').textContent=pick;chime();used.add(pick);save();info();spin=false;$('npName').animate([{transform:'scale(1.15)'},{transform:'scale(1)'}],{duration:400})}})()};
$('npReset').onclick=()=>{used.clear();save();info();$('npName').textContent='Ready?'};
$('npShuf').onclick=()=>{$('npList').value=sh(names()).join('\\n');save()};
$('npGroups').onclick=()=>{const n=sh(names()),k=+$('npSize').value,g=Math.max(1,Math.round(n.length/k)),G=Array.from({length:g},()=>[]);n.forEach((x,i)=>G[i%g].push(x));
 $('npOut').innerHTML='<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px">'+G.map((x,i)=>'<div style="border:2px solid rgba(242,240,228,.3);border-radius:12px;padding:10px"><b>Group '+(i+1)+'</b><br>'+x.map(s=>s.replace(/[<&]/g,'')).join('<br>')+'</div>').join('')+'</div>'};
info()})();</script>'''

PICKER_TEXT = '''<h2>How to use the random name picker</h2>
<ol><li>Type or paste your class list into the box, one name per line. You can copy a column straight from a spreadsheet.</li>
<li>Press <b>Pick a name</b>. The names spin for a moment and stop on one.</li>
<li>Leave <b>Don’t pick the same name twice</b> on, and everyone gets a turn before anyone is picked again.</li>
<li>Press <b>Full screen</b> to show it big on the projector. The list hides so only the name shows.</li></ol>
<p>Your list is saved on this device, so it’s there next time. Nothing is sent anywhere.</p>

<h2>Make random groups</h2>
<p>Choose a group size and press <b>Make groups</b>. The picker shuffles your class and splits it into groups as evenly as possible. If the class doesn’t divide exactly, some groups get one extra person. Press it again for a new mix.</p>

<h2>Why teachers pick names at random</h2>
<ul><li><b>Everyone stays ready.</b> When anyone might be asked, the whole class keeps thinking, not just the students who raise their hands.</li>
<li><b>It feels fair.</b> Students accept a random pick more easily than a choice that might look like favoritism.</li>
<li><b>Quieter students get a voice.</b> A random picker gently includes students who rarely volunteer.</li>
<li><b>It saves time.</b> No more deciding who goes first, who presents, or who hands out the books.</li></ul>

<h2>Tips for kind cold-calling</h2>
<ul><li><b>Give think time first.</b> Ask the question, wait 10 to 20 seconds (try the <a href="/tools/timer/">timer</a>), then pick a name.</li>
<li><b>Let students “phone a friend”.</b> If the picked student is stuck, they can ask a classmate and then answer in their own words.</li>
<li><b>Use pair talk.</b> Let partners discuss first, then pick one person to share their pair’s idea.</li>
<li><b>Keep the stakes low.</b> Use it for sharing ideas and opinions more than for tricky right-or-wrong answers.</li></ul>

<h2>Other uses</h2>
<ul><li>Choosing who presents first, who leads a group, or the order of turns.</li>
<li>Picking a book, a topic, a warm-up activity or a game: just type those instead of names.</li>
<li>Prize draws and raffles at school events.</li></ul>

<h2>Questions</h2>
<p><b>Is my class list private?</b> Yes. The names stay in this browser on this device. We never see them.</p>
<p><b>Can I use it on a phone?</b> Yes. It works on phones, tablets and computers.</p>'''

# ---------------------------------------------------------------- dice
DICE = '''<div class="tool" id="dc">''' + FS + '''
 <div class="tbar ed"><span>Dice:</span><span id="dcN"></span></div>
 <div id="dcBox" style="display:flex;flex-wrap:wrap;gap:18px;justify-content:center;margin:14px 0;min-height:150px"></div>
 <div class="big" id="dcSum" style="font-size:clamp(36px,6vw,64px)"></div>
 <div class="tbar"><button class="go" type="button" id="dcGo">Roll</button></div>
 <p class="note">Tip: press the space bar to roll.</p>
</div>
<script>(()=>{''' + CHIME + '''
const $=i=>document.getElementById(i);let n=+store.get('pp-dc',2),busy=false;
const P={1:[[50,50]],2:[[28,28],[72,72]],3:[[25,25],[50,50],[75,75]],4:[[28,28],[72,28],[28,72],[72,72]],5:[[27,27],[73,27],[50,50],[27,73],[73,73]],6:[[28,24],[72,24],[28,50],[72,50],[28,76],[72,76]]};
const face=v=>'<svg viewBox="0 0 100 100" width="130" height="130" aria-label="'+v+'"><rect x="4" y="4" width="92" height="92" rx="18" fill="#F2F0E4"/>'+P[v].map(p=>'<circle cx="'+p[0]+'" cy="'+p[1]+'" r="9" fill="#203A2F"/>').join('')+'</svg>';
for(let k=1;k<=6;k++){const b=document.createElement('button');b.type='button';b.textContent=k;b.onclick=()=>{n=k;store.set('pp-dc',n);show(Array(n).fill(1));mark()};$('dcN').appendChild(b)}
function mark(){document.querySelectorAll('#dcN button').forEach(b=>b.classList.toggle('on',+b.textContent===n))}
function show(v){$('dcBox').innerHTML=v.map(face).join('');$('dcSum').textContent=v.length>1?'Total: '+v.reduce((a,b)=>a+b,0):''}
function roll(){if(busy)return;busy=true;let k=0;const r=()=>Array.from({length:n},()=>1+Math.floor(Math.random()*6));
 (function step(){show(r());tick(300+k*30);k++;if(k<10)setTimeout(step,50+k*12);else{const v=r();show(v);busy=false;$('dcBox').animate([{transform:'scale(1.08)'},{transform:'scale(1)'}],{duration:300})}})()}
$('dcGo').onclick=roll;document.addEventListener('keydown',e=>{if(e.code==='Space'&&!/INPUT|TEXTAREA|SELECT|BUTTON/.test(document.activeElement.tagName)){e.preventDefault();roll()}});mark();show(Array(n).fill(1))})();</script>'''

DICE_TEXT = '''<h2>How to use the dice</h2>
<ol><li>Choose how many dice to roll, from 1 to 6.</li>
<li>Press <b>Roll</b> or the space bar. With two or more dice, the total appears underneath.</li>
<li>Press <b>Full screen</b> to show the dice big on the projector, so everyone sees the same roll.</li></ol>

<h2>Math games with dice</h2>
<ul><li><b>Addition race:</b> roll two dice and add. Older students can roll three and add, or multiply two.</li>
<li><b>Make the biggest number:</b> roll three dice and arrange the digits to make the largest (or smallest) three-digit number.</li>
<li><b>Race to 100:</b> teams take turns rolling and adding to their total. First to reach 100 exactly wins.</li>
<li><b>Probability:</b> roll two dice 30 times as a class and tally the totals. Why does 7 come up more often than 2 or 12?</li>
<li><b>Fractions:</b> roll two dice and make a fraction with the smaller number on top. Compare fractions with a partner.</li></ul>

<h2>Dice for every subject</h2>
<ul><li><b>Language:</b> number six question words (who, what, where, when, why, how) and roll to choose which one students answer about a story.</li>
<li><b>Review games:</b> number six topics and roll to choose the next review question.</li>
<li><b>Writing prompts:</b> roll for a character, a place and a problem from three lists, then write a short story.</li>
<li><b>Brain breaks:</b> number six exercises (jumping jacks, stretches, balance) and roll to pick the next one.</li></ul>

<h2>Why digital dice in class?</h2>
<p>Physical dice roll off desks, get lost and are hard for a whole class to see. Big on-screen dice are fair, visible to everyone and always ready. Pair them with the <a href="/board/">PizarraPad board</a> to write down the results or keep score.</p>

<h2>Questions</h2>
<p><b>Are the rolls really random?</b> Yes. Each die uses the browser’s random number generator, so every face is equally likely.</p>
<p><b>Is it free?</b> Yes, with no sign-up, and it works offline once the page has loaded.</p>'''

# ---------------------------------------------------------------- noise meter
NOISE = '''<div class="tool" id="nm">''' + FS + '''
 <div style="display:flex;justify-content:center;gap:18px;margin:8px 0 14px" id="nmLights"><i></i><i></i><i></i></div>
 <div class="big" id="nmWord" style="font-size:clamp(40px,8vw,96px)">Press Start</div>
 <div style="height:28px;background:rgba(242,240,228,.15);border-radius:99px;overflow:hidden;max-width:900px;margin:10px auto 16px"><i id="nmBar" style="display:block;height:100%;width:0;background:#6FCF97;transition:width .1s linear"></i></div>
 <div class="tbar"><button class="go" type="button" id="nmGo">Start</button><label class="ed">Sensitivity <input type="range" id="nmSens" min="1" max="10" value="5"></label>
  <label class="ed">Level <select id="nmMode"><option value="quiet">Silent work</option><option value="talk" selected>Partner talk</option><option value="group">Group work</option></select></label></div>
 <p class="note" id="nmNote">Uses your microphone to measure loudness. Nothing is recorded, saved or sent anywhere.</p>
</div>
<style>#nmLights i{display:block;width:70px;height:70px;border-radius:50%;background:rgba(242,240,228,.12);transition:background .2s,box-shadow .2s}
#nm:fullscreen #nmLights i{width:16vh;height:16vh}</style>
<script>(()=>{''' + CHIME + '''
const $=i=>document.getElementById(i);let ctx=null,an=null,stream=null,raf=0,sm=0,hold=0;
$('nmSens').value=store.get('pp-nm-s',5);$('nmMode').value=store.get('pp-nm-m','talk');
$('nmSens').oninput=()=>store.set('pp-nm-s',$('nmSens').value);$('nmMode').onchange=()=>store.set('pp-nm-m',$('nmMode').value);
const L=[...document.querySelectorAll('#nmLights i')],C=['#6FCF97','#F2C94C','#EB5757'];
const W={quiet:['Silent work 🤫','A little noisy','Too loud!'],talk:['Just right 👍','Getting loud','Too loud!'],group:['Great teamwork','Getting loud','Too loud!']};
const LIM={quiet:[.18,.32],talk:[.38,.58],group:[.5,.72]};
function set(k){L.forEach((x,i)=>{x.style.background=i===k?C[k]:'rgba(242,240,228,.12)';x.style.boxShadow=i===k?'0 0 40px '+C[k]:'none'});if(k<0){$('nmBar').style.width='0';return}$('nmWord').textContent=W[$('nmMode').value][k];$('nmBar').style.background=C[k]}
function loop(){const d=new Float32Array(an.fftSize);an.getFloatTimeDomainData(d);let s=0;for(const v of d)s+=v*v;const rms=Math.sqrt(s/d.length);
 const lvl=Math.min(1,rms*(+$('nmSens').value)*12);sm=sm*.85+lvl*.15;$('nmBar').style.width=(sm*100)+'%';
 const [a,b]=LIM[$('nmMode').value];let k=sm<a?0:sm<b?1:2;if(k===2)hold=performance.now();else if(performance.now()-hold<1500)k=2;set(k);raf=requestAnimationFrame(loop)}
$('nmGo').onclick=async()=>{if(stream){cancelAnimationFrame(raf);stream.getTracks().forEach(t=>t.stop());stream=null;set(-1);$('nmGo').textContent='Start';$('nmWord').textContent='Stopped';return}
 try{stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:false,noiseSuppression:false,autoGainControl:false}});ctx=ctx||new (window.AudioContext||window.webkitAudioContext)();await ctx.resume();
  an=ctx.createAnalyser();an.fftSize=1024;ctx.createMediaStreamSource(stream).connect(an);$('nmGo').textContent='Stop';loop()}
 catch(e){$('nmWord').textContent='Microphone blocked';$('nmNote').textContent='Allow microphone access for this site in your browser settings, then press Start again.'}};})();</script>'''

NOISE_TEXT = '''<h2>How to use the noise meter</h2>
<ol><li>Press <b>Start</b> and allow microphone access when your browser asks.</li>
<li>Choose the level for the activity: <b>Silent work</b>, <b>Partner talk</b> or <b>Group work</b>. Each one allows a different amount of noise.</li>
<li>Show it on the projector with <b>Full screen</b>. Green means just right, yellow means getting loud, red means too loud.</li>
<li>If it turns red too easily (or never), adjust the <b>Sensitivity</b> slider. Every room and microphone is different.</li></ol>

<h2>Your privacy</h2>
<p>The noise meter only measures <b>how loud</b> the room is, many times a second. It doesn’t record, save or send any sound, and it can’t hear words. Press <b>Stop</b> and the microphone turns off. You can check: your browser shows a microphone symbol while it’s on.</p>

<h2>Making a noise meter work in your class</h2>
<ul><li><b>Agree on the levels together.</b> Before you start, model what “partner talk” and “silent work” sound like, and test the meter with the class.</li>
<li><b>Stay positive.</b> Point out when the class keeps it green: “Ten minutes in the green, great focus!”</li>
<li><b>Use a goal, not a punishment.</b> For example, if the class stays out of red for the whole activity, they earn two minutes of free choice at the end.</li>
<li><b>Expect some yellow.</b> Group work is supposed to be a bit noisy. Red is the only level that needs a reminder.</li>
<li><b>Calibrate in an empty room.</b> Set the sensitivity so normal classroom background noise stays green.</li></ul>

<h2>Where it helps most</h2>
<ul><li>Independent reading and silent writing time.</li>
<li>Group projects and science experiments.</li>
<li>Indoor lunch or rainy-day breaks.</li>
<li>Exam rooms and libraries.</li></ul>

<h2>Questions</h2>
<p><b>Why does it ask for the microphone?</b> To measure loudness. Without it, the meter can’t work. Nothing is recorded.</p>
<p><b>Which devices work?</b> Most laptops, tablets and phones with a browser like Chrome, Edge, Safari or Firefox. A laptop near the middle of the room gives the best reading.</p>
<p><b>Is it free?</b> Yes, with no sign-up.</p>'''

TOOLS = [
 ('/tools/timer/', 'Classroom Timer: Free Big-Screen Countdown for Teachers', 'Classroom timer',
  'A free classroom countdown timer for the projector or TV: 1 to 30 minutes, full screen, color warnings and a gentle chime. No sign-up, works offline.', TIMER, TIMER_TEXT,
  'A big countdown for the projector, with color warnings and a chime.'),
 ('/tools/random-name-picker/', 'Random Name Picker for the Classroom (Free, with Groups)', 'Random name picker',
  'A free random name picker for teachers: paste your class list, pick names fairly without repeats, and make random groups. Full screen for the projector. Private, no sign-up.', PICKER, PICKER_TEXT,
  'Pick students fairly, without repeats, and make random groups.'),
 ('/tools/dice/', 'Online Dice for the Classroom: Roll 1 to 6 Dice', 'Classroom dice',
  'Free online dice for the classroom: roll 1 to 6 big dice on the projector, with totals. Math and review game ideas included. No sign-up.', DICE, DICE_TEXT,
  'Roll 1 to 6 big dice for math games and review, with totals.'),
 ('/tools/noise-meter/', 'Classroom Noise Meter: Free Traffic-Light Sound Level', 'Noise meter',
  'A free classroom noise meter with traffic lights for silent work, partner talk and group work. Uses the microphone only to measure loudness; nothing is recorded.', NOISE, NOISE_TEXT,
  'A traffic light that shows when the room is getting too loud.'),
]

HUB = '''<p class="lead">Free classroom tools for your projector or TV. They open instantly, work offline once loaded, and need no sign-up.</p>
<div class="ttiles">''' + ''.join(f'<a href="{p}"><b>{s}</b>{blurb}</a>' for p, _, s, _, _, _, blurb in TOOLS) + '''<a href="/board/"><b>Whiteboard</b>Write, draw and teach on a whiteboard, blackboard or greenboard.</a></div>
<h2>Made for the front of the classroom</h2>
<p>Every tool has a <b>Full screen</b> button and big, high-contrast text that’s easy to read from the back of the room. They work on a laptop connected to a projector, a smart TV browser, a tablet or a phone.</p>
<h2>Private by design</h2>
<p>Your class list, your last timer setting and your dice choice are saved only in this browser. Nothing is sent to us. The noise meter measures loudness only and never records sound.</p>
<h2>Use them with the board</h2>
<p>Open the <a href="/board/">PizarraPad board</a> in one tab and a tool in another, and switch between them during the lesson. For more ideas, see our <a href="/guides/">guides for teachers</a>.</p>'''
