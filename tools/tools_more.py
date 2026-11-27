"""More classroom tools: Pomodoro / interval timer, spinner wheel, animal race, icebreaker cards.
Same look and helpers as tools_content.py (chalkboard card, Full screen button, chime, store)."""
from tools_content import FS, CHIME

# ------------------------------------------------------------------ 1. Pomodoro and interval timer
POMO = '''<div class="tool" id="pm">''' + FS + '''
 <div class="tbar ed" id="pmPre"></div>
 <div class="ed pm-set" id="pmSet">
  <div class="tbar" id="pmPomo"><label>Focus <input type="number" id="pmW" min="1" max="180"> min</label><label>Break <input type="number" id="pmB" min="0" max="60"> min</label><label>Rounds <input type="number" id="pmR" min="1" max="12"></label><label>Long break <input type="number" id="pmL" min="0" max="60"> min</label></div>
  <div id="pmCust" hidden><textarea id="pmSteps" rows="5" placeholder="One step per line: name, then minutes&#10;Reading 10&#10;Break 2&#10;Writing 15"></textarea></div>
 </div>
 <div class="pm-now"><span id="pmName">Focus</span><small id="pmRound"></small></div>
 <div class="big" id="pmT" style="font-size:clamp(90px,21vw,250px)">25:00</div>
 <div class="pm-bar"><i id="pmBar"></i></div>
 <div class="pm-dots" id="pmDots"></div>
 <p class="note" id="pmNext"></p>
 <div class="tbar"><button class="go" type="button" id="pmGo">Start</button><button type="button" id="pmSkip">Skip ⏭</button><button type="button" id="pmReset">Reset</button></div>
 <div class="tbar ed"><label><input type="checkbox" id="pmAuto" checked> Start the next step by itself</label><label><input type="checkbox" id="pmSnd" checked> Chime between steps</label></div>
</div>
<style>
.tool [hidden]{display:none!important}
#pm{transition:background .6s}#pm.brk{background:#1F3A4A}#pm.lng{background:#3A2F4A}
.pm-set input{width:70px;border-radius:10px;border:2px solid rgba(242,240,228,.3);background:rgba(0,0,0,.18);color:var(--chalk);font:inherit;font-size:17px;padding:5px 8px;text-align:center}
.pm-now{text-align:center;font-family:var(--display);font-size:clamp(28px,5vw,56px);margin-top:6px}.pm-now small{display:block;font-family:var(--body);font-size:clamp(15px,2vw,20px);opacity:.75;margin-top:2px}
.pm-bar{height:12px;background:rgba(242,240,228,.18);border-radius:99px;overflow:hidden;max-width:900px;margin:0 auto 14px}.pm-bar i{display:block;height:100%;width:0;background:#F2C94C;transition:width .25s linear}
#pm.brk .pm-bar i{background:#7FD1E8}#pm.lng .pm-bar i{background:#C9A7F5}
.pm-dots{display:flex;gap:7px;justify-content:center;flex-wrap:wrap;margin-bottom:6px}.pm-dots i{width:14px;height:14px;border-radius:50%;border:2px solid rgba(242,240,228,.55)}.pm-dots i.b{width:10px;height:10px;margin-top:2px}
.pm-dots i.done{background:var(--chalk);border-color:var(--chalk)}.pm-dots i.cur{background:#F2C94C;border-color:#F2C94C;transform:scale(1.25)}
</style>
<script>(()=>{''' + CHIME + '''
const $=i=>document.getElementById(i);
const PRE=[['pomo','Pomodoro 25 / 5',{w:25,b:5,r:4,l:15}],['study','Study 50 / 10',{w:50,b:10,r:3,l:0}],['short','Short 15 / 3',{w:15,b:3,r:4,l:10}],['cust','My own steps',null]];
let C=JSON.parse(store.get('pp-pomo','null')||'null')||{mode:'pomo',w:25,b:5,r:4,l:15,steps:'Reading 10\\nBreak 2\\nWriting 15\\nBreak 2\\nSharing 8'};
let S=[],i=0,left=0,run=false,end=0,raf=0;
function steps(){if(C.mode==='cust')return C.steps.split('\\n').map(l=>{const m=l.trim().match(/^(.*?)[\\s,:-]+(\\d+(?:\\.\\d+)?)\\s*(?:min(?:utes)?)?$/i);return m?{n:m[1].trim()||'Step',s:Math.round(+m[2]*60),k:/break|rest|pause|descanso/i.test(m[1])?'brk':'work'}:null}).filter(x=>x&&x.s>0);
 const out=[];for(let r=1;r<=C.r;r++){out.push({n:'Focus',s:C.w*60,k:'work',r});if(r<C.r&&C.b>0)out.push({n:'Short break',s:C.b*60,k:'brk',r});}if(C.l>0)out.push({n:'Long break',s:C.l*60,k:'lng',r:C.r});return out}
const fmt=s=>{s=Math.max(0,Math.ceil(s));const h=Math.floor(s/3600),m=Math.floor(s%3600/60),r=s%60;return (h?h+':'+String(m).padStart(2,'0'):m)+':'+String(r).padStart(2,'0')};
function save(){store.set('pp-pomo',JSON.stringify(C))}
function build(){S=steps();i=0;left=S.length?S[0].s:0;run=false;cancelAnimationFrame(raf);$('pmGo').textContent='Start';draw()}
function draw(){const st=S[i];$('pm').className='tool'+(st&&st.k!=='work'?' '+st.k:'');
 $('pmName').textContent=st?st.n:'Add a step';$('pmT').textContent=fmt(left);
 const works=S.filter(x=>x.k==='work').length,wn=S.slice(0,i+1).filter(x=>x.k==='work').length;
 $('pmRound').textContent=!st?'':C.mode==='cust'?'Step '+(i+1)+' of '+S.length:(st.k==='work'?'Round '+st.r+' of '+C.r:st.k==='lng'?'Well done! All '+C.r+' rounds finished':'After round '+st.r+' of '+C.r);
 $('pmBar').style.width=st?(100*(1-left/st.s))+'%':'0';
 $('pmDots').innerHTML=S.map((x,k)=>'<i class="'+(x.k!=='work'?'b ':'')+(k<i?'done':k===i?'cur':'')+'" title="'+x.n.replace(/[<"&]/g,'')+'"></i>').join('');
 const nx=S[i+1];$('pmNext').textContent=nx?'Next: '+nx.n+' · '+fmt(nx.s):(st?'Last step':'');document.title=(run?fmt(left)+' · '+(st?st.n:'')+' · ':'')+'Pomodoro Timer | PizarraPad'}
function loop(){left=(end-Date.now())/1000;if(left<=0){next(true);return}draw();raf=requestAnimationFrame(loop)}
function next(auto){cancelAnimationFrame(raf);if($('pmSnd').checked&&auto)chime();if(i>=S.length-1){run=false;left=0;$('pmGo').textContent='Start again';$('pmName').textContent='All done! 🎉';$('pmT').textContent='0:00';$('pmBar').style.width='100%';$('pmNext').textContent='';document.title='Pomodoro Timer | PizarraPad';return}
 i++;left=S[i].s;if(run&&(!auto||$('pmAuto').checked)){end=Date.now()+left*1000;raf=requestAnimationFrame(loop)}else{run=false;$('pmGo').textContent='Start';}draw()}
$('pmGo').onclick=()=>{if(!S.length)return;if($('pmGo').textContent==='Start again'){build()}
 if(run){run=false;cancelAnimationFrame(raf);$('pmGo').textContent='Resume';draw()}else{run=true;end=Date.now()+left*1000;$('pmGo').textContent='Pause';raf=requestAnimationFrame(loop)}};
$('pmSkip').onclick=()=>next(false);$('pmReset').onclick=build;
$('pmPre').innerHTML=PRE.map(p=>'<button type="button" data-p="'+p[0]+'">'+p[1]+'</button>').join('');
function setUI(){document.querySelectorAll('#pmPre button').forEach(b=>b.classList.toggle('on',b.dataset.p===C.mode));$('pmPomo').hidden=C.mode==='cust';$('pmCust').hidden=C.mode!=='cust';
 $('pmW').value=C.w;$('pmB').value=C.b;$('pmR').value=C.r;$('pmL').value=C.l;$('pmSteps').value=C.steps}
document.querySelectorAll('#pmPre button').forEach(b=>b.onclick=()=>{const p=PRE.find(x=>x[0]===b.dataset.p);C.mode=p[0];if(p[2])Object.assign(C,p[2]);save();setUI();build()});
[['pmW','w',1,180],['pmB','b',0,60],['pmR','r',1,12],['pmL','l',0,60]].forEach(([id,k,lo,hi])=>$(id).oninput=function(){const v=Math.min(hi,Math.max(lo,Math.round(+this.value||0)));if(!this.value)return;C[k]=v;C.mode=C.mode==='cust'?'cust':(PRE.find(p=>p[2]&&p[2].w===C.w&&p[2].b===C.b&&p[2].r===C.r&&p[2].l===C.l)||['mine'])[0];save();document.querySelectorAll('#pmPre button').forEach(b=>b.classList.toggle('on',b.dataset.p===C.mode));if(!run)build()});
$('pmSteps').oninput=function(){C.steps=this.value;save();if(!run)build()};
document.addEventListener('keydown',e=>{if(e.code==='Space'&&!/INPUT|TEXTAREA|SELECT|BUTTON/.test(e.target.tagName)){e.preventDefault();$('pmGo').click()}});
setUI();build()})();</script>'''

