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
    {"id": 1, "name": "США", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/us.svg"},
    {"id": 2, "name": "Россия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ru.svg"},
    {"id": 3, "name": "Франция", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/fr.svg"},
    {"id": 4, "name": "Германия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/de.svg"},
    {"id": 5, "name": "Япония", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/jp.svg"},
    {"id": 6, "name": "Китай", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/cn.svg"},
    {"id": 7, "name": "Бразилия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/br.svg"},
    {"id": 8, "name": "Канада", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ca.svg"},
    {"id": 9, "name": "Австралия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/au.svg"},
    {"id": 10, "name": "Индия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/in.svg"},
    {"id": 11, "name": "Италия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/it.svg"},
    {"id": 12, "name": "Испания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/es.svg"},
    {"id": 13, "name": "Мексика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mx.svg"},
    {"id": 14, "name": "Южная Корея", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/kr.svg"},
    {"id": 15, "name": "Великобритания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/gb.svg"},
    {"id": 16, "name": "Египет", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/eg.svg"},
    {"id": 17, "name": "Турция", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/tr.svg"},
    {"id": 18, "name": "Нидерланды", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/nl.svg"},
    {"id": 19, "name": "Польша", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/pl.svg"},
    {"id": 20, "name": "Швеция", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/se.svg"},
    {"id": 21, "name": "Швейцария", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ch.svg"},
    {"id": 22, "name": "Аргентина", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ar.svg"},
    {"id": 23, "name": "Австрия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/at.svg"},
    {"id": 24, "name": "Бельгия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/be.svg"},
    {"id": 25, "name": "Греция", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/gr.svg"},
    {"id": 26, "name": "Индонезия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/id.svg"},
    {"id": 27, "name": "Ирландия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ie.svg"},
    {"id": 28, "name": "Израиль", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/il.svg"},
    {"id": 29, "name": "Норвегия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/no.svg"},
    {"id": 30, "name": "Португалия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/pt.svg"},
]

MEDIUM_COUNTRIES = [
    {"id": 31, "name": "Чили", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/cl.svg"},
    {"id": 32, "name": "Таиланд", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/th.svg"},
    {"id": 33, "name": "Финляндия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/fi.svg"},
    {"id": 34, "name": "Дания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/dk.svg"},
    {"id": 35, "name": "Украина", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ua.svg"},
    {"id": 36, "name": "Чехия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/cz.svg"},
    {"id": 37, "name": "Венгрия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/hu.svg"},
    {"id": 38, "name": "Румыния", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ro.svg"},
    {"id": 39, "name": "Болгария", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bg.svg"},
    {"id": 40, "name": "Сербия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/rs.svg"},
    {"id": 41, "name": "Хорватия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/hr.svg"},
    {"id": 42, "name": "Словакия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sk.svg"},
    {"id": 43, "name": "Словения", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/si.svg"},
    {"id": 44, "name": "Латвия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/lv.svg"},
    {"id": 45, "name": "Литва", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/lt.svg"},
    {"id": 46, "name": "Эстония", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ee.svg"},
    {"id": 47, "name": "Исландия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/is.svg"},
    {"id": 48, "name": "Казахстан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/kz.svg"},
    {"id": 49, "name": "Узбекистан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/uz.svg"},
    {"id": 50, "name": "Колумбия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/co.svg"},
    {"id": 51, "name": "Перу", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/pe.svg"},
    {"id": 52, "name": "Венесуэла", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ve.svg"},
    {"id": 53, "name": "Куба", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/cu.svg"},
    {"id": 54, "name": "ЮАР", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/za.svg"},
    {"id": 55, "name": "Малайзия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/my.svg"},
    {"id": 56, "name": "Сингапур", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sg.svg"},
    {"id": 57, "name": "Филиппины", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ph.svg"},
    {"id": 58, "name": "Пакистан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/pk.svg"},
    {"id": 59, "name": "Бангладеш", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bd.svg"},
    {"id": 60, "name": "Ирак", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/iq.svg"},
    {"id": 61, "name": "Иран", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ir.svg"},
    {"id": 62, "name": "Саудовская Аравия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sa.svg"},
    {"id": 63, "name": "ОАЭ", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ae.svg"},
    {"id": 64, "name": "Катар", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/qa.svg"},
    {"id": 65, "name": "Кувейт", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/kw.svg"},
    {"id": 66, "name": "Новая Зеландия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/nz.svg"},
    {"id": 67, "name": "Кипр", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/cy.svg"},
    {"id": 68, "name": "Мальта", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mt.svg"},
    {"id": 69, "name": "Люксембург", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/lu.svg"},
    {"id": 70, "name": "Монако", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mc.svg"},
    {"id": 71, "name": "Лихтенштейн", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/li.svg"},
    {"id": 72, "name": "Андорра", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ad.svg"},
    {"id": 73, "name": "Сан-Марино", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sm.svg"},
    {"id": 74, "name": "Ватикан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/va.svg"},
    {"id": 75, "name": "Албания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/al.svg"},
    {"id": 76, "name": "Босния и Герцеговина", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ba.svg"},
    {"id": 77, "name": "Северная Македония", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mk.svg"},
    {"id": 78, "name": "Черногория", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/me.svg"},
    {"id": 79, "name": "Молдова", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/md.svg"},
    {"id": 80, "name": "Грузия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ge.svg"},
    {"id": 81, "name": "Армения", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/am.svg"},
    {"id": 82, "name": "Азербайджан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/az.svg"},
    {"id": 83, "name": "Тунис", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/tn.svg"},
    {"id": 84, "name": "Марокко", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ma.svg"},
    {"id": 85, "name": "Алжир", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/dz.svg"},
    {"id": 86, "name": "Нигерия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ng.svg"},
    {"id": 87, "name": "Кения", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ke.svg"},
    {"id": 88, "name": "Гана", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/gh.svg"},
    {"id": 89, "name": "Сенегал", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sn.svg"},
    {"id": 90, "name": "Камерун", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/cm.svg"},
    {"id": 91, "name": "Конго", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/cg.svg"},
    {"id": 92, "name": "Танзания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/tz.svg"},
    {"id": 93, "name": "Уганда", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ug.svg"},
    {"id": 94, "name": "Замбия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/zm.svg"},
    {"id": 95, "name": "Зимбабве", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/zw.svg"},
    {"id": 96, "name": "Мозамбик", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mz.svg"},
    {"id": 97, "name": "Ангола", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ao.svg"},
    {"id": 98, "name": "Эфиопия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/et.svg"},
    {"id": 99, "name": "Судан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sd.svg"},
    {"id": 100, "name": "Ливия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ly.svg"},
]

HARD_COUNTRIES = [
    {"id": 101, "name": "Бутан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bt.svg"},
    {"id": 102, "name": "Суринам", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sr.svg"},
    {"id": 103, "name": "Того", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/tg.svg"},
    {"id": 104, "name": "Бенин", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bj.svg"},
    {"id": 105, "name": "Буркина-Фасо", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bf.svg"},
    {"id": 106, "name": "Гвинея", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/gn.svg"},
    {"id": 107, "name": "Гвинея-Бисау", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/gw.svg"},
    {"id": 108, "name": "Либерия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/lr.svg"},
    {"id": 109, "name": "Сьерра-Леоне", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sl.svg"},
    {"id": 110, "name": "Мали", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ml.svg"},
    {"id": 111, "name": "Нигер", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ne.svg"},
    {"id": 112, "name": "Чад", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/td.svg"},
    {"id": 113, "name": "Центральноафриканская Республика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/cf.svg"},
    {"id": 114, "name": "Габон", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ga.svg"},
    {"id": 115, "name": "Кабо-Верде", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/cv.svg"},
    {"id": 116, "name": "Сан-Томе и Принсипи", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/st.svg"},
    {"id": 117, "name": "Экваториальная Гвинея", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/gq.svg"},
    {"id": 118, "name": "Коморы", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/km.svg"},
    {"id": 119, "name": "Сейшелы", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sc.svg"},
    {"id": 120, "name": "Маврикий", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mu.svg"},
    {"id": 121, "name": "Мадагаскар", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mg.svg"},
    {"id": 122, "name": "Малави", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mw.svg"},
    {"id": 123, "name": "Лесото", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ls.svg"},
    {"id": 124, "name": "Эсватини", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sz.svg"},
    {"id": 125, "name": "Ботсвана", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bw.svg"},
    {"id": 126, "name": "Намибия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/na.svg"},
    {"id": 127, "name": "Южный Судан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ss.svg"},
    {"id": 128, "name": "Эритрея", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/er.svg"},
    {"id": 129, "name": "Джибути", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/dj.svg"},
    {"id": 130, "name": "Сомали", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/so.svg"},
    {"id": 131, "name": "Йемен", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ye.svg"},
    {"id": 132, "name": "Оман", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/om.svg"},
    {"id": 133, "name": "Бахрейн", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bh.svg"},
    {"id": 134, "name": "Иордания", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/jo.svg"},
    {"id": 135, "name": "Ливан", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/lb.svg"},
    {"id": 136, "name": "Сирия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sy.svg"},
    {"id": 137, "name": "Монголия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mn.svg"},
    {"id": 138, "name": "Вьетнам", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/vn.svg"},
    {"id": 139, "name": "Лаос", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/la.svg"},
    {"id": 140, "name": "Камбоджа", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/kh.svg"},
    {"id": 141, "name": "Мьянма", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mm.svg"},
    {"id": 142, "name": "Непал", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/np.svg"},
    {"id": 143, "name": "Шри-Ланка", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/lk.svg"},
    {"id": 144, "name": "Мальдивы", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mv.svg"},
    {"id": 145, "name": "Бруней", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bn.svg"},
    {"id": 146, "name": "Восточный Тимор", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/tl.svg"},
    {"id": 147, "name": "Папуа – Новая Гвинея", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/pg.svg"},
    {"id": 148, "name": "Соломоновы Острова", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sb.svg"},
    {"id": 149, "name": "Вануату", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/vu.svg"},
    {"id": 150, "name": "Фиджи", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/fj.svg"},
    {"id": 151, "name": "Кирибати", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ki.svg"},
    {"id": 152, "name": "Науру", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/nr.svg"},
    {"id": 153, "name": "Тувалу", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/tv.svg"},
    {"id": 154, "name": "Маршалловы Острова", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mh.svg"},
    {"id": 155, "name": "Микронезия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/fm.svg"},
    {"id": 156, "name": "Палау", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/pw.svg"},
    {"id": 157, "name": "Сент-Китс и Невис", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/kn.svg"},
    {"id": 158, "name": "Сент-Люсия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/lc.svg"},
    {"id": 159, "name": "Сент-Винсент и Гренадины", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/vc.svg"},
    {"id": 160, "name": "Гренада", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/gd.svg"},
    {"id": 161, "name": "Барбадос", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bb.svg"},
    {"id": 162, "name": "Тринидад и Тобаго", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/tt.svg"},
    {"id": 163, "name": "Доминика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/dm.svg"},
    {"id": 164, "name": "Доминиканская Республика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/do.svg"},
    {"id": 165, "name": "Гаити", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ht.svg"},
    {"id": 166, "name": "Ямайка", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/jm.svg"},
    {"id": 167, "name": "Багамы", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bs.svg"},
    {"id": 168, "name": "Белиз", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bz.svg"},
    {"id": 169, "name": "Гондурас", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/hn.svg"},
    {"id": 170, "name": "Сальвадор", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sv.svg"},
    {"id": 171, "name": "Никарагуа", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ni.svg"},
    {"id": 172, "name": "Коста-Рика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/cr.svg"},
    {"id": 173, "name": "Панама", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/pa.svg"},
    {"id": 174, "name": "Эквадор", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ec.svg"},
    {"id": 175, "name": "Колумбия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/co.svg"},
    {"id": 176, "name": "Венесуэла", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ve.svg"},
    {"id": 177, "name": "Гайана", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/gy.svg"},
    {"id": 178, "name": "Суринам", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/sr.svg"},
    {"id": 179, "name": "Уругвай", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/uy.svg"},
    {"id": 180, "name": "Парагвай", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/py.svg"},
    {"id": 181, "name": "Боливия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/bo.svg"},
    {"id": 182, "name": "Чили", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/cl.svg"},
    {"id": 183, "name": "Перу", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/pe.svg"},
    {"id": 184, "name": "Аргентина", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ar.svg"},
    {"id": 185, "name": "Бразилия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/br.svg"},
    {"id": 186, "name": "Канада", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ca.svg"},
    {"id": 187, "name": "США", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/us.svg"},
    {"id": 188, "name": "Мексика", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/mx.svg"},
    {"id": 189, "name": "Гренландия", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/gl.svg"},
    {"id": 190, "name": "Фарерские острова", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/fo.svg"},
    {"id": 191, "name": "Аландские острова", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ax.svg"},
    {"id": 192, "name": "Палестина", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ps.svg"},
    {"id": 193, "name": "Косово", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/xk.svg"},
    {"id": 194, "name": "Западная Сахара", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/eh.svg"},
    {"id": 195, "name": "Антигуа и Барбуда", "flag": "https://cdn.jsdelivr.net/gh/hjnilsson/country-flags@master/svg/ag.svg"},
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

@app.get("/api/questions")
def get_questions(authorization: str = Header(...), level: str = "easy", count: int = 10):
    user_id = parse_telegram_data(authorization)
    pool = get_countries_by_difficulty(level)
    
    # Выбираем уникальные страны
    if len(pool) < count:
        selected = pool
    else:
        selected = random.sample(pool, count)
    
    questions = []
    for country in selected:
        others = [c for c in pool if c["name"] != country["name"]]
        options = [country["name"]] + [c["name"] for c in random.sample(others, 3)]
        random.shuffle(options)
        questions.append({
            "image_url": country["flag"],
            "options": options,
            "correct_answer": country["name"]
        })
    
    return questions

@app.post("/api/answer")
def check_answer(data: dict):
    submitted = data.get("answer")
    correct = data.get("correct_answer")
    is_correct = submitted == correct
    return {
        "correct": is_correct,
        "correct_answer": correct
    }
