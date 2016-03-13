class ChampionListDto(object):
    def __init__(self, dictionary):
        self.data = {name: ChampionDto(champ) if not isinstance(champ, ChampionDto) else champ for name, champ in dictionary.get("data", {}).items()}
        self.format = dictionary.get("format", "")
        self.keys = dictionary.get("keys", {})
        self.type = dictionary.get("type", "")
        self.version = dictionary.get("version", "")


class ChampionDto(object):
    def __init__(self, dictionary):
        self.allytips = dictionary.get("allytips", [])
        self.blurb = dictionary.get("blurb", "")
        self.enemytips = dictionary.get("enemytips", [])
        self.id = dictionary.get("id", 0)
        val = dictionary.get("image", None)
        self.image = ImageDto(val) if val and not isinstance(val, ImageDto) else val
        val = dictionary.get("info", None)
        self.info = InfoDto(val) if val and not isinstance(val, InfoDto) else val
        self.key = dictionary.get("key", "")
        self.lore = dictionary.get("lore", "")
        self.name = dictionary.get("name", "")
        self.partype = dictionary.get("partype", "")
        val = dictionary.get("passive", None)
        self.passive = PassiveDto(val) if val and not isinstance(val, PassiveDto) else val
        self.recommended = [(RecommendedDto(rec) if not isinstance(rec, RecommendedDto) else rec) for rec in dictionary.get("recommended", []) if rec]
        self.skins = [(SkinDto(skin) if val and not isinstance(skin, SkinDto) else skin) for skin in dictionary.get("skins", []) if skin]
        self.spells = [(ChampionSpellDto(spell) if not isinstance(spell, ChampionSpellDto) else spell) for spell in dictionary.get("spells", []) if spell]
        val = dictionary.get("stats", None)
        self.stats = StatsDto(val) if val and not isinstance(val, StatsDto) else val
        self.tags = dictionary.get("tags", [])
        self.title = dictionary.get("title", "")


class ImageDto(object):
    def __init__(self, dictionary):
        self.full = dictionary.get("full", "")
        self.group = dictionary.get("group", "")
        self.h = dictionary.get("h", 0)
        self.sprite = dictionary.get("sprite", "")
        self.w = dictionary.get("w", 0)
        self.x = dictionary.get("x", 0)
        self.y = dictionary.get("y", 0)


class InfoDto(object):
    def __init__(self, dictionary):
        self.attack = dictionary.get("attack", 0)
        self.defense = dictionary.get("defense", 0)
        self.difficulty = dictionary.get("difficulty", 0)
        self.magic = dictionary.get("magic", 0)


class PassiveDto(object):
    def __init__(self, dictionary):
        self.description = dictionary.get("description", "")
        val = dictionary.get("image", None)
        self.image = ImageDto(val) if val and not isinstance(val, ImageDto) else val
        self.name = dictionary.get("name", "")
        self.sanitizeddescription = dictionary.get("sanitizedDescription", "")


class RecommendedDto(object):
    def __init__(self, dictionary):
        self.blocks = [(BlockDto(block) if not isinstance(block, BlockDto) else block) for block in dictionary.get("blocks", []) if block]
        self.champion = dictionary.get("champion", "")
        self.map = dictionary.get("map", "")
        self.mode = dictionary.get("mode", "")
        self.priority = dictionary.get("priority", False)
        self.title = dictionary.get("title", "")
        self.type = dictionary.get("type", "")


class BlockDto(object):
    def __init__(self, dictionary):
        self.items = [(BlockItemDto(item) if not isinstance(item, BlockItemDto) else item) for item in dictionary.get("items", []) if item]
        self.recmath = dictionary.get("recMath", False)
        self.type = dictionary.get("type", "")


class BlockItemDto(object):
    def __init__(self, dictionary):
        self.count = dictionary.get("count", 0)
        self.id = dictionary.get("id", 0)


class SkinDto(object):
    def __init__(self, dictionary):
        self.id = dictionary.get("id", 0)
        self.name = dictionary.get("name", "")
        self.num = dictionary.get("num", 0)