POMO_TEXT = '''<h2>How to use the Pomodoro timer</h2>
<ol><li><b>Pick a plan:</b> the classic Pomodoro (25 minutes of focus, 5-minute breaks, 4 rounds, then a 15-minute long break), Study 50 / 10, Short 15 / 3, or <b>My own steps</b>.</li>
<li><b>Change any number</b>: focus time, break time, rounds, and the long break (0 for none).</li>
<li><b>Press Start</b> and put it on full screen. A chime plays between steps, the screen changes color for breaks, and the next step starts by itself.</li>
<li>The dots show every step, so the class can see how far they are. <b>Skip</b> moves to the next step; the space bar starts and pauses.</li></ol>
<h2>What is the Pomodoro technique?</h2>
<p>It’s a simple way to focus: work on one task for a short, fixed time, then take a real break. Short sprints make a big task feel manageable, and planned breaks keep energy up. After a few rounds, a longer break helps the brain reset. Many students find 25 minutes on, 5 minutes off easier than “study for two hours”.</p>
<h2>Ideas for the classroom</h2>
<ul><li><b>Independent work:</b> 15 minutes of focus and a 3-minute stretch break, twice, in one period.</li>
<li><b>Stations or centers:</b> use <b>My own steps</b> with one line per station: “Station 1 10”, “Move 1”, “Station 2 10”.</li>
<li><b>Lesson flow:</b> “Warm-up 5”, “Mini lesson 10”, “Group work 15”, “Share 8”, so everyone sees what’s next.</li>
<li><b>Exam review days</b> and <b>study halls</b>: 50 / 10 for older students.</li>
<li><b>At home:</b> students can use the same timer for homework and test review.</li></ul>
<h2>Break ideas</h2>
<ul><li>Stand, stretch and shake it out for one minute.</li><li>Drink water, or look out of the window and rest your eyes.</li><li>A quick round of the <a href="/tools/icebreaker-cards/">icebreaker cards</a>, or a one-question chat with a partner.</li></ul>
<h2>Questions</h2>
<h3>Does it keep time if I switch tabs?</h3><p>Yes. The timer counts from the clock, so it stays right even if the tab is in the background. The tab’s title shows the time left.</p>
<h3>Is it saved?</h3><p>Your plan is saved in this browser, so it’s ready next time. Nothing is sent to us.</p>'''

