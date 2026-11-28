#!/usr/bin/env python3
"""Full resumes from HH.ru — RU/EN, photo, no phone."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY

pdfmetrics.registerFont(TTFont("D","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DB","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
C,Dk,M,T,L = HexColor("#0a8fad"),HexColor("#1a1a22"),HexColor("#5a5a6a"),HexColor("#22222a"),HexColor("#d8dde6")

def photo():
    for p in ["photo-resume.jpg","photo-avatar-240.png"]+list(map(str,Path(".").glob("IMG_*.*"))):
        if Path(p).exists(): return p
    return None

def S():
    def p(n,fn,sz,c,ld,sa=0,**k):
        return ParagraphStyle(n,fontName=fn,fontSize=sz,textColor=c,leading=ld,spaceAfter=sa,**k)
    return dict(name=p("n","DB",15,Dk,18,1), role=p("r","DB",10.5,C,13,3), meta=p("m","D",8,M,10.5,0.5),
        h2=p("h","DB",10,C,12,2,spaceBefore=8), jt=p("jt","DB",9,T,11,0.5), jm=p("jm","D",7.6,M,9.5,1.5),
        body=p("b","D",8,T,10.5,1.5,alignment=TA_JUSTIFY), bl=p("bl","D",7.8,T,10.2,0.8,leftIndent=4),
        sm=p("sm","D",7.6,T,9.8,1))

def hdr(s,ph,name,role,ct,loc):
    img=RLImage(ph,width=26*mm,height=26*mm) if ph else Spacer(26*mm,26*mm)
    t=Table([[img,[Paragraph(name,s["name"]),Paragraph(role,s["role"]),Paragraph(ct,s["meta"]),Paragraph(loc,s["meta"])]]],colWidths=[30*mm,148*mm])
    t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"MIDDLE"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(0,0),6),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    return t

def sec(title,s): return [Paragraph(title,s["h2"]),HRFlowable(width="100%",thickness=0.8,color=L,spaceAfter=3)]
def job(title,meta,intro,bullets,s):
    parts=[Paragraph(title,s["jt"]),Paragraph(meta,s["jm"])]
    if intro: parts.append(Paragraph(intro,s["body"]))
    for b in bullets: parts.append(Paragraph("• "+b,s["bl"]))
    return KeepTogether(parts)
def foot(c,d):
    c.saveState(); c.setFont("D",7); c.setFillColor(M); c.drawCentredString(A4[0]/2,8*mm,f"topdevops.pro  ·  page {d.page}"); c.restoreState()

def build(path, lang):
    s,ph=S(),photo()
    doc=SimpleDocTemplate(path,pagesize=A4,leftMargin=13*mm,rightMargin=13*mm,topMargin=10*mm,bottomMargin=14*mm)
    story=[]
    if lang=="ru":
        story+=[hdr(s,ph,"Парамонов Дмитрий Валерьевич","Senior DevOps · DevOps / SRE Team Lead",
            "Telegram: @TopDevOps · paramdim@ya.ru · LinkedIn: /in/topdevops · topdevops.pro",
            "Санкт-Петербург · Россия · Готов к переезду · 42 года"), Spacer(1,3*mm)]
        story+=sec("Желаемая должность",s)
        story.append(Paragraph("Senior DevOps, DevOps / SRE Team Lead · Полная занятость · Удалённо / гибрид / офис<br/>Специализации: DevOps-инженер · Руководитель проектов · Системный администратор · Системный инженер",s["body"]))
        story+=sec("Опыт работы",s)
        jobs=[
         ("DevOps Team Lead","Июнь 2023 — Октябрь 2026 · 3г 5м · NDA (UAE) · CryptoTech / FinTech",
          "Международный криптохолдинг. Управление DevOps, инфраструктурой, архитектурой и стабильностью платформенных сервисов.",
          ["Руководство DevOps-командой, распределение ответственности, развитие специалистов.","Приоритизация инфраструктурных инициатив; архитектура микросервисов и платформ.","CI/CD и автоматизация поставки; контейнерная инфраструктура и эксплуатация.","Мониторинг, incident management, контроль стабильности IT-систем.","Координация DevOps / dev / QA / SRE; подбор и онбординг.","AI-инструменты для инженерии: LLM, AI API, MCP, AI-assisted Engineering."]),
         ("Lead DevOps","Апрель 2021 — Июнь 2023 · 2г 3м · Иннотех · Москва · Банковский сектор (ВТБ)",
          "Проектная деятельность для банковского сектора, включая ВТБ. Развитие DevOps-практик и инфраструктурных решений.",
          ["Координация DevOps- и инфраструктурных задач в банковских IT-проектах.","Kubernetes / OpenShift / Helm; CI/CD на TeamCity.","PostgreSQL, Kafka, Nexus, Bitbucket, VTB.Cloud.","Координация dev / architecture / QA / SRE / ops; согласование с ИБ.","Аудиты, приёмочные испытания; техсобеседования и наставничество."]),
         ("Senior DevOps","Декабрь 2018 — Апрель 2021 · 2г 5м · DELL · Россия",None,
          ["Kubernetes в гибриде Azure + VMware ESXi; CI/CD на Jenkins и GitLab CI.","Автоматизация Ansible; Docker / Docker Compose.","Prometheus / Grafana; NGINX; UrBackup; Jira / Confluence / Bitbucket.","Взаимодействие с командами из США и Индии."]),
         ("Middle DevOps","Февраль — Август 2018 · 7м · FINOM · СПб · FinTech / Crypto",
          "FinTech-компания с финансовыми и криптовалютными сервисами.",
          ["Инфраструктура FinTech-платформы; GitLab CI/CD и Ansible.","Linux, NGINX, Apache; PostgreSQL, MariaDB; Node.js, Vue.js, PHP.","Bash- и Python-скрипты автоматизации."]),
         ("DevOps","Февраль — Август 2017 · 7м · ПрофИТ Солюшенз · СПб",None,
          ["CI/CD Jenkins; Docker / Docker Compose; VMware ESXi.","Nagios / Zabbix; Atlassian; PostgreSQL, MySQL, MariaDB, MS SQL; GLPI."]),
         ("Founder (CEO & CIO)","Март 2016 — Февраль 2017 · 1г · IThelperSPb · СПб",None,
          ["Создание IT-компании; техническая стратегия и архитектура.","Azure и VPS; техподдержка; ITSM/ITIL; мониторинг и backup; проекты с заказчиками."]),
         ("Старший системный администратор","Декабрь 2014 — Март 2016 · 1г 4м · ОВК · Москва",None,
          ["Корпоративная IT-инфраструктура; AD / GPO; VMware; GLPI.","Nagios / Zabbix / Cacti; Squid, Openfire, ONLYOFFICE, Odoo."]),
         ("Co-Founder (CEO & CIO)","Январь 2012 — Декабрь 2014 · 3г · Микрозаймфинанс · Москва · МФО",
          "Микрофинансовая организация.",
          ["Создание компании и IT-инфраструктуры; серверы и БД; CRM.","Автоматизация бизнес-процессов; внутренние ИС и аналитика."]),
         ("Главный системный администратор","Январь — Декабрь 2011 · 1г · Т-Банк · Москва",
          "Масштаб: 250+ серверов, 1200+ пользователей, 4 ЦОД, команда 6 человек.",
          ["Координация команды системных администраторов.","Эксплуатация серверной инфраструктуры; IT-сервисы для 1200+ пользователей.","Взаимодействие с 4 дата-центрами; контроль эксплуатационных задач."]),
         ("Заместитель директора департамента ИТ","Февраль 2008 — Январь 2011 · 3г · ЛЕКСПРО · Москва",
          "Масштаб: ~40 серверов, 500 пользователей, 6 офисов, команда ~12.",
          ["Управление IT-департаментом; инфраструктура сети офисов.","Hyper-V; хранение данных и backup; непрерывность 24/7."]),
        ]
        for t,m,i,b in jobs:
            story.append(job(t,m,i,b,s)); story.append(Spacer(1,1.5*mm))
        story+=sec("Образование",s)
        story.append(Paragraph("<b>2006 — Высшее</b> · СПбГУАП · Вычислительные машины, системы и сети · инженер-программист",s["body"]))
        story+=sec("Навыки",s)
        story.append(Paragraph("<b>Leadership:</b> DevOps Team Leadership · Engineering Management · Hiring<br/><b>Platform:</b> Kubernetes · OpenShift · Docker · Helm<br/><b>CI/CD:</b> Jenkins · GitLab CI · TeamCity · Ansible · Git<br/><b>Observability:</b> Prometheus · Grafana · Zabbix · ELK · ITIL<br/><b>Data:</b> PostgreSQL · Kafka · MariaDB<br/><b>Cloud:</b> AWS · Azure · GCP · Yandex · VTB.Cloud<br/><b>AI:</b> LLM / MCP · FastAPI · Prompt Engineering<br/><b>Domains:</b> FinTech · Banking IT · CryptoTech<br/><b>Языки:</b> Русский — родной · Английский — C1",s["sm"]))
        story+=sec("Рекомендации",s)
        story.append(Paragraph("ПрофИТ Солюшенз — Сергей Мазиев (IT Director) · Finom — Екатерина Артемьева (HR Director)",s["body"]))
        story+=sec("Обо мне",s)
        story.append(Paragraph("DevOps Team Lead с 20+ лет в IT: финансы, банки, FinTech, CryptoTech. Управление командами, платформенная архитектура, CI/CD, контейнеризация, надёжность критичных систем. Опыт с ВТБ, Т-Банком. AI для инженерии: LLM, MCP, Claude/Codex/Qwen/Grok/Kimi/DeepSeek.",s["body"]))
    else:
        story+=[hdr(s,ph,"Dmitry Valerievich Paramonov","Senior DevOps · DevOps / SRE Team Lead",
            "Telegram: @TopDevOps · paramdim@ya.ru · LinkedIn: /in/topdevops · topdevops.pro",
            "Saint Petersburg · Russia · Open to relocation · Age 42"), Spacer(1,3*mm)]
        story+=sec("Desired Position",s)
        story.append(Paragraph("Senior DevOps, DevOps / SRE Team Lead · Full-time · Remote / hybrid / on-site<br/>Specializations: DevOps Engineer · Project Manager · System Administrator · Systems Engineer",s["body"]))
        story+=sec("Work Experience",s)
        jobs=[
         ("DevOps Team Lead","Jun 2023 — Oct 2026 · 3y 5m · NDA (UAE) · CryptoTech / FinTech",
          "International crypto holding. Managing DevOps, infrastructure, architecture, and platform stability.",
          ["Leading the DevOps team, ownership model, engineer development.","Infrastructure priorities; microservice and platform architecture.","CI/CD and delivery automation; container infrastructure and operations.","Monitoring, incident management, IT stability control.","Cross-team coordination; hiring and onboarding.","AI tooling for engineering: LLM, AI API, MCP, AI-assisted Engineering."]),
         ("Lead DevOps","Apr 2021 — Jun 2023 · 2y 3m · Innotech · Moscow · Banking (VTB)",
          "Project work for banking, including VTB. DevOps practices and infrastructure solutions.",
          ["Coordinating DevOps and infrastructure tasks in banking IT projects.","Kubernetes / OpenShift / Helm; CI/CD with TeamCity.","PostgreSQL, Kafka, Nexus, Bitbucket, VTB.Cloud.","Coordination of dev / architecture / QA / SRE / ops; InfoSec alignment.","Audits, acceptance testing; technical interviews and mentoring."]),
         ("Senior DevOps","Dec 2018 — Apr 2021 · 2y 5m · DELL · Russia",None,
          ["Kubernetes on Azure + VMware ESXi; CI/CD on Jenkins and GitLab CI.","Ansible automation; Docker / Docker Compose.","Prometheus / Grafana; NGINX; UrBackup; Jira / Confluence / Bitbucket.","Collaboration with US and India engineering teams."]),
         ("Middle DevOps","Feb — Aug 2018 · 7m · FINOM · SPb · FinTech / Crypto",
          "FinTech company with financial and cryptocurrency services.",
          ["FinTech platform infrastructure; GitLab CI/CD and Ansible.","Linux, NGINX, Apache; PostgreSQL, MariaDB; Node.js, Vue.js, PHP.","Bash and Python automation scripts."]),
         ("DevOps","Feb — Aug 2017 · 7m · ProfIT Solutions · SPb",None,
          ["Jenkins CI/CD; Docker / Docker Compose; VMware ESXi.","Nagios / Zabbix; Atlassian; PostgreSQL, MySQL, MariaDB, MS SQL; GLPI."]),
         ("Founder (CEO & CIO)","Mar 2016 — Feb 2017 · 1y · IThelperSPb · SPb",None,
          ["Founding an IT company; technical strategy and architecture.","Azure and VPS; support processes; ITSM/ITIL; monitoring and backup."]),
         ("Senior Systems Administrator","Dec 2014 — Mar 2016 · 1y 4m · United Wagon Company · Moscow",None,
          ["Corporate IT infrastructure; AD / GPO; VMware; GLPI.","Nagios / Zabbix / Cacti; Squid, Openfire, ONLYOFFICE, Odoo."]),
         ("Co-Founder (CEO & CIO)","Jan 2012 — Dec 2014 · 3y · Microzaimfinance · Moscow · Microfinance",
          "Microfinance organization.",
          ["Company creation and IT infrastructure; servers and DBs; CRM.","Business process automation; internal systems and analytics."]),
         ("Head of Systems Administration","Jan — Dec 2011 · 1y · T-Bank · Moscow",
          "Scale: 250+ servers, 1200+ users, 4 DCs, team of 6.",
          ["Coordinating the systems administration team.","Server infrastructure operations; IT services for 1200+ users.","Four data centers; operational task control."]),
         ("Deputy IT Department Director","Feb 2008 — Jan 2011 · 3y · LEXPRO · Moscow",
          "Scale: ~40 servers, 500 users, 6 offices, team ~12.",
          ["IT department management; distributed office infrastructure.","Hyper-V; data storage and backup; 24/7 continuity."]),
        ]
        for t,m,i,b in jobs:
            story.append(job(t,m,i,b,s)); story.append(Spacer(1,1.5*mm))
        story+=sec("Education",s)
        story.append(Paragraph("<b>2006 — Higher education</b> · SUAI, Saint Petersburg · Computers, systems and networks · Software Engineer",s["body"]))
        story+=sec("Skills",s)
        story.append(Paragraph("<b>Leadership:</b> DevOps Team Leadership · Engineering Management · Hiring<br/><b>Platform:</b> Kubernetes · OpenShift · Docker · Helm<br/><b>CI/CD:</b> Jenkins · GitLab CI · TeamCity · Ansible · Git<br/><b>Observability:</b> Prometheus · Grafana · Zabbix · ELK · ITIL<br/><b>Data:</b> PostgreSQL · Kafka · MariaDB<br/><b>Cloud:</b> AWS · Azure · GCP · Yandex · VTB.Cloud<br/><b>AI:</b> LLM / MCP · FastAPI · Prompt Engineering<br/><b>Domains:</b> FinTech · Banking IT · CryptoTech<br/><b>Languages:</b> Russian — native · English — C1",s["sm"]))
        story+=sec("References",s)
        story.append(Paragraph("ProfIT Solutions — Sergey Maziev (IT Director) · Finom — Ekaterina Artemyeva (HR Director)",s["body"]))
        story+=sec("About",s)
        story.append(Paragraph("DevOps Team Lead with 20+ years in IT: finance, banking, FinTech, CryptoTech. Leading teams, platform architecture, CI/CD, containers, reliability of critical systems. Experience with VTB, T-Bank. AI for engineering: LLM, MCP, Claude/Codex/Qwen/Grok/Kimi/DeepSeek.",s["body"]))
    doc.build(story,onFirstPage=foot,onLaterPages=foot)
    print(path, Path(path).stat().st_size)

if __name__=="__main__":
    build("resume.pdf","ru")
    build("resume_en.pdf","en")