class ChampionSpellDto(object):
    def __init__(self, dictionary):
        """ not used """
        self.altimages = [(ImageDto(img) if not isinstance(img, ImageDto) else img) for img in dictionary.get("altimages", []) if img]
        self.cooldown = dictionary.get("cooldown", [])
        self.cooldownburn = dictionary.get("cooldownBurn", "")
        self.cost = dictionary.get("cost", [])
        self.costburn = dictionary.get("costBurn", "")
        self.costtype = dictionary.get("costType", "")
        self.description = dictionary.get("description", "")
        self.effect = dictionary.get("effect", [])
        self.effectburn = dictionary.get("effectBurn", [])
        val = dictionary.get("image", None)
        self.image = ImageDto(val) if val and not isinstance(val, ImageDto) else val
        self.key = dictionary.get("key", "")
        val = dictionary.get("leveltip", None)
        self.leveltip = LevelTipDto(val) if val and not isinstance(val, LevelTipDto) else val
        self.maxrank = dictionary.get("maxrank", 0)
        self.name = dictionary.get("name", "")
        self.range = dictionary.get("range", "self")
        self.rangeburn = dictionary.get("rangeBurn", "")
        self.resource = dictionary.get("resource", "")
        self.sanitizeddescription = dictionary.get("sanitizedDescription", "")
        self.sanitizedtooltip = dictionary.get("sanitizedTooltip", "")
        self.tooltip = dictionary.get("tooltip", "")
        self.vars = [(SpellVarsDto(svars) if not isinstance(svars, SpellVarsDto) else svars) for svars in dictionary.get("vars", []) if svars]


class LevelTipDto(object):
    def __init__(self, dictionary):
        self.effect = dictionary.get("effect", [])
        self.label = dictionary.get("label", [])


class SpellVarsDto(object):
    def __init__(self, dictionary):
        self.coeff = dictionary.get("coeff", [])
        self.dyn = dictionary.get("dyn", "")
        self.key = dictionary.get("key", "")
        self.link = dictionary.get("link", "")
        self.rankswith = dictionary.get("ranksWith", "")


class StatsDto(object):
    def __init__(self, dictionary):
        self.armor = dictionary.get("armor", 0.0)
        self.armorperlevel = dictionary.get("armorperlevel", 0.0)
        self.attackdamage = dictionary.get("attackdamage", 0.0)
        self.attackdamageperlevel = dictionary.get("attackdamageperlevel", 0.0)
        self.attackrange = dictionary.get("attackrange", 0.0)
        self.attackspeedoffset = dictionary.get("attackspeedoffset", 0.0)
        self.attackspeedperlevel = dictionary.get("attackspeedperlevel", 0.0)
        self.crit = dictionary.get("crit", 0.0)
        self.critperlevel = dictionary.get("critperlevel", 0.0)
        self.hp = dictionary.get("hp", 0.0)
        self.hpperlevel = dictionary.get("hpperlevel", 0.0)
        self.hpregen = dictionary.get("hpregen", 0.0)
        self.hpregenperlevel = dictionary.get("hpregenperlevel", 0.0)
        self.movespeed = dictionary.get("movespeed", 0.0)
        self.mp = dictionary.get("mp", 0.0)
        self.mpperlevel = dictionary.get("mpperlevel", 0.0)
        self.mpregen = dictionary.get("mpregen", 0.0)
        self.mpregenperlevel = dictionary.get("mpregenperlevel", 0.0)
        self.spellblock = dictionary.get("spellblock", 0.0)
        self.spellblockperlevel = dictionary.get("spellblockperlevel", 0.0)


class RealmDto(object):
    def __init__(self, dictionary):
        self.cdn = dictionary.get("cdn", "")
        self.css = dictionary.get("css", "")
        self.dd = dictionary.get("dd", "")
        self.l = dictionary.get("l", "")
        self.lg = dictionary.get("lg", "")
        self.n = dictionary.get("n", {})
        self.profileiconmax = dictionary.get("profileiconmax", 0)
        self.store = dictionary.get("store", "")
        self.v = dictionary.get("v", "")