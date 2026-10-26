# -*- coding: utf-8 -*-
"""Генератор сайта «Мой сад» — интерактивная карта + карточки растений."""
import html
import os
import json
from plants_data import PLANTS, ORDER, MAP_ROWS

OUT = os.path.dirname(os.path.abspath(__file__))


def validate(plants, order, map_rows):
    """Проверка целостности данных перед сборкой; при ошибках — SystemExit."""
    errs = []
    ids = [p["id"] for p in plants]
    if len(ids) != len(set(ids)):
        errs.append("дублирующиеся id растений")
    known = set(ids)
    if sorted(order) != sorted(ids):
        errs.append(f"ORDER не совпадает со списком id (ORDER: {len(order)}, PLANTS: {len(ids)})")
    for p in plants:
        for key in ("name", "species", "kind", "row_label", "tagline", "emoji",
                    "count", "facts", "chars", "planting", "care", "pruning",
                    "pests", "harvest", "tips", "sources", "garden_note"):
            if key not in p:
                errs.append(f"{p.get('id','?')}: нет поля '{key}'")
    used = set()
    for rname, items in map_rows:
        for it in items:
            pid = it["plant"]
            if pid not in known:
                errs.append(f"MAP_ROWS ({rname}): растение '{pid}' отсутствует в PLANTS")
            else:
                used.add(pid)
    missing = known - used
    if missing:
        errs.append(f"не размещены на карте: {', '.join(sorted(missing))}")
    if errs:
        raise SystemExit("Ошибка в данных:\n  - " + "\n  - ".join(errs))


validate(PLANTS, ORDER, MAP_ROWS)

P = {p["id"]: p for p in PLANTS}
ORDERED = [P[i] for i in ORDER]
with open(os.path.join(OUT, "photos.json"), encoding="utf-8") as f:
    PHOTOS = json.load(f)

KINDS = {
    "apple":    dict(name="Яблони",         color="#5b9a3e", fruit="#d64545", shape="tree"),
    "pear":     dict(name="Груши",          color="#b09a2e", fruit="#d8c53e", shape="tree"),
    "cherry":   dict(name="Вишни",          color="#c0392b", fruit="#8e1f2f", shape="tree"),
    "plum":     dict(name="Сливы",          color="#7d4f9e", fruit="#5d3a7d", shape="tree"),
    "wildplum": dict(name="Тёрн",           color="#55618f", fruit="#2e3a66", shape="bush"),
    "haw":      dict(name="Боярышник",      color="#d0532a", fruit="#a5351a", shape="bush"),
    "hazel":    dict(name="Орешник",        color="#9a7b4f", fruit="#6f5230", shape="bush"),
    "oak":      dict(name="Дуб",            color="#3e6b35", fruit="#6b4f2a", shape="oak"),
    "unknown":  dict(name="Сорт уточняется", color="#8a8f85", fruit="#757b70", shape="tree"),
}

def e(s):
    return html.escape(str(s), quote=True)

# ------------------------------------------------------------------ CSS
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#f6f4ec;--card:#ffffff;--ink:#26331f;--muted:#6c7a63;--line:#e4e1d2;
  --green:#4a7c3f;--green-d:#33582c;--gold:#c9a227;--tip:#2c3a26;
  --apple:#5b9a3e;--pear:#b09a2e;--cherry:#c0392b;--plum:#7d4f9e;--wildplum:#8e6f9e;
  --haw:#d0532a;--hazel:#9a7b4f;--oak:#3e6b35;--unknown:#8a8f85;
}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
     background:var(--bg);color:var(--ink);line-height:1.6}