# ------------------------------------------------------------------ 2. Spinner wheel
WHEEL = '''<div class="tool" id="wh">''' + FS + '''
 <div class="wh-stage"><canvas id="whC" width="900" height="900" aria-label="Spinner wheel"></canvas><div class="wh-ptr" aria-hidden="true"></div><button type="button" class="wh-hub" id="whHub" aria-label="Spin the wheel">SPIN</button></div>
 <div class="big" id="whOut" style="font-size:clamp(36px,7vw,90px);min-height:1.2em" aria-live="polite"></div>
 <div class="tbar"><button class="go" type="button" id="whGo">Spin</button><label class="ed"><input type="checkbox" id="whRm"> Remove the winner after each spin</label></div>
 <div class="ed" style="margin-top:12px">
  <textarea id="whList" placeholder="Type names, prizes or topics, one per line"></textarea>
  <div class="tbar" style="margin-top:10px"><button type="button" id="whShuf">Shuffle</button><button type="button" id="whBack">Put removed items back</button><label>Colors <select id="whPal"><option value="bright">Bright</option><option value="pastel">Pastel</option><option value="chalk">Chalk</option></select></label></div>
  <p class="note" id="whInfo"></p>
 </div>
</div>
<style>
.tool [hidden]{display:none!important}
.wh-stage{position:relative;width:min(560px,100%);margin:0 auto}#wh:fullscreen .wh-stage{width:min(66vh,90vw)}
.wh-stage canvas{width:100%;height:auto;display:block;filter:drop-shadow(0 10px 18px rgba(0,0,0,.35))}
.wh-ptr{position:absolute;top:50%;right:-6px;width:0;height:0;border-top:22px solid transparent;border-bottom:22px solid transparent;border-right:46px solid #F2C94C;transform:translateY(-50%);filter:drop-shadow(0 2px 3px rgba(0,0,0,.4))}
.tool .wh-hub{position:absolute;left:50%;top:50%;width:19%;height:19%;transform:translate(-50%,-50%);border-radius:50%;background:var(--chalk);color:var(--board);border:4px solid var(--board);font-weight:800;font-size:clamp(13px,2.4vw,20px);padding:0}
</style>
<script>(()=>{''' + CHIME + '''
const $=i=>document.getElementById(i),cv=$('whC'),ctx=cv.getContext('2d');
const PAL={bright:['#E4572E','#F2C94C','#2D9CDB','#27AE60','#9B51E0','#F2994A','#EB5757','#56CCF2','#6FCF97','#BB6BD9'],pastel:['#F8B4B4','#FDE68A','#A7F3D0','#BFDBFE','#DDD6FE','#FBCFE8','#FED7AA','#C7F9CC','#E9D5FF','#BAE6FD'],chalk:['#F2F0E4','#C9D6C3','#F2F0E4','#B7C9C1','#F2F0E4','#D8CDB3']};
const SAMPLE='Mia\\nNoah\\nWei\\nAva\\nLiam\\nSofia\\nEthan\\nChloe\\nLucas\\nMei';
$('whList').value=store.get('pp-wh',SAMPLE);$('whPal').value=store.get('pp-wh-pal','bright');$('whRm').checked=store.get('pp-wh-rm','')==='1';
let removed=JSON.parse(store.get('pp-wh-out','[]')),ang=0,spin=false,pend=null;
const all=()=>$('whList').value.split('\\n').map(s=>s.trim()).filter(Boolean);
const items=()=>{const r=removed.slice();return all().filter(x=>{const k=r.indexOf(x);if(k>=0){r.splice(k,1);return false}return true})};
function lum(h){const c=parseInt(h.slice(1),16);return (.299*(c>>16&255)+.587*(c>>8&255)+.114*(c&255))/255}
function draw(){const L=items(),n=L.length,W=cv.width,R=W/2-10,cx=W/2,cy=W/2,pal=PAL[$('whPal').value];ctx.clearRect(0,0,W,W);
 if(!n){ctx.fillStyle='rgba(242,240,228,.15)';ctx.beginPath();ctx.arc(cx,cy,R,0,7);ctx.fill();ctx.fillStyle='#F2F0E4';ctx.font='700 40px sans-serif';ctx.textAlign='center';ctx.fillText('Add some names',cx,cy-100);return}
 const a=2*Math.PI/n;for(let k=0;k<n;k++){const s=ang+k*a,col=pal[(n%pal.length===1&&k===n-1)?(k+1)%pal.length:k%pal.length];
  ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,R,s,s+a);ctx.closePath();ctx.fillStyle=col;ctx.fill();ctx.strokeStyle='rgba(32,58,47,.55)';ctx.lineWidth=3;ctx.stroke();
  ctx.save();ctx.translate(cx,cy);ctx.rotate(s+a/2);ctx.fillStyle=lum(col)>.6?'#203A2F':'#fff';ctx.textAlign='right';ctx.textBaseline='middle';
  let fs=Math.min(58,Math.max(16,R*a*.55));ctx.font='800 '+fs+'px sans-serif';let t=L[k];while(ctx.measureText(t).width>R*.68&&fs>14){fs-=2;ctx.font='800 '+fs+'px sans-serif'}
  if(ctx.measureText(t).width>R*.7){while(t.length>3&&ctx.measureText(t+'…').width>R*.7)t=t.slice(0,-1);t+='…'}ctx.fillText(t,R-22,0);ctx.restore()}
 ctx.beginPath();ctx.arc(cx,cy,R,0,7);ctx.lineWidth=10;ctx.strokeStyle='#F2F0E4';ctx.stroke()}
function info(){const n=all().length,l=items().length;$('whInfo').textContent=n?(removed.length?l+' of '+n+' left on the wheel':n+' on the wheel'):'Add names, prizes or topics, one per line.';$('whBack').disabled=!removed.length}
function save(){store.set('pp-wh',$('whList').value);store.set('pp-wh-out',JSON.stringify(removed));store.set('pp-wh-pal',$('whPal').value);store.set('pp-wh-rm',$('whRm').checked?'1':'')}
function go(){if(spin)return;if(pend!==null){removed.push(pend);pend=null;save();draw();info()}const L=items(),n=L.length;if(spin||!n)return;if(n===1){$('whOut').textContent=L[0];return}spin=true;$('whOut').textContent='';
 const a=2*Math.PI/n,pick=crypto.getRandomValues(new Uint32Array(1))[0]%n,jit=(Math.random()*.7+.15)*a;
 const turns=6+Math.floor(Math.random()*3),from=ang;let to=-(pick*a+jit);while(to>from)to-=2*Math.PI;to-=2*Math.PI*turns;
 const dist=from-to,dur=5200,t0=performance.now();let lastSeg=-1;
 (function f(t){let p=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-p,4);ang=from-dist*e;draw();
  const seg=Math.floor(((-ang)%(2*Math.PI)+2*Math.PI)%(2*Math.PI)/a);if(seg!==lastSeg){lastSeg=seg;tick(1000-p*500)}
  if(p<1)requestAnimationFrame(f);else{spin=false;const w=L[pick];$('whOut').textContent='🎉 '+w;chime();$('whOut').animate([{transform:'scale(1.2)'},{transform:'scale(1)'}],{duration:450});
   if($('whRm').checked){pend=w;const l=items().length-1;$('whInfo').textContent=w+' comes off the wheel on the next spin · '+l+' left'}}})(t0)}
$('whGo').onclick=go;$('whHub').onclick=go;
$('whList').oninput=()=>{removed=removed.filter(x=>all().includes(x));save();draw();info()};$('whPal').onchange=()=>{save();draw()};$('whRm').onchange=save;
$('whShuf').onclick=()=>{const a=all();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}$('whList').value=a.join('\\n');save();draw()};
$('whBack').onclick=()=>{removed=[];pend=null;save();draw();info();$('whOut').textContent=''};
document.addEventListener('keydown',e=>{if(e.code==='Space'&&!/INPUT|TEXTAREA|SELECT|BUTTON/.test(e.target.tagName)){e.preventDefault();go()}});
draw();info()})();</script>'''

WHEEL_TEXT = '''<h2>How to use the spinner wheel</h2>
<ol><li><b>Type the choices</b> under the wheel, one per line: names, prizes, topics, questions or groups. Up to about 100 fit.</li>
<li><b>Press Spin</b>, tap the middle of the wheel, or press the space bar. The wheel slows down with a ticking sound and lands on a random choice.</li>
<li>Tick <b>Remove the winner after each spin</b> so nobody is picked twice. <b>Put removed items back</b> starts over.</li>
<li>Use <b>Full screen</b> on the projector, and pick <b>Bright</b>, <b>Pastel</b> or <b>Chalk</b> colors.</li></ol>
<h2>Ideas for the wheel</h2>
<ul><li><b>Who answers next:</b> your class list, with “remove the winner” on, so everyone gets a turn.</li>
<li><b>Review games:</b> spin for the topic (“Fractions”, “Decimals”, “Word problems”) or for points (“1 point”, “2 points”, “Double!”, “Lose a turn”).</li>
<li><b>Prizes and raffles</b> at a class party or a school event.</li>
<li><b>Writing prompts</b> and <b>debate topics</b>.</li>
<li><b>Brain breaks:</b> “10 jumping jacks”, “Dance for 30 seconds”, “Stretch”, “Tell a joke”.</li>
<li><b>Jobs and roles:</b> who leads the group, who writes, who presents.</li></ul>
<h2>Is it fair?</h2>
<p>Yes. The winner is chosen with your browser’s secure random numbers before the wheel starts turning, so every choice has the same chance, and the spin itself is just for show. To give an item more chances, type it on more than one line.</p>
<h2>Questions</h2>
<h3>Is my list saved?</h3><p>Yes, in this browser only, so it’s ready next time. Nothing is sent to us.</p>
<h3>Want a race instead?</h3><p>Try the <a href="/tools/animal-race/">animal race</a>: each student gets a cute animal, and the winner crosses the finish line first.</p>'''

