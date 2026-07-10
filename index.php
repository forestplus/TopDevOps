<?php
/* ============================================================
   index.php — Дмитрий Парамонов, DevOps Team Lead
   Динамическая версия личной страницы.
   ============================================================ */

date_default_timezone_set('Europe/Moscow');

/* ---------- Данные (легко редактировать) ---------- */

$profile = [
    'name'         => 'Дмитрий Парамонов',
    'role'         => 'DevOps Team Lead',
    'city'         => 'Санкт-Петербург',
    'work_permit'  => 'Россия, ОАЭ',
    'career_start' => '2008-02-01', // от этой даты считается стаж — динамически, а не вручную
    'linkedin'     => 'https://www.linkedin.com/in/topdevops',
    'telegram'     => 'https://t.me/TopDevOps',
    'email'        => 'forestplus@ya.ru',
    'phone'        => '+7 (931) 972-45-46',
];

$jobs = [
    [
        'from' => '2023-06-01', 'to' => '2025-12-01',
        'title' => 'DevOps Team Lead',
        'company' => 'Crypto Industry International · ОАЭ',
        'text' => 'Управлял DevOps-процессами компании: стабильность микросервисной инфраструктуры, инцидент-менеджмент, CI/CD, найм и обучение технических специалистов.',
    ],
    [
        'from' => '2021-04-01', 'to' => '2023-06-01',
        'title' => 'Lead DevOps',
        'company' => 'Иннотех · для Банка ВТБ (ПАО), Москва',
        'text' => 'Руководил DevOps-направлением на двух стримах: эквайринг для МСБ (9 микросервисов, перенос в VTB.Cloud) и госуслуги в банковских процессах (12 микросервисов, миграция на DreamPipe CI/CD).',
    ],
    [
        'from' => '2018-12-01', 'to' => '2021-04-01',
        'title' => 'Senior DevOps',
        'company' => 'DELL, Россия',
        'text' => 'Инфраструктура разработки и автоматизация в команде Pipelines: Kubernetes «с нуля» на Azure + VMware ESXi, Ansible, Jenkins, мониторинг Prometheus/Grafana.',
    ],
    [
        'from' => '2008-02-01', 'to' => '2018-08-01',
        'title' => 'DevOps → системное администрирование → основатель бизнеса',
        'company' => 'FINOM · ПрофИТ Солюшенз · IThelperSPb · Т-Банк (Тинькофф) · ЛЕКСПРО',
        'text' => 'От замдиректора IT-департамента до сооснователя (CEO/CIO) собственных компаний — построение IT-инфраструктуры, ITSM/ITIL, виртуализация, мониторинг, автоматизация с нуля.',
    ],
];

$skills = [
    'Оркестрация'    => ['Kubernetes', 'OpenShift', 'Docker', 'Helm', 'VMware ESXi'],
    'CI / CD'        => ['TeamCity', 'Jenkins', 'GitLab CI', 'GitHub'],
    'Автоматизация'  => ['Ansible', 'Bash', 'Python', 'PowerShell'],
    'Мониторинг'     => ['Prometheus', 'Grafana', 'Zabbix', 'Nagios'],
    'Данные'         => ['PostgreSQL', 'MySQL/MariaDB', 'Kafka', 'ActiveMQ'],
    'Управление'     => ['ITIL/ITSM', 'DevSecOps', 'SRE', 'Roadmap'],
];

// Строки для "живого" терминального тикера в шапке — чисто стилистический элемент
$ticker = [
    'мониторинг > все системы в норме',
    'ci/cd > пайплайн выполнен успешно, 0 ошибок',
    'инцидент > устранён за 4 минуты',
    'бэкап > завершён без сбоев',
    'деплой > 12 микросервисов без даунтайма',
    'аптайм > 99.98% за последний квартал',
];

/* ---------- Динамика на стороне сервера ---------- */

$start = new DateTime($profile['career_start']);
$now   = new DateTime();
$diff  = $start->diff($now);
$experienceYears  = $diff->y;
$experienceMonths = $diff->m;

