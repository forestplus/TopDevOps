# TopDevOps V4 — Preview

Вся разработка V4 изолирована в этой директории. Preview: https://topdevops.pro/v4/

## Принципы
- Production, V3 (/new), старые URL и существующие файлы не изменяются.
- Все страницы V4 используют `noindex,nofollow`; V4 не добавляется в production sitemap.
- Существующие CV, фото и статьи используются по относительным ссылкам, без копирования.
- Не публиковать неподтверждённые метрики, достижения, роли или результаты.
- Визуальная система Aurora Engineering сохраняет фоновую анимацию частиц и связей; reduced-motion отключает её.
- Общие стили и логика находятся в `assets/css/main.css` и `assets/js/main.js`.

## Структура
- `index.html` — главная V4.
- `engineering/` — инженерные направления.
- `projects/` — кейсы и проектный портфель.
- `ai-mlops/` — AI Infrastructure & MLOps Lab.
- `knowledge/` — каталог существующих материалов.
- `resume/` — профиль и карьерная история.

## Этапы
1. Foundation — дизайн-система, навигация, RU/EN, responsive, фон.
2. Professional Identity — расширенный профиль и timeline после получения актуального CV.
3. Engineering Portfolio — реальные кейсы, схемы и проверяемые артефакты.
4. AI/MLOps — MLflow Engineering Lab с Docker Compose и пошаговым HowTo.
5. Knowledge Hub — инвентаризация статей, поиск, теги и связи.
6. QA — маршруты, mobile, доступность, SEO, производительность.

## Release gate
Production не переключать до отдельного явного одобрения владельца сайта.