# ------------------------------------------------------------------ 3. Animal race
ANIMALS_JS = r'''
// original, simple animal drawings (side view, facing right), each an SVG string
function face(x,y,s){return '<circle cx="'+x+'" cy="'+y+'" r="'+(4.2*s)+'" fill="#1b1b1b"/><circle cx="'+(x+1.4*s)+'" cy="'+(y-1.4*s)+'" r="'+(1.4*s)+'" fill="#fff"/>'}
function cheek(x,y){return '<ellipse cx="'+x+'" cy="'+y+'" rx="5" ry="3.2" fill="#ff8fa3" opacity=".75"/>'}
const ANIMALS={
 duck:{n:'Duck',svg:'<ellipse cx="44" cy="62" rx="30" ry="20" fill="#FFD84D"/><path d="M18 58 q-10 -8 -6 -18 q8 6 14 8z" fill="#FFD84D"/><circle cx="70" cy="36" r="17" fill="#FFD84D"/><path d="M84 36 l16 3 l-16 6z" fill="#FF9F1C"/>'+face(74,32,1)+cheek(72,44)+'<path d="M36 60 q10 10 22 0" stroke="#E8B800" stroke-width="3" fill="none"/><path d="M40 82 v8 M52 82 v8" stroke="#FF9F1C" stroke-width="4" stroke-linecap="round"/>'},
 bunny:{n:'Bunny',svg:'<ellipse cx="44" cy="62" rx="28" ry="20" fill="#F5F0F7"/><circle cx="18" cy="58" r="7" fill="#fff"/><ellipse cx="62" cy="14" rx="6" ry="17" fill="#F5F0F7"/><ellipse cx="62" cy="14" rx="3" ry="12" fill="#FFC2D1"/><ellipse cx="74" cy="12" rx="6" ry="17" fill="#F5F0F7" transform="rotate(14 74 12)"/><ellipse cx="74" cy="12" rx="3" ry="12" fill="#FFC2D1" transform="rotate(14 74 12)"/><circle cx="70" cy="40" r="17" fill="#F5F0F7"/>'+face(76,37,1)+cheek(74,48)+'<circle cx="86" cy="43" r="2.6" fill="#FF8FA3"/><path d="M36 80 v8 M54 80 v8" stroke="#E5DCEB" stroke-width="6" stroke-linecap="round"/>'},
 turtle:{n:'Turtle',svg:'<ellipse cx="44" cy="70" rx="34" ry="6" fill="#5FAE63"/><path d="M14 68 q30 -50 60 0z" fill="#3E8E41"/><path d="M28 64 l8 -14 l14 0 l8 14 M36 50 l6 -8 l6 8" stroke="#2C6B2F" stroke-width="2.5" fill="none"/><circle cx="84" cy="56" r="12" fill="#7BC67E"/>'+face(88,53,.9)+cheek(87,62)+'<path d="M24 74 v8 M60 74 v8" stroke="#5FAE63" stroke-width="7" stroke-linecap="round"/>'},
 cat:{n:'Cat',svg:'<ellipse cx="44" cy="62" rx="28" ry="19" fill="#F2A65A"/><path d="M16 56 q-14 -18 -2 -30" stroke="#F2A65A" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M58 30 l3 -18 l12 12z M78 24 l10 -14 l3 18z" fill="#F2A65A"/><circle cx="72" cy="38" r="17" fill="#F2A65A"/><path d="M40 50 q4 10 0 22 M50 48 q4 10 0 24" stroke="#D9853B" stroke-width="3" fill="none"/>'+face(78,35,1)+cheek(76,46)+'<path d="M86 42 l8 -2 M86 45 l8 2" stroke="#6b4a2b" stroke-width="1.6"/><path d="M34 80 v8 M56 80 v8" stroke="#F2A65A" stroke-width="7" stroke-linecap="round"/>'},
 pig:{n:'Piggy',svg:'<ellipse cx="44" cy="62" rx="30" ry="21" fill="#FFB3C1"/><path d="M14 58 q-6 -4 -3 -9 q4 4 -1 9" stroke="#FF8FA3" stroke-width="2.5" fill="none"/><circle cx="72" cy="42" r="17" fill="#FFB3C1"/><path d="M62 26 l4 -10 l8 8z" fill="#FF8FA3"/><ellipse cx="88" cy="46" rx="7" ry="6" fill="#FF8FA3"/><circle cx="86" cy="46" r="1.4" fill="#b85c6e"/><circle cx="90" cy="46" r="1.4" fill="#b85c6e"/>'+face(76,37,.95)+'<path d="M32 80 v9 M56 80 v9" stroke="#FF8FA3" stroke-width="7" stroke-linecap="round"/>'},
 frog:{n:'Frog',svg:'<ellipse cx="46" cy="64" rx="32" ry="18" fill="#6CCB5F"/><circle cx="66" cy="34" r="9" fill="#6CCB5F"/><circle cx="82" cy="36" r="9" fill="#6CCB5F"/><ellipse cx="74" cy="48" rx="20" ry="14" fill="#6CCB5F"/>'+face(67,33,1)+face(83,35,1)+'<path d="M66 54 q10 6 20 0" stroke="#2f7a28" stroke-width="2.5" fill="none"/>'+cheek(64,52)+'<path d="M22 76 q-8 6 -2 10 M60 78 q6 6 12 6" stroke="#4FA845" stroke-width="7" fill="none" stroke-linecap="round"/>'},
 chick:{n:'Chick',svg:'<circle cx="52" cy="56" r="28" fill="#FFE873"/><path d="M50 26 q4 -10 10 -4 q-6 0 -6 6" fill="#FFE873"/><path d="M78 52 l14 4 l-14 6z" fill="#FF9F1C"/>'+face(68,48,1)+cheek(66,60)+'<path d="M38 60 q8 8 16 0" stroke="#F2C94C" stroke-width="3" fill="none"/><path d="M44 82 v8 M58 82 v8" stroke="#FF9F1C" stroke-width="4" stroke-linecap="round"/>'},
 penguin:{n:'Penguin',svg:'<ellipse cx="50" cy="56" rx="24" ry="30" fill="#2B2D42"/><ellipse cx="56" cy="62" rx="15" ry="22" fill="#fff"/><path d="M70 40 l14 3 l-14 5z" fill="#FF9F1C"/>'+face(62,38,.95).replace('#1b1b1b','#1b1b1b')+'<circle cx="62" cy="38" r="6" fill="#fff"/>'+face(63,38,.9)+cheek(60,50)+'<path d="M30 54 q-10 12 -2 20" stroke="#2B2D42" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M44 86 h8 M58 86 h8" stroke="#FF9F1C" stroke-width="5" stroke-linecap="round"/>'},
 bear:{n:'Bear',svg:'<ellipse cx="44" cy="62" rx="30" ry="21" fill="#A47148"/><circle cx="62" cy="24" r="7" fill="#A47148"/><circle cx="84" cy="26" r="7" fill="#A47148"/><circle cx="72" cy="40" r="18" fill="#A47148"/><ellipse cx="84" cy="46" rx="9" ry="7" fill="#E0C097"/><circle cx="88" cy="43" r="2.6" fill="#3a2414"/>'+face(74,36,1)+cheek(70,48)+'<path d="M32 80 v9 M56 80 v9" stroke="#8C5E3C" stroke-width="8" stroke-linecap="round"/>'},
 fox:{n:'Fox',svg:'<ellipse cx="46" cy="62" rx="28" ry="18" fill="#F07B3F"/><path d="M20 60 q-20 -6 -14 -22 q10 12 22 14z" fill="#F07B3F"/><path d="M8 40 q2 -4 6 -2 l-4 6z" fill="#fff"/><path d="M60 30 l2 -18 l12 12z M80 26 l8 -16 l4 18z" fill="#F07B3F"/><path d="M58 40 q14 -20 30 0 l8 8 q-18 10 -38 -8z" fill="#F07B3F"/><path d="M78 46 l18 2 q-10 8 -22 2z" fill="#fff"/><circle cx="96" cy="47" r="2.4" fill="#1b1b1b"/>'+face(78,38,.95)+'<path d="M34 78 v9 M56 78 v9" stroke="#3a2a20" stroke-width="6" stroke-linecap="round"/>'},
 mouse:{n:'Mouse',svg:'<ellipse cx="46" cy="64" rx="26" ry="17" fill="#C9C9D3"/><path d="M20 66 q-16 2 -16 -12" stroke="#E7A9B6" stroke-width="3" fill="none" stroke-linecap="round"/><circle cx="64" cy="30" r="11" fill="#C9C9D3"/><circle cx="64" cy="30" r="6" fill="#FFC2D1"/><ellipse cx="76" cy="48" rx="16" ry="13" fill="#C9C9D3"/><circle cx="92" cy="50" r="3" fill="#FF8FA3"/>'+face(80,44,.9)+cheek(76,54)+'<path d="M38 80 v7 M54 80 v7" stroke="#B5B5C2" stroke-width="5" stroke-linecap="round"/>'},
 panda:{n:'Panda',svg:'<ellipse cx="44" cy="62" rx="30" ry="21" fill="#F7F7F7"/><path d="M30 46 q14 -6 28 0 v18 q-14 6 -28 0z" fill="#2B2D42"/><circle cx="62" cy="24" r="7" fill="#2B2D42"/><circle cx="84" cy="26" r="7" fill="#2B2D42"/><circle cx="72" cy="40" r="18" fill="#F7F7F7"/><ellipse cx="78" cy="37" rx="6" ry="7" fill="#2B2D42"/><circle cx="79" cy="36" r="2.4" fill="#fff"/><circle cx="88" cy="46" r="2.6" fill="#2B2D42"/>'+cheek(70,48)+'<path d="M32 80 v9 M56 80 v9" stroke="#2B2D42" stroke-width="8" stroke-linecap="round"/>'}
};
const ORDER=['duck','bunny','turtle','cat','pig','frog','chick','penguin','bear','fox','mouse','panda'];
function animalSVG(k){return '<svg viewBox="0 0 104 96" aria-hidden="true">'+ANIMALS[k].svg+'</svg>'}
'''

