from main.models import Province, District

# --- VILOYATLAR ---
provinces = {
    "Toshkent shahri": ["Bektemir", "Chilonzor", "Mirobod", "Mirzo Ulug‘bek", "Sergeli",
                        "Olmazor", "Uchtepa", "Shayxontohur", "Yakkasaroy", "Yashnobod",
                        "Yunusobod", "Yangihayot"],

    "Toshkent viloyati": ["Bekobod", "Bo‘stonliq", "Bo‘ka", "Chinoz", "Oqqo‘rg‘on",
                          "Ohangaron", "Parkent", "Piskent", "Quyi Chirchiq", "Orta Chirchiq",
                          "Yuqori Chirchiq", "Yangiyo‘l", "Zangiota", "Qibray", "Nurafshon shahri"],

    "Andijon viloyati": ["Andijon", "Asaka", "Baliqchi", "Buloqboshi", "Bo‘z", "Jalolquduq",
                         "Izboskan", "Marhamat", "Oltinko‘l", "Paxtaobod", "Shahrixon",
                         "Ulug‘nor", "Xo‘jaobod", "Qo‘rg‘ontepa", "Andijon shahri"],

    "Farg‘ona viloyati": ["Beshariq", "Bog‘dod", "Buvayda", "Dang‘ara", "Furqat", "Farg‘ona",
                          "Oltiariq", "Qo‘shtepa", "Quva", "Rishton", "So‘x", "Toshloq",
                          "Uchko‘prik", "O‘zbekistan tumani", "Yozyovon",
                          "Farg‘ona shahri", "Quvasoy shahri", "Qo‘qon shahri", "Marg‘ilon shahri"],

    "Namangan viloyati": ["Chortoq", "Chust", "Kosonsoy", "Mingbuloq", "Namangan", "Norin",
                          "Pap", "To‘raqo‘rg‘on", "Uchqo‘rg‘on", "Uychi", "Yangiqo‘rg‘on", "Namangan shahri"],

    "Samarqand viloyati": ["Bulung‘ur", "Ishtixon", "Jomboy", "Kattaqo‘rg‘on", "Narpay", "Nurobod",
                           "Oqdaryo", "Paxtachi", "Payariq", "Pastdarg‘om", "Qo‘shrabot",
                           "Samarqand", "Toyloq", "Urgut", "Kattaqo‘rg‘on shahri", "Samarqand shahri"],

    "Buxoro viloyati": ["Buxoro", "G‘ijduvon", "Jondor", "Kogon", "Olot", "Peshku", "Qorako‘l",
                        "Qorovulbozor", "Romitan", "Shofirkon", "Kogon shahri", "Buxoro shahri"],

    "Navoiy viloyati": ["Karmana", "Konimex", "Qiziltepa", "Navbahor", "Nurota", "Tomdi",
                        "Uchquduq", "Xatirchi", "Zarafshon shahri", "Navoiy shahri"],

    "Qashqadaryo viloyati": ["Dehqonobod", "Kasbi", "Kitob", "Koson", "Mirishkor", "Muborak",
                             "Nishon", "Qarshi", "Qamashi", "Shahrisabz", "Yakkabog‘",
                             "Chiroqchi", "Qarshi shahri", "Shahrisabz shahri"],

    "Surxondaryo viloyati": ["Angor", "Bandixon", "Boysun", "Denov", "Jarqo‘rg‘on", "Muzrabot",
                             "Oltinsoy", "Qiziriq", "Qumqo‘rg‘on", "Sariosiyo", "Sherobod",
                             "Sho‘rchi", "Termiz", "Uzun", "Termiz shahri"],

    "Jizzax viloyati": ["Arnasoy", "Baxmal", "Do‘stlik", "Forish", "G‘allaorol", "Jizzax",
                        "Mirzacho‘l", "Paxtakor", "Yangiobod", "Zafarobod", "Zarbdor", "Jizzax shahri"],

    "Sirdaryo viloyati": ["Boyovut", "Guliston", "Mirzaobod", "Oqoltin", "Sardoba", "Sayxunobod",
                          "Sirdaryo", "Xovos", "Shirin shahri", "Guliston shahri", "Yangiyer shahri"],

    "Xorazm viloyati": ["Bog‘ot", "Gurlan", "Hazorasp", "Urganch", "Xiva", "Shovot", "Yangiariq",
                        "Yangibozor", "Qo‘shko‘pir", "Urganch shahri", "Xiva shahri"],

    "Qoraqalpog‘iston Respublikasi": ["Amudaryo", "Beruniy", "Chimboy", "Ellikqal’a", "Kegeyli",
                                      "Mo‘ynoq", "Nukus", "Qonliko‘l", "Qorao‘zak", "Shumanay",
                                      "Taxtako‘pir", "To‘rtko‘l", "Xo‘jayli", "Nukus shahri"]
}

for province_name, districts in provinces.items():
    province_obj = Province.objects.create(name=province_name)
    for district_name in districts:
        District.objects.create(name=district_name, province=province_obj)