h1,h2,h3{font-family:Georgia,"Times New Roman",serif;font-weight:700;line-height:1.25}
a{color:var(--green-d)}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
/* ---------- header ---------- */
header.top{background:linear-gradient(135deg,#3d6b33 0%,#4a7c3f 55%,#5b9a3e 100%);color:#fff;position:relative;overflow:hidden}
header.top::after{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.08) 1.5px,transparent 1.5px);background-size:26px 26px;pointer-events:none}
.top-in{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:18px 0;position:relative;z-index:1}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:#fff}
.brand .logo{width:44px;height:44px;border-radius:12px;background:rgba(255,255,255,.16);display:flex;align-items:center;justify-content:center;font-size:24px}
.brand b{font-family:Georgia,serif;font-size:21px;letter-spacing:.3px;display:block;line-height:1.15}
.brand span{font-size:12.5px;opacity:.85}
nav.main{display:flex;gap:6px;flex-wrap:wrap}
nav.main a{color:#fff;text-decoration:none;padding:8px 14px;border-radius:999px;font-size:14.5px;background:rgba(255,255,255,.12)}
nav.main a:hover{background:rgba(255,255,255,.26)}
/* ---------- hero ---------- */
.hero{padding:40px 0 8px;text-align:center}
.hero h1{font-size:clamp(28px,4.5vw,44px);color:var(--green-d)}
.hero p.lead{max-width:760px;margin:14px auto 0;color:var(--muted);font-size:16.5px}
.stats{display:flex;flex-wrap:wrap;gap:14px;justify-content:center;margin:26px 0 8px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 22px;text-align:center;min-width:130px;box-shadow:0 2px 8px rgba(60,80,40,.06)}
.stat b{display:block;font-size:26px;color:var(--green);font-family:Georgia,serif}
.stat span{font-size:13px;color:var(--muted)}
/* ---------- sections ---------- */
section{margin:44px 0}
.sec-head{display:flex;align-items:baseline;gap:12px;margin-bottom:18px;flex-wrap:wrap}
.sec-head h2{font-size:26px;color:var(--green-d)}
.sec-head span{color:var(--muted);font-size:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;box-shadow:0 3px 12px rgba(60,80,40,.06)}
/* ---------- map ---------- */
.map-card{padding:18px}
.map-toolbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:12px}
.chip{border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:6px 14px;font-size:13.5px;cursor:pointer;display:inline-flex;align-items:center;gap:7px;color:var(--ink);transition:.15s}
.chip:hover{border-color:var(--green)}
.chip:focus-visible,.tree-link:focus-visible,a:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.tree-link:focus-visible circle:first-child{stroke-width:3;stroke-opacity:1}
.chip.on{background:var(--green);border-color:var(--green);color:#fff}
.chip i{width:11px;height:11px;border-radius:50%;display:inline-block}
.map-wrap{position:relative;border-radius:12px;overflow:hidden;background:#eef2e0;border:1px solid #dfe6cc}
.map-wrap svg{display:block;width:100%;height:auto}
svg text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
.tree{cursor:pointer;transition:opacity .2s}
.tree .zoom{transition:transform .18s ease;transform-box:fill-box;transform-origin:center}
.tree:hover .zoom{transform:scale(1.09)}
.tree.dim{opacity:.14;pointer-events:none}
.rowband{transition:.2s}
#maptip{position:absolute;z-index:9;pointer-events:none;background:var(--tip);color:#f2f5ea;border-radius:10px;padding:10px 13px;font-size:13px;max-width:260px;line-height:1.45;box-shadow:0 6px 20px rgba(0,0,0,.3);opacity:0;transition:opacity .12s}
#maptip b{color:#fff;font-size:13.5px;display:block;margin-bottom:2px}
#maptip i{color:#fff;font-style:normal}
#maptip .go{color:#bcd7a8;margin-top:5px;display:block;font-size:12px}
/* ---------- catalog ---------- */
.cat-group{margin-bottom:26px}
.cat-group h3{font-size:19px;margin-bottom:12px;display:flex;align-items:center;gap:9px;color:var(--green-d)}
.cat-group h3 i{width:13px;height:13px;border-radius:50%;display:inline-block}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:14px}
.pcard{background:var(--card);border:1px solid var(--line);border-left:5px solid var(--green);border-radius:14px;padding:16px 16px 14px;text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:7px;transition:.15s;box-shadow:0 2px 8px rgba(60,80,40,.05)}
.pcard:hover{transform:translateY(-3px);box-shadow:0 8px 22px rgba(60,80,40,.13)}
.pcard .ttl{display:flex;align-items:center;gap:9px}
.pcard .em{font-size:24px}
.pcard b{font-family:Georgia,serif;font-size:17px;color:var(--ink)}
.pcard small{color:var(--muted);font-size:12.5px}
.pcard p{font-size:13.5px;color:#4d5a46;flex:1}
.pcard .tags{display:flex;gap:6px;flex-wrap:wrap}
.tag{font-size:11.5px;background:#eef2e2;color:#4b6b3d;border-radius:999px;padding:3px 10px}
.pcard .more{color:var(--green);font-size:13.5px;font-weight:600}
/* ---------- calendar ---------- */
.seasons{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}
.season{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}
.season h3{font-size:16.5px;margin-bottom:9px;display:flex;gap:8px;align-items:center}
.season ul{list-style:none}
.season li{font-size:13.5px;padding:4px 0 4px 20px;position:relative;color:#46523e}
.season li::before{content:"🌿";position:absolute;left:0;font-size:11px;top:6px}
/* ---------- plant page ---------- */
.crumbs{font-size:13.5px;color:var(--muted);padding:18px 0 0}
.crumbs a{color:var(--green-d)}
.plant-head{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:26px;margin-top:14px;box-shadow:0 3px 12px rgba(60,80,40,.06)}
.plant-head .big-em{font-size:56px;width:96px;height:96px;border-radius:20px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.plant-head h1{font-size:clamp(26px,4vw,36px);color:var(--green-d)}
.plant-head .sp{color:var(--muted);font-size:15px;margin-top:2px}
.badges{display:flex;gap:7px;flex-wrap:wrap;margin-top:11px}
.badge{font-size:12px;border-radius:999px;padding:4px 12px;background:#eef2e2;color:#41602f;border:1px solid #dbe4c8}
.tagline{margin-top:11px;font-size:15.5px;color:#46523e;max-width:640px}
.toc{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0}
.toc a{font-size:13px;text-decoration:none;color:var(--green-d);background:#eef2e2;border-radius:999px;padding:6px 13px;border:1px solid #e0e7cd}
.toc a:hover{background:var(--green);color:#fff;border-color:var(--green)}
.psec{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:24px 26px;margin-bottom:18px;box-shadow:0 2px 8px rgba(60,80,40,.05)}
.psec h2{font-size:21px;color:var(--green-d);margin-bottom:13px;display:flex;align-items:center;gap:10px}
.psec h2 .ic{font-size:20px}
.psec p{margin-bottom:10px}
.psec ul{margin:6px 0 6px 4px;list-style:none}
.psec ul li{padding:5px 0 5px 24px;position:relative;font-size:15px}
.psec ul li::before{content:"✔";position:absolute;left:0;color:var(--green);font-size:13px;top:7px}
.facts-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:10px;margin-top:4px}
.fact{background:#f4f6ec;border:1px solid #e6eadb;border-radius:12px;padding:11px 14px}
.fact span{display:block;font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px}
.fact b{font-size:14.5px;color:var(--ink);font-weight:600}
table.chars{width:100%;border-collapse:collapse;font-size:14.5px}
table.chars td{padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
table.chars td:first-child{color:var(--muted);width:34%;font-size:13.5px}
table.chars tr:last-child td{border-bottom:none}
.note-box{background:#f0f5e6;border:1px solid #d8e4c2;border-left:5px solid var(--green);border-radius:12px;padding:15px 18px;font-size:14.5px;margin-bottom:18px}
.note-box b{color:var(--green-d)}
.tips li::before{content:"💡";font-size:13px;top:6px}
.tips{background:#fdf9ec;border:1px solid #f0e4bd}
.tips h2{color:#8a6d1a}
.poll-box{background:#f3ecf7;border:1px solid #e2d4ec;border-radius:12px;padding:15px 18px;font-size:14.5px}
.sources ol{margin-left:20px;font-size:14px}
.sources li{padding:3px 0}
.pn{display:flex;justify-content:space-between;gap:12px;margin:26px 0 50px;flex-wrap:wrap}
.pn a{flex:1;min-width:230px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px;text-decoration:none;color:inherit;transition:.15s;box-shadow:0 2px 8px rgba(60,80,40,.05)}
.pn a:hover{border-color:var(--green);transform:translateY(-2px)}
.pn a span{display:block;font-size:12px;color:var(--muted)}
.pn a b{font-family:Georgia,serif;color:var(--green-d);font-size:16px}
.pn a.next{text-align:right}
/* ---------- gallery ---------- */
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:12px}
.gallery figure{margin:0;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}
.gallery a{display:block;overflow:hidden}
.gallery img{width:100%;height:150px;object-fit:cover;display:block;transition:transform .25s}
.gallery figure:hover img{transform:scale(1.06)}
.gallery figcaption{font-size:12px;color:var(--muted);padding:8px 10px;line-height:1.4}
/* ---------- footer ---------- */
footer{background:#31452a;color:#cdd8c4;margin-top:60px;padding:34px 0;font-size:13.5px}
footer b{color:#fff}
footer a{color:#b8d3a5}
footer .fin{display:flex;gap:30px;flex-wrap:wrap;margin-top:14px;opacity:.85}
@media(max-width:640px){
  .plant-head{padding:20px}
  .psec{padding:18px}
}
@media print{
  header.top nav,.toc,.pn,.map-toolbar{display:none}
  body{background:#fff}
  .psec,.card{box-shadow:none;border-color:#ccc}
}
"""

JS = """
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
"""

FAVICON = ("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20100%20100'%3E"
           "%3Ctext%20y='0.9em'%20font-size='90'%3E%F0%9F%8C%B3%3C/text%3E%3C/svg%3E")

# ------------------------------------------------------------------ helpers
def page(title, body, root=""):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="Мой сад — учёт деревьев и кустарников, интерактивная карта, характеристики, посадка, уход и тонкости выращивания.">
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
{body}
<script src="{root}app.js"></script>
</body>
</html>"""

def header(active="", root=""):
    def act(k, label, href):
        cls = ' style="background:rgba(255,255,255,.3)"' if active == k else ""
        return f'<a href="{root}{href}"{cls}>{label}</a>'
    return f"""<header class="top"><div class="wrap top-in">
<a class="brand" href="{root}index.html"><span class="logo">🌳</span>
<span><b>Мой сад</b><span>учёт растений · карта · карточки</span></span></a>
<nav class="main">
{act("map", "🗺 Карта сада", "index.html#map")}
{act("cat", "📇 Каталог", "index.html#catalog")}
{act("cal", "🗓 Календарь", "index.html#calendar")}
</nav></div></header>"""

def footer():
    return """<footer><div class="wrap">
<b>Мой сад</b> — интерактивная карта участка и энциклопедия его растений.<br>
Информация собрана из профильных источников (sortoved.ru, vniispk.ru, sadsezon.com, КП-сад, supersadovnik.ru, питомники)
и дополнена отзывами опытных садоводов с форумов (forum.prihoz.ru, plodpitomnik.ru, forum.tvoysad.ru, vsesorta.ru).
<div class="fin"><span>🍎 9 яблонь</span><span>🍐 2 груши</span><span>🍒 5 вишен</span><span>🟣 6 слив</span><span>🫐 тёрн · 🌰 орешник · 🔴 боярышник · 🌳 дуб</span></div>
<div class="fin"><span>Порядок группы первой линии показан как «вишни слева, сливы справа» — если на участке иначе, поправьте раскладку в MAP_ROWS (plants_data.py) и пересоберите сайт.</span></div>
</div></footer>"""

# ------------------------------------------------------------------ SVG map
def glyph(cx, cy, s, kind, unknown=False):
    k = KINDS[kind]
    color, fruit, shape = k["color"], k["fruit"], k["shape"]
    out = [f'<circle cx="{cx}" cy="{cy}" r="{30*s:.1f}" fill="{color}" fill-opacity="0.10" stroke="{color}" stroke-opacity="0.45" stroke-width="1.4"/>']
    trunk = f'<rect x="{cx-2.6*s:.1f}" y="{cy+2*s:.1f}" width="{5.2*s:.1f}" height="{20*s:.1f}" rx="{2*s:.1f}" fill="#9a744c"/>'
    if shape == "tree":
        out.append(trunk)
        if unknown:
            out.append(f'<circle cx="{cx}" cy="{cy-5*s:.1f}" r="{16*s:.1f}" fill="#9aa08f" stroke="#7b8172" stroke-width="1.2"/>')
            out.append(f'<text x="{cx}" y="{cy-5*s+6*s:.1f}" text-anchor="middle" font-size="{17*s:.1f}" font-weight="700" fill="#fff">?</text>')
        else:
            out.append(f'<circle cx="{cx}" cy="{cy-5*s:.1f}" r="{16*s:.1f}" fill="#5f9a49" stroke="#46783a" stroke-width="1.2"/>')
            out.append(f'<circle cx="{cx-6*s:.1f}" cy="{cy-11*s:.1f}" r="{5*s:.1f}" fill="#ffffff" fill-opacity="0.22"/>')
            for fx, fy in ((7, -2), (-3, 3), (1, -10)):
                out.append(f'<circle cx="{cx+fx*s:.1f}" cy="{cy+fy*s:.1f}" r="{2.7*s:.1f}" fill="{fruit}" stroke="#00000022" stroke-width="0.6"/>')
    elif shape == "bush":
        out.append(f'<rect x="{cx-2*s:.1f}" y="{cy+8*s:.1f}" width="{4*s:.1f}" height="{13*s:.1f}" rx="{1.6*s:.1f}" fill="#9a744c"/>')
        for bx, by in ((-9, 2), (9, 2), (0, -8)):
            out.append(f'<circle cx="{cx+bx*s:.1f}" cy="{cy+by*s:.1f}" r="{10.5*s:.1f}" fill="#5f9a49" stroke="#46783a" stroke-width="1.2"/>')
        for fx, fy in ((-11, 5), (10, 4), (2, -12)):
            out.append(f'<circle cx="{cx+fx*s:.1f}" cy="{cy+fy*s:.1f}" r="{2.6*s:.1f}" fill="{fruit}"/>')
    elif shape == "oak":
        out.append(f'<rect x="{cx-3.4*s:.1f}" y="{cy:.1f}" width="{6.8*s:.1f}" height="{21*s:.1f}" rx="{2.4*s:.1f}" fill="#8a6242"/>')
        for ox, oy, orr in ((-12, -2, 9), (0, -9, 11.5), (12, -2, 9), (-6, 4, 8), (6, 4, 8)):
            out.append(f'<circle cx="{cx+ox*s:.1f}" cy="{cy+oy*s:.1f}" r="{orr*s:.1f}" fill="#4e8a3f" stroke="#3a6b2e" stroke-width="1.1"/>')
        for fx, fy in ((-8, -4), (6, -8), (10, 1)):
            out.append(f'<circle cx="{cx+fx*s:.1f}" cy="{cy+fy*s:.1f}" r="{2.4*s:.1f}" fill="{fruit}"/>')
    return "".join(out)

def label(x, y, line1, line2, color):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-size="10.5" fill="{color}" font-weight="600">{e(line1)}</text>'
            f'<text x="{x}" y="{y+14}" text-anchor="middle" font-size="12.5" fill="#2c3a26" font-weight="700">{e(line2)}</text>')

def tip_html(p, extra=""):
    rows = "".join(f"{e(a)}: <i>{e(b)}</i><br>" for a, b in p["facts"][:3])
    return ('<b>' + e(p['name']) + '</b><span style="opacity:.75">' + e(p['species']) + '</span><br>'
            + rows + e(extra) + '<span class="go">клик — открыть карточку →</span>')


def tip_attr(p, extra=""):
    """tip_html с двойным экранированием кавычек — значение атрибута data-tip."""
    return e(tip_html(p, extra)).replace('"', "&quot;")


def join_dot(*parts):
    """Соединяет непустые фрагменты через « · » (row_label может быть пустым)."""
    return " · ".join(x for x in parts if x)

def build_map():
    W, BAND_X0, BAND_X1 = 1080, 96, 1056
    parts = []
    # фон
    parts.append(f'<rect width="{W}" height="734" fill="#eef2e0"/>')

    row_ys = [30, 200, 304, 408, 512, 616]
    row_hs = [160, 96, 96, 96, 96, 96]

    for ri, (rname, items) in enumerate(MAP_ROWS):
        y, h = row_ys[ri], row_hs[ri]
        parts.append(f'<rect class="rowband" x="{BAND_X0}" y="{y}" width="{BAND_X1-BAND_X0}" height="{h}" rx="14" fill="#e7eed6" stroke="#d3ddb8"/>')

        if ri == 0:
            # две компактные группы по 5, прижаты к левому краю
            GSTEP, GPAD, GGAP = 82, 25, 12
            gw = 5 * GSTEP + 2 * GPAD
            for gi, it in enumerate(items):
                p = P[it["plant"]]
                k = KINDS[it["color_key"]]
                gx0 = BAND_X0 + 14 + gi * (gw + GGAP)
                parts.append(f'<a class="tree-link" href="plants/{p["id"]}.html" aria-label="{e(p["name"])}"><g class="tree" data-kind="{it["color_key"]}" data-tip="{tip_attr(p, join_dot(p["row_label"], "5 деревьев") + " · ")}">')
                parts.append(f'<rect x="{gx0:.0f}" y="{y+8}" width="{gw:.0f}" height="{h-46}" rx="12" fill="{k["color"]}" fill-opacity="0.07" stroke="{k["color"]}" stroke-opacity="0.3" stroke-dasharray="4 3"/>')
                for ti in range(5):
                    cx = gx0 + GPAD + GSTEP * (ti + 0.5)
                    parts.append(f'<g class="zoom">{glyph(cx, y + 62, 0.62, it["color_key"])}</g>')
                parts.append(f'<text x="{gx0+gw/2:.0f}" y="{y+h-12}" text-anchor="middle" font-size="13.5" font-weight="700" fill="#2c3a26">{e(p["name"])} ×5 <tspan fill="{k["color"]}" font-size="11">· сорта не определены</tspan></text>')
                parts.append('</g></a>')
        else:
            LEFT, STEP = BAND_X0 + 80, 220
            for ii, it in enumerate(items):
                p = P[it["plant"]]
                cx = LEFT + STEP * ii
                cy = y + 36
                s = it.get("scale", 1.0)
                k = KINDS[p["kind"]]
                parts.append(f'<a class="tree-link" href="plants/{p["id"]}.html" aria-label="{e(p["name"])}"><g class="tree" data-kind="{p["kind"]}" data-tip="{tip_attr(p, p["row_label"])}">')
                parts.append(f'<g class="zoom">{glyph(cx, cy, s, p["kind"], unknown=(p["kind"]=="unknown"))}</g>')
                l2 = p["name"] if len(p["name"]) < 18 else p["name"]
                parts.append(label(cx, y + h - 24, k["name"], l2, k["color"]))
                if it.get("tag"):
                    parts.append(f'<text x="{cx+26}" y="{cy-26}" font-size="10" fill="#8a9a7e" font-style="italic">({e(it["tag"])})</text>')
                parts.append('</g></a>')

    svg = (f'<svg viewBox="0 0 {W} 734" xmlns="http://www.w3.org/2000/svg" role="img" '
           f'aria-label="Интерактивная карта сада: растения рядами, всего 26">' + "".join(parts) + '</svg>')
    return svg

# ------------------------------------------------------------------ index
def build_index():
    n_trees = sum(x["count"] for x in PLANTS)
    legend_kinds = ["apple", "pear", "cherry", "plum", "wildplum", "haw", "hazel", "oak", "unknown"]
    chips = "".join(
        f'<button class="chip" type="button" aria-pressed="false" data-kind="{k}"><i style="background:{KINDS[k]["color"]}"></i>{e(KINDS[k]["name"])}</button>'
        for k in legend_kinds)

    # каталог по группам
    groups = []
    for k in ["apple", "pear", "cherry", "plum", "wildplum", "haw", "hazel", "oak", "unknown"]:
        plist = [p for p in ORDERED if p["kind"] == k]
        if not plist:
            continue
        cards = ""
        for p in plist:
            badges = "".join(f'<span class="tag">{e(b)}</span>' for b in p["badges"][:3])
            short = p["tagline"][:120] + ("…" if len(p["tagline"]) > 120 else "")
            cards += f"""<a class="pcard" style="border-left-color:{KINDS[k]['color']}" href="plants/{p['id']}.html">
<div class="ttl"><span class="em">{p['emoji']}</span><span><b>{e(p['name'])}</b>{f'<br><small>{e(p["row_label"])}</small>' if p['row_label'] else ''}</span></div>
<div class="tags">{badges}</div><p>{e(short)}</p><span class="more">Открыть карточку →</span></a>"""
        total = sum(p["count"] for p in plist)
        word = {1: "растение"}.get(total, "растения" if 2 <= total <= 4 else "растений")
        groups.append(f"""<div class="cat-group"><h3><i style="background:{KINDS[k]['color']}"></i>{e(KINDS[k]['name'])} <span style="color:var(--muted);font-weight:400;font-size:14px">({total} {word} в саду)</span></h3><div class="grid">{cards}</div></div>""")

    body = f"""{header()}
<div class="wrap">
<div class="hero">
<h1>Мой сад: 26 деревьев и кустарников</h1>
<p class="lead">Интерактивная карта участка с растениями, посаженными рядами. Кликните дерево на карте —
откроется его персональная карточка: характеристики, посадка, уход, обрезка, защита и тонкости от опытных садоводов.</p>
<div class="stats">
<div class="stat"><b>{n_trees}</b><span>растений в саду</span></div>
<div class="stat"><b>{len(PLANTS)}</b><span>карточек растений</span></div>
<div class="stat"><b>9</b><span>сортов яблони</span></div>
<div class="stat"><b>2</b><span>сорта груши</span></div>
</div>
</div>

<section id="map">
<div class="sec-head"><h2>🗺 Карта сада</h2><span>наведите на дерево — краткая справка, клик — карточка; кнопки ниже фильтруют по видам</span></div>
<div class="card map-card">
<div class="map-toolbar">
<button class="chip on" type="button" aria-pressed="true" data-kind="">Все растения</button>
{chips}
</div>
<div class="map-wrap">
{build_map()}
<div id="maptip"></div>
</div>
</div>
</section>

<section id="catalog">
<div class="sec-head"><h2>📇 Каталог растений</h2><span>карточки по видам — от вишен первой линии до дуба и «загадочной» яблони</span></div>
{''.join(groups)}
</section>

<section id="calendar">
<div class="sec-head"><h2>🗓 Календарь садовода</h2><span>общий ритм работ для этого сада</span></div>
<div class="seasons">
<div class="season"><h3>🌱 Весна (март–май)</h3><ul>
<li>Обрезка до распускания почек: вишня, слива, груши, яблони</li>
<li>Обновление побелки; снятие зимних обвязок</li>
<li>Первое опрыскивание по «зелёному конусу» (бордоская жидкость / мочевина 700 г)</li>
<li>Азотная подкормка (мочевина, перегной) после схода снега</li>
<li>Осмотр боярышника: снять и сжечь зимние гнёзда боярышницы</li>
</ul></div>
<div class="season"><h3>☀️ Лето (июнь–август)</h3><ul>
<li>Полив в засуху: сливы, груши, орешник в фазе налива плодов</li>
<li>Прореживание завязей на яблонях (Брянское, Народное, Антоновка)</li>
<li>Подпорки под нагруженные ветви — до начала налива</li>
<li>Сбор: Конфетное и Кафедральная (август), Медуница (конец августа)</li>
<li>Ловушки для ос у Конфетного и груш; сетка от птиц на вишни</li>
</ul></div>
<div class="season"><h3>🍂 Осень (сентябрь–ноябрь)</h3><ul>
<li>Съём Антоновки (конец сентября), Брянского, Московского зимнего</li>
<li>Северный синап — в октябре, не раньше (защита от «загара»)</li>
<li>Фосфорно-калийные подкормки (зола, суперфосфат), влагозарядный полив</li>
<li>Побелка штамбов, обвязка от мышей: вишни, сливы, груши, молодой дуб</li>
<li>Уборка листвы из-под вишен (коккомикоз) — в компост только здоровую</li>
</ul></div>
<div class="season"><h3>❄️ Зима (декабрь–февраль)</h3><ul>
<li>Стряхивание мокрого снега с крон (сливы, орешник — ломкие ветви)</li>
<li>Притаптывание снега у штамбов молодых деревьев</li>
<li>Ревизия хранилища: яблоки (Московское зимнее, Синап — до весны)</li>
<li>Планирование сезона: прививки «?»-яблони и Конфетного, покупка черенков</li>
<li>Фотодосье сортов: подготовка бирок для неопознанных деревьев</li>
</ul></div>
</div>
</section>
</div>
{footer()}"""
    return page("Мой сад — интерактивная карта и карточки растений", body)

# ------------------------------------------------------------------ plant page
def gallery_html(pid):
    items = PHOTOS.get(pid, [])
    if not items:
        return ""
    figs = ""
    for it in items:
        tp = os.path.join(OUT, "img", pid, f"thumb-{it['n']}.jpg")
        if not os.path.exists(tp):
            continue
        figs += (f'<figure><a href="../img/{pid}/full-{it["n"]}.jpg" target="_blank" rel="noopener" title="Открыть в полном размере">'
                 f'<img src="../img/{pid}/thumb-{it["n"]}.jpg" alt="{e(it["cap"])}" loading="lazy" width="320" height="150"></a>'
                 f'<figcaption>{e(it["cap"])}<br><span style="opacity:.75">фото: {e(it["src"])}</span></figcaption></figure>')
    return (f'<div class="psec" id="photos"><h2><span class="ic">📷</span>Фотографии</h2>'
            f'<div class="gallery">{figs}</div>'
            f'<p style="font-size:12.5px;color:var(--muted);margin-top:10px">Клик по фото — полный размер. '
            f'Фотографии иллюстрируют сорт/вид; собраны из открытых источников (питомники, сортовые каталоги, Википедия).</p></div>')

def build_plant(p, idx):
    k = KINDS[p["kind"]]
    prev_p, next_p = ORDERED[idx - 1], ORDERED[(idx + 1) % len(ORDERED)]

    toc = [('photos', 'Фото'), ('facts', 'Кратко'), ('desc', 'Описание'), ('chars', 'Характеристики'),
           ('planting', 'Посадка'), ('care', 'Уход'), ('pruning', 'Обрезка'),
           ('pests', 'Болезни и вредители'), ('harvest', 'Урожай'), ('tips', 'Тонкости садоводов'),
           ('garden', 'В вашем саду'), ('sources', 'Источники')]
    toc_html = "".join(f'<a href="#{a}">{e(t)}</a>' for a, t in toc)

    facts = "".join(f'<div class="fact"><span>{e(a)}</span><b>{e(b)}</b></div>' for a, b in p["facts"])
    desc = "".join(f"<p>{e(t)}</p>" for t in p["description"])

    identify = ""
    if p.get("identify"):
        items = "".join(f"<li>{e(t.split('. ',1)[1])}</li>" for t in p["identify"])
        identify = f'<div class="psec" id="identify"><h2><span class="ic">🔍</span>Как определить сорт: план на сезон</h2><ul>{items}</ul></div>'

    chars = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in p["chars"])
    planting = "".join(f"<li>{e(t)}</li>" for t in p["planting"])
    care = "".join(f"<li>{e(t)}</li>" for t in p["care"])
    pruning = "".join(f"<li>{e(t)}</li>" for t in p["pruning"])
    pests = "".join(f"<li>{e(t)}</li>" for t in p["pests"])
    harvest = "".join(f"<li>{e(t)}</li>" for t in p["harvest"])
    tips = "".join(f"<li>{e(t)}</li>" for t in p["tips"])
    sources = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for t, u in p["sources"])

    poll = ""
    if p.get("pollination"):
        poll = f'<div class="poll-box"><b>🐝 Опыление и соседи.</b> {e(p["pollination"])}</div>'

    badges = "".join(f'<span class="badge">{e(b)}</span>' for b in p["badges"])

    body = f"""{header(root="../")}
<div class="wrap">
<div class="crumbs"><a href="../index.html">🌳 Мой сад</a> → <a href="../index.html#map">Карта</a> → {f"{e(p['row_label'])} → " if p['row_label'] else ''}<b>{e(p['name'])}</b></div>
<div class="plant-head">
<div class="big-em" style="background:{k['color']}1f;border:2px solid {k['color']}66">{p['emoji']}</div>
<div>
<h1>{e(p['name'])}</h1>
<div class="sp">{e(join_dot(p['species'], p['row_label'], f"{p['count']} {'шт.' if p['count']>1 else 'дерево'}"))}</div>
<div class="badges">{badges}</div>
<p class="tagline">{e(p['tagline'])}</p>
</div></div>

{gallery_html(p["id"])}

<div class="toc">{toc_html}</div>

<div class="psec" id="facts"><h2><span class="ic">⚡</span>Кратко о растении</h2><div class="facts-grid">{facts}</div></div>

<div class="psec" id="desc"><h2><span class="ic">📖</span>Описание</h2>{desc}</div>

{identify}

<div class="psec" id="chars"><h2><span class="ic">📋</span>Характеристики</h2><table class="chars">{chars}</table></div>

<div class="psec" id="planting"><h2><span class="ic">🌱</span>Посадка</h2><ul>{planting}</ul></div>

<div class="psec" id="care"><h2><span class="ic">💧</span>Уход</h2><ul>{care}</ul>{poll}</div>

<div class="psec" id="pruning"><h2><span class="ic">✂️</span>Обрезка и формирование</h2><ul>{pruning}</ul></div>

<div class="psec" id="pests"><h2><span class="ic">🛡</span>Болезни и вредители</h2><ul>{pests}</ul></div>

<div class="psec" id="harvest"><h2><span class="ic">🧺</span>Урожай и использование</h2><ul>{harvest}</ul></div>

<div class="psec tips" id="tips"><h2><span class="ic">💡</span>Тонкости от опытных садоводов</h2><ul class="tips">{tips}</ul>
<p style="font-size:12.5px;color:var(--muted);margin-top:10px">Советы собраны из отзывов садоводов на форумах и из практики питомников; цитаты приведены по источникам ниже.</p></div>

<div class="psec" id="garden"><h2><span class="ic">📍</span>В вашем саду</h2><div class="note-box">{f"<b>{e(p['name'])} — {e(p['row_label'])}.</b> " if p['row_label'] else f"<b>{e(p['name'])}.</b> "}{e(p['garden_note'])}<br>
<a href="../index.html#map">← Найти на карте сада</a></div></div>

<div class="psec sources" id="sources"><h2><span class="ic">🔗</span>Источники</h2><ol>{sources}</ol></div>

<div class="pn">
<a href="{prev_p['id']}.html" class="prev"><span>← Предыдущее растение</span><b>{prev_p['emoji']} {e(prev_p['name'])}</b></a>
<a href="{next_p['id']}.html" class="next"><span>Следующее растение →</span><b>{next_p['emoji']} {e(next_p['name'])}</b></a>
</div>
</div>
{footer()}"""
    return page(f"{p['name']} — {p['species']} | Мой сад", body, root="../")

# ------------------------------------------------------------------ build
def main():
    os.makedirs(os.path.join(OUT, "plants"), exist_ok=True)
    # общие статические файлы — один раз вместо инлайна в каждой из 18 страниц
    with open(os.path.join(OUT, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS.strip() + "\n")
    with open(os.path.join(OUT, "app.js"), "w", encoding="utf-8") as f:
        f.write(JS.strip() + "\n")
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index())
    for i, p in enumerate(ORDERED):
        html_text = build_plant(p, i)
        with open(os.path.join(OUT, "plants", p["id"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html_text)
    # README
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("""# Мой сад — сайт учёта растений

- `index.html` — главная: интерактивная карта сада (SVG), каталог, календарь работ.
- `plants/*.html` — карточки растений: характеристики, посадка, уход, обрезка,
  защита, тонкости из отзывов садоводов, источники.
- `style.css`, `app.js` — общие стили и скрипты (генерируются, править через `build.py`).
- `plants_data.py` — данные растений (можно править: сорта, тексты, раскладка карты в MAP_ROWS).
- `build.py` — генератор: после правки данных выполните `python3 build.py`.
  Сборка начинается с проверки целостности данных (id, поля, раскладка карты);
  при ошибках сайт не пересобирается.

Откройте `index.html` в браузере. Клик по дереву на карте ведёт в его карточку,
кнопки-фильтры подсвечивают выбранный вид. Деревья на карте и кнопки доступны
с клавиатуры (Tab — обводка и подсказка, Enter — переход).

## Фотографии
- В каждую карточку встроена галерея (миниатюры — `img/<id>/thumb-N.jpg`, грузятся лениво;
  клик по фото открывает полноразмерную версию из `img/<id>/full-N.jpg`).
- Подписи и источники фото — в `photos.json`; там же можно заменить номер/подпись кадра.
- После правок `photos.json` выполните `python3 build.py`.
""")
    print("Сгенерировано:", 1 + len(ORDERED), "страниц + style.css + app.js")

if __name__ == "__main__":
    main()
