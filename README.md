# Моделирование уровней секретности и потков между ними

## Описание работы

Лабораторная по дисциплине **"Моделирование безопасности компьютерных систем"**

Тема: **Модель Белла—Лападулы**

Программа, управляет уровнями секретности папок в файловой системе и контролируюет информационные потоки между ними.

Основные функции программы делятся на две части — работа с уровнями секретности и копирование файлов.

Работа с уровнями секретности:
1. Создание (с заданным именем), изменение (имя и секретность) и удаление уровней секретности. Все изменения в уровнях секретности внутри программы должны влиять на папки, которым этим уровни назначены.
2. Могут существовать уровни секретности, которые не установлены ни для одной папки.
3. Создание (с заданным именем), переименование и удаление папок и подпапок внутри заданной корневой папки.
4. Новые папки создаваются с минимальным доступным уровнем секретности.
5. Как следствие, в списке всегда должен быть хотя бы один уровень секретности, который считается минимальным.
6. Выбор уровня секретности для папок и подпапок из нескольких заданных в программе вариантов.

Копирование файлов:
1. Копирование файлов между папками согласно модели Белла — Лападулы. При этом копируются все файлы, лежащие внутри папки.
2. Выбор папок для копирования происходит в интерфейсе программы. При этом должны отображаться только папки, подходящие под выбранный уровень секретности.
3. Предусмотрена работа со вложенностью папок — папки разных уровней секретности могут быть вложенными друг в друга, копирование должно учитывать эту ситуацию.

Оба приложения — оконные, с пользовательским интерфейсом.
