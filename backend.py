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
    {"id": 1, "name": "США", "flag": "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg"},
    {"id": 2, "name": "Россия", "flag": "https://upload.wikimedia.org/wikipedia/en/f/f3/Flag_of_Russia.svg"},
    {"id": 3, "name": "Франция", "flag": "https://upload.wikimedia.org/wikipedia/en/c/c3/Flag_of_France.svg"},
    {"id": 4, "name": "Германия", "flag": "https://upload.wikimedia.org/wikipedia/en/b/ba/Flag_of_Germany.svg"},
    {"id": 5, "name": "Япония", "flag": "https://upload.wikimedia.org/wikipedia/en/9/9e/Flag_of_Japan.svg"},
    {"id": 6, "name": "Китай", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_the_People%27s_Republic_of_China.svg"},
    {"id": 7, "name": "Бразилия", "flag": "https://upload.wikimedia.org/wikipedia/en/0/05/Flag_of_Brazil.svg"},
    {"id": 8, "name": "Канада", "flag": "https://upload.wikimedia.org/wikipedia/en/c/cf/Flag_of_Canada.svg"},
    {"id": 9, "name": "Австралия", "flag": "https://upload.wikimedia.org/wikipedia/commons/8/88/Flag_of_Australia_%28converted%29.svg"},
    {"id": 10, "name": "Индия", "flag": "https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg"},
    {"id": 11, "name": "Италия", "flag": "https://upload.wikimedia.org/wikipedia/en/0/03/Flag_of_Italy.svg"},
    {"id": 12, "name": "Испания", "flag": "https://upload.wikimedia.org/wikipedia/en/9/9a/Flag_of_Spain.svg"},
    {"id": 13, "name": "Мексика", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/fc/Flag_of_Mexico.svg"},
    {"id": 14, "name": "Южная Корея", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/09/Flag_of_South_Korea.svg"},
    {"id": 15, "name": "Великобритания", "flag": "https://upload.wikimedia.org/wikipedia/en/a/ae/Flag_of_the_United_Kingdom.svg"},
    {"id": 16, "name": "Египет", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/fe/Flag_of_Egypt.svg"},
    {"id": 17, "name": "Турция", "flag": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Flag_of_Turkey.svg"},
    {"id": 18, "name": "Нидерланды", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/20/Flag_of_the_Netherlands.svg"},
    {"id": 19, "name": "Польша", "flag": "https://upload.wikimedia.org/wikipedia/en/1/12/Flag_of_Poland.svg"},
    {"id": 20, "name": "Швеция", "flag": "https://upload.wikimedia.org/wikipedia/en/4/4c/Flag_of_Sweden.svg"},
    {"id": 21, "name": "Швейцария", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/08/Flag_of_Switzerland_(Pantone).svg"},
    {"id": 22, "name": "Аргентина", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Flag_of_Argentina.svg"},
    {"id": 23, "name": "Австрия", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_Austria.svg"},
    {"id": 24, "name": "Бельгия", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/92/Flag_of_Belgium.svg"},
    {"id": 25, "name": "Греция", "flag": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_Greece.svg"},
    {"id": 26, "name": "Индонезия", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Flag_of_Indonesia.svg"},
    {"id": 27, "name": "Ирландия", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/45/Flag_of_Ireland.svg"},
    {"id": 28, "name": "Израиль", "flag": "https://upload.wikimedia.org/wikipedia/commons/d/d4/Flag_of_Israel.svg"},
    {"id": 29, "name": "Норвегия", "flag": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Flag_of_Norway.svg"},
    {"id": 30, "name": "Португалия", "flag": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Flag_of_Portugal.svg"},
]

MEDIUM_COUNTRIES = [
    {"id": 31, "name": "Чили", "flag": "https://upload.wikimedia.org/wikipedia/commons/7/78/Flag_of_Chile.svg"},
    {"id": 32, "name": "Таиланд", "flag": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Flag_of_Thailand.svg"},
    {"id": 33, "name": "Финляндия", "flag": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Flag_of_Finland.svg"},
    {"id": 34, "name": "Дания", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/9c/Flag_of_Denmark.svg"},
    {"id": 35, "name": "Украина", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/49/Flag_of_Ukraine.svg"},
    {"id": 36, "name": "Чехия", "flag": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Flag_of_the_Czech_Republic.svg"},
    {"id": 37, "name": "Венгрия", "flag": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Flag_of_Hungary.svg"},
    {"id": 38, "name": "Румыния", "flag": "https://upload.wikimedia.org/wikipedia/commons/7/73/Flag_of_Romania.svg"},
    {"id": 39, "name": "Болгария", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Flag_of_Bulgaria.svg"},
    {"id": 40, "name": "Сербия", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Flag_of_Serbia.svg"},
    {"id": 41, "name": "Хорватия", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Flag_of_Croatia.svg"},
    {"id": 42, "name": "Словакия", "flag": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Flag_of_Slovakia.svg"},
    {"id": 43, "name": "Словения", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Flag_of_Slovenia.svg"},
    {"id": 44, "name": "Латвия", "flag": "https://upload.wikimedia.org/wikipedia/commons/8/84/Flag_of_Latvia.svg"},
    {"id": 45, "name": "Литва", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/11/Flag_of_Lithuania.svg"},
    {"id": 46, "name": "Эстония", "flag": "https://upload.wikimedia.org/wikipedia/commons/8/8f/Flag_of_Estonia.svg"},
    {"id": 47, "name": "Исландия", "flag": "https://upload.wikimedia.org/wikipedia/commons/c/ce/Flag_of_Iceland.svg"},
    {"id": 48, "name": "Казахстан", "flag": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Flag_of_Kazakhstan.svg"},
    {"id": 49, "name": "Узбекистан", "flag": "https://upload.wikimedia.org/wikipedia/commons/8/84/Flag_of_Uzbekistan.svg"},
    {"id": 50, "name": "Колумбия", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/21/Flag_of_Colombia.svg"},
    {"id": 51, "name": "Перу", "flag": "https://upload.wikimedia.org/wikipedia/commons/c/cf/Flag_of_Peru.svg"},
    {"id": 52, "name": "Венесуэла", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/06/Flag_of_Venezuela.svg"},
    {"id": 53, "name": "Куба", "flag": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Flag_of_Cuba.svg"},
    {"id": 54, "name": "ЮАР", "flag": "https://upload.wikimedia.org/wikipedia/commons/a/af/Flag_of_South_Africa.svg"},
    {"id": 55, "name": "Малайзия", "flag": "https://upload.wikimedia.org/wikipedia/commons/6/66/Flag_of_Malaysia.svg"},
    {"id": 56, "name": "Сингапур", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/48/Flag_of_Singapore.svg"},
    {"id": 57, "name": "Филиппины", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/99/Flag_of_the_Philippines.svg"},
    {"id": 58, "name": "Пакистан", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/32/Flag_of_Pakistan.svg"},
    {"id": 59, "name": "Бангладеш", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/f9/Flag_of_Bangladesh.svg"},
    {"id": 60, "name": "Ирак", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Flag_of_Iraq.svg"},
    {"id": 61, "name": "Иран", "flag": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Flag_of_Iran.svg"},
    {"id": 62, "name": "Саудовская Аравия", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg"},
    {"id": 63, "name": "ОАЭ", "flag": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Flag_of_the_United_Arab_Emirates.svg"},
    {"id": 64, "name": "Катар", "flag": "https://upload.wikimedia.org/wikipedia/commons/6/65/Flag_of_Qatar.svg"},
    {"id": 65, "name": "Кувейт", "flag": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Flag_of_Kuwait.svg"},
    {"id": 66, "name": "Новая Зеландия", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Flag_of_New_Zealand.svg"},
    {"id": 67, "name": "Кипр", "flag": "https://upload.wikimedia.org/wikipedia/commons/d/d4/Flag_of_Cyprus.svg"},
    {"id": 68, "name": "Мальта", "flag": "https://upload.wikimedia.org/wikipedia/commons/7/73/Flag_of_Malta.svg"},
    {"id": 69, "name": "Люксембург", "flag": "https://upload.wikimedia.org/wikipedia/commons/d/da/Flag_of_Luxembourg.svg"},
    {"id": 70, "name": "Монако", "flag": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Flag_of_Monaco.svg"},
    {"id": 71, "name": "Лихтенштейн", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/47/Flag_of_Liechtenstein.svg"},
    {"id": 72, "name": "Андорра", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/19/Flag_of_Andorra.svg"},
    {"id": 73, "name": "Сан-Марино", "flag": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Flag_of_San_Marino.svg"},
    {"id": 74, "name": "Ватикан", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_the_Vatican_City.svg"},
    {"id": 75, "name": "Албания", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/36/Flag_of_Albania.svg"},
    {"id": 76, "name": "Босния и Герцеговина", "flag": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Flag_of_Bosnia_and_Herzegovina.svg"},
    {"id": 77, "name": "Северная Македония", "flag": "https://upload.wikimedia.org/wikipedia/commons/7/79/Flag_of_North_Macedonia.svg"},
    {"id": 78, "name": "Черногория", "flag": "https://upload.wikimedia.org/wikipedia/commons/6/64/Flag_of_Montenegro.svg"},
    {"id": 79, "name": "Молдова", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/27/Flag_of_Moldova.svg"},
    {"id": 80, "name": "Грузия", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Flag_of_Georgia.svg"},
    {"id": 81, "name": "Армения", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Flag_of_Armenia.svg"},
    {"id": 82, "name": "Азербайджан", "flag": "https://upload.wikimedia.org/wikipedia/commons/d/dd/Flag_of_Azerbaijan.svg"},
    {"id": 83, "name": "Тунис", "flag": "https://upload.wikimedia.org/wikipedia/commons/c/ce/Flag_of_Tunisia.svg"},
    {"id": 84, "name": "Марокко", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Morocco.svg"},
    {"id": 85, "name": "Алжир", "flag": "https://upload.wikimedia.org/wikipedia/commons/7/77/Flag_of_Algeria.svg"},
    {"id": 86, "name": "Нигерия", "flag": "https://upload.wikimedia.org/wikipedia/commons/7/79/Flag_of_Nigeria.svg"},
    {"id": 87, "name": "Кения", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/49/Flag_of_Kenya.svg"},
    {"id": 88, "name": "Гана", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/19/Flag_of_Ghana.svg"},
    {"id": 89, "name": "Сенегал", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/fd/Flag_of_Senegal.svg"},
    {"id": 90, "name": "Камерун", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Flag_of_Cameroon.svg"},
    {"id": 91, "name": "Конго", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/92/Flag_of_the_Republic_of_the_Congo.svg"},
    {"id": 92, "name": "Танзания", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/38/Flag_of_Tanzania.svg"},
    {"id": 93, "name": "Уганда", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Flag_of_Uganda.svg"},
    {"id": 94, "name": "Замбия", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/06/Flag_of_Zambia.svg"},
    {"id": 95, "name": "Зимбабве", "flag": "https://upload.wikimedia.org/wikipedia/commons/6/6a/Flag_of_Zimbabwe.svg"},
    {"id": 96, "name": "Мозамбик", "flag": "https://upload.wikimedia.org/wikipedia/commons/d/d0/Flag_of_Mozambique.svg"},
    {"id": 97, "name": "Ангола", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/9d/Flag_of_Angola.svg"},
    {"id": 98, "name": "Эфиопия", "flag": "https://upload.wikimedia.org/wikipedia/commons/7/71/Flag_of_Ethiopia.svg"},
    {"id": 99, "name": "Судан", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/01/Flag_of_Sudan.svg"},
    {"id": 100, "name": "Ливия", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/05/Flag_of_Libya.svg"},
]

HARD_COUNTRIES = [
    {"id": 101, "name": "Бутан", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/91/Flag_of_Bhutan.svg"},
    {"id": 102, "name": "Суринам", "flag": "https://upload.wikimedia.org/wikipedia/commons/6/60/Flag_of_Suriname.svg"},
    {"id": 103, "name": "Того", "flag": "https://upload.wikimedia.org/wikipedia/commons/6/68/Flag_of_Togo.svg"},
    {"id": 104, "name": "Бенин", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Flag_of_Benin.svg"},
    {"id": 105, "name": "Буркина-Фасо", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/31/Flag_of_Burkina_Faso.svg"},
    {"id": 106, "name": "Гвинея", "flag": "https://upload.wikimedia.org/wikipedia/commons/e/ed/Flag_of_Guinea.svg"},
    {"id": 107, "name": "Гвинея-Бисау", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/01/Flag_of_Guinea-Bissau.svg"},
    {"id": 108, "name": "Либерия", "flag": "https://upload.wikimedia.org/wikipedia/commons/b/b8/Flag_of_Liberia.svg"},
    {"id": 109, "name": "Сьерра-Леоне", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/17/Flag_of_Sierra_Leone.svg"},
    {"id": 110, "name": "Мали", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/92/Flag_of_Mali.svg"},
    {"id": 111, "name": "Нигер", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Flag_of_Niger.svg"},
    {"id": 112, "name": "Чад", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Flag_of_Chad.svg"},
    {"id": 113, "name": "Центральноафриканская Республика", "flag": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Flag_of_the_Central_African_Republic.svg"},
    {"id": 114, "name": "Габон", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/01/Flag_of_Gabon.svg"},
    {"id": 115, "name": "Кабо-Верде", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/38/Flag_of_Cape_Verde.svg"},
    {"id": 116, "name": "Сан-Томе и Принсипи", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Flag_of_São_Tomé_and_Príncipe.svg"},
    {"id": 117, "name": "Экваториальная Гвинея", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/31/Flag_of_Equatorial_Guinea.svg"},
    {"id": 118, "name": "Коморы", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/94/Flag_of_the_Comoros.svg"},
    {"id": 119, "name": "Сейшелы", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/fc/Flag_of_Seychelles.svg"},
    {"id": 120, "name": "Маврикий", "flag": "https://upload.wikimedia.org/wikipedia/commons/7/77/Flag_of_Mauritius.svg"},
    {"id": 121, "name": "Мадагаскар", "flag": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Flag_of_Madagascar.svg"},
    {"id": 122, "name": "Малави", "flag": "https://upload.wikimedia.org/wikipedia/commons/d/d1/Flag_of_Malawi.svg"},
    {"id": 123, "name": "Лесото", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Flag_of_Lesotho.svg"},
    {"id": 124, "name": "Свазиленд", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Flag_of_Eswatini.svg"},
    {"id": 125, "name": "Ботсвана", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_Botswana.svg"},
    {"id": 126, "name": "Намибия", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_Namibia.svg"},
    {"id": 127, "name": "Южный Судан", "flag": "https://upload.wikimedia.org/wikipedia/commons/7/7a/Flag_of_South_Sudan.svg"},
    {"id": 128, "name": "Эритрея", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/29/Flag_of_Eritrea.svg"},
    {"id": 129, "name": "Джибути", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/34/Flag_of_Djibouti.svg"},
    {"id": 130, "name": "Сомали", "flag": "https://upload.wikimedia.org/wikipedia/commons/a/a0/Flag_of_Somalia.svg"},
    {"id": 131, "name": "Йемен", "flag": "https://upload.wikimedia.org/wikipedia/commons/8/89/Flag_of_Yemen.svg"},
    {"id": 132, "name": "Оман", "flag": "https://upload.wikimedia.org/wikipedia/commons/d/dd/Flag_of_Oman.svg"},
    {"id": 133, "name": "Бахрейн", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Bahrain.svg"},
    {"id": 134, "name": "Иордания", "flag": "https://upload.wikimedia.org/wikipedia/commons/c/c0/Flag_of_Jordan.svg"},
    {"id": 135, "name": "Ливан", "flag": "https://upload.wikimedia.org/wikipedia/commons/5/59/Flag_of_Lebanon.svg"},
    {"id": 136, "name": "Сирия", "flag": "https://upload.wikimedia.org/wikipedia/commons/5/53/Flag_of_Syria.svg"},
    {"id": 137, "name": "Монголия", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/4c/Flag_of_Mongolia.svg"},
    {"id": 138, "name": "Вьетнам", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/21/Flag_of_Vietnam.svg"},
    {"id": 139, "name": "Лаос", "flag": "https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Laos.svg"},
    {"id": 140, "name": "Камбоджа", "flag": "https://upload.wikimedia.org/wikipedia/commons/8/84/Flag_of_Cambodia.svg"},
    {"id": 141, "name": "Мьянма", "flag": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Flag_of_Myanmar.svg"},
    {"id": 142, "name": "Непал", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/9b/Flag_of_Nepal.svg"},
    {"id": 143, "name": "Бутан", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/91/Flag_of_Bhutan.svg"},
    {"id": 144, "name": "Шри-Ланка", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/11/Flag_of_Sri_Lanka.svg"},
    {"id": 145, "name": "Мальдивы", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Flag_of_Maldives.svg"},
    {"id": 146, "name": "Бруней", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/11/Flag_of_Brunei.svg"},
    {"id": 147, "name": "Восточный Тимор", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/26/Flag_of_East_Timor.svg"},
    {"id": 148, "name": "Папуа – Новая Гвинея", "flag": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Flag_of_Papua_New_Guinea.svg"},
    {"id": 149, "name": "Соломоновы Острова", "flag": "https://upload.wikimedia.org/wikipedia/commons/7/74/Flag_of_the_Solomon_Islands.svg"},
    {"id": 150, "name": "Вануату", "flag": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Flag_of_Vanuatu.svg"},
    {"id": 151, "name": "Фиджи", "flag": "https://upload.wikimedia.org/wikipedia/commons/b/ba/Flag_of_Fiji.svg"},
    {"id": 152, "name": "Кирибати", "flag": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Flag_of_Kiribati.svg"},
    {"id": 153, "name": "Науру", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/30/Flag_of_Nauru.svg"},
    {"id": 154, "name": "Тувалу", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/38/Flag_of_Tuvalu.svg"},
    {"id": 155, "name": "Маршалловы Острова", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Flag_of_the_Marshall_Islands.svg"},
    {"id": 156, "name": "Микронезия", "flag": "https://upload.wikimedia.org/wikipedia/commons/e/e4/Flag_of_the_Federated_States_of_Micronesia.svg"},
    {"id": 157, "name": "Палау", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/48/Flag_of_Palau.svg"},
    {"id": 158, "name": "Сент-Китс и Невис", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/fe/Flag_of_Saint_Kitts_and_Nevis.svg"},
    {"id": 159, "name": "Сент-Люсия", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Flag_of_Saint_Lucia.svg"},
    {"id": 160, "name": "Сент-Винсент и Гренадины", "flag": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Flag_of_Saint_Vincent_and_the_Grenadines.svg"},
    {"id": 161, "name": "Гренада", "flag": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Flag_of_Grenada.svg"},
    {"id": 162, "name": "Барбадос", "flag": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Flag_of_Barbados.svg"},
    {"id": 163, "name": "Тринидад и Тобаго", "flag": "https://upload.wikimedia.org/wikipedia/commons/6/64/Flag_of_Trinidad_and_Tobago.svg"},
    {"id": 164, "name": "Доминика", "flag": "https://upload.wikimedia.org/wikipedia/commons/c/c4/Flag_of_Dominica.svg"},
    {"id": 165, "name": "Доминиканская Республика", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Flag_of_the_Dominican_Republic.svg"},
    {"id": 166, "name": "Гаити", "flag": "https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg"},
    {"id": 167, "name": "Ямайка", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Flag_of_Jamaica.svg"},
    {"id": 168, "name": "Багамы", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/93/Flag_of_the_Bahamas.svg"},
    {"id": 169, "name": "Белиз", "flag": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Flag_of_Belize.svg"},
    {"id": 170, "name": "Гондурас", "flag": "https://upload.wikimedia.org/wikipedia/commons/8/82/Flag_of_Honduras.svg"},
    {"id": 171, "name": "Сальвадор", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/34/Flag_of_El_Salvador.svg"},
    {"id": 172, "name": "Никарагуа", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/19/Flag_of_Nicaragua.svg"},
    {"id": 173, "name": "Коста-Рика", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Flag_of_Costa_Rica.svg"},
    {"id": 174, "name": "Панама", "flag": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Flag_of_Panama.svg"},
    {"id": 175, "name": "Эквадор", "flag": "https://upload.wikimedia.org/wikipedia/commons/e/e8/Flag_of_Ecuador.svg"},
    {"id": 176, "name": "Колумбия", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/21/Flag_of_Colombia.svg"},
    {"id": 177, "name": "Венесуэла", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/06/Flag_of_Venezuela.svg"},
    {"id": 178, "name": "Гайана", "flag": "https://upload.wikimedia.org/wikipedia/commons/9/99/Flag_of_Guyana.svg"},
    {"id": 179, "name": "Суринам", "flag": "https://upload.wikimedia.org/wikipedia/commons/6/60/Flag_of_Suriname.svg"},
    {"id": 180, "name": "Уругвай", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/fe/Flag_of_Uruguay.svg"},
    {"id": 181, "name": "Парагвай", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/27/Flag_of_Paraguay.svg"},
    {"id": 182, "name": "Боливия", "flag": "https://upload.wikimedia.org/wikipedia/commons/4/48/Flag_of_Bolivia.svg"},
    {"id": 183, "name": "Чили", "flag": "https://upload.wikimedia.org/wikipedia/commons/7/78/Flag_of_Chile.svg"},
    {"id": 184, "name": "Перу", "flag": "https://upload.wikimedia.org/wikipedia/commons/c/cf/Flag_of_Peru.svg"},
    {"id": 185, "name": "Аргентина", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/1a/Flag_of_Argentina.svg"},
    {"id": 186, "name": "Бразилия", "flag": "https://upload.wikimedia.org/wikipedia/en/0/05/Flag_of_Brazil.svg"},
    {"id": 187, "name": "Канада", "flag": "https://upload.wikimedia.org/wikipedia/en/c/cf/Flag_of_Canada.svg"},
    {"id": 188, "name": "США", "flag": "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg"},
    {"id": 189, "name": "Мексика", "flag": "https://upload.wikimedia.org/wikipedia/commons/f/fc/Flag_of_Mexico.svg"},
    {"id": 190, "name": "Гренландия", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/09/Flag_of_Greenland.svg"},
    {"id": 191, "name": "Фарерские острова", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Flag_of_the_Faroe_Islands.svg"},
    {"id": 192, "name": "Аландские острова", "flag": "https://upload.wikimedia.org/wikipedia/commons/3/36/Flag_of_%C3%85land.svg"},
    {"id": 193, "name": "Палестина", "flag": "https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_Palestine.svg"},
    {"id": 194, "name": "Косово", "flag": "https://upload.wikimedia.org/wikipedia/commons/1/1f/Flag_of_Kosovo.svg"},
    {"id": 195, "name": "Западная Сахара", "flag": "https://upload.wikimedia.org/wikipedia/commons/2/26/Flag_of_the_Sahrawi_Arab_Democratic_Republic.svg"}
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
