from distutils.version import StrictVersion

from riotapi import riotapicontroller

from riotapi_static.models import PatchVersions
from riotapi_static.models import ModuleVersions
from riotapi_static.models import Champion
from riotapi_static.models import Image
from riotapi_static.models import Info
from riotapi_static.models import Passive
from riotapi_static.models import ChampionStats
from riotapi_static.models import ChampionAllyTip
from riotapi_static.models import ChampionEnemyTip
from riotapi_static.models import ChampionTag
from riotapi_static.models import Recommended
from riotapi_static.models import Block
from riotapi_static.models import BlockItem
from riotapi_static.models import Skin
from riotapi_static.models import ChampionSpell
from riotapi_static.models import ChampionSpellCooldown
from riotapi_static.models import ChampionSpellCost
from riotapi_static.models import ChampionSpellEffectA
from riotapi_static.models import ChampionSpellEffectB
from riotapi_static.models import ChampionSpellEffectBurn
from riotapi_static.models import LevelTipEffect
from riotapi_static.models import LevelTipLabel
from riotapi_static.models import ChampionSpellRange
from riotapi_static.models import SpellVars
from riotapi_static.models import SpellVarsCoeff

class LeagueMainsUpdater:

    def __init__(self):
        self.riotcontroller = riotapicontroller.RiotApiController("592839cb-d4a2-4bee-84e8-4f23ef80135e")
        self.latestchampionlist = None

    """
    Update and create data
    """
    def update(self):
        self.update_champions()

    """
    Add new patch versions to existing patch versions
    """
    def update_patchlist(self, _patchversion, _module):
        patchlist = PatchVersions.objects.filter(patch_version__exact=_patchversion)
        """ add or query the specified patch """
        if patchlist.count() == 0:
            new_patch = PatchVersions(patch_version=_patchversion)
            new_patch.save()
        else:
            new_patch = PatchVersions.objects.get(patch_version__exact=_patchversion)
        """ update the specified module version to the specified version """
        try:
            moduleversion = ModuleVersions.objects.get(pk_module_name=_module)
        except Exception as e:
            moduleversion = ModuleVersions(pk_module_name=_module)
        moduleversion.module_version = new_patch
        moduleversion.save()
        return new_patch

    """
    Create champions that do not exist and update champions which already do exist
    """
    def update_champions(self):
        mostrecentapiversion = self.riotcontroller.get_realms("euw").n['champion']
        try:
            leaguemainsversion = ModuleVersions.objects.get(pk_module_name='champion')
        except Exception as e:
            leaguemainsversion = None
        """ only update when no version is available or when there is a more recent version available at the api """
        if (leaguemainsversion is None) or (StrictVersion(mostrecentapiversion) > StrictVersion(leaguemainsversion.module_version.patch_version)):
            self.latestchampionlist = self.riotcontroller.get_championlist(version=mostrecentapiversion)
            champion_counter = 0
            for new_name, new_data in self.latestchampionlist.data.items():
                champion_counter += 1
                print("[ " + str(champion_counter) + " / " + str(len(self.latestchampionlist.data.items())) + " ]: " + new_name)
                championlist = Champion.objects.filter(pk_id__exact=new_data.id)
                if championlist.count() == 0:
                    self.update_champion(new_data, mostrecentapiversion, _isupdate=False)
                else:
                    self.update_champion(new_data, mostrecentapiversion, _isupdate=True)
            self.update_patchlist(mostrecentapiversion, 'champion')
            return True
        else:
            return False

    """
    Create champion that does not exist yet by a ChampionDto
    """
    def update_champion(self, _championdata, _version, _isupdate=False):
        """ champion image """
        if not _isupdate:
            newchampion_image = Image()
        else:
            newchampion_image = Champion.objects.get(pk_id__exact=_championdata.id).image
        newchampion_image.full = _championdata.image.full
        newchampion_image.group = _championdata.image.group
        newchampion_image.h = _championdata.image.h
        newchampion_image.sprite = _championdata.image.sprite
        newchampion_image.w = _championdata.image.w
        newchampion_image.x = _championdata.image.x
        newchampion_image.y = _championdata.image.y
        newchampion_image.path = "versions/" + _version + "/img/champion/" + _championdata.image.full
        newchampion_image.save()
        """ champion info """
        if not _isupdate:
            newchampion_info = Info()
        else:
            newchampion_info = Champion.objects.get(pk_id__exact=_championdata.id).info
        newchampion_info.attack = _championdata.info.attack
        newchampion_info.defense = _championdata.info.defense
        newchampion_info.difficulty = _championdata.info.difficulty
        newchampion_info.magic = _championdata.info.magic
        newchampion_info.save()
        """ champion passive image """
        if not _isupdate:
            newchampion_passive_image = Image()
        else:
            newchampion_passive_image = Champion.objects.get(pk_id__exact=_championdata.id).passive.image
        newchampion_passive_image.full = _championdata.passive.image.full
        newchampion_passive_image.group = _championdata.passive.image.group
        newchampion_passive_image.h = _championdata.passive.image.h
        newchampion_passive_image.sprite = _championdata.passive.image.sprite
        newchampion_passive_image.w = _championdata.passive.image.w
        newchampion_passive_image.x = _championdata.passive.image.x
        newchampion_passive_image.y = _championdata.passive.image.y
        newchampion_passive_image.path = "versions/" + _version + "/img/passive/" + _championdata.passive.image.full
        newchampion_passive_image.save()
        """ champion passive """
        if not _isupdate:
            newchampion_passive = Passive()
        else:
            newchampion_passive = Champion.objects.get(pk_id__exact=_championdata.id).passive
        newchampion_passive.description = _championdata.passive.description
        newchampion_passive.name = _championdata.passive.name
        newchampion_passive.sanitizeddescription = _championdata.passive.sanitizeddescription
        newchampion_passive.image = newchampion_passive_image
        newchampion_passive.save()
        """ champion stats """
        if not _isupdate:
            newchampion_stats = ChampionStats()
        else:
            newchampion_stats = Champion.objects.get(pk_id__exact=_championdata.id).stats
        newchampion_stats.armor = _championdata.stats.armor
        newchampion_stats.armorperlevel = _championdata.stats.armorperlevel
        newchampion_stats.attackdamage = _championdata.stats.attackdamage
        newchampion_stats.attackdamageperlevel = _championdata.stats.attackdamageperlevel
        newchampion_stats.attackrange = _championdata.stats.attackrange
        newchampion_stats.attackspeedoffset = _championdata.stats.attackspeedoffset
        newchampion_stats.attackspeedperlevel = _championdata.stats.attackspeedperlevel
        newchampion_stats.crit = _championdata.stats.crit
        newchampion_stats.hp = _championdata.stats.hp
        newchampion_stats.hpperlevel = _championdata.stats.hpperlevel
        newchampion_stats.hpregen = _championdata.stats.hpregen
        newchampion_stats.hpregenperlevel = _championdata.stats.hpregenperlevel
        newchampion_stats.movespeed = _championdata.stats.movespeed
        newchampion_stats.mp = _championdata.stats.mp
        newchampion_stats.mpperlevel = _championdata.stats.mpperlevel
        newchampion_stats.mpregen = _championdata.stats.mpregen
        newchampion_stats.mpregenperlevel = _championdata.stats.mpregenperlevel
        newchampion_stats.spellblock = _championdata.stats.spellblock
        newchampion_stats.spellblockperlevel = _championdata.stats.spellblockperlevel
        newchampion_stats.save()
        """ champion data, already created or queried at the start """
        if not _isupdate:
            newchampion = Champion(pk_id=_championdata.id)
        else:
            newchampion = Champion.objects.get(pk_id__exact=_championdata.id)
        newchampion.blurb = _championdata.blurb
        newchampion.image = newchampion_image
        newchampion.info = newchampion_info
        newchampion.key = _championdata.key
        newchampion.lore = _championdata.lore
        newchampion.name = _championdata.name
        newchampion.partype = _championdata.partype
        newchampion.passive = newchampion_passive
        newchampion.stats = newchampion_stats
        newchampion.title = _championdata.title
        newchampion.save()
        """ champion ally tips """
        db_allytips = ChampionAllyTip.objects.filter(fk_champion=newchampion)
        for db_allytip in db_allytips:
            db_allytip.delete()
        for allytip in _championdata.allytips:
            championallytip = ChampionAllyTip()
            championallytip.championallytip = allytip
            championallytip.fk_champion = newchampion
            championallytip.save()
        """ champion enemy tips """
        db_enemytips = ChampionEnemyTip.objects.filter(fk_champion=newchampion)
        for db_enemytip in db_enemytips:
            db_enemytip.delete()
        for enemytip in _championdata.enemytips:
            championenemytip = ChampionEnemyTip()
            championenemytip.championenemytip = enemytip
            championenemytip.fk_champion = newchampion
            championenemytip.save()
        """ champion tags """
        db_championtags = ChampionTag.objects.filter(fk_champion=newchampion)
        for db_championtag in db_championtags:
            db_championtag.delete()
        for tag in _championdata.tags:
            championtag = ChampionTag()
            championtag.championtag = tag
            championtag.fk_champion = newchampion
            championtag.save()
        """ champion recommended, blocks and block items"""
        db_recommendeds = Recommended.objects.filter(fk_champion=newchampion)
        for db_recommended in db_recommendeds:
            db_blocks = Block.objects.filter(fk_recommended=db_recommended)
            for db_block in db_blocks:
                db_blockitems = BlockItem.objects.filter(fk_block=db_block)
                for db_blockitem in db_blockitems:
                    db_blockitem.delete()
                db_block.delete()
            db_recommended.delete()
        for recommended in _championdata.recommended:
            newrecommended = Recommended()
            newrecommended.champion = recommended.champion
            newrecommended.map = recommended.map
            newrecommended.mode = recommended.mode
            newrecommended.priority = recommended.priority
            newrecommended.title = recommended.title
            newrecommended.type = recommended.type
            newrecommended.fk_champion = newchampion
            newrecommended.save()
            for block in recommended.blocks:
                newblock = Block()
                newblock.recmath = block.recmath
                newblock.type = block.type
                newblock.fk_recommended = newrecommended
                newblock.save()
                for blockitem in block.items:
                    newblockitem = BlockItem()
                    newblockitem.id = blockitem.id
                    newblockitem.count = blockitem.count
                    newblockitem.fk_block = newblock
                    newblockitem.save()
        """ champion skin loading screen """
        db_skins = Skin.objects.filter(fk_champion=newchampion)
        for db_skin in db_skins:
            db_skin.delete()
        for skin in _championdata.skins:
            newchampion_skin = Skin()
            newchampion_skin.id = skin.id
            newchampion_skin.name = skin.name
            newchampion_skin.num = skin.num
            newchampion_skin.fk_champion = newchampion
            newchampion_skin_loading = Image()
            newchampion_skin_loading.path = "versions/" + _version + "/img/champion/loading/" + newchampion.name + "_" + str(skin.num) + ".jpg"
            newchampion_skin_loading.save()
            newchampion_skin.loading = newchampion_skin_loading
            newchampion_skin_splash = Image()
            newchampion_skin_splash.path = "versions/" + _version + "/img/champion/splash/" + newchampion.name + "_" + str(skin.num) + ".jpg"
            newchampion_skin_splash.save()
            newchampion_skin.splash = newchampion_skin_splash
            newchampion_skin.save()
        """ champion spells and featured values """
        db_spells = ChampionSpell.objects.filter(fk_champion=newchampion)
        for db_spell in db_spells:
            db_spell.delete()
            """ TODO: maybe clear all other spell stuff either? """
        for spell in _championdata.spells:
            newchampion_spell = ChampionSpell()
            newchampion_spell.cooldownburn = spell.cooldownburn
            newchampion_spell.costburn = spell.costburn
            newchampion_spell.costtype = spell.costtype
            newchampion_spell.description = spell.description
            newchampion_spell_image = Image()
            newchampion_spell_image.full = spell.image.full
            newchampion_spell_image.group = spell.image.group
            newchampion_spell_image.h = spell.image.h
            newchampion_spell_image.sprite = spell.image.sprite
            newchampion_spell_image.w = spell.image.w
            newchampion_spell_image.x = spell.image.x
            newchampion_spell_image.y = spell.image.y
            newchampion_spell_image.path = "versions/" + _version + "/img/spell/" + spell.image.full
            newchampion_spell_image.save()
            newchampion_spell.image = newchampion_spell_image
            newchampion_spell.key = spell.key
            newchampion_spell.maxrank = spell.maxrank
            newchampion_spell.name = spell.name
            if spell.range is "self":
                newchampion_spell.isranged = False
            else:
                newchampion_spell.isranged = True
            newchampion_spell.rangeburn = spell.rangeburn
            newchampion_spell.resource = spell.resource
            newchampion_spell.sanitizeddescription = spell.sanitizeddescription
            newchampion_spell.sanitizedtooltip = spell.sanitizedtooltip
            newchampion_spell.tooltip = spell.tooltip
            newchampion_spell.fk_champion = newchampion
            newchampion_spell.save()
            """ champion spell cooldowns """
            for spellcooldown in spell.cooldown:
                newchampion_spell_cooldown = ChampionSpellCooldown()
                newchampion_spell_cooldown.championspellcooldown = spellcooldown
                newchampion_spell_cooldown.fk_championspell = newchampion_spell
                newchampion_spell_cooldown.save()
            """ champion spell costs """
            for spellcost in spell.cost:
                newchampion_spell_cost = ChampionSpellCost()
                newchampion_spell_cost.championspellcost = spellcost
                newchampion_spell_cost.fk_championspell = newchampion_spell
                newchampion_spell_cost.save()
            """ champion spell effects, first and second level """
            for spelleffect in spell.effect:
                newchampion_spell_effect_a = ChampionSpellEffectA()
                newchampion_spell_effect_a.fk_championspell = newchampion_spell
                newchampion_spell_effect_a.save()
                if spelleffect is not None:
                    for spelleffect_b in spelleffect:
                        newchampion_spell_effect_b = ChampionSpellEffectB()
                        newchampion_spell_effect_b.championspelleffect_b = spelleffect_b
                        newchampion_spell_effect_b.fk_championspelleffect_a = newchampion_spell_effect_a
                        newchampion_spell_effect_b.save()
            """ champion spell effect burn """
            for spelleffectburn in spell.effectburn:
                newchampion_spell_effectburn = ChampionSpellEffectBurn()
                newchampion_spell_effectburn.championspelleffectburn = spelleffectburn
                newchampion_spell_effectburn.fk_championspell = newchampion_spell
                newchampion_spell_effectburn.save()
            """ champion spell level tip effect """
            for spellleveltipeffect in spell.leveltip.effect:
                newchampion_spell_leveltip_effect = LevelTipEffect()
                newchampion_spell_leveltip_effect.leveltipeffect = spellleveltipeffect
                newchampion_spell_leveltip_effect.fk_championspell = newchampion_spell
                newchampion_spell_leveltip_effect.save()
            """ champion spell level tip label """
            for spellleveltiplabel in spell.leveltip.label:
                newchampion_spell_leveltip_label = LevelTipLabel()
                newchampion_spell_leveltip_label.leveltiplabel = spellleveltiplabel
                newchampion_spell_leveltip_label.fk_championspell = newchampion_spell
                newchampion_spell_leveltip_label.save()
            """ champion spell range """
            if newchampion_spell.isranged:
                for spellrange in spell.range:
                    newchampion_spell_range = ChampionSpellRange()
                    newchampion_spell_range.championspellrange = spellrange
                    newchampion_spell_range.fk_championspell = newchampion_spell
                    newchampion_spell_range.save()
            """ champion spell vars """
            for spellvars in spell.vars:
                newchampion_spell_vars = SpellVars()
                newchampion_spell_vars.dyn = spellvars.dyn
                newchampion_spell_vars.key = spellvars.key
                newchampion_spell_vars.link = spellvars.link
                newchampion_spell_vars.rankswith = spellvars.rankswith
                newchampion_spell_vars.fk_championspell = newchampion_spell
                newchampion_spell_vars.save()
                for spellvars_coeff in spellvars.coeff:
                    newchampion_spell_vars_coeff = SpellVarsCoeff()
                    newchampion_spell_vars_coeff.coeff = spellvars_coeff
                    newchampion_spell_vars_coeff.fk_spellvars = newchampion_spell_vars
                    newchampion_spell_vars_coeff.save()
        return