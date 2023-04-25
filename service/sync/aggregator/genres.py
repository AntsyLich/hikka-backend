from service.models import AnimeGenre
from tortoise import Tortoise
from service import utils
from . import requests
import config

TRANSLATIONS = {
    "action": "Бойовик", "adventure": "Пригоди",
    "avant-garde": "Авангард", "boys-love": "Хлопчаче кохання",
    "comedy": "Комедія", "drama": "Драма", "fantasy": "Фентезі",
    "girls-love": "Дівчаче кохання", "gourmet": "Про їжу",
    "horror": "Жахи", "mystery": "Загадкове", "romance": "Романтика",
    "sci-fi": "Фантастика", "slice-of-life": "Буденність",
    "sports": "Спорт", "supernatural": "Надприродне", "suspense": "Трилер",
    "ecchi": "Еччі", "erotica": "Еротика", "hentai": "Хентай",
    "adult-cast": "Про дорослих", "anthropomorphic": "Антропоморфізм",
    "cgdct": "Милі дівчата роблять милі речі", "childcare": "Догляд за дітьми",
    "combat-sports": "Бойовий спорт", "crossdressing": "Переодягання",
    "delinquents": "Порушники", "detective": "Детектив",
    "educational": "Освітнє", "gag-humor": "Жарти", "gore": "Гротеск",
    "harem": "Гарем", "high-stakes-game": "Високі ставки",
    "historical": "Історичне", "idols-female": "Ідоли (дівчата)",
    "idols-male": "Ідоли (чоловіки)", "isekai": "Ісекай",
    "iyashikei": "Іяшикай", "love-polygon": "Любовний багатокутник",
    "magical-sex-shift": "Зміна статі", "mahou-shoujo": "Дівчина-чарівниця",
    "martial-arts": "Бойові мистецтва", "mecha": "Мехи",
    "medical": "Медицина", "military": "Війна", "music": "Музика",
    "mythology": "Міфологія", "organized-crime": "Організована злочинність",
    "otaku-culture": "Культура отаку", "parody": "Пародія",
    "performing-arts": "Виконавче мистецтво", "pets": "Тварини",
    "psychological": "Психологія", "racing": "Гонки",
    "reincarnation": "Переродження", "reverse-harem": "Реверсивний гарем",
    "romantic-subtext": "Романтичний підтекст", "samurai": "Самураї",
    "school": "Школа", "showbiz": "Шоу-біз", "space": "Космос",
    "strategy-game": "Стратегія", "super-power": "Супергерої",
    "survival": "Виживання", "team-sports": "Командний спорт",
    "time-travel": "Подорожі в часі", "vampire": "Вампіри",
    "video-game": "Комп'ютерні ігри", "visual-arts": "Візуальне мистецтво",
    "workplace": "Робота", "josei": "Дзьосей", "kids": "Для дітей",
    "seinen": "Сейнен", "shoujo": "Шьоджьо", "shounen": "Шьонен",
    "award-winning": "Відзначений нагородами"
}

async def aggregator_anime_genres():
    await Tortoise.init(config=config.tortoise)
    await Tortoise.generate_schemas()

    data = await requests.get_anime_genres()
    create_genres = []

    for genre_data in data:
        slug = utils.slugify(genre_data["name"])
        name_ua = TRANSLATIONS.get(slug)

        if await AnimeGenre.filter(slug=slug).first():
            continue

        genre = AnimeGenre(**{
            "conetent_id": genre_data["reference"],
            "name_en": genre_data["name"],
            "type": genre_data["type"],
            "name_ua": name_ua,
            "slug": slug
        })

        create_genres.append(genre)

        print(f"Added genre: {genre.name_en}")

    await AnimeGenre.bulk_create(create_genres)
