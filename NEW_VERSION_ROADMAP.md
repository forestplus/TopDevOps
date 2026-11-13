# TopDevOps V3 — Roadmap

> Статус: **Preview / active development**  
> Production-сайт не изменяется. Вся новая реализация находится в `/new`.

## 1. Цель

Создать двуязычный (RU/EN) инженерный сайт-портфолио, который объединяет профессиональный профиль, Engineering Portfolio, AI/MLOps Lab, базу знаний и интерактивные инструменты.

## 2. Ограничения и правила

- Репозиторий: `forestplus/TopDevOps`, основная ветка: `main`.
- Публикация: существующий рабочий механизм GitHub Pages; изменения попадают на сайт после обычного push в `main`.
- Cloudflare не используется в рамках текущего этапа.
- GitHub Actions не является обязательной частью разработки V3.
- Production-файлы и текущие URL не менять до отдельного согласования.
- Все новые стили, скрипты, изображения и шрифты хранить внутри `new/assets/`.
- Все страницы Preview должны содержать `noindex,nofollow`.
- Не добавлять Preview URL в production sitemap.
- Не публиковать неподтверждённые метрики, достижения, опыт или характеристики проектов.

## 3. Архитектура

```text
new/
├── index.html
├── assets/{css,js,images,fonts,icons}/
├── engineering/
├── ai-mlops/
├── knowledge/
├── playground/
├── projects/
└── resume/
```

На старте используется один общий stylesheet и небольшой JS-модуль для RU/EN-переключения. Разделы создаются постепенно, по мере появления проверенного содержимого.

## 4. Дизайн-направление

- Dark engineering aesthetic: глубокий navy, холодные голубые и cyan-акценты.
- Типографика: Manrope + DM Mono с системными fallback.
- Карточная композиция, тонкие границы, мягкие свечения, технические подписи.
- Адаптивность для desktop, tablet и mobile.
- Доступность: семантические элементы, видимые интерактивные состояния, reduced-motion.
- Preview badge на всех страницах.

## 5. Статус реализации

### Foundation
- [x] Создана изолированная директория `/new`.
- [x] Добавлена адаптивная главная страница RU/EN.
- [x] Добавлены базовые дизайн-токены и компоненты.
- [x] Добавлен переключатель языка с сохранением выбора.
- [x] Добавлена стартовая страница AI & MLOps.
- [x] Созданы каркасы Engineering, Knowledge Base, Playground, Projects и Resume.
- [ ] Проверить Preview в реальном браузере на desktop и mobile.
- [ ] Проверить маршруты и изображения после публикации GitHub Pages.
- [ ] Проверить accessibility, контрастность и консоль браузера.

### Engineering Portfolio
- [ ] Kubernetes Lab: архитектура, manifests, Helm, troubleshooting.
- [ ] CI/CD & GitOps: pipeline patterns и примеры.
- [ ] Observability & SRE: metrics, logs, traces, SLI/SLO.
- [ ] DevSecOps: security gates, SAST/DAST, supply chain.

### AI & MLOps
- [x] Подготовлена стартовая страница раздела.
- [ ] MLflow Tracking + PostgreSQL backend store.
- [ ] Local artifact storage.
- [ ] Model Registry и управление версиями.
- [ ] Model serving и inference.
- [ ] Monitoring и reproducible lab guide.

### Knowledge Base
- [ ] Каталог материалов и категории.
- [ ] Поиск, теги и оглавление статей.
- [ ] Кнопки копирования кода.
- [ ] Дата обновления и связанные материалы.
- [ ] Сохранение существующих URL статей.

### Playground
- [ ] YAML Validator.
- [ ] Cron Expression Builder.
- [ ] CIDR Calculator.
- [ ] Kubernetes Manifest Helper.

### Release
- [ ] Полный аудит ссылок, SEO, доступности и производительности.
- [ ] Сверка RU/EN-контента.
- [ ] Согласование релиза с владельцем сайта.
- [ ] План миграции без потери текущих URL.
- [ ] Переключение production только после явного одобрения.

## 6. Текущий релиз

**V3 Foundation 0.1** — новая главная страница, RU/EN переключатель, базовая дизайн-система, ссылки на существующие разделы сайта и стартовая страница AI & MLOps.

## 7. Примечания

- Фото и CV ссылаются на существующие файлы в корне репозитория, без копирования и изменения оригиналов.
- Содержимое текущей базы знаний переиспользуется через ссылки на существующие каталоги.
- Внешний Google Fonts используется с системными fallback; при необходимости шрифты будут локализованы.
