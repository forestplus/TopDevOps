const translations = {
  ru: {
    preview:"TOPDEVOPS V3 · PREVIEW",navAbout:"Обо мне",navEngineering:"Инженерия",navAI:"AI & MLOps",navKnowledge:"База знаний",navContact:"Контакты",resume:"Резюме ↗",
    eyebrow:"ENGINEERING · AUTOMATION · RELIABILITY",heroLine1:"Инфраструктура,",heroLine2:"которая ускоряет бизнес.",heroLead:"Парамонов Дмитрий. DevOps / SRE-инженер и технический руководитель. Проектирую, автоматизирую и развиваю надёжные платформы — от CI/CD до Kubernetes и AI-инфраструктуры.",explore:"Смотреть инженерные проекты",downloadCV:"Скачать CV",openTo:"Открыт к интересным инженерным задачам",scroll:"ПРОКРУТИТЕ, ЧТОБЫ ИССЛЕДОВАТЬ",
    profileKicker:"ОТ СИСТЕМНОГО АДМИНИСТРИРОВАНИЯ ДО PLATFORM ENGINEERING",profileTitle:"Соединяю инженерную глубину, автоматизацию и системное мышление.",profileText:"Мой профессиональный путь охватывает системное администрирование, построение инфраструктуры, DevOps/SRE-практики и техническое управление. В фокусе — Kubernetes, контейнеризация, CI/CD, автоматизация, наблюдаемость, безопасность и применение AI для инженерных задач.",fullProfile:"Полный профиль и опыт",
    capKicker:"ОТ АРХИТЕКТУРЫ ДО ЭКСПЛУАТАЦИИ",capTitle:"Инженерные направления",capNote:"Практические лаборатории, архитектурные решения и кейсы. Разделы будут наполняться проверяемыми примерами и документацией.",k8sDesc:"Оркестрация, Helm, OpenShift, сетевые модели, эксплуатация и troubleshooting.",cicdDesc:"Поставка изменений, pipeline design, GitOps-подходы и автоматизация релизов.",obsDesc:"Метрики, логи, алертинг, доступность сервисов и инженерия надёжности.",secDesc:"Встраивание проверок безопасности в жизненный цикл разработки и поставки.",existingMaterials:"Материалы сайта",inProgress:"В разработке",
    aiTitle:"AI — это тоже инженерная система.",aiText:"От экспериментов и управления моделями до serving, наблюдаемости и локального inference. Здесь собирается практический MLOps-стенд с понятной архитектурой и воспроизводимыми шагами.",exploreAI:"Исследовать AI & MLOps ↗",
    kbKicker:"ЗАМЕТКИ, ИНСТРУКЦИИ, ШПАРГАЛКИ",kbTitle:"Знания, которые можно применить.",allArticles:"Все материалы",linuxText:"Команды, диагностика, процессы, сеть и повседневная эксплуатация.",dockerText:"Образы, контейнеры, Dockerfile и практики сборки.",gitText:"Ветвление, история, удалённые репозитории и рабочие приёмы.",pgText:"База данных, эксплуатация и практические руководства.",
    contactKicker:"LET'S BUILD SOMETHING RELIABLE",contactTitle:"Есть сложная инфраструктурная задача?",contactText:"Открыт к профессиональному диалогу, инженерным вызовам и обмену опытом.",footer:"Инженерия без лишнего шума.",backTop:"Наверх ↑",
    aiPageIntro:"Практическая лаборатория: от первого эксперимента до воспроизводимого развёртывания ML-модели.",
    aiStatus:"ТЕКУЩИЙ СТАТУС · LAB IN PROGRESS",aiArchitecture:"АРХИТЕКТУРА ЛАБОРАТОРИИ",
    aiTracking:"Эксперименты, параметры и метрики",aiDatabase:"Метаданные, runs и Model Registry",aiArtifacts:"Файлы моделей и результаты обучения",
    aiStepTitle:"Первый стенд: MLflow + PostgreSQL + локальные артефакты",
    aiStepText:"MLflow Tracking Server использует PostgreSQL как backend store. Файлы моделей хранятся на локальном диске, подключённом к контейнеру через bind mount. Клиент обращается к серверу по HTTP; сервер проксирует операции с артефактами.",
    aiPrereq:"Что понадобится",aiPrereqText:"Windows 11, Docker Desktop с Docker Compose, Python 3.11+ и PowerShell.",
    aiRunTitle:"Запуск инфраструктуры",aiRunText:"Создай каталог проекта, добавь Dockerfile и docker-compose.yml, затем собери и запусти сервисы.",
    aiVerifyTitle:"Проверка результата",aiVerifyText:"Открой MLflow UI, запусти train.py и проверь Experiment, Run, Parameters, Metrics и Artifacts.",
    aiNextTitle:"Следующие инженерные этапы",aiNext1:"Model Registry и управление версиями",aiNext2:"Автоматизация обучения через CI/CD",aiNext3:"Контейнеризация Model Serving",aiNext4:"Развёртывание в Kubernetes и observability",
    aiGuideNote:"Это учебная лаборатория, а не заявление о production-внедрении. Материалы будут дополняться по мере проверки каждого этапа."
  },
  en: {
    preview:"TOPDEVOPS V3 · PREVIEW",navAbout:"About",navEngineering:"Engineering",navAI:"AI & MLOps",navKnowledge:"Knowledge",navContact:"Contact",resume:"Resume ↗",
    eyebrow:"ENGINEERING · AUTOMATION · RELIABILITY",heroLine1:"Infrastructure",heroLine2:"that moves business forward.",heroLead:"Dmitry Paramonov. DevOps / SRE engineer and technology leader. I design, automate and evolve reliable platforms — from CI/CD to Kubernetes and AI infrastructure.",explore:"Explore engineering work",downloadCV:"Download CV",openTo:"Open to challenging engineering opportunities",scroll:"SCROLL TO EXPLORE",
    profileKicker:"FROM SYSTEM ADMINISTRATION TO PLATFORM ENGINEERING",profileTitle:"Combining engineering depth, automation and systems thinking.",profileText:"My professional journey spans system administration, infrastructure engineering, DevOps/SRE practices and technology leadership. My focus areas include Kubernetes, containers, CI/CD, automation, observability, security and applying AI to engineering workflows.",fullProfile:"Full profile & experience",
    capKicker:"FROM ARCHITECTURE TO OPERATIONS",capTitle:"Engineering domains",capNote:"Hands-on labs, architecture decisions and case studies. Sections will grow with verifiable examples and practical documentation.",k8sDesc:"Orchestration, Helm, OpenShift, networking, operations and troubleshooting.",cicdDesc:"Software delivery, pipeline design, GitOps practices and release automation.",obsDesc:"Metrics, logs, alerting, service availability and reliability engineering.",secDesc:"Embedding security controls into the software development and delivery lifecycle.",existingMaterials:"Existing resources",inProgress:"In progress",
    aiTitle:"AI is an engineering system, too.",aiText:"From experimentation and model management to serving, observability and local inference. This area documents a practical MLOps lab with clear architecture and reproducible steps.",exploreAI:"Explore AI & MLOps ↗",
    kbKicker:"NOTES, GUIDES & CHEAT SHEETS",kbTitle:"Knowledge you can put to work.",allArticles:"Browse all resources",linuxText:"Commands, diagnostics, processes, networking and everyday operations.",dockerText:"Images, containers, Dockerfiles and build practices.",gitText:"Branching, history, remotes and practical workflows.",pgText:"Database operations and practical PostgreSQL guides.",
    contactKicker:"LET'S BUILD SOMETHING RELIABLE",contactTitle:"Have a challenging infrastructure problem?",contactText:"Open to professional conversations, engineering challenges and sharing experience.",footer:"Engineering without unnecessary noise.",backTop:"Back to top ↑",
    aiPageIntro:"A hands-on lab covering the path from the first experiment to a reproducible ML model deployment.",
    aiStatus:"CURRENT STATUS · LAB IN PROGRESS",aiArchitecture:"LAB ARCHITECTURE",
    aiTracking:"Experiments, parameters and metrics",aiDatabase:"Metadata, runs and Model Registry",aiArtifacts:"Model files and training outputs",
    aiStepTitle:"First stack: MLflow + PostgreSQL + local artifacts",
    aiStepText:"The MLflow Tracking Server uses PostgreSQL as its backend store. Model files are stored on local disk mounted into the container. The client talks to the server over HTTP; the server proxies artifact operations.",
    aiPrereq:"Prerequisites",aiPrereqText:"Windows 11, Docker Desktop with Docker Compose, Python 3.11+ and PowerShell.",
    aiRunTitle:"Start the infrastructure",aiRunText:"Create the project directory, add Dockerfile and docker-compose.yml, then build and start the services.",
    aiVerifyTitle:"Verify the result",aiVerifyText:"Open the MLflow UI, run train.py and inspect the Experiment, Run, Parameters, Metrics and Artifacts.",
    aiNextTitle:"Next engineering steps",aiNext1:"Model Registry and version management",aiNext2:"Automated training with CI/CD",aiNext3:"Containerized Model Serving",aiNext4:"Kubernetes deployment and observability",
    aiGuideNote:"This is a learning lab, not a claim of production deployment. The material will expand as each step is verified."
  }
};
let currentLang = localStorage.getItem("topdevops-v3-lang") || "ru";
function applyLanguage(lang) {
  currentLang = lang;
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach(node => {
    const key = node.dataset.i18n;
    if (translations[lang][key]) node.textContent = translations[lang][key];
  });
  const switcher = document.querySelector("[data-lang-switch]");
  if (switcher) switcher.textContent = lang === "ru" ? "EN" : "RU";
  localStorage.setItem("topdevops-v3-lang", lang);
}
document.addEventListener("DOMContentLoaded", () => {
  const ambient = document.createElement("div");
  ambient.className = "ambient-layer";
  ambient.setAttribute("aria-hidden", "true");
  ambient.innerHTML = '<canvas id="ambient-particles"></canvas><span class="ambient-orb ambient-orb--cyan"></span><span class="ambient-orb ambient-orb--blue"></span><span class="ambient-orb ambient-orb--purple"></span><span class="ambient-orb ambient-orb--mint"></span>';
  document.body.prepend(ambient);
  initAmbientParticles();
  applyLanguage(currentLang);
  document.querySelector("[data-lang-switch]")?.addEventListener("click", () => applyLanguage(currentLang === "ru" ? "en" : "ru"));
  const year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();
});