RACE = '''<div class="tool" id="ar">''' + FS + '''
 <div class="ar-track" id="arTrack"></div>
 <div class="big" id="arMsg" style="font-size:clamp(30px,6vw,70px);min-height:1.2em" aria-live="polite"></div>
 <div class="tbar"><button class="go" type="button" id="arGo">Start the race</button><label class="ed">Race length <select id="arLen"><option value="8">Quick (8 s)</option><option value="14" selected>Normal (14 s)</option><option value="24">Long (24 s)</option></select></label><label class="ed"><input type="checkbox" id="arSnd" checked> Sound</label></div>
 <div class="ed" style="margin-top:12px">
  <textarea id="arList" placeholder="One racer per line: names or teams (up to 12)"></textarea>
  <div class="tbar" style="margin-top:10px"><button type="button" id="arShuf">Shuffle the animals</button></div>
  <p class="note" id="arInfo"></p>
 </div>
</div>
<style>
.tool [hidden]{display:none!important}
.ar-track{position:relative;background:repeating-linear-gradient(90deg,transparent 0 60px,rgba(242,240,228,.05) 60px 61px);border:2px dashed rgba(242,240,228,.35);border-radius:16px;padding:6px 0;margin-bottom:10px;overflow:hidden}
.ar-lane{position:relative;height:var(--lh,64px);border-bottom:2px dashed rgba(242,240,228,.18)}.ar-lane:last-child{border-bottom:0}
.ar-lane .nm{position:absolute;left:10px;top:50%;transform:translateY(-50%);font-weight:800;font-size:clamp(13px,1.8vw,18px);opacity:.55;white-space:nowrap;max-width:30%;overflow:hidden;text-overflow:ellipsis}
.ar-run{position:absolute;top:0;height:100%;left:0;display:flex;align-items:center;will-change:transform}
.ar-run svg{height:88%;width:auto}.ar-run.hop svg{animation:hop .32s ease-in-out infinite alternate}
.ar-run b{background:var(--chalk);color:var(--board);border-radius:99px;padding:1px 9px;font-size:clamp(11px,1.5vw,15px);margin-left:4px;white-space:nowrap;max-width:130px;overflow:hidden;text-overflow:ellipsis}
.ar-fin{position:absolute;top:0;bottom:0;right:7%;width:14px;background:repeating-linear-gradient(0deg,#f2f0e4 0 10px,#203a2f 10px 20px);opacity:.9}
.ar-place{font-weight:800;margin-right:6px;opacity:1}.ar-lane .nm .ar-place:empty{display:none}.ar-lane.fin .nm{opacity:1}#arTrack:not(.on) .nm{visibility:hidden}@media(max-width:640px){.ar-run b{display:none}}
@keyframes hop{from{transform:translateY(0) rotate(-3deg)}to{transform:translateY(-14%) rotate(3deg)}}
.ar-count{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:var(--display);font-size:clamp(70px,14vw,180px);text-shadow:0 4px 12px rgba(0,0,0,.4);pointer-events:none}
</style>
<script>(()=>{''' + CHIME + ANIMALS_JS + '''
const $=i=>document.getElementById(i);const SAMPLE='Mia\\nNoah\\nWei\\nAva\\nLiam\\nSofia';
$('arList').value=store.get('pp-ar',SAMPLE);$('arLen').value=store.get('pp-ar-len','14');let order=JSON.parse(store.get('pp-ar-order','null'))||ORDER.slice(),racing=false;
const racers=()=>$('arList').value.split('\\n').map(s=>s.trim()).filter(Boolean).slice(0,12);
function esc(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function lay(){const R=racers(),n=R.length;$('arInfo').textContent=n?n+' racer'+(n>1?'s':'')+(R.length<$('arList').value.split('\\n').filter(s=>s.trim()).length?' (12 is the most)':''):'Add 2 to 12 racers, one per line.';
 const lh=Math.max(44,Math.min(90,Math.round(420/Math.max(n,1))));$('arTrack').style.setProperty('--lh',lh+'px');
 $('arTrack').classList.remove('on');$('arTrack').innerHTML='<div class="ar-fin"></div>'+R.map((r,i)=>'<div class="ar-lane" id="arL'+i+'"><span class="nm"><span class="ar-place" id="arP'+i+'"></span>'+esc(r)+'</span><div class="ar-run" id="arR'+i+'">'+animalSVG(order[i%order.length])+'<b>'+esc(r)+'</b></div></div>').join('')}
function save(){store.set('pp-ar',$('arList').value);store.set('pp-ar-len',$('arLen').value);store.set('pp-ar-order',JSON.stringify(order))}
function beep(f,d){if(!$('arSnd').checked)return;try{AC=AC||new (window.AudioContext||window.webkitAudioContext)();const o=AC.createOscillator(),g=AC.createGain();o.frequency.value=f;o.connect(g);g.connect(AC.destination);g.gain.setValueAtTime(.15,AC.currentTime);g.gain.exponentialRampToValueAtTime(.0001,AC.currentTime+d);o.start();o.stop(AC.currentTime+d)}catch(e){}}
function race(){const R=racers(),n=R.length;if(racing||n<2){if(n<2)$('arMsg').textContent='Add at least 2 racers';return}racing=true;lay();$('arMsg').textContent='';$('arGo').disabled=true;
 // finishing order is drawn fairly first; the race then plays it out with surprises along the way
 const rnd=()=>crypto.getRandomValues(new Uint32Array(1))[0]/4294967296,fin=[...Array(n).keys()];for(let i=n-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[fin[i],fin[j]]=[fin[j],fin[i]]}
 const T=+$('arLen').value*1000,track=$('arTrack'),W=track.clientWidth,runW=Math.min(170,W*.2),goal=W*.93-runW*.62;
 const P=fin.map((who,place)=>({who,place,end:T*(.86+place*.14/Math.max(1,n-1))+rnd()*120*place,k:[...Array(5)].map(()=>.6+rnd()*.8)}));
 const ov=document.createElement('div');ov.className='ar-count';track.appendChild(ov);let c=3;
 (function count(){if(c>0){ov.textContent=c;beep(660,.18);c--;setTimeout(count,700)}else{ov.textContent='GO!';beep(990,.35);setTimeout(()=>ov.remove(),500);start()}})();
 function pos(p,t){if(t>=p.end)return 1;const u=t/p.end;let s=0,tot=0;p.k.forEach(k=>tot+=k);let acc=0;for(let i=0;i<5;i++){const seg=Math.min(1,Math.max(0,u*5-i));acc+=p.k[i]*seg}return Math.min(1,acc/tot)}
 function start(){$('arTrack').classList.add('on');const t0=performance.now();let done=0;R.forEach((_,i)=>$('arR'+i).classList.add('hop'));const placed=new Set();
  (function f(t){const e=t-t0;P.forEach(p=>{const x=pos(p,e)*goal;$('arR'+p.who).style.transform='translateX('+x+'px)';
    if(x>=goal-.5&&!placed.has(p.who)){placed.add(p.who);$('arR'+p.who).classList.remove('hop');$('arP'+p.who).textContent=['🥇','🥈','🥉'][p.place]||(p.place+1)+'th';$('arL'+p.who).classList.add('fin');if(p.place===0){$('arMsg').textContent='🏆 '+R[p.who]+' wins!';$('arMsg').animate([{transform:'scale(1.2)'},{transform:'scale(1)'}],{duration:450});if($('arSnd').checked)chime()}}});
   if(placed.size<n)requestAnimationFrame(f);else{racing=false;$('arGo').disabled=false;$('arGo').textContent='Race again'}})(t0)}}
$('arGo').onclick=race;$('arList').oninput=()=>{save();if(!racing)lay()};$('arLen').onchange=save;
$('arShuf').onclick=()=>{for(let i=order.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[order[i],order[j]]=[order[j],order[i]]}save();if(!racing)lay()};
addEventListener('resize',()=>{if(!racing)lay()});
document.addEventListener('keydown',e=>{if(e.code==='Space'&&!/INPUT|TEXTAREA|SELECT|BUTTON/.test(e.target.tagName)){e.preventDefault();race()}});
lay()})();</script>'''