$hour = (int)$now->format('G');
if ($hour >= 5 && $hour < 12)      { $greeting = 'Доброе утро'; }
elseif ($hour >= 12 && $hour < 18) { $greeting = 'Добрый день'; }
elseif ($hour >= 18 && $hour < 23) { $greeting = 'Добрый вечер'; }
else                                { $greeting = 'Доброй ночи'; }

$weekday = (int)$now->format('N');
$isWorkingHours = ($weekday <= 5 && $hour >= 10 && $hour < 20);
$statusText = $isWorkingHours ? 'СИСТЕМА: НА СВЯЗИ, ОТКРЫТ К ПРЕДЛОЖЕНИЯМ' : 'СИСТЕМА: РЕЖИМ ОЖИДАНИЯ (ОТВЕЧУ В РАБОЧЕЕ ВРЕМЯ)';
$statusShort   = $isWorkingHours ? 'на связи' : 'отошёл';

$counterFile = __DIR__ . '/visits.count';
$visits = 1;
if (is_writable(__DIR__)) {
    $visits = @file_exists($counterFile) ? (int)file_get_contents($counterFile) : 0;
    $visits++;
    @file_put_contents($counterFile, $visits);
}

$metrics = [
    ['num' => $experienceYears . '+', 'label' => 'лет опыта'],
    ['num' => '250+',                 'label' => 'серверов под управлением'],
    ['num' => '2',                    'label' => 'страны найма: РФ / ОАЭ'],
    ['num' => '№' . $visits,          'label' => 'визит на страницу'],
];