function initAmbientParticles() {
  const canvas = document.getElementById("ambient-particles");
  if (!canvas) return;
  const ctx = canvas.getContext("2d", { alpha: true });
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const coarsePointer = window.matchMedia("(pointer: coarse)").matches;
  let particles = [], width = 0, height = 0, raf = 0, lastFrame = 0;
  let mouse = { x: -1000, y: -1000 };
  const maxParticles = coarsePointer ? 55 : 125;

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    width = window.innerWidth; height = window.innerHeight;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    canvas.style.width = width + "px"; canvas.style.height = height + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.min(maxParticles, Math.max(35, Math.floor(width * height / 11000)));
    while (particles.length < count) particles.push({
      x:Math.random()*width,y:Math.random()*height,
      vx:(Math.random()-.5)*.28,vy:(Math.random()-.5)*.28,
      size:Math.random()*1.35+.35,alpha:Math.random()*.35+.12
    });
    particles.length = count;
  }
  function frame(timestamp) {
    if (timestamp - lastFrame < 32) { raf = requestAnimationFrame(frame); return; }
    lastFrame = timestamp;
    ctx.clearRect(0,0,width,height);
    for (let i=0;i<particles.length;i++) {
      const p=particles[i]; p.x+=p.vx; p.y+=p.vy;
      if(p.x<0||p.x>width)p.vx*=-1;
      if(p.y<0||p.y>height)p.vy*=-1;
      const dx=mouse.x-p.x,dy=mouse.y-p.y,dist=Math.hypot(dx,dy);
      if(!coarsePointer&&dist<125){p.vx-=dx*.00012;p.vy-=dy*.00012;}
      p.vx=Math.max(-.42,Math.min(.42,p.vx));p.vy=Math.max(-.42,Math.min(.42,p.vy));
      ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);
      ctx.fillStyle="rgba(98,229,208,"+p.alpha+")";ctx.fill();
      for(let j=i+1;j<particles.length;j++){
        const q=particles[j],d=Math.hypot(p.x-q.x,p.y-q.y);
        if(d<125){ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);
          ctx.strokeStyle="rgba(101,169,255,"+(0.075*(1-d/125))+")";ctx.lineWidth=.55;ctx.stroke();}
      }
    }
    raf=requestAnimationFrame(frame);
  }
  function stop(){if(raf)cancelAnimationFrame(raf);raf=0;}
  function start(){if(reduceMotion||document.hidden||raf)return;raf=requestAnimationFrame(frame);}
  resize();window.addEventListener("resize",resize,{passive:true});
  if(!coarsePointer)window.addEventListener("pointermove",e=>{mouse.x=e.clientX;mouse.y=e.clientY;},{passive:true});
  document.addEventListener("visibilitychange",()=>document.hidden?stop():start());
  if(!reduceMotion)start();
}