RACE_TEXT = '''<h2>How to play the animal race</h2>
<ol><li><b>Type the racers</b>, one per line: student names, teams or even answer choices. Up to 12 can race.</li>
<li>Each racer gets a cute animal: a duck, bunny, turtle, cat, piggy, frog, chick, penguin, bear, fox, mouse or panda. <b>Shuffle the animals</b> to swap them.</li>
<li><b>Press Start the race</b>. After “3, 2, 1, GO!”, the animals hop to the finish line, overtaking each other along the way.</li>
<li>The winner gets 🥇, then 🥈 and 🥉. Press <b>Race again</b> for another round.</li></ol>
<h2>Is the race fair?</h2>
<p>Yes. The finishing order is drawn with your browser’s secure random numbers when you press Start, so every racer has the same chance. The overtaking you see is just for fun, and the slow turtle wins as often as the fox.</p>
<h2>Ideas for class</h2>
<ul><li><b>Who goes first:</b> presentations, games or lining up.</li>
<li><b>Team points:</b> race the teams; 1st place earns 3 points, 2nd 2 points, 3rd 1 point.</li>
<li><b>Predict the winner:</b> before the race, students write down who they think will win. A fun way to talk about chance and probability.</li>
<li><b>Answer race:</b> type four answer choices as the racers for a light-hearted “which one wins?” before revealing the right answer.</li>
<li><b>Party games</b> and raffles at class parties.</li></ul>
<h2>Questions</h2>
<h3>Is the class list saved?</h3><p>Yes, in this browser only. Nothing is sent to us.</p>
<h3>Want a quieter way to pick?</h3><p>Use the <a href="/tools/spinner-wheel/">spinner wheel</a> or the <a href="/tools/random-name-picker/">random name picker</a>.</p>'''

