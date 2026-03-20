"""
Manual translation fix for remaining Arabic text in ru, fr, tr locale files.
Uses English translations as source to create proper translations.
"""
import json
from pathlib import Path

LOCALES_DIR = Path(__file__).parent.parent / 'frontend' / 'src' / 'locales'

# Load English as source
with open(LOCALES_DIR / 'en.json', 'r') as f:
    en = json.load(f)

# Manual translations for the remaining keys
TRANSLATIONS = {
    'ru': {
        'duaAfterPrayer3': 'Субхан Аллах (33), Альхамдулиллях (33), Аллаху Акбар (33)',
        'duaVisitSick1': 'Не беспокойся, это очищение, если пожелает Аллах',
        'duaRuqyah1': 'С именем Аллаха (трижды). Прибегаю к защите Аллаха и Его мощи от зла того, что я испытываю и чего опасаюсь',
        'duaHappy1': 'Хвала Аллаху, по милости Которого совершаются благие дела',
        'duaHappy2': 'О Аллах, Тебе хвала, как подобает величию Твоего лика и величию Твоей власти',
        'duaCondolence1': 'Поистине, Аллаху принадлежит то, что Он забрал, и то, что Он дал, и у Него для всего определён срок, так проявляй терпение и надейся на награду',
        'duaGrave1': 'Мир вам, обитатели этих мест из числа верующих и мусульман. И мы, если пожелает Аллах, присоединимся к вам. Просим Аллаха для нас и для вас благополучия',
        'duaSai1': 'Поистине, ас-Сафа и аль-Марва — из обрядов Аллаха',
        'duaSai2': 'Начнём с того, с чего начал Аллах',
        'duaArafat1': 'Нет божества, кроме Аллаха, Единого, у Которого нет сотоварища. Ему принадлежит власть и хвала, и Он над всем сущим властен',
        'duaSuhoor1': 'Я намерен поститься завтрашний день месяца Рамадан',
    },
    'fr': {
        'duaVisitSick1': 'Ne t\'inquiète pas, c\'est une purification, si Allah le veut',
        'duaRuqyah1': 'Au nom d\'Allah (trois fois). Je cherche refuge auprès d\'Allah et de Sa puissance contre le mal de ce que je ressens et de ce que je crains',
        'duaHappy1': 'Louange à Allah par la grâce duquel les bonnes actions s\'accomplissent',
        'duaHappy2': 'Ô Allah, à Toi la louange comme il sied à la majesté de Ton visage et à la grandeur de Ton pouvoir',
        'duaCondolence1': 'Certes, à Allah appartient ce qu\'Il a pris et ce qu\'Il a donné, et chaque chose a auprès de Lui un terme fixé, alors patiente et espère la récompense',
        'duaGrave1': 'Paix sur vous, habitants de ces demeures parmi les croyants et les musulmans. Et nous, si Allah le veut, nous vous rejoindrons. Nous demandons à Allah le bien-être pour nous et pour vous',
        'duaSai1': 'Certes, as-Safa et al-Marwa font partie des rites d\'Allah',
        'duaSai2': 'Commençons par ce par quoi Allah a commencé',
        'duaArafat1': 'Il n\'y a de divinité qu\'Allah, Seul, sans associé. À Lui la royauté et la louange, et Il est Omnipotent',
        'duaSuhoor1': 'J\'ai l\'intention de jeûner demain pour le mois de Ramadan',
        'duaRain1': 'Nous avons reçu la pluie par la grâce et la miséricorde d\'Allah',
    },
    'tr': {
        'duaAfterPrayer1': 'Allah\'tan bağışlanma dilerim, Allah\'tan bağışlanma dilerim, Allah\'tan bağışlanma dilerim',
        'duaAfterPrayer2': 'Allah\'ım! Sen Selam\'sın, selamet Senden gelir. Ey celal ve ikram sahibi, Sen ne yücesin',
        'duaAfterPrayer3': 'Sübhanallah (33), Elhamdülillah (33), Allahu Ekber (33)',
        'duaAfterPrayer4': 'Allah\'tan başka ilah yoktur, O tektir, ortağı yoktur. Mülk O\'nundur, hamd O\'nadır ve O her şeye kadirdir',
        'duaAfterPrayer5': 'Allah\'ım! Seni anmam, Sana şükretmem ve Sana güzel ibadet etmem konusunda bana yardım et',
        'duaFaith3': 'Rabbimiz! Bizi hidayete erdirdikten sonra kalplerimizi saptırma ve bize katından bir rahmet bahşet. Şüphesiz Sen çok bağışlayansın',
        'duaJudgment3': 'Allah\'ım! Beni ateşten koru',
        'duaPraising3': 'Allah\'ı yarattıklarının sayısınca, rızası miktarınca, arşının ağırlığınca ve kelimelerinin mürekkebi sayısınca tespih ederim',
        'duaHealth3': 'Allah\'ın adıyla sana rukye yapıyorum, sana zarar veren her şeyden, her nefsin ve hasetçi gözün şerrinden. Allah sana şifa versin',
        'duaLoss3': 'Allah\'ım! Senin kolaylaştırdığından başka kolay yoktur. Sen dilersen hüznü kolaylığa çevirirsin',
        'duaSadness3': 'Allah bize yeter, O ne güzel vekildir',
        'duaMens1': 'Sübhanallahi ve bihamdihi (Allah\'ı hamd ile tespih ederim)',
        'duaMens2': 'Allah\'tan bağışlanma diler ve O\'na tövbe ederim',
        'duaMens3': 'Allah\'tan başka ilah yoktur, O tektir, ortağı yoktur',
        'duaDeceased3': 'Allah\'ım! Bizi onun ecrinden mahrum etme, ondan sonra bizi fitneye düşürme, bizi ve onu bağışla',
        'duaHajj3': 'Bismillahi Allahu Ekber (Allah\'ın adıyla, Allah en büyüktür)',
        'duaRamadan3': 'Allah\'ım! Senin için oruç tuttum ve Senin rızkınla iftar ettim',
        'duaNature3': 'Allah\'ım! Onun hayrını, içindeki hayrı ve onunla gönderilen hayrı Senden isterim. Onun şerrinden, içindeki şerden ve onunla gönderilen şerden Sana sığınırım',
        'duaManners1': 'Allah\'ım! Beni en güzel ahlaka yönelt, çünkü en güzel ahlaka ancak Sen yöneltirsin. Kötü ahlakı benden uzaklaştır, çünkü onu ancak Sen uzaklaştırırsın',
        'duaManners2': 'Allah\'ım! Kötü ahlaktan, kötü amellerden ve kötü arzulardan Sana sığınırım',
        'duaGuidance3': 'Allah\'ım! Benim için hayırlısını seç ve beni hayırlısına yönelt',
        'duaMosqueLeave1': 'Allah\'ın adıyla, salat ve selam Rasulullah\'ın üzerine olsun. Allah\'ım! Senden fazlını isterim',
        'duaMosqueLeave2': 'Allah\'ım! Beni kovulmuş şeytandan koru',
        'duaHomeLeave1': 'Allah\'ın adıyla, Allah\'a tevekkül ettim. Güç ve kuvvet ancak Allah\'tandır',
        'duaHomeLeave2': 'Allah\'ım! Sapıtmaktan veya saptırılmaktan, kaymaktan veya kaydırılmaktan, zulmetmekten veya zulme uğramaktan, cahillik etmekten veya cahilliğe maruz kalmaktan Sana sığınırım',
        'duaClothesRemove1': 'Bismillah (Allah\'ın adıyla)',
        'duaClothesSee1': 'Eskisin, Allah yenisini versin',
        'duaClothesSee2': 'Yeni giy, övülerek yaşa, şehit olarak öl',
        'duaTravelReturn1': 'Dönenler, tövbe edenler, ibadet edenler, Rabbimize hamd edenleriz',
        'duaTravelReturn2': 'Allah\'ım! Senden girişlerin ve çıkışların hayırlısını isterim',
        'duaVehicle1': 'Bunu bizim hizmetimize veren Allah münezzehtir, yoksa biz buna güç yetiremezdik. Şüphesiz biz Rabbimize döneceğiz',
        'duaVehicle2': 'Bismillah, Elhamdülillah (Allah\'ın adıyla, hamd Allah\'adır)',
        'duaFoodBefore2': 'Allah\'ım! Bize rızık olarak verdiğin şeyleri bereketli kıl ve bizi cehennem azabından koru',
        'duaFoodBefore3': 'Başında ve sonunda Allah\'ın adıyla',
        'duaDrink1': 'Allah\'ım! İçinde bize bereket ver ve bize daha fazlasını nasip et',
        'duaGuestFood1': 'Allah\'ım! Onlara verdiğin rızıkta bereket ver, onları bağışla ve onlara rahmet et',
        'duaGuestFood2': 'Yanınızda oruçlular iftar etsin, yemeğinizi iyiler yesin ve melekler size dua etsin',
        'duaMorning1': 'Allah\'ım! Bedenimde afiyet ver. Allah\'ım! Kulağımda afiyet ver. Allah\'ım! Gözümde afiyet ver. Senden başka ilah yoktur',
        'duaEvening1': 'Akşama erdik, mülk de Allah\'a ait olarak akşamladı. Hamd Allah\'adır. Allah\'tan başka ilah yoktur, O tektir, ortağı yoktur',
        'duaEvening2': 'Allah\'ım! Seninle akşamladık, seninle sabahladık, seninle yaşar, seninle ölürüz. Dönüş Sanadır',
        'duaEvening3': 'Allah\'ım! Bende veya yaratıklarından herhangi birinde bulunan nimet yalnızca Sendendir, ortağın yoktur. Hamd ve şükür Sanadır',
        'duaProtection1': 'Adıyla yerde ve gökte hiçbir şeyin zarar veremeyeceği Allah\'ın adıyla. O her şeyi işiten ve bilendir',
        'duaProtection2': 'Allah bana yeter, O\'ndan başka ilah yoktur. O\'na tevekkül ettim, O yüce arşın Rabbidir',
        'duaSalawat1': 'Allah\'ım! Peygamberimiz Muhammed\'e salat ve selam eyle',
        'duaSalawat2': 'Allah\'ım! İbrahim\'e ve İbrahim\'in ailesine salat ettiğin gibi Muhammed\'e ve Muhammed\'in ailesine de salat et. Şüphesiz Sen övülen ve yüce olansın',
        'duaExam1': 'Rabbim! Göğsümü aç, işimi kolaylaştır, dilimdeki düğümü çöz ki sözümü anlasınlar',
        'duaExam2': 'Allah\'ım! Senin kolaylaştırdığından başka kolay yoktur. Sen dilersen hüznü kolaylığa çevirirsin',
        'duaParents1': 'Rabbim! Onlara merhamet et, beni küçükken yetiştirdikleri gibi',
        'duaParents2': 'Rabbimiz! Hesap gününde beni, anne babamı ve müminleri bağışla',
        'duaSpouse1': 'Allah\'ım! İkisine bereket ver, üzerlerine bereket indir ve ikisini hayırda birleştir',
        'duaVisitSick1': 'Endişelenme, inşallah bu bir temizliktir',
        'duaRuqyah1': 'Bismillah (üç kere). Hissettiğim ve çekindiğim şeyin şerrinden Allah\'a ve O\'nun kudretine sığınırım',
        'duaHappy1': 'Nimetiyle salih amellerin tamamlandığı Allah\'a hamd olsun',
        'duaHappy2': 'Allah\'ım! Yüzünün celaline ve saltanatının büyüklüğüne layık olduğu şekilde Sana hamd olsun',
        'duaCondolence1': 'Şüphesiz aldığı da Allah\'ındır, verdiği de. Her şeyin O\'nun katında belirli bir eceli vardır. Sabret ve karşılığını Allah\'tan bekle',
        'duaGrave1': 'Selam olsun size, ey bu diyarların mümin ve Müslüman sakinleri! İnşallah biz de size katılacağız. Allah\'tan bizim ve sizin için afiyet dileriz',
        'duaSai1': 'Şüphesiz Safa ve Merve, Allah\'ın nişanelerindendir',
        'duaSai2': 'Allah\'ın başladığı yerden başlıyoruz',
        'duaArafat1': 'Allah\'tan başka ilah yoktur, O tektir, ortağı yoktur. Mülk O\'nundur, hamd O\'nadır ve O her şeye kadirdir',
        'duaSuhoor1': 'Ramazan ayında yarın oruç tutmaya niyet ettim',
        'duaRain1': 'Allah\'ın lütfu ve rahmetiyle yağmura kavuştuk',
    },
}

for lang_code, translations in TRANSLATIONS.items():
    locale_path = LOCALES_DIR / f'{lang_code}.json'
    with open(locale_path, 'r') as f:
        data = json.load(f)
    
    for k, v in translations.items():
        data[k] = v
    
    with open(locale_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {lang_code}.json with {len(translations)} manual translations")

print("\nDone! All remaining Arabic text fixed.")
