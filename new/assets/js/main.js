const translations = {
  ru: {
    preview:"TOPDEVOPS V3 · PREVIEW",navAbout:"Обо мне",navEngineering:"Инженерия",navAI:"AI & MLOps",navKnowledge:"База знаний",navContact:"Контакты",resume:"Резюме ↗",
    eyebrow:"ENGINEERING · AUTOMATION · RELIABILITY",heroLine1:"Инфраструктура,",heroLine2:"которая ускоряет бизнес.",heroLead:"Парамонов Дмитрий. DevOps / SRE-инженер и технический руководитель. Проектирую, автоматизирую и развиваю надёжные платформы — от CI/CD до Kubernetes и AI-инфраструктуры.",explore:"Смотреть инженерные проекты",downloadCV:"Скачать CV",openTo:"Открыт к интересным инженерным задачам",scroll:"ПРОКРУТИТЕ, ЧТОБЫ ИССЛЕДОВАТЬ",
    profileKicker:"ОТ СИСТЕМНОГО АДМИНИСТРИРОВАНИЯ ДО PLATFORM ENGINEERING",profileTitle:"Соединяю инженерную глубину, автоматизацию и системное мышление.",profileText:"Мой профессиональный путь охватывает системное администрирование, построение инфраструктуры, DevOps/SRE-практики и техническое управление. В фокусе — Kubernetes, контейнеризация, CI/CD, автоматизация, наблюдаемость, безопасность и применение AI для инженерных задач.",fullProfile:"Полный профиль и опыт",
    capKicker:"ОТ АРХИТЕКТУРЫ ДО ЭКСПЛУАТАЦИИ",capTitle:"Инженерные направления",capNote:"Практические лаборатории, архитектурные решения и кейсы. Разделы будут наполняться проверяемыми примерами и документацией.",k8sDesc:"Оркестрация, Helm, OpenShift, сетевые модели, эксплуатация и troubleshooting.",cicdDesc:"Поставка изменений, pipeline design, GitOps-подходы и автоматизация релизов.",obsDesc:"Метрики, логи, алертинг, доступность сервисов и инженерия надёжности.",secDesc:"Встраивание проверок безопасности в жизненный цикл разработки и поставки.",existingMaterials:"Материалы сайта",inProgress:"В разработке",
    aiTitle:"AI — это тоже инженерная система.",aiText:"От экспериментов и управления моделями до serving, наблюдаемости и локального inference. Здесь собирается практический MLOps-стенд с понятной архитектурой и воспроизводимыми шагами.",exploreAI:"Исследовать AI & MLOps ↗",
    kbKicker:"ЗАМЕТКИ, ИНСТРУКЦИИ, ШПАРГАЛКИ",kbTitle:"Знания, которые можно применить.",allArticles:"Все материалы",linuxText:"Команды, диагностика, процессы, сеть и повседневная эксплуатация.",dockerText:"Образы, контейнеры, Dockerfile и практики сборки.",gitText:"Ветвление, история, удалённые репозитории и рабочие приёмы.",pgText:"База данных, эксплуатация и практические руководства.",
    contactKicker:"LET'S BUILD SOMETHING RELIABLE",contactTitle:"Есть сложная инфраструктурная задача?",contactText:"Открыт к профессиональному диалогу, инженерным вызовам и обмену опытом.",footer:"Инженерия без лишнего шума.",backTop:"Наверх ↑"
  },
  en: {
    preview:"TOPDEVOPS V3 · PREVIEW",navAbout:"About",navEngineering:"Engineering",navAI:"AI & MLOps",navKnowledge:"Knowledge",navContact:"Contact",resume:"Resume ↗",
    eyebrow:"ENGINEERING · AUTOMATION · RELIABILITY",heroLine1:"Infrastructure",heroLine2:"that moves business forward.",heroLead:"Dmitry Paramonov. DevOps / SRE engineer and technology leader. I design, automate and evolve reliable platforms — from CI/CD to Kubernetes and AI infrastructure.",explore:"Explore engineering work",downloadCV:"Download CV",openTo:"Open to challenging engineering opportunities",scroll:"SCROLL TO EXPLORE",
    profileKicker:"FROM SYSTEM ADMINISTRATION TO PLATFORM ENGINEERING",profileTitle:"Combining engineering depth, automation and systems thinking.",profileText:"My professional journey spans system administration, infrastructure engineering, DevOps/SRE practices and technology leadership. My focus areas include Kubernetes, containers, CI/CD, automation, observability, security and applying AI to engineering workflows.",fullProfile:"Full profile & experience",
    capKicker:"FROM ARCHITECTURE TO OPERATIONS",capTitle:"Engineering domains",capNote:"Hands-on labs, architecture decisions and case studies. Sections will grow with verifiable examples and practical documentation.",k8sDesc:"Orchestration, Helm, OpenShift, networking, operations and troubleshooting.",cicdDesc:"Software delivery, pipeline design, GitOps practices and release automation.",obsDesc:"Metrics, logs, alerting, service availability and reliability engineering.",secDesc:"Embedding security controls into the software development and delivery lifecycle.",existingMaterials:"Existing resources",inProgress:"In progress",
    aiTitle:"AI is an engineering system, too.",aiText:"From experimentation and model management to serving, observability and local inference. This area documents a practical MLOps lab with clear architecture and reproducible steps.",exploreAI:"Explore AI & MLOps ↗",
    kbKicker:"NOTES, GUIDES & CHEAT SHEETS",kbTitle:"Knowledge you can put to work.",allArticles:"Browse all resources",linuxText:"Commands, diagnostics, processes, networking and everyday operations.",dockerText:"Images, containers, Dockerfiles and build practices.",gitText:"Branching, history, remotes and practical workflows.",pgText:"Database operations and practical PostgreSQL guides.",
    contactKicker:"LET'S BUILD SOMETHING RELIABLE",contactTitle:"Have a challenging infrastructure problem?",contactText:"Open to professional conversations, engineering challenges and sharing experience.",footer:"Engineering without unnecessary noise.",backTop:"Back to top ↑"
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
  applyLanguage(currentLang);
  document.querySelector("[data-lang-switch]")?.addEventListener("click", () => applyLanguage(currentLang === "ru" ? "en" : "ru"));
  const year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();
});