# ------------------------------------------------------------------ 4. Icebreaker cards
DECKS = {
 'wyr': ('Would you rather…?', [
  'Would you rather be able to fly or be invisible?', 'Would you rather live by the beach or in the mountains?', 'Would you rather have a pet dragon or a pet unicorn?',
  'Would you rather read minds or see the future?', 'Would you rather always be too hot or always be too cold?', 'Would you rather visit the past or the future?',
  'Would you rather talk to animals or speak every language?', 'Would you rather eat only pizza or only noodles for a week?', 'Would you rather be a famous singer or a famous athlete?',
  'Would you rather explore space or the deep ocean?', 'Would you rather have no homework or no tests?', 'Would you rather have super speed or super strength?',
  'Would you rather live in a treehouse or a houseboat?', 'Would you rather be the oldest or the youngest in your family?', 'Would you rather have a robot helper or a magic backpack?',
  'Would you rather be able to breathe underwater or never need sleep?', 'Would you rather always tell the truth or never speak again?', 'Would you rather be a teacher or a student for a day?',
  'Would you rather win a talent show or a science fair?', 'Would you rather go camping or stay in a fancy hotel?', 'Would you rather have a rewind button or a pause button for your life?',
  'Would you rather live without music or without movies?', 'Would you rather be a dinosaur or a dragon?', 'Would you rather have an extra day of weekend or an hour more of sleep every night?',
  'Would you rather build a sandcastle or a snowman?', 'Would you rather write a book or make a movie?', 'Would you rather never use a phone again or never watch TV again?',
  'Would you rather be really good at drawing or at singing?', 'Would you rather travel by hot air balloon or by submarine?', 'Would you rather have a giant cookie or a mountain of ice cream?']),
 'tot': ('This or that?', [
  'Cats or dogs?', 'Sunrise or sunset?', 'Books or movies?', 'Summer or winter?', 'Pancakes or waffles?', 'Beach or pool?', 'Morning or night?', 'Chocolate or vanilla?',
  'Math or reading?', 'Sneakers or sandals?', 'Rainy days or sunny days?', 'Sweet or salty?', 'Board games or video games?', 'City or countryside?', 'Drawing or writing?',
  'Soccer or basketball?', 'Phone call or text message?', 'Space or the ocean?', 'Pizza or burgers?', 'Comedy or adventure?', 'Early bird or night owl?', 'Mountains or islands?',
  'Ice cream cone or cup?', 'Singing or dancing?', 'Robots or dinosaurs?', 'Puzzles or sports?', 'Fruit or candy?', 'Superhero or wizard?', 'Train or plane?', 'Hot cocoa or cold juice?']),
 'fts': ('Finish the sentence', [
  'The best day of my life was…', 'If I could have any job, it would be…', 'Something that always makes me smile is…', 'If I had a superpower, it would be…',
  'My favorite place in the world is…', 'One thing I’m really good at is…', 'If I won a prize, I would spend it on…', 'The food I could eat every day is…',
  'One thing I want to learn this year is…', 'My dream holiday is…', 'If I were an animal, I would be…', 'The best advice I ever got was…', 'A song that makes me happy is…',
  'If I could meet anyone, I would meet…', 'Something I’m proud of is…', 'On a free day, I like to…', 'If I could invent something, it would be…', 'My favorite thing about school is…',
  'One thing that surprises people about me is…', 'If I had a time machine, I would go to…', 'A small thing that makes my day better is…', 'Something new I tried recently is…',
  'The funniest thing that happened to me was…', 'When I grow up, I hope to…', 'My perfect weekend would be…']),
 'gtk': ('Get to know you', [
  'What is your favorite snack?', 'What is the best gift you’ve ever received?', 'What do you like to do after school?', 'What is a hobby you’d like to try?',
  'Who is someone you look up to, and why?', 'What is your favorite season, and why?', 'What is a book, show or game you love?', 'Do you have a pet? If not, what pet would you like?',
  'What is your favorite holiday or celebration?', 'What is something you can teach others?', 'What was your favorite toy when you were little?', 'What is one place you’d love to visit?',
  'What is your favorite way to relax?', 'What is a skill you’d like to be better at?', 'What makes a good friend?', 'What is your favorite school subject, and why?',
  'What is something that made you laugh this week?', 'If you could have dinner with a famous person, who would it be?', 'What is your favorite kind of weather?', 'What is a goal you have for this year?',
  'What is your favorite family tradition?', 'What would your perfect sandwich have in it?', 'What talent would you love to have?', 'What is the best thing about where you live?',
  'What is a word that describes you?']),
 'draw': ('Quick draw', [
  'A cat on a skateboard', 'A house made of candy', 'A robot doing homework', 'A fish wearing a hat', 'A dragon eating ice cream', 'Your dream treehouse', 'A rainy day',
  'A monster that is afraid of the dark', 'A superhero dog', 'An alien visiting school', 'A tree with a face', 'A snowman on the beach', 'A bicycle with wings', 'Your favorite food with a face',
  'A turtle racing a rabbit', 'A castle in the clouds', 'A bus full of animals', 'A shoe that is also a car', 'An octopus playing drums', 'A sleepy sun', 'A birthday cake for a giant',
  'A penguin in the desert', 'A volcano made of popcorn', 'A rocket made of cardboard', 'A happy cactus']),
 'ttl': ('Two truths and a lie', [
  'Think of two true things about you and one that isn’t. Share all three; the class guesses the lie!', 'Two truths and a lie: about your favorite foods.', 'Two truths and a lie: about places you’ve been.',
  'Two truths and a lie: about things you can do.', 'Two truths and a lie: about your family or pets.', 'Two truths and a lie: about your weekend.', 'Two truths and a lie: about things you like and dislike.',
  'Two truths and a lie: about when you were little.', 'Two truths and a lie: about your hobbies.', 'Two truths and a lie: about your dreams for the future.']),
}

def _decks_js():
    import json
    return 'const DECKS=' + json.dumps({k: {'n': n, 'c': c} for k, (n, c) in DECKS.items()}, ensure_ascii=False) + ';'

