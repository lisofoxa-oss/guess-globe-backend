from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
import hmac
import hashlib
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = "8164563339:AAGz6nMXwaXkBSNdCF0-UwtuBVvZd1-ApLA"

EASY_COUNTRIES = [
    {"id": 1, "name": "США", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/us.png"},
    {"id": 2, "name": "Россия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ru.png"},
    {"id": 3, "name": "Франция", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/fr.png"},
    {"id": 4, "name": "Германия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/de.png"},
    {"id": 5, "name": "Япония", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/jp.png"},
    {"id": 6, "name": "Китай", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/cn.png"},
    {"id": 7, "name": "Бразилия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/br.png"},
    {"id": 8, "name": "Канада", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ca.png"},
    {"id": 9, "name": "Австралия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/au.png"},
    {"id": 10, "name": "Индия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/in.png"},
    {"id": 11, "name": "Италия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/it.png"},
    {"id": 12, "name": "Испания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/es.png"},
    {"id": 13, "name": "Мексика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mx.png"},
    {"id": 14, "name": "Южная Корея", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/kr.png"},
    {"id": 15, "name": "Великобритания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/gb.png"},
    {"id": 16, "name": "Египет", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/eg.png"},
    {"id": 17, "name": "Турция", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/tr.png"},
    {"id": 18, "name": "Нидерланды", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/nl.png"},
    {"id": 19, "name": "Польша", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/pl.png"},
    {"id": 20, "name": "Швеция", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/se.png"},
    {"id": 21, "name": "Швейцария", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ch.png"},
    {"id": 22, "name": "Аргентина", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ar.png"},
    {"id": 23, "name": "Австрия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/at.png"},
    {"id": 24, "name": "Бельгия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/be.png"},
    {"id": 25, "name": "Греция", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/gr.png"},
    {"id": 26, "name": "Индонезия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/id.png"},
    {"id": 27, "name": "Ирландия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ie.png"},
    {"id": 28, "name": "Израиль", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/il.png"},
    {"id": 29, "name": "Норвегия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/no.png"},
    {"id": 30, "name": "Португалия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/pt.png"},
]

MEDIUM_COUNTRIES = [
    {"id": 31, "name": "Чили", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/cl.png"},
    {"id": 32, "name": "Таиланд", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/th.png"},
    {"id": 33, "name": "Финляндия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/fi.png"},
    {"id": 34, "name": "Дания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/dk.png"},
    {"id": 35, "name": "Украина", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ua.png"},
    {"id": 36, "name": "Чехия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/cz.png"},
    {"id": 37, "name": "Венгрия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/hu.png"},
    {"id": 38, "name": "Румыния", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ro.png"},
    {"id": 39, "name": "Болгария", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bg.png"},
    {"id": 40, "name": "Сербия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/rs.png"},
    {"id": 41, "name": "Хорватия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/hr.png"},
    {"id": 42, "name": "Словакия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sk.png"},
    {"id": 43, "name": "Словения", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/si.png"},
    {"id": 44, "name": "Латвия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/lv.png"},
    {"id": 45, "name": "Литва", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/lt.png"},
    {"id": 46, "name": "Эстония", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ee.png"},
    {"id": 47, "name": "Исландия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/is.png"},
    {"id": 48, "name": "Казахстан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/kz.png"},
    {"id": 49, "name": "Узбекистан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/uz.png"},
    {"id": 50, "name": "Колумбия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/co.png"},
    {"id": 51, "name": "Перу", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/pe.png"},
    {"id": 52, "name": "Венесуэла", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ve.png"},
    {"id": 53, "name": "Куба", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/cu.png"},
    {"id": 54, "name": "ЮАР", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/za.png"},
    {"id": 55, "name": "Малайзия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/my.png"},
    {"id": 56, "name": "Сингапур", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sg.png"},
    {"id": 57, "name": "Филиппины", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ph.png"},
    {"id": 58, "name": "Пакистан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/pk.png"},
    {"id": 59, "name": "Бангладеш", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bd.png"},
    {"id": 60, "name": "Ирак", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/iq.png"},
    {"id": 61, "name": "Иран", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ir.png"},
    {"id": 62, "name": "Саудовская Аравия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sa.png"},
    {"id": 63, "name": "ОАЭ", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ae.png"},
    {"id": 64, "name": "Катар", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/qa.png"},
    {"id": 65, "name": "Кувейт", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/kw.png"},
    {"id": 66, "name": "Новая Зеландия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/nz.png"},
    {"id": 67, "name": "Кипр", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/cy.png"},
    {"id": 68, "name": "Мальта", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mt.png"},
    {"id": 69, "name": "Люксембург", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/lu.png"},
    {"id": 70, "name": "Монако", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mc.png"},
    {"id": 71, "name": "Лихтенштейн", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/li.png"},
    {"id": 72, "name": "Андорра", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ad.png"},
    {"id": 73, "name": "Сан-Марино", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sm.png"},
    {"id": 74, "name": "Ватикан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/va.png"},
    {"id": 75, "name": "Албания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/al.png"},
    {"id": 76, "name": "Босния и Герцеговина", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ba.png"},
    {"id": 77, "name": "Северная Македония", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mk.png"},
    {"id": 78, "name": "Черногория", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/me.png"},
    {"id": 79, "name": "Молдова", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/md.png"},
    {"id": 80, "name": "Грузия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ge.png"},
    {"id": 81, "name": "Армения", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/am.png"},
    {"id": 82, "name": "Азербайджан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/az.png"},
    {"id": 83, "name": "Тунис", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/tn.png"},
    {"id": 84, "name": "Марокко", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ma.png"},
    {"id": 85, "name": "Алжир", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/dz.png"},
    {"id": 86, "name": "Нигерия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ng.png"},
    {"id": 87, "name": "Кения", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ke.png"},
    {"id": 88, "name": "Гана", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/gh.png"},
    {"id": 89, "name": "Сенегал", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sn.png"},
    {"id": 90, "name": "Камерун", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/cm.png"},
    {"id": 91, "name": "Конго", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/cg.png"},
    {"id": 92, "name": "Танзания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/tz.png"},
    {"id": 93, "name": "Уганда", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ug.png"},
    {"id": 94, "name": "Замбия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/zm.png"},
    {"id": 95, "name": "Зимбабве", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/zw.png"},
    {"id": 96, "name": "Мозамбик", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mz.png"},
    {"id": 97, "name": "Ангола", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ao.png"},
    {"id": 98, "name": "Эфиопия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/et.png"},
    {"id": 99, "name": "Судан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sd.png"},
    {"id": 100, "name": "Ливия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ly.png"},
]

HARD_COUNTRIES = [
    {"id": 101, "name": "Бутан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bt.png"},
    {"id": 102, "name": "Суринам", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sr.png"},
    {"id": 103, "name": "Того", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/tg.png"},
    {"id": 104, "name": "Бенин", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bj.png"},
    {"id": 105, "name": "Буркина-Фасо", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bf.png"},
    {"id": 106, "name": "Гвинея", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/gn.png"},
    {"id": 107, "name": "Гвинея-Бисау", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/gw.png"},
    {"id": 108, "name": "Либерия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/lr.png"},
    {"id": 109, "name": "Сьерра-Леоне", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sl.png"},
    {"id": 110, "name": "Мали", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ml.png"},
    {"id": 111, "name": "Нигер", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ne.png"},
    {"id": 112, "name": "Чад", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/td.png"},
    {"id": 113, "name": "Центральноафриканская Республика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/cf.png"},
    {"id": 114, "name": "Габон", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ga.png"},
    {"id": 115, "name": "Кабо-Верде", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/cv.png"},
    {"id": 116, "name": "Сан-Томе и Принсипи", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/st.png"},
    {"id": 117, "name": "Экваториальная Гвинея", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/gq.png"},
    {"id": 118, "name": "Коморы", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/km.png"},
    {"id": 119, "name": "Сейшелы", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sc.png"},
    {"id": 120, "name": "Маврикий", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mu.png"},
    {"id": 121, "name": "Мадагаскар", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mg.png"},
    {"id": 122, "name": "Малави", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mw.png"},
    {"id": 123, "name": "Лесото", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ls.png"},
    {"id": 124, "name": "Эсватини", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sz.png"},
    {"id": 125, "name": "Ботсвана", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bw.png"},
    {"id": 126, "name": "Намибия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/na.png"},
    {"id": 127, "name": "Южный Судан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ss.png"},
    {"id": 128, "name": "Эритрея", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/er.png"},
    {"id": 129, "name": "Джибути", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/dj.png"},
    {"id": 130, "name": "Сомали", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/so.png"},
    {"id": 131, "name": "Йемен", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ye.png"},
    {"id": 132, "name": "Оман", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/om.png"},
    {"id": 133, "name": "Бахрейн", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bh.png"},
    {"id": 134, "name": "Иордания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/jo.png"},
    {"id": 135, "name": "Ливан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/lb.png"},
    {"id": 136, "name": "Сирия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sy.png"},
    {"id": 137, "name": "Монголия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mn.png"},
    {"id": 138, "name": "Вьетнам", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/vn.png"},
    {"id": 139, "name": "Лаос", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/la.png"},
    {"id": 140, "name": "Камбоджа", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/kh.png"},
    {"id": 141, "name": "Мьянма", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mm.png"},
    {"id": 142, "name": "Непал", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/np.png"},
    {"id": 143, "name": "Шри-Ланка", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/lk.png"},
    {"id": 144, "name": "Мальдивы", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mv.png"},
    {"id": 145, "name": "Бруней", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bn.png"},
    {"id": 146, "name": "Восточный Тимор", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/tl.png"},
    {"id": 147, "name": "Папуа – Новая Гвинея", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/pg.png"},
    {"id": 148, "name": "Соломоновы Острова", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sb.png"},
    {"id": 149, "name": "Вануату", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/vu.png"},
    {"id": 150, "name": "Фиджи", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/fj.png"},
    {"id": 151, "name": "Кирибати", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ki.png"},
    {"id": 152, "name": "Науру", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/nr.png"},
    {"id": 153, "name": "Тувалу", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/tv.png"},
    {"id": 154, "name": "Маршалловы Острова", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mh.png"},
    {"id": 155, "name": "Микронезия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/fm.png"},
    {"id": 156, "name": "Палау", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/pw.png"},
    {"id": 157, "name": "Сент-Китс и Невис", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/kn.png"},
    {"id": 158, "name": "Сент-Люсия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/lc.png"},
    {"id": 159, "name": "Сент-Винсент и Гренадины", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/vc.png"},
    {"id": 160, "name": "Гренада", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/gd.png"},
    {"id": 161, "name": "Барбадос", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bb.png"},
    {"id": 162, "name": "Тринидад и Тобаго", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/tt.png"},
    {"id": 163, "name": "Доминика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/dm.png"},
    {"id": 164, "name": "Доминиканская Республика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/do.png"},
    {"id": 165, "name": "Гаити", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ht.png"},
    {"id": 166, "name": "Ямайка", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/jm.png"},
    {"id": 167, "name": "Багамы", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bs.png"},
    {"id": 168, "name": "Белиз", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bz.png"},
    {"id": 169, "name": "Гондурас", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/hn.png"},
    {"id": 170, "name": "Сальвадор", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sv.png"},
    {"id": 171, "name": "Никарагуа", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ni.png"},
    {"id": 172, "name": "Коста-Рика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/cr.png"},
    {"id": 173, "name": "Панама", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/pa.png"},
    {"id": 174, "name": "Эквадор", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ec.png"},
    {"id": 175, "name": "Колумбия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/co.png"},
    {"id": 176, "name": "Венесуэла", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ve.png"},
    {"id": 177, "name": "Гайана", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/gy.png"},
    {"id": 178, "name": "Суринам", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/sr.png"},
    {"id": 179, "name": "Уругвай", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/uy.png"},
    {"id": 180, "name": "Парагвай", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/py.png"},
    {"id": 181, "name": "Боливия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/bo.png"},
    {"id": 182, "name": "Чили", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/cl.png"},
    {"id": 183, "name": "Перу", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/pe.png"},
    {"id": 184, "name": "Аргентина", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ar.png"},
    {"id": 185, "name": "Бразилия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/br.png"},
    {"id": 186, "name": "Канада", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ca.png"},
    {"id": 187, "name": "США", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/us.png"},
    {"id": 188, "name": "Мексика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/mx.png"},
    {"id": 189, "name": "Гренландия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/gl.png"},
    {"id": 190, "name": "Фарерские острова", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/fo.png"},
    {"id": 191, "name": "Аландские острова", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ax.png"},
    {"id": 192, "name": "Палестина", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ps.png"},
    {"id": 193, "name": "Косово", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/xk.png"},
    {"id": 194, "name": "Западная Сахара", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/eh.png"},
    {"id": 195, "name": "Антигуа и Барбуда", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/png/ag.png"},
]


def get_countries_by_difficulty(level: str):
    if level == "easy":
        return EASY_COUNTRIES
    elif level == "medium":
        return EASY_COUNTRIES + MEDIUM_COUNTRIES
    elif level == "hard":
        return EASY_COUNTRIES + MEDIUM_COUNTRIES + HARD_COUNTRIES
    else:
        return EASY_COUNTRIES


def parse_telegram_data(init_data):
    if not init_data or init_data == "undefined":
        raise HTTPException(status_code=400, detail="Missing init data")
    try:
        pairs = init_data.split("&")
        params = {}
        for pair in pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)
                import urllib.parse
                params[key] = urllib.parse.unquote(value)
        if "hash" not in params:
            raise HTTPException(status_code=400, detail="Missing hash")
        hash_val = params.pop("hash")
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(params.items()))
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        if computed_hash != hash_val:
            raise HTTPException(status_code=403, detail="Invalid hash")
        if "user" not in params:
            raise HTTPException(status_code=400, detail="Missing user data")
        user = json.loads(params["user"])
        return user["id"]
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid init data")

@app.get("/api/question")
def get_question(authorization: str = Header(...), level: str = "easy"):
    user_id = parse_telegram_data(authorization)
    pool = get_countries_by_difficulty(level)
    country = random.choice(pool)
    others = [c for c in pool if c["name"] != country["name"]]
    options = [country["name"]] + [c["name"] for c in random.sample(others, 3)]
    random.shuffle(options)
    return {
        "question_id": country["id"],
        "image_url": country["flag"],
        "options": options,
        "correct_answer": country["name"],
        "level": level
    }

@app.post("/api/answer")
def check_answer(data: dict):
    submitted = data.get("answer")
    correct = data.get("correct_answer")
    is_correct = submitted == correct
    return {
        "correct": is_correct,
        "correct_answer": correct
    }
