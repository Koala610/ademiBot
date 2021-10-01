--
-- Файл сгенерирован с помощью SQLiteStudio v3.3.2 в Пт окт 1 23:48:54 2021
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: admins
CREATE TABLE admins (id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id VARCHAR);
INSERT INTO admins (id, tg_id) VALUES (0, '335271283');
INSERT INTO admins (id, tg_id) VALUES (1, '907390694');

-- Таблица: businesses
CREATE TABLE businesses (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, address VARCHAR, email VARCHAR, website VARCHAR);
INSERT INTO businesses (id, name, address, email, website) VALUES (0, 'Кабачок1', 'Кунаева, 19', 'cum@mail.com', '1.ru');
INSERT INTO businesses (id, name, address, email, website) VALUES (1, 'Шашлычок1', 'Ливаева, 1', '1@mail.com', '2.ru');
INSERT INTO businesses (id, name, address, email, website) VALUES (2, 'Gym', 'Ленина,202', '212@gmail.com', '10.ru');

-- Таблица: models
CREATE TABLE models (id INTEGER PRIMARY KEY AUTOINCREMENT, login VARCHAR UNIQUE, password VARCHAR, offers_used VARCHAR, type VARCHAR, offers_taken VARCHAR, tg_id VARCHAR, is_new BOOLEAN DEFAULT (1), offers_in_process VARCHAR, name VARCHAR, surname VARCHAR, birth_date DATE, isMale BOOLEAN);
INSERT INTO models (id, login, password, offers_used, type, offers_taken, tg_id, is_new, offers_in_process, name, surname, birth_date, isMale) VALUES (0, 'Koala610', '123456', NULL, 'ig', '1,', '335271283', 0, NULL, 'Владлен', 'Ли', '10/10/2000', 1);
INSERT INTO models (id, login, password, offers_used, type, offers_taken, tg_id, is_new, offers_in_process, name, surname, birth_date, isMale) VALUES (1, 'Person', '123', NULL, NULL, '', '', 1, NULL, 'Человек', 'Человек', NULL, NULL);
INSERT INTO models (id, login, password, offers_used, type, offers_taken, tg_id, is_new, offers_in_process, name, surname, birth_date, isMale) VALUES (2, 'GodFather', 'Father', NULL, 'tt', '2,3,0,1,', '907390694', 0, NULL, 'You father', 'Менлибаев', '6/10/2000', 1);

-- Таблица: notifications
CREATE TABLE notifications (id INTEGER PRIMARY KEY AUTOINCREMENT, new_offers VARCHAR, category VARCHAR);

-- Таблица: offers
CREATE TABLE offers (id INTEGER PRIMARY KEY AUTOINCREMENT, theme VARCHAR, text VARCHAR, category INTEGER, start_date DATE, finish_date DATE, start_time TIME, end_time TIME, bus_id INTEGER REFERENCES businesses (id), views_limit INTEGER DEFAULT (10), views_count INTEGER DEFAULT (0));
INSERT INTO offers (id, theme, text, category, start_date, finish_date, start_time, end_time, bus_id, views_limit, views_count) VALUES (0, 'Беспредельные скидки в Шашлычке', 'Однопроцентная скидка с 8 до 9 часов в понедельник', 1000, '10/10/2000', '10/10/2021', '00:00', '01:00', 1, 10, 9);
INSERT INTO offers (id, theme, text, category, start_date, finish_date, start_time, end_time, bus_id, views_limit, views_count) VALUES (1, 'Платите в 2 раза дороже только сегодня!', 'С 6 до 10 вечера', 1000, '10/09/2000', '20/09/2100', '06:00', '10:00', 1, 10, 7);
INSERT INTO offers (id, theme, text, category, start_date, finish_date, start_time, end_time, bus_id, views_limit, views_count) VALUES (2, 'Бесполезные скидки!', 'Работают на 0 процентов!', 1000, '06/10/2000', '06/10/2021', '00:00', '12:00', 0, 10, 10);
INSERT INTO offers (id, theme, text, category, start_date, finish_date, start_time, end_time, bus_id, views_limit, views_count) VALUES (3, 'Хуета', '123', 1000, '10/10/2000', '10/10/2021', '00:00', '12:00', 0, 10, 6);
INSERT INTO offers (id, theme, text, category, start_date, finish_date, start_time, end_time, bus_id, views_limit, views_count) VALUES (4, 'Качка', 'Стань Boss of the gym за 300 bucks', 2000, '06/10/2000', '06/10/2021', '00:00', '12:00', 2, 10, 5);

-- Таблица: requests
CREATE TABLE requests (id INTEGER PRIMARY KEY AUTOINCREMENT, tg_id INTEGER, login VARCHAR, offer_id INTEGER REFERENCES offers (id), story_link VARCHAR, photo_check_id VARCHAR, trans_photo_id VARCHAR, status INTEGER DEFAULT (0) CHECK (status < 2 AND status > - 2));
INSERT INTO requests (id, tg_id, login, offer_id, story_link, photo_check_id, trans_photo_id, status) VALUES (18, 335271283, 'Koala610', 2, 'instagram.com/p', 'AgACAgIAAxkBAAIV5WFQQ8HtDlyrG-JNGXCEt1LVsOcEAAJMtzEbsFOAShO24JprScGYAQADAgADeQADIQQ', 'AgACAgIAAxkBAAIV42FQQ60RWkbqw2QMvgGhcBbyv_lHAAJAtzEbsFOASmGnVgb1SNslAQADAgADeQADIQQ', 1);
INSERT INTO requests (id, tg_id, login, offer_id, story_link, photo_check_id, trans_photo_id, status) VALUES (19, 335271283, 'Koala610', 0, 'instagram.com/p', 'AgACAgIAAxkBAAIV82FQRHjSxIvRxXEYwT_p7rolbGAiAAJNtzEbsFOASvZNdryRzdz5AQADAgADeQADIQQ', 'AgACAgIAAxkBAAIV8WFQRHFm9acJSC5livqULUEFolq3AAJAtzEbsFOASmGnVgb1SNslAQADAgADeQADIQQ', -1);
INSERT INTO requests (id, tg_id, login, offer_id, story_link, photo_check_id, trans_photo_id, status) VALUES (20, 907390694, 'GodFather', 4, 'https://www.instagram.com/p/CUaSyzCDhjT/?utm_medium=copy_link', 'AgACAgIAAxkBAAIeE2FUm3kskPAlrINj4ZsPg4-LY48SAAKdtzEb1iSoSkmcPLo5ucbvAQADAgADeAADIQQ', 'AgACAgIAAxkBAAIeEWFUm2q-aaZqpEm6bP09i_8CYkXZAALYtTEbBk6YSuWBLV4qqqZLAQADAgADeQADIQQ', 1);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