ICE = '''<div class="tool" id="ic">''' + FS + '''
 <div class="tbar ed" id="icDecks"></div>
 <div class="ic-card" id="icCard"><div class="ic-in"><small id="icDeck"></small><div id="icQ" aria-live="polite">Tap “Next card” to start</div></div></div>
 <div class="ic-timer" id="icTimer" hidden><b id="icTL"></b><i><span id="icTB"></span></i></div>
 <div class="tbar"><button type="button" id="icPrev">◀ Back</button><button class="go" type="button" id="icNext">Next card ▶</button><button type="button" id="icTime">⏱ Timer</button><label class="ed">for <select id="icTsel"><option>30</option><option selected>60</option><option>90</option><option>120</option></select> s</label></div>
 <p class="note" id="icInfo"></p>
 <div class="ed" id="icOwnBox" hidden style="margin-top:12px"><textarea id="icOwn" placeholder="Type your own questions or prompts, one per line"></textarea></div>
</div>
<style>
.tool [hidden]{display:none!important}
.ic-card{perspective:1200px;max-width:900px;margin:6px auto 10px}.ic-in{background:var(--chalk);color:var(--board);border-radius:22px;min-height:clamp(220px,34vw,380px);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:28px 34px;text-align:center;box-shadow:0 14px 30px rgba(0,0,0,.35);transition:transform .35s;position:relative}
.ic-in.flip{transform:rotateX(90deg)}.ic-in small{position:absolute;top:14px;left:20px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:13px;opacity:.6}
#icQ{font-family:var(--display);font-size:clamp(26px,5vw,62px);line-height:1.18}#ic:fullscreen .ic-card{max-width:none;width:88vw}#ic:fullscreen #icQ{font-size:clamp(34px,6vw,86px)}
.ic-timer{display:flex;align-items:center;gap:12px;max-width:900px;margin:0 auto 10px}.ic-timer b{font-family:var(--display);font-size:34px;min-width:70px;text-align:right}.ic-timer i{flex:1;height:12px;background:rgba(242,240,228,.18);border-radius:99px;overflow:hidden}.ic-timer span{display:block;height:100%;background:#F2C94C;width:100%}
</style>
<script>(()=>{''' + CHIME + _decks_js() + '''
const $=i=>document.getElementById(i);DECKS.own={n:'My own cards',c:[]};
let d=store.get('pp-ic-deck','wyr');if(!DECKS[d])d='wyr';$('icOwn').value=store.get('pp-ic-own','');let Q=[],k=-1,ts=+store.get('pp-ic-ts','60'),tr=0,tEnd=0;
function own(){return $('icOwn').value.split('\\n').map(s=>s.trim()).filter(Boolean)}
function deal(){const c=d==='own'?own():DECKS[d].c.slice();for(let i=c.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[c[i],c[j]]=[c[j],c[i]]}Q=c;k=-1}
function show(dir){const el=document.querySelector('.ic-in');if(!Q.length){$('icQ').textContent=d==='own'?'Type your own cards below':'No cards';info();return}
 el.classList.add('flip');setTimeout(()=>{$('icQ').textContent=Q[k];$('icDeck').textContent=DECKS[d].n;el.classList.remove('flip');info()},180);if(d==='draw'||d==='ttl')startT();else stopT()}
function info(){$('icInfo').textContent=Q.length?(k<0?Q.length+' cards in this deck':'Card '+(k+1)+' of '+Q.length+(k===Q.length-1?' · next shuffles the deck again':'')):'';$('icPrev').disabled=k<=0}
function drawDecks(){$('icDecks').innerHTML=Object.keys(DECKS).map(x=>'<button type="button" data-d="'+x+'" class="'+(x===d?'on':'')+'">'+DECKS[x].n+'</button>').join('');
 document.querySelectorAll('#icDecks button').forEach(b=>b.onclick=()=>{d=b.dataset.d;store.set('pp-ic-deck',d);$('icOwnBox').hidden=d!=='own';drawDecks();deal();$('icDeck').textContent=DECKS[d].n;$('icQ').textContent=d==='own'&&!Q.length?'Type your own cards below':'Tap “Next card” to start';stopT();info()})}
$('icNext').onclick=()=>{if(!Q.length)deal();if(!Q.length)return show();k++;if(k>=Q.length){deal();k=0}show(1)};
$('icPrev').onclick=()=>{if(k>0){k--;show(-1)}};
$('icOwn').oninput=()=>{store.set('pp-ic-own',$('icOwn').value);if(d==='own'){deal();info()}};
function stopT(){cancelAnimationFrame(tr);$('icTimer').hidden=true}
function startT(){stopT();$('icTimer').hidden=false;tEnd=Date.now()+ts*1000;(function f(){const l=(tEnd-Date.now())/1000;$('icTL').textContent=Math.max(0,Math.ceil(l));$('icTB').style.width=Math.max(0,l/ts*100)+'%';if(l>0)tr=requestAnimationFrame(f);else{$('icTL').textContent='⏰';chime()}})()}
$('icTime').onclick=()=>{if(!$('icTimer').hidden&&Date.now()<tEnd){stopT();return}startT()};
$('icTsel').value=String(ts);$('icTsel').onchange=function(){ts=+this.value;store.set('pp-ic-ts',ts)};
document.addEventListener('keydown',e=>{if(/INPUT|TEXTAREA|SELECT/.test(e.target.tagName))return;if(e.code==='Space'||e.key==='ArrowRight'){e.preventDefault();$('icNext').click()}else if(e.key==='ArrowLeft')$('icPrev').click()});
$('icOwnBox').hidden=d!=='own';drawDecks();deal();$('icDeck').textContent=DECKS[d].n;info()})();</script>'''

ICE_TEXT = '''<h2>How to use the icebreaker cards</h2>
<ol><li><b>Choose a deck:</b> Would you rather, This or that, Finish the sentence, Get to know you, Quick draw, Two truths and a lie, or <b>My own cards</b>.</li>
<li><b>Press Next card</b> (or the space bar) to show a big card on the projector. Cards come in a random order, with no repeats until the deck runs out.</li>
<li>Use the <b>timer</b> for thinking or drawing time. It starts by itself in Quick draw and Two truths and a lie. Choose 30, 60, 90 or 120 seconds next to the timer button.</li></ol>
<h2>Ways to play</h2>
<ul><li><b>Would you rather / This or that:</b> students move to one side of the room for each answer, or show a thumbs up or down. Ask one or two to explain why.</li>
<li><b>Finish the sentence:</b> go around the circle, or pair up and share for one minute each.</li>
<li><b>Get to know you:</b> partners interview each other, then introduce their partner to the class.</li>
<li><b>Quick draw:</b> one student draws the prompt on the <a href="/board/">PizarraPad board</a> while the class guesses. No words or letters allowed!</li>
<li><b>Two truths and a lie:</b> a student shares three statements, and the class votes on the lie.</li>
<li><b>My own cards:</b> type review questions, vocabulary or discussion topics for any subject.</li></ul>
<h2>When to use icebreakers</h2>
<ul><li>The first days of school, and with a new class or group.</li><li>Brain breaks between long tasks, or after a <a href="/tools/pomodoro-timer/">Pomodoro</a> round.</li>
<li>Morning meetings, advisory and homeroom.</li><li>Team building in clubs, youth groups and workshops for adults.</li></ul>
<p>All the cards are written to be friendly and comfortable for every age. Students can always say “pass”.</p>
<h2>Questions</h2>
<h3>Are my own cards saved?</h3><p>Yes, in this browser only. Nothing is sent to us.</p>'''

TOOLS_MORE = [
 ('/tools/pomodoro-timer/', 'Pomodoro Timer for the Classroom: Focus and Break Intervals (Free)', 'Pomodoro timer',
  'A free Pomodoro timer for the classroom and studying: 25 minutes of focus and 5-minute breaks, or your own steps and stations. Big full-screen countdown, chime between steps, starts the next step by itself.', POMO, POMO_TEXT,
  'Focus and break intervals, or your own steps and stations, with a chime.'),
 ('/tools/spinner-wheel/', 'Spinner Wheel: Free Random Name and Prize Wheel for the Classroom', 'Spinner wheel',
  'A free spinner wheel for the classroom: type names, prizes or topics and spin. Ticking sound, remove the winner, full screen for the projector. Fair and random, no sign-up.', WHEEL, WHEEL_TEXT,
  'Spin a colorful wheel of names, prizes or topics.'),
 ('/tools/animal-race/', 'Animal Race: A Fun Random Name Picker Game for the Classroom', 'Animal race',
  'A free animal race for the classroom: each student or team gets a cute animal, and they race to the finish line. A fun, fair way to pick a winner or who goes first. Full screen for the projector.', RACE, RACE_TEXT,
  'Cute animals race to the finish: a fun way to pick a winner.'),
 ('/tools/icebreaker-cards/', 'Icebreaker Cards: Would You Rather, This or That and More for the Classroom', 'Icebreaker cards',
  'Free icebreaker cards for the projector: Would you rather, This or that, Finish the sentence, Get to know you, Quick draw, Two truths and a lie, or your own cards. With a timer, no sign-up.', ICE, ICE_TEXT,
  'Would you rather, this or that, quick draw and more, on big cards.'),
]
