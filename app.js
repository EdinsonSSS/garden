(function(){
  'use strict';
  var wrap=document.querySelector('.map-wrap');
  var tip=document.getElementById('maptip');
  var trees=wrap?Array.prototype.slice.call(wrap.querySelectorAll('.tree')):[];
  function show(ev,g){
    if(!tip)return;
    tip.innerHTML=g.getAttribute('data-tip')||'';
    tip.style.opacity='1';
    move(ev);
  }
  function move(ev){
    if(!tip)return;
    var r=wrap.getBoundingClientRect();
    var x=ev.clientX-r.left+16, y=ev.clientY-r.top+14;
    if(x+tip.offsetWidth>r.width-8)x=ev.clientX-r.left-tip.offsetWidth-14;
    if(y+tip.offsetHeight>r.height-8)y=Math.max(6,ev.clientY-r.top-tip.offsetHeight-12);
    tip.style.left=x+'px';tip.style.top=y+'px';
  }
  function hide(){if(tip)tip.style.opacity='0';}
  trees.forEach(function(g){
    g.addEventListener('mouseenter',function(ev){show(ev,g);});
    g.addEventListener('mousemove',move);
    g.addEventListener('mouseleave',hide);
    // доступность с клавиатуры: подсказка при фокусе ссылки на дереве
    var link=g.closest?g.closest('a'):null;
    if(link){
      link.setAttribute('tabindex','0');
      link.addEventListener('focus',function(){
        if(!tip)return;
        tip.innerHTML=g.getAttribute('data-tip')||'';
        tip.style.opacity='1';
        var lr=link.getBoundingClientRect(),wr=wrap.getBoundingClientRect();
        tip.style.left=Math.max(6,lr.left-wr.left)+'px';
        tip.style.top=Math.max(6,lr.bottom-wr.top+6)+'px';
      });
      link.addEventListener('blur',hide);
    }
  });
  var chips=Array.prototype.slice.call(document.querySelectorAll('.chip[data-kind]'));
  var active=null;
  function apply(){
    chips.forEach(function(cc){
      var kk=cc.getAttribute('data-kind');
      var on=(active===null)?(kk===''):(kk===active);
      cc.classList.toggle('on',on);
      cc.setAttribute('aria-pressed',on?'true':'false');
    });
    trees.forEach(function(g){
      if(!active)g.classList.remove('dim');
      else g.classList.toggle('dim',g.getAttribute('data-kind')!==active);
    });
  }
  chips.forEach(function(c){
    c.setAttribute('aria-pressed',c.classList.contains('on')?'true':'false');
    c.addEventListener('click',function(){
      var k=c.getAttribute('data-kind');
      active=(active===k)?null:k;
      apply();
    });
  });
})();
