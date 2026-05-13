# Система управленческой отчётности для группы предприятий "Открытие"

## Первичная постановка задачи
Требуется разработать систему управленческой отчётности для группы предприятий "Открытие".

## Принцип работы с версиями

### Локальные файлы (Markdown)
- Основные файлы: `opening_Business_YYYY_MM_DD.md` и `opening_Reports_YYYY_MM_DD.md`
- Дата в имени файла — дата последнего изменения
- Старые версии перемещаются в `BRD/history/` (папка в `.gitignore`)

### Google Docs (для заказчика)
- Документы в Google Docs — это "публичная" версия для согласования
- Заказчик пишет замечания в Google Docs
- Вы переносите замечания в локальные .md файлы

### GitHub
- В Git коммитятся только актуальные .md файлы (без истории)
- История версий хранится локально в `BRD/history/`

## Цикл редактирования

```
Google Docs (заказчик пишет замечания)
        ↓
Вы копируете замечания → правите .md файлы
        ↓
Коммитите в Git → пушите в GitHub
        ↓
Экспортируете .md → .docx → загружаете в Google Docs
        ↓
Заказчик снова пишет замечания → цикл повторяется
```

## Ссылки проекта

| Документ | Google Docs | Локальный файл |
|---|---|---|
| Описание бизнеса | https://docs.google.com/document/d/1pFtPhzIiRICVLKfWMNwVQ0pG-NptcvcA5umQFmlzpkQ/edit | `BRD/opening_Business_YYYY_MM_DD.md` |
| Список отчётов | https://docs.google.com/document/d/1T6fcswMsTK06jPWgKkhowon3NPqDbaHyApWYxQe-41s/edit | `BRD/opening_Reports_YYYY_MM_DD.md` |
| Ключевые контакты | https://docs.google.com/document/d/1jSXiU_BF9eci5XVUPK4t3P469_8Aznc8sxTpNsGsmtE/edit | — |
