"""
Tizedes Tört Kalkulátor
=======================
Futtatás: python decimal_calculator.py
Majd nyisd meg: http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect
from fractions import Fraction
import math

app = Flask(__name__)
app.secret_key = "tizedes_titok_2024"
PASSWORD = "nemtudom"

LOGIN_HTML = """<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Belépés — Tizedes Tört Kalkulátor</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Code+Pro:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  :root { --ink:#1a1a2e;--paper:#f5f0e8;--aged:#e8dfc8;--rust:#c0392b;--line:#c8b89a;--muted:#7a6f5e; }
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:var(--paper);background-image:repeating-linear-gradient(transparent,transparent 31px,var(--line) 31px,var(--line) 32px);min-height:100vh;font-family:'Source Code Pro',monospace;display:flex;align-items:center;justify-content:center;}
  .card{background:white;border:2px solid var(--ink);padding:2.5rem 2rem;width:340px;position:relative;box-shadow:6px 6px 0 var(--aged);}
  .card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:8px;background:var(--rust);}
  h1{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:900;color:var(--ink);margin-bottom:0.3rem;padding-left:0.8rem;}
  .sub{font-size:0.72rem;color:var(--muted);margin-bottom:1.8rem;padding-left:0.8rem;letter-spacing:0.08em;}
  label{display:block;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;color:var(--muted);margin-bottom:0.4rem;padding-left:0.8rem;}
  input[type=password]{width:100%;font-family:'Source Code Pro',monospace;font-size:1.1rem;padding:0.6rem 0.8rem;border:2px solid var(--ink);background:#fffdf9;color:var(--ink);outline:none;margin-bottom:1rem;letter-spacing:0.15em;}
  input[type=password]:focus{border-color:var(--rust);}
  button{width:100%;font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;padding:0.65rem;background:var(--ink);color:var(--paper);border:2px solid var(--ink);cursor:pointer;letter-spacing:0.05em;transition:all 0.15s;}
  button:hover{background:var(--rust);border-color:var(--rust);}
  .error{background:#fdf0ee;border-left:3px solid var(--rust);padding:0.5rem 0.8rem;font-size:0.8rem;color:var(--rust);margin-bottom:1rem;}
  .lock{font-size:2.5rem;text-align:center;margin-bottom:1rem;}
</style>
</head>
<body>
<div class="card">
  <div class="lock">🔒</div>
  <h1>Belépés</h1>
  <p class="sub">Tizedes Tört Kalkulátor</p>
  {% if error %}<div class="error">❌ Hibás jelszó! Próbáld újra.</div>{% endif %}
  <form method="POST" action="/login">
    <label>Jelszó</label>
    <input type="password" name="password" placeholder="••••••••" autofocus>
    <button type="submit">Belépés →</button>
  </form>
</div>
</body>
</html>
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["logged_in"] = True
            return redirect("/")
        return render_template_string(LOGIN_HTML, error=True)
    return render_template_string(LOGIN_HTML, error=False)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect("/login")

HTML = """<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tizedes Tört Kalkulátor</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Code+Pro:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  :root {
    --ink: #1a1a2e;
    --paper: #f5f0e8;
    --aged: #e8dfc8;
    --rust: #c0392b;
    --gold: #b8860b;
    --muted: #7a6f5e;
    --line: #c8b89a;
    --green: #2c7a4b;
    --blue: #1a4f6e;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    background: var(--paper);
    background-image:
      repeating-linear-gradient(
        transparent,
        transparent 31px,
        var(--line) 31px,
        var(--line) 32px
      );
    min-height: 100vh;
    font-family: 'Source Code Pro', monospace;
    color: var(--ink);
    padding: 2rem 1rem 4rem;
  }

  .notebook {
    max-width: 860px;
    margin: 0 auto;
    position: relative;
  }

  /* Notebook binding holes */
  .notebook::before {
    content: '';
    position: fixed;
    left: 0; top: 0; bottom: 0;
    width: 72px;
    background: repeating-linear-gradient(
      to bottom,
      transparent 0,
      transparent 78px,
      var(--aged) 78px,
      var(--aged) 82px
    );
    border-right: 3px solid var(--rust);
    z-index: 0;
  }

  /* Red margin line */
  .margin-line {
    position: fixed;
    left: 88px;
    top: 0; bottom: 0;
    width: 2px;
    background: rgba(192,57,43,0.35);
    z-index: 1;
  }

  .content {
    margin-left: 40px;
    position: relative;
    z-index: 2;
  }

  header {
    margin-bottom: 2.5rem;
    padding-top: 1rem;
  }

  .subject-line {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
  }

  h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 900;
    color: var(--ink);
    line-height: 1;
    letter-spacing: -0.02em;
    text-shadow: 2px 2px 0 var(--aged);
  }

  h1 span {
    color: var(--rust);
  }

  .subtitle {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 0.6rem;
    font-style: italic;
  }

  /* Tabs */
  .tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid var(--ink);
    padding-bottom: 0;
  }

  .tab-btn {
    font-family: 'Playfair Display', serif;
    font-size: 0.78rem;
    padding: 0.45rem 0.9rem;
    border: 2px solid var(--ink);
    border-bottom: none;
    background: var(--aged);
    color: var(--muted);
    cursor: pointer;
    transition: all 0.15s;
    font-weight: 700;
    letter-spacing: 0.02em;
    position: relative;
    top: 2px;
    white-space: nowrap;
  }

  .tab-btn:hover {
    background: var(--paper);
    color: var(--ink);
  }

  .tab-btn.active {
    background: var(--paper);
    color: var(--rust);
    border-color: var(--rust);
    top: 2px;
    z-index: 1;
  }

  /* Panels */
  .panel {
    display: none;
    animation: fadeIn 0.2s ease;
  }
  .panel.active { display: block; }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .panel-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--blue);
    margin-bottom: 1.2rem;
    border-bottom: 1px dashed var(--line);
    padding-bottom: 0.5rem;
  }

  /* Input groups */
  .input-row {
    display: flex;
    gap: 0.8rem;
    align-items: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
  }

  .field-group {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
    font-weight: 600;
  }

  input[type="number"], input[type="text"], select {
    font-family: 'Source Code Pro', monospace;
    font-size: 1.05rem;
    padding: 0.5rem 0.75rem;
    border: 2px solid var(--ink);
    background: white;
    color: var(--ink);
    width: 150px;
    outline: none;
    transition: border-color 0.15s;
    -moz-appearance: textfield;
  }

  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button { -webkit-appearance: none; }

  input:focus, select:focus {
    border-color: var(--rust);
    background: #fff9f5;
  }

  select { width: 180px; cursor: pointer; }

  /* Buttons */
  .calc-btn {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 700;
    padding: 0.6rem 1.6rem;
    background: var(--ink);
    color: var(--paper);
    border: 2px solid var(--ink);
    cursor: pointer;
    transition: all 0.15s;
    letter-spacing: 0.04em;
    margin-top: 1.2rem;
  }

  .calc-btn:hover {
    background: var(--rust);
    border-color: var(--rust);
    transform: translateY(-1px);
    box-shadow: 3px 3px 0 var(--muted);
  }

  .calc-btn:active { transform: translateY(0); box-shadow: none; }

  /* Result box */
  .result-box {
    margin-top: 1.5rem;
    padding: 1.2rem 1.4rem;
    background: white;
    border: 2px solid var(--ink);
    border-left: 5px solid var(--rust);
    min-height: 60px;
    position: relative;
    display: none;
  }

  .result-box.show { display: block; }

  .result-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--muted);
    margin-bottom: 0.5rem;
  }

  .result-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--green);
  }

  .result-explanation {
    font-size: 0.8rem;
    color: var(--muted);
    margin-top: 0.6rem;
    line-height: 1.6;
    font-style: italic;
  }

  .result-steps {
    margin-top: 0.8rem;
    padding-top: 0.8rem;
    border-top: 1px dashed var(--line);
  }

  .step {
    font-size: 0.82rem;
    color: var(--ink);
    line-height: 1.9;
    font-family: 'Source Code Pro', monospace;
  }

  .step b { color: var(--rust); }

  /* Number line */
  #numberline-canvas {
    width: 100%;
    max-width: 680px;
    height: 120px;
    background: white;
    border: 2px solid var(--ink);
    border-radius: 0;
    display: block;
    margin-top: 1rem;
  }

  /* Average special */
  .avg-inputs {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.8rem;
    align-items: center;
  }

  .avg-inputs input {
    width: 100px;
  }

  .add-num-btn {
    font-family: 'Source Code Pro', monospace;
    font-size: 1.1rem;
    width: 36px; height: 36px;
    border: 2px solid var(--green);
    background: white;
    color: var(--green);
    cursor: pointer;
    font-weight: 700;
    transition: all 0.15s;
    display: flex; align-items: center; justify-content: center;
  }

  .add-num-btn:hover { background: var(--green); color: white; }

  .remove-num-btn {
    font-family: 'Source Code Pro', monospace;
    font-size: 1rem;
    width: 28px; height: 28px;
    border: 1px solid var(--rust);
    background: white;
    color: var(--rust);
    cursor: pointer;
    font-weight: 700;
    transition: all 0.15s;
  }

  .remove-num-btn:hover { background: var(--rust); color: white; }

  /* Error */
  .error-msg {
    color: var(--rust);
    font-size: 0.82rem;
    margin-top: 0.5rem;
    font-style: italic;
  }

  /* Fraction display */
  .frac-display {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    font-family: 'Source Code Pro', monospace;
    font-size: 1.1rem;
    vertical-align: middle;
    margin: 0 0.3rem;
  }
  .frac-display span:first-child {
    border-bottom: 2px solid var(--ink);
    padding: 0 4px 2px;
  }
  .frac-display span:last-child { padding: 2px 4px 0; }

  /* Decorative corner marks */
  .corner-mark {
    position: absolute;
    font-family: 'Playfair Display', serif;
    font-size: 0.65rem;
    color: var(--muted);
  }

  .hint {
    font-size: 0.72rem;
    color: var(--muted);
    font-style: italic;
    margin-top: 0.3rem;
  }

  footer {
    margin-top: 3rem;
    font-size: 0.68rem;
    color: var(--muted);
    text-align: center;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
</style>
</head>
<body>
<div class="margin-line"></div>
<div class="notebook">
<div class="content">

<header>
  <div class="subject-line">Matematika · 5–6. osztály</div>
  <h1>Tizedes Tört<span>.</span></h1>
  <div class="subtitle">Interaktív számolóeszköz — minden feladattípushoz</div>
</header>

<div class="tabs">
  <button class="tab-btn active" onclick="showTab('szamegyenes')">📏 Számegyenes</button>
  <button class="tab-btn" onclick="showTab('kerekites')">🔢 Kerekítés</button>
  <button class="tab-btn" onclick="showTab('osszeadas')">➕ Összeadás</button>
  <button class="tab-btn" onclick="showTab('kivonas')">➖ Kivonás</button>
  <button class="tab-btn" onclick="showTab('tizes')">✕ × ÷ 10/100/1000</button>
  <button class="tab-btn" onclick="showTab('szorzas')">🔢 × ÷ természetes</button>
  <button class="tab-btn" onclick="showTab('atlag')">📊 Átlag</button>
  <button class="tab-btn" onclick="showTab('torthex')">½ Tört → Tizedes</button>
</div>

<!-- SZÁMEGYENES -->
<div class="panel active" id="panel-szamegyenes">
  <div class="panel-title">Tizedes törtek ábrázolása számegyenesen</div>
  <div class="input-row">
    <div class="field-group">
      <label>Szám</label>
      <input type="number" id="nl-num" value="3.7" step="0.1" placeholder="pl. 3.7">
    </div>
  </div>
  <p class="hint">Adj meg egy tizedes törtszámot, és megjelenítem a számegyenesen!</p>
  <button class="calc-btn" onclick="calcNumberLine()">Ábrázolás</button>
  <canvas id="numberline-canvas" width="680" height="120"></canvas>
  <div class="result-box" id="res-nl">
    <div class="result-label">Eredmény</div>
    <div class="result-value" id="res-nl-val"></div>
    <div class="result-explanation" id="res-nl-exp"></div>
  </div>
</div>

<!-- KEREKÍTÉS -->
<div class="panel" id="panel-kerekites">
  <div class="panel-title">Tizedes törtek kerekítése</div>
  <div class="input-row">
    <div class="field-group">
      <label>Szám</label>
      <input type="number" id="rnd-num" value="4.67" step="0.01" placeholder="pl. 4.67">
    </div>
    <div class="field-group">
      <label>Kerekítés</label>
      <select id="rnd-to">
        <option value="0">Egészre</option>
        <option value="1">Tizedre</option>
        <option value="2">Századra</option>
        <option value="3">Ezredre</option>
      </select>
    </div>
  </div>
  <button class="calc-btn" onclick="calcRound()">Kerekítés</button>
  <div class="result-box" id="res-rnd">
    <div class="result-label">Kerekített érték</div>
    <div class="result-value" id="res-rnd-val"></div>
    <div class="result-steps" id="res-rnd-steps"></div>
  </div>
</div>

<!-- ÖSSZEADÁS -->
<div class="panel" id="panel-osszeadas">
  <div class="panel-title">Tizedes törtek összeadása</div>
  <div class="input-row">
    <div class="field-group">
      <label>Első szám</label>
      <input type="number" id="add-a" value="3.45" step="0.01">
    </div>
    <div style="font-size:1.5rem;padding-top:1.2rem;color:var(--green);font-weight:700;">+</div>
    <div class="field-group">
      <label>Második szám</label>
      <input type="number" id="add-b" value="2.78" step="0.01">
    </div>
  </div>
  <button class="calc-btn" onclick="calcAdd()">Kiszámít</button>
  <div class="result-box" id="res-add">
    <div class="result-label">Összeg</div>
    <div class="result-value" id="res-add-val"></div>
    <div class="result-steps" id="res-add-steps"></div>
  </div>
</div>

<!-- KIVONÁS -->
<div class="panel" id="panel-kivonas">
  <div class="panel-title">Tizedes törtek kivonása</div>
  <div class="input-row">
    <div class="field-group">
      <label>Első szám</label>
      <input type="number" id="sub-a" value="7.5" step="0.01">
    </div>
    <div style="font-size:1.5rem;padding-top:1.2rem;color:var(--rust);font-weight:700;">−</div>
    <div class="field-group">
      <label>Második szám</label>
      <input type="number" id="sub-b" value="3.28" step="0.01">
    </div>
  </div>
  <button class="calc-btn" onclick="calcSub()">Kiszámít</button>
  <div class="result-box" id="res-sub">
    <div class="result-label">Különbség</div>
    <div class="result-value" id="res-sub-val"></div>
    <div class="result-steps" id="res-sub-steps"></div>
  </div>
</div>

<!-- TÍZES SZORZÁS/OSZTÁS -->
<div class="panel" id="panel-tizes">
  <div class="panel-title">Szorzás / Osztás 10-zel, 100-zal, 1000-rel</div>
  <div class="input-row">
    <div class="field-group">
      <label>Szám</label>
      <input type="number" id="pow-num" value="4.56" step="0.01">
    </div>
    <div class="field-group">
      <label>Művelet</label>
      <select id="pow-op">
        <option value="m10">× 10</option>
        <option value="m100">× 100</option>
        <option value="m1000">× 1000</option>
        <option value="d10">÷ 10</option>
        <option value="d100">÷ 100</option>
        <option value="d1000">÷ 1000</option>
      </select>
    </div>
  </div>
  <button class="calc-btn" onclick="calcPow()">Kiszámít</button>
  <div class="result-box" id="res-pow">
    <div class="result-label">Eredmény</div>
    <div class="result-value" id="res-pow-val"></div>
    <div class="result-steps" id="res-pow-steps"></div>
  </div>
</div>

<!-- TERMÉSZETES SZÁMMAL -->
<div class="panel" id="panel-szorzas">
  <div class="panel-title">Szorzás / Osztás természetes számmal</div>
  <div class="input-row">
    <div class="field-group">
      <label>Tizedes tört</label>
      <input type="number" id="nat-dec" value="2.4" step="0.1">
    </div>
    <div class="field-group">
      <label>Művelet</label>
      <select id="nat-op">
        <option value="mul">×</option>
        <option value="div">÷</option>
      </select>
    </div>
    <div class="field-group">
      <label>Természetes szám</label>
      <input type="number" id="nat-num" value="5" min="1" step="1">
    </div>
  </div>
  <button class="calc-btn" onclick="calcNat()">Kiszámít</button>
  <div class="result-box" id="res-nat">
    <div class="result-label">Eredmény</div>
    <div class="result-value" id="res-nat-val"></div>
    <div class="result-steps" id="res-nat-steps"></div>
  </div>
</div>

<!-- ÁTLAG -->
<div class="panel" id="panel-atlag">
  <div class="panel-title">Az átlag kiszámítása</div>
  <p class="hint" style="margin-bottom:0.8rem;">Add meg a számokat (legalább 2 szám szükséges):</p>
  <div class="avg-inputs" id="avg-inputs">
    <input type="number" class="avg-val" value="3.5" step="0.1" placeholder="szám">
    <input type="number" class="avg-val" value="4.2" step="0.1" placeholder="szám">
    <input type="number" class="avg-val" value="5.8" step="0.1" placeholder="szám">
    <button class="add-num-btn" onclick="addAvgInput()" title="Szám hozzáadása">+</button>
  </div>
  <button class="calc-btn" onclick="calcAvg()">Átlag kiszámítása</button>
  <div class="result-box" id="res-avg">
    <div class="result-label">Átlag</div>
    <div class="result-value" id="res-avg-val"></div>
    <div class="result-steps" id="res-avg-steps"></div>
  </div>
</div>

<!-- TÖRT ALAKBÓL TIZEDES -->
<div class="panel" id="panel-torthex">
  <div class="panel-title">Tört alakban írt szám tizedes tört alakja</div>
  <div class="input-row">
    <div class="field-group">
      <label>Számláló</label>
      <input type="number" id="fr-num" value="3" step="1">
    </div>
    <div style="font-size:2rem;padding-top:1rem;color:var(--ink);">/</div>
    <div class="field-group">
      <label>Nevező</label>
      <input type="number" id="fr-den" value="4" min="1" step="1">
    </div>
  </div>
  <p class="hint">Pl. 3/4 = 0,75</p>
  <button class="calc-btn" onclick="calcFrac()">Átalakítás</button>
  <div class="result-box" id="res-fr">
    <div class="result-label">Tizedes tört alakja</div>
    <div class="result-value" id="res-fr-val"></div>
    <div class="result-steps" id="res-fr-steps"></div>
  </div>
</div>

<footer>Tizedes Tört Kalkulátor &nbsp;·&nbsp; Általános iskola &nbsp;·&nbsp; 5–6. osztály</footer>
</div>
</div>

<script>
function showTab(id) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + id).classList.add('active');
  event.target.classList.add('active');
}

function showResult(id, val, steps) {
  const box = document.getElementById('res-' + id);
  document.getElementById('res-' + id + '-val').textContent = val;
  const s = document.getElementById('res-' + id + '-steps');
  if (s) s.innerHTML = steps || '';
  box.classList.add('show');
}

function fmt(n) {
  // Format number with comma as decimal separator (Hungarian)
  return String(parseFloat(n.toFixed(10))).replace('.', ',');
}

// NUMBER LINE
function calcNumberLine() {
  const num = parseFloat(document.getElementById('nl-num').value);
  if (isNaN(num)) return;
  drawNumberLine(num);
  const fl = Math.floor(num);
  const dec = num - fl;
  const exp = dec === 0
    ? `${fmt(num)} egész szám, pontosan az ${fl} jelölésén áll.`
    : `${fmt(num)} az ${fl} és ${fl + 1} között helyezkedik el. A tizedes rész: ${fmt(parseFloat(dec.toFixed(4)))}`;
  document.getElementById('res-nl-val').textContent = fmt(num);
  document.getElementById('res-nl-exp').textContent = exp;
  document.getElementById('res-nl').classList.add('show');
}

function drawNumberLine(num) {
  const canvas = document.getElementById('numberline-canvas');
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0, 0, W, H);

  const pad = 60;
  const lineY = 75;

  // Determine range
  let lo = Math.floor(num) - 2;
  let hi = Math.ceil(num) + 2;
  if (hi - lo < 6) hi = lo + 6;

  const toX = v => pad + ((v - lo) / (hi - lo)) * (W - 2 * pad);

  // Background
  ctx.fillStyle = '#fffdf9';
  ctx.fillRect(0, 0, W, H);

  // Main line
  ctx.strokeStyle = '#1a1a2e';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(pad - 10, lineY);
  ctx.lineTo(W - pad + 10, lineY);
  ctx.stroke();

  // Arrows
  ctx.fillStyle = '#1a1a2e';
  ctx.beginPath();
  ctx.moveTo(W - pad + 10, lineY);
  ctx.lineTo(W - pad, lineY - 5);
  ctx.lineTo(W - pad, lineY + 5);
  ctx.fill();

  // Tick marks - integers
  ctx.strokeStyle = '#1a1a2e';
  ctx.fillStyle = '#1a1a2e';
  ctx.font = '13px "Source Code Pro", monospace';
  ctx.textAlign = 'center';

  for (let i = lo; i <= hi; i++) {
    const x = toX(i);
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x, lineY - 12);
    ctx.lineTo(x, lineY + 12);
    ctx.stroke();
    ctx.fillText(i, x, lineY + 26);
  }

  // Tick marks - tenths (smaller)
  ctx.strokeStyle = '#9a8a75';
  ctx.lineWidth = 1;
  for (let i = lo * 10; i <= hi * 10; i++) {
    if (i % 10 === 0) continue;
    const x = toX(i / 10);
    ctx.beginPath();
    ctx.moveTo(x, lineY - 6);
    ctx.lineTo(x, lineY + 6);
    ctx.stroke();
  }

  // Point
  const px = toX(num);
  ctx.fillStyle = '#c0392b';
  ctx.beginPath();
  ctx.arc(px, lineY, 9, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#fff';
  ctx.beginPath();
  ctx.arc(px, lineY, 4, 0, Math.PI * 2);
  ctx.fill();

  // Label above point
  ctx.fillStyle = '#c0392b';
  ctx.font = 'bold 14px "Source Code Pro", monospace';
  ctx.textAlign = 'center';
  ctx.fillText(String(num).replace('.', ','), px, lineY - 20);

  // Dashed drop line
  ctx.strokeStyle = '#c0392b';
  ctx.setLineDash([3, 3]);
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(px, lineY - 13);
  ctx.lineTo(px, lineY - 18);
  ctx.stroke();
  ctx.setLineDash([]);
}

// ROUNDING
function calcRound() {
  const num = parseFloat(document.getElementById('rnd-num').value);
  const to = parseInt(document.getElementById('rnd-to').value);
  if (isNaN(num)) return;

  const result = parseFloat(num.toFixed(to));
  const placeNames = ['egészre', 'tizedre', 'századra', 'ezredre'];
  const digit = to === 0 ? 'egész' : ['tized', 'század', 'ezred'][to - 1];

  // Find the deciding digit
  const deciding = Math.abs(num * Math.pow(10, to + 1)) % 10 | 0;
  const direction = deciding >= 5 ? 'felfelé (≥ 5)' : 'lefelé (< 5)';

  const steps = `
    <div class="step">Szám: <b>${fmt(num)}</b></div>
    <div class="step">Kerekítés: <b>${placeNames[to]}</b></div>
    <div class="step">Döntő jegy (${to + 1}. tizedes): <b>${deciding}</b> → ${direction} kerekítünk</div>
    <div class="step">Eredmény: <b>${fmt(result)}</b></div>
  `;
  showResult('rnd', fmt(result), steps);
}

// ADDITION
function calcAdd() {
  const a = parseFloat(document.getElementById('add-a').value);
  const b = parseFloat(document.getElementById('add-b').value);
  if (isNaN(a) || isNaN(b)) return;

  const result = parseFloat((a + b).toFixed(10));
  const dA = (a.toString().split('.')[1] || '').length;
  const dB = (b.toString().split('.')[1] || '').length;
  const maxD = Math.max(dA, dB);

  const aStr = a.toFixed(maxD);
  const bStr = b.toFixed(maxD);

  const steps = `
    <div class="step">Azonos számú tizedesjegyre hozzuk:</div>
    <div class="step" style="font-family:monospace;letter-spacing:0.05em">
      &nbsp;&nbsp;${aStr.replace('.', ',')}<br>
      + ${bStr.replace('.', ',')}<br>
      <span style="border-top:2px solid var(--ink);display:inline-block;padding-top:2px;min-width:80px">${result.toFixed(maxD).replace('.', ',')}</span>
    </div>
  `;
  showResult('add', fmt(result), steps);
}

// SUBTRACTION
function calcSub() {
  const a = parseFloat(document.getElementById('sub-a').value);
  const b = parseFloat(document.getElementById('sub-b').value);
  if (isNaN(a) || isNaN(b)) return;

  const result = parseFloat((a - b).toFixed(10));
  const dA = (a.toString().split('.')[1] || '').length;
  const dB = (b.toString().split('.')[1] || '').length;
  const maxD = Math.max(dA, dB);

  const steps = `
    <div class="step">Azonos számú tizedesjegyre hozzuk:</div>
    <div class="step" style="font-family:monospace;letter-spacing:0.05em">
      &nbsp;&nbsp;${a.toFixed(maxD).replace('.', ',')}<br>
      − ${b.toFixed(maxD).replace('.', ',')}<br>
      <span style="border-top:2px solid var(--ink);display:inline-block;padding-top:2px;min-width:80px">${result.toFixed(maxD).replace('.', ',')}</span>
    </div>
    ${result < 0 ? '<div class="step" style="color:var(--rust)">⚠ Negatív eredmény: a kisebb számból vontuk ki a nagyobbat.</div>' : ''}
  `;
  showResult('sub', fmt(result), steps);
}

// POWER OF 10
function calcPow() {
  const num = parseFloat(document.getElementById('pow-num').value);
  const op = document.getElementById('pow-op').value;
  if (isNaN(num)) return;

  const opMap = { m10: [10,'×',10], m100: [100,'×',100], m1000: [1000,'×',1000],
                  d10: [10,'÷',0.1], d100: [100,'÷',0.01], d1000: [1000,'÷',0.001] };
  const [divisor, sym, factor] = opMap[op];
  const result = parseFloat((num * factor).toFixed(10));

  const moveDir = sym === '×' ? 'jobbra' : 'balra';
  const zeros = String(divisor).length - 1;
  const rule = sym === '×'
    ? `Szorzásnál a tizedesvesszőt ${zeros} hellyel jobbra toljuk.`
    : `Osztásnál a tizedesvesszőt ${zeros} hellyel balra toljuk.`;

  const steps = `
    <div class="step">${fmt(num)} ${sym} ${divisor} = <b>${fmt(result)}</b></div>
    <div class="step">💡 ${rule}</div>
    <div class="step">${fmt(num)} → <b>${fmt(result)}</b> (${zeros} hely ${moveDir})</div>
  `;
  showResult('pow', fmt(result), steps);
}

// NATURAL NUMBER
function calcNat() {
  const dec = parseFloat(document.getElementById('nat-dec').value);
  const nat = parseInt(document.getElementById('nat-num').value);
  const op = document.getElementById('nat-op').value;
  if (isNaN(dec) || isNaN(nat) || nat === 0) return;

  const result = op === 'mul'
    ? parseFloat((dec * nat).toFixed(10))
    : parseFloat((dec / nat).toFixed(10));

  const sym = op === 'mul' ? '×' : '÷';

  let steps;
  if (op === 'mul') {
    steps = `
      <div class="step">${fmt(dec)} ${sym} ${nat}</div>
      <div class="step">= ${fmt(dec)} + ${Array(nat - 1).fill(fmt(dec)).join(' + ')}</div>
      <div class="step">= <b>${fmt(result)}</b></div>
    `;
  } else {
    steps = `
      <div class="step">${fmt(dec)} ÷ ${nat}</div>
      <div class="step">Minden tizedesjegyet elosztunk ${nat}-vel.</div>
      <div class="step">= <b>${fmt(result)}</b></div>
    `;
  }
  showResult('nat', fmt(result), steps);
}

// AVERAGE
function addAvgInput() {
  const container = document.getElementById('avg-inputs');
  const inp = document.createElement('input');
  inp.type = 'number';
  inp.className = 'avg-val';
  inp.step = '0.1';
  inp.placeholder = 'szám';

  const btn = document.createElement('button');
  btn.className = 'remove-num-btn';
  btn.textContent = '×';
  btn.onclick = () => { container.removeChild(inp); container.removeChild(btn); };

  container.insertBefore(btn, container.lastElementChild);
  container.insertBefore(inp, btn);
  inp.focus();
}

function calcAvg() {
  const inputs = document.querySelectorAll('.avg-val');
  const vals = Array.from(inputs)
    .map(i => parseFloat(i.value))
    .filter(v => !isNaN(v));

  if (vals.length < 2) {
    document.getElementById('res-avg').classList.add('show');
    document.getElementById('res-avg-val').textContent = 'Legalább 2 szám kell!';
    document.getElementById('res-avg-steps').innerHTML = '';
    return;
  }

  const sum = vals.reduce((a, b) => a + b, 0);
  const avg = parseFloat((sum / vals.length).toFixed(10));

  const steps = `
    <div class="step">Számok: <b>${vals.map(fmt).join(', ')}</b></div>
    <div class="step">Összeg: ${vals.map(fmt).join(' + ')} = <b>${fmt(parseFloat(sum.toFixed(10)))}</b></div>
    <div class="step">Darabszám: <b>${vals.length}</b></div>
    <div class="step">Átlag: ${fmt(parseFloat(sum.toFixed(10)))} ÷ ${vals.length} = <b>${fmt(avg)}</b></div>
  `;
  showResult('avg', fmt(avg), steps);
}

// FRACTION TO DECIMAL
function calcFrac() {
  const num = parseInt(document.getElementById('fr-num').value);
  const den = parseInt(document.getElementById('fr-den').value);
  if (isNaN(num) || isNaN(den) || den === 0) return;

  const result = parseFloat((num / den).toFixed(10));

  // Long division simulation
  let remainder = Math.abs(num) % den;
  let digits = String(Math.abs(Math.floor(num / den)));
  let divSteps = [];
  let seen = {};
  let isRecurring = false;
  let recurStart = -1;
  const decDigits = [];

  for (let i = 0; i < 8 && remainder !== 0; i++) {
    if (seen[remainder] !== undefined) {
      isRecurring = true;
      recurStart = seen[remainder];
      break;
    }
    seen[remainder] = i;
    remainder *= 10;
    decDigits.push(Math.floor(remainder / den));
    divSteps.push(`${remainder} ÷ ${den} = ${Math.floor(remainder / den)}, maradék: ${remainder % den}`);
    remainder = remainder % den;
  }

  let decStr = digits + ',' + decDigits.join('');
  if (isRecurring) decStr += '...';
  if (num < 0) decStr = '−' + decStr;

  const steps = `
    <div class="step">Törtszám: <b>${num}/${den}</b></div>
    <div class="step">Elvégezzük az osztást: ${num} ÷ ${den}</div>
    ${divSteps.map(s => `<div class="step" style="padding-left:1rem">→ ${s}</div>`).join('')}
    ${isRecurring ? '<div class="step" style="color:var(--blue)">♾ Végtelen tizedes tört (periodikus)</div>' : ''}
    <div class="step">Eredmény: <b>${decStr}</b></div>
  `;
  showResult('fr', decStr, steps);
}

// Init number line on load
window.onload = () => calcNumberLine();
</script>
</body>
</html>"""


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template_string(HTML)


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