function fmt_period($fromStr, $toStr) {
    $months = ['янв','фев','мар','апр','май','июн','июл','авг','сен','окт','ноя','дек'];
    $f = new DateTime($fromStr);
    $t = new DateTime($toStr);
    $label = $months[$f->format('n') - 1] . ' ' . $f->format('Y') . ' — ' . $months[$t->format('n') - 1] . ' ' . $t->format('Y');
    $d = $f->diff($t);
    $dur = '';
    if ($d->y > 0) $dur .= $d->y . 'г ';
    if ($d->m > 0) $dur .= $d->m . 'м';
    return [trim($label), trim($dur)];
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title><?php echo htmlspecialchars($profile['name']); ?> — <?php echo htmlspecialchars($profile['role']); ?></title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Inter:wght@400;500;600;700&display=swap');

  :root{
    --bg:#0B1120; --panel:#121A2E; --panel-2:#161F38; --border:#253253;
    --accent:#5EEAD4; --accent-dim:#2A6E64; --warn:#F2B84B;
    --text:#E7ECF3; --muted:#8B96AC;
    --mono:'JetBrains Mono', monospace; --sans:'Inter', -apple-system, sans-serif;
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  html{scroll-behavior:smooth;}
  body{
    background:var(--bg); color:var(--text); font-family:var(--sans); line-height:1.6;
    background-image:
      radial-gradient(circle at 15% 0%, rgba(94,234,212,0.06), transparent 40%),
      radial-gradient(circle at 85% 20%, rgba(242,184,75,0.04), transparent 35%);
  }
  a{color:var(--accent); text-decoration:none;}
  .wrap{max-width:920px; margin:0 auto; padding:0 24px;}

  .topbar{border-bottom:1px solid var(--border); padding:14px 0; font-family:var(--mono); font-size:12px; color:var(--muted); position:sticky; top:0; background:rgba(11,17,32,0.92); backdrop-filter:blur(6px); z-index:50;}
  .topbar .wrap{display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;}
  .status-dot{width:8px; height:8px; border-radius:50%; background:var(--accent); display:inline-block; margin-right:8px; animation:pulse 2s infinite;}
  .status-dot.idle{background:var(--warn); animation:none;}
  @keyframes pulse{0%{box-shadow:0 0 0 0 rgba(94,234,212,0.5);} 70%{box-shadow:0 0 0 6px rgba(94,234,212,0);} 100%{box-shadow:0 0 0 0 rgba(94,234,212,0);}}
  #live-clock{font-variant-numeric:tabular-nums;}

  .hero{padding:56px 0 24px;}
  .hero-grid{display:flex; gap:40px; align-items:center;}
  .avatar{width:132px; height:132px; border-radius:12px; object-fit:cover; border:1px solid var(--border); flex-shrink:0; transition:transform .3s;}
  .avatar:hover{transform:scale(1.04) rotate(-1deg); border-color:var(--accent);}
  .eyebrow{font-family:var(--mono); font-size:12px; color:var(--accent); letter-spacing:1.5px; text-transform:uppercase; margin-bottom:10px;}
  h1{font-family:var(--mono); font-weight:800; font-size:38px; letter-spacing:-0.5px; color:#fff; margin-bottom:8px;}
  .role{font-size:17px; color:var(--muted); margin-bottom:14px; min-height:52px;}
  #typed-cursor{color:var(--accent); animation:blink 1s step-start infinite;}
  @keyframes blink{50%{opacity:0;}}

  .ticker-box{
    font-family:var(--mono); font-size:12px; color:var(--accent);
    background:var(--panel); border:1px solid var(--border); border-radius:6px;
    padding:8px 12px; margin-bottom:20px; max-width:460px; overflow:hidden;
    white-space:nowrap;
  }
  .ticker-box::before{content:"$ "; color:var(--muted);}

  .metrics-row{display:flex; gap:28px; flex-wrap:wrap; margin-top:6px;}
  .metric{font-family:var(--mono);}
  .metric .num{font-size:20px; font-weight:700; color:var(--accent);}
  .metric .lbl{font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:0.5px;}

  .section{padding:40px 0; border-top:1px solid var(--border); opacity:0; transform:translateY(16px); transition:opacity .5s ease, transform .5s ease;}
  .section.visible{opacity:1; transform:translateY(0);}
  .section-label{font-family:var(--mono); font-size:12px; color:var(--warn); letter-spacing:1px; margin-bottom:18px;}
  .section-label::before{content:"// ";}
  .section-label .hint{color:var(--muted); text-transform:none;}
  h2{font-size:22px; font-weight:700; color:#fff; margin-bottom:16px;}
  .about-text{color:#C7CFDE; font-size:15px; max-width:680px;}

  .principles{display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px; margin-top:20px;}
  .principle{background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:14px 16px; font-size:13.5px; color:#C7CFDE;}
  .principle b{display:block; color:var(--accent); font-family:var(--mono); font-size:12px; margin-bottom:6px; text-transform:uppercase;}

  .log-entry{border-bottom:1px solid var(--border); padding:16px 0; cursor:pointer;}
  .log-entry:last-child{border-bottom:none;}
  .log-head{display:flex; gap:20px; align-items:flex-start;}
  .log-ts{font-family:var(--mono); font-size:11.5px; color:var(--muted); width:130px; flex-shrink:0; padding-top:3px; line-height:1.5;}
  .log-body{flex:1;}
  .log-body b{font-size:15.5px; color:#fff; display:block; margin-bottom:2px;}
  .log-company{font-size:13px; color:var(--accent); margin-bottom:6px; font-family:var(--mono);}
  .log-toggle{font-family:var(--mono); color:var(--muted); font-size:13px; padding-top:3px; transition:transform .2s;}
  .log-entry.open .log-toggle{transform:rotate(45deg); color:var(--accent);}
  .log-text{color:#AEB7C9; font-size:14px; max-height:0; overflow:hidden; transition:max-height .25s ease; margin-left:150px;}
  .log-entry.open .log-text{max-height:200px; margin-top:8px;}

  .skills-grid{display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:14px;}
  .skill-panel{background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:16px;}
  .skill-panel .cat{font-family:var(--mono); font-size:11px; color:var(--warn); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:10px;}
  .tag-list{display:flex; flex-wrap:wrap; gap:6px;}
  .tag{font-family:var(--mono); font-size:11.5px; background:var(--panel-2); border:1px solid var(--border); color:#C7CFDE; padding:3px 8px; border-radius:4px; cursor:pointer; transition:.15s;}
  .tag:hover, .tag.active{border-color:var(--accent); color:var(--accent); box-shadow:0 0 0 1px var(--accent) inset;}

  .contact-panel{background:var(--panel); border:1px solid var(--border); border-radius:12px; padding:32px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:24px;}
  .contact-links{display:flex; flex-direction:column; gap:10px;}
  .contact-row{display:flex; align-items:center; gap:10px; font-family:var(--mono); font-size:14px;}
  .contact-row a{color:var(--text); display:flex; align-items:center; gap:10px;}
  .contact-row a:hover{color:var(--accent);}
  .contact-row .k{color:var(--muted); width:80px; display:inline-block; font-size:12px;}
  .copy-btn{background:none; border:1px solid var(--border); color:var(--muted); font-family:var(--mono); font-size:10.5px; padding:2px 7px; border-radius:4px; cursor:pointer; transition:.15s;}
  .copy-btn:hover{color:var(--accent); border-color:var(--accent);}
  .cta{font-family:var(--mono); font-weight:700; background:var(--accent); color:#04231F; padding:12px 22px; border-radius:6px; font-size:14px; white-space:nowrap; border:none; cursor:pointer;}
  .cta:hover{background:#7FF3E0;}

  footer{text-align:center; padding:36px 0; color:var(--muted); font-family:var(--mono); font-size:12px; border-top:1px solid var(--border);}

  #to-top{
    position:fixed; right:20px; bottom:20px; width:42px; height:42px; border-radius:50%;
    background:var(--panel); border:1px solid var(--border); color:var(--accent);
    display:flex; align-items:center; justify-content:center; cursor:pointer;
    opacity:0; pointer-events:none; transition:opacity .25s, transform .2s; font-family:var(--mono); font-size:16px;
  }
  #to-top.show{opacity:1; pointer-events:auto;}
  #to-top:hover{transform:translateY(-3px);}

  @media (max-width:640px){
    .hero-grid{flex-direction:column; align-items:flex-start;}
    h1{font-size:29px;}
    .contact-panel{flex-direction:column; align-items:flex-start;}
    .log-head{flex-direction:column; gap:4px;}
    .log-ts{width:auto;}
    .log-text{margin-left:0;}
    .ticker-box{max-width:100%;}
  }
</style>
</head>
<body>

  <div class="topbar">
    <div class="wrap">
      <div><span class="status-dot <?php echo $isWorkingHours ? '' : 'idle'; ?>"></span><?php echo htmlspecialchars($statusText); ?></div>
      <div><?php echo htmlspecialchars($profile['city']); ?> · <span id="live-clock"></span></div>
    </div>
  </div>

  <div class="wrap">
    <div class="hero">
      <div class="hero-grid">
        <img class="avatar" src="data:image/jpeg;base64,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" alt="<?php echo htmlspecialchars($profile['name']); ?>">
        <div>
          <div class="eyebrow"><?php echo htmlspecialchars($greeting); ?> · статус: <?php echo htmlspecialchars($statusShort); ?></div>
          <h1><?php echo htmlspecialchars($profile['name']); ?></h1>
          <div class="role"><span id="typed-role"></span><span id="typed-cursor">|</span></div>
          <div class="ticker-box"><span id="ticker-text"></span></div>
          <div class="metrics-row">
            <?php foreach ($metrics as $m): ?>
            <div class="metric">
              <div class="num" data-count="<?php echo htmlspecialchars($m['num']); ?>">0</div>
              <div class="lbl"><?php echo htmlspecialchars($m['label']); ?></div>
            </div>
            <?php endforeach; ?>
          </div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">кто_я</div>
      <p class="about-text">
        Прошёл путь от системного администратора до совладельца бизнеса и CEO/CIO. Последние 8+ лет полностью сфокусирован на DevOps-практиках: контейнеризация приложений на Docker с оркестрацией в Kubernetes и OpenShift, преимущественно в финтех-проектах. Строю production-инфраструктуру с минимальным time-to-market и внедряю практики DevSecOps для повышения надёжности систем. Открыт к интересным проектам и долгосрочному сотрудничеству — удалённо, гибридно или на месте, в России и ОАЭ.
      </p>
      <div class="principles">
        <div class="principle"><b>Надёжность</b>Проектирую инфраструктуру так, чтобы инциденты решались быстро, а не повторялись.</div>
        <div class="principle"><b>Скорость</b>Выстраиваю CI/CD и автоматизацию, которые сокращают time-to-market.</div>
        <div class="principle"><b>Люди</b>Нанимаю, обучаю и выращиваю сильные DevOps-команды.</div>
        <div class="principle"><b>Безопасность</b>Внедряю DevSecOps как часть процесса, а не отдельный этап.</div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">журнал_опыта <span class="hint">— нажмите на запись, чтобы раскрыть подробности</span></div>
      <h2>Опыт работы (<?php echo $experienceYears; ?> лет <?php echo $experienceMonths; ?> мес.)</h2>

      <?php foreach ($jobs as $job): list($period, $dur) = fmt_period($job['from'], $job['to']); ?>
      <div class="log-entry" onclick="this.classList.toggle('open')">
        <div class="log-head">
          <div class="log-ts"><?php echo htmlspecialchars($period); ?><br><?php echo htmlspecialchars($dur); ?></div>
          <div class="log-body">
            <b><?php echo htmlspecialchars($job['title']); ?></b>
            <div class="log-company"><?php echo htmlspecialchars($job['company']); ?></div>
          </div>
          <div class="log-toggle">+</div>
        </div>
        <div class="log-text"><?php echo htmlspecialchars($job['text']); ?></div>
      </div>
      <?php endforeach; ?>
    </div>

    <div class="section">
      <div class="section-label">стек_навыков <span class="hint">— нажмите на тег, чтобы подсветить похожие</span></div>
      <h2>Навыки и инструменты</h2>
      <div class="skills-grid">
        <?php foreach ($skills as $cat => $items): ?>
        <div class="skill-panel">
          <div class="cat"><?php echo htmlspecialchars($cat); ?></div>
          <div class="tag-list">
            <?php foreach ($items as $item): ?>
            <span class="tag" onclick="highlightTag(this)"><?php echo htmlspecialchars($item); ?></span>
            <?php endforeach; ?>
          </div>
        </div>
        <?php endforeach; ?>
      </div>
    </div>

    <div class="section">
      <div class="section-label">контакты</div>
      <div class="contact-panel">
        <div class="contact-links">
          <div class="contact-row"><span class="k">linkedin</span><a href="<?php echo htmlspecialchars($profile['linkedin']); ?>" target="_blank">linkedin.com/in/topdevops</a></div>
          <div class="contact-row"><span class="k">telegram</span><a href="<?php echo htmlspecialchars($profile['telegram']); ?>" target="_blank">t.me/TopDevOps</a></div>
          <div class="contact-row"><span class="k">почта</span><a href="mailto:<?php echo htmlspecialchars($profile['email']); ?>"><?php echo htmlspecialchars($profile['email']); ?></a><button class="copy-btn" onclick="copyText('<?php echo htmlspecialchars($profile['email']); ?>', this)">копировать</button></div>
          <div class="contact-row"><span class="k">телефон</span><a href="tel:<?php echo htmlspecialchars(str_replace([' ','(',')','-'], '', $profile['phone'])); ?>"><?php echo htmlspecialchars($profile['phone']); ?></a><button class="copy-btn" onclick="copyText('<?php echo htmlspecialchars($profile['phone']); ?>', this)">копировать</button></div>
        </div>
        <button class="cta" onclick="window.open('<?php echo htmlspecialchars($profile['linkedin']); ?>','_blank')">Написать в LinkedIn →</button>
      </div>
    </div>

    <footer>
      <?php echo htmlspecialchars($profile['name']); ?> · <?php echo htmlspecialchars($profile['role']); ?> · <?php echo htmlspecialchars($profile['city']); ?> / ОАЭ · страница сгенерирована <?php echo $now->format('d.m.Y H:i'); ?> (визит №<?php echo $visits; ?>)
    </footer>
  </div>

  <div id="to-top" onclick="window.scrollTo({top:0, behavior:'smooth'})">↑</div>

<script>
// Живые часы в шапке
function tick(){
  const d = new Date();
  const p = n => String(n).padStart(2,'0');
  document.getElementById('live-clock').textContent = p(d.getHours())+':'+p(d.getMinutes())+':'+p(d.getSeconds())+' МСК';
}
setInterval(tick, 1000); tick();

// Эффект печатной машинки для строки роли
const roleText = "От системного администратора до DevOps Team Lead — 17+ лет строю и стабилизирую инфраструктуру для банков, финтеха и криптопроектов.";
let ti = 0;
const roleEl = document.getElementById('typed-role');
function typeStep(){
  if(ti <= roleText.length){
    roleEl.textContent = roleText.slice(0, ti);
    ti++;
    setTimeout(typeStep, 14);
  } else {
    startTicker();
  }
}
typeStep();

// "Живой" терминальный тикер под заголовком
const tickerLines = <?php echo json_encode($ticker, JSON_UNESCAPED_UNICODE); ?>;
let tIdx = 0;
const tickerEl = document.getElementById('ticker-text');
function startTicker(){
  showTickerLine();
  setInterval(showTickerLine, 3200);
}
function showTickerLine(){
  tickerEl.style.opacity = 0;
  setTimeout(() => {
    tickerEl.textContent = tickerLines[tIdx % tickerLines.length];
    tickerEl.style.opacity = 1;
    tIdx++;
  }, 250);
}
tickerEl.style.transition = 'opacity .25s';

// Анимация счёта метрик при появлении в зоне видимости
function animateCount(el){
  const raw = el.getAttribute('data-count');
  const match = raw.match(/[\d]+/);
  if(!match){ el.textContent = raw; return; }
  const target = parseInt(match[0], 10);
  const before = raw.slice(0, raw.indexOf(match[0]));
  const after = raw.slice(raw.indexOf(match[0]) + match[0].length);
  let cur = 0;
  const step = Math.max(1, Math.ceil(target / 40));
  const iv = setInterval(() => {
    cur += step;
    if(cur >= target){ cur = target; clearInterval(iv); }
    el.textContent = before + cur + after;
  }, 25);
}
const counters = document.querySelectorAll('.metric .num');
const counterObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if(e.isIntersecting){ animateCount(e.target); counterObs.unobserve(e.target); }
  });
}, {threshold:0.4});
counters.forEach(c => counterObs.observe(c));

// Плавное появление секций при скролле
const sectionObs = new IntersectionObserver((entries) => {
  entries.forEach(e => { if(e.isIntersecting){ e.target.classList.add('visible'); } });
}, {threshold:0.12});
document.querySelectorAll('.section').forEach(s => sectionObs.observe(s));

// Подсветка одинаковых тегов при клике
function highlightTag(el){
  const name = el.textContent;
  document.querySelectorAll('.tag').forEach(t => {
    t.classList.toggle('active', t.textContent === name);
  });
}

// Копирование почты/телефона в буфер обмена
function copyText(value, btn){
  navigator.clipboard?.writeText(value).then(() => {
    const old = btn.textContent;
    btn.textContent = 'скопировано ✓';
    setTimeout(() => { btn.textContent = old; }, 1500);
  });
}

// Кнопка "наверх"
const toTop = document.getElementById('to-top');
window.addEventListener('scroll', () => {
  toTop.classList.toggle('show', window.scrollY > 500);
});
</script>
</body>
</html>
