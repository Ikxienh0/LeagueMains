from django.db import models


class PatchVersions(models.Model):
    pk_patch_id = models.AutoField(primary_key=True)
    patch_version = models.CharField(max_length=20)
    patch_date = models.DateField(auto_now_add=True)


class ModuleVersions(models.Model):
    pk_module_name = models.CharField(primary_key=True, max_length=50)
    module_version = models.ForeignKey(PatchVersions)


class Image(models.Model):
    pk_image_id = models.AutoField(primary_key=True)
    full = models.CharField(max_length=100, null=True)
    group = models.CharField(max_length=100, null=True)
    h = models.IntegerField(null=True)
    sprite = models.CharField(max_length=100, null=True)
    w = models.IntegerField(null=True)
    x = models.IntegerField(null=True)
    y = models.IntegerField(null=True)
    path = models.CharField(max_length=100, null=True)


class Info(models.Model):
    pk_info_id = models.AutoField(primary_key=True)
    attack = models.IntegerField()
    defense = models.IntegerField()
    difficulty = models.IntegerField()
    magic = models.IntegerField()


class Passive(models.Model):
    pk_passive_id = models.AutoField(primary_key=True)
    description = models.TextField()
    image = models.ForeignKey(Image)
    name = models.CharField(max_length=100)
    sanitizeddescription = models.TextField()


class ChampionStats(models.Model):
    pk_championstats_id = models.AutoField(primary_key=True)
    armor = models.DecimalField(max_digits=10, decimal_places=6)
    armorperlevel = models.DecimalField(max_digits=10, decimal_places=6)
    attackdamage = models.DecimalField(max_digits=10, decimal_places=6)
    attackdamageperlevel = models.DecimalField(max_digits=10, decimal_places=6)
    attackrange = models.DecimalField(max_digits=10, decimal_places=6)
    attackspeedoffset = models.DecimalField(max_digits=10, decimal_places=6)
    attackspeedperlevel = models.DecimalField(max_digits=10, decimal_places=6)
    crit = models.DecimalField(max_digits=10, decimal_places=6)
    hp = models.DecimalField(max_digits=10, decimal_places=6)
    hpperlevel = models.DecimalField(max_digits=10, decimal_places=6)
    hpregen = models.DecimalField(max_digits=10, decimal_places=6)
    hpregenperlevel = models.DecimalField(max_digits=10, decimal_places=6)
    movespeed = models.DecimalField(max_digits=10, decimal_places=6)
    mp = models.DecimalField(max_digits=10, decimal_places=6)
    mpperlevel = models.DecimalField(max_digits=10, decimal_places=6)
    mpregen = models.DecimalField(max_digits=10, decimal_places=6)
    mpregenperlevel = models.DecimalField(max_digits=10, decimal_places=6)
    spellblock = models.DecimalField(max_digits=10, decimal_places=6)
    spellblockperlevel = models.DecimalField(max_digits=10, decimal_places=6)


class Champion(models.Model):
    blurb = models.TextField()
    pk_id = models.IntegerField(primary_key=True)
    image = models.ForeignKey(Image, null=True)
    info = models.ForeignKey(Info, null=True)
    key = models.CharField(max_length=100)
    lore = models.TextField()
    name = models.CharField(max_length=100)
    partype = models.CharField(max_length=100)
    passive = models.ForeignKey(Passive, null=True)
    stats = models.ForeignKey(ChampionStats, null=True)
    title = models.CharField(max_length=100)


class ChampionAllyTip(models.Model):
    pk_championallytip_id = models.AutoField(primary_key=True)
    championallytip = models.TextField()
    fk_champion = models.ForeignKey(Champion, related_name='allytips')


class ChampionEnemyTip(models.Model):
    pk_championenemytip_id = models.AutoField(primary_key=True)
    championenemytip = models.TextField()
    fk_champion = models.ForeignKey(Champion, related_name='enemytips')


class ChampionTag(models.Model):
    pk_championtag_id = models.AutoField(primary_key=True)
    championtag = models.CharField(max_length=100)
    fk_champion = models.ForeignKey(Champion, related_name='tags')


class Recommended(models.Model):
    pk_recommended_id = models.AutoField(primary_key=True)
    champion = models.CharField(max_length=100)
    map = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)
    priority = models.BooleanField()
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    fk_champion = models.ForeignKey(Champion, related_name='recommended')


class Block(models.Model):
    pk_block_id = models.AutoField(primary_key=True)
    recmath = models.BooleanField()
    type = models.CharField(max_length=100)
    fk_recommended = models.ForeignKey(Recommended, related_name='blocks')


class BlockItem(models.Model):
    pk_blockitem_id = models.AutoField(primary_key=True)
    id = models.IntegerField()
    count = models.IntegerField()
    fk_block = models.ForeignKey(Block, related_name='items')


class Skin(models.Model):
    pk_skin_id = models.AutoField(primary_key=True)
    id = models.IntegerField()
    name = models.CharField(max_length=100)
    num = models.IntegerField()
    loading = models.ForeignKey(Image, related_name='loading', on_delete=models.CASCADE)
    splash = models.ForeignKey(Image, related_name='splash', on_delete=models.CASCADE)
    fk_champion = models.ForeignKey(Champion, related_name='skins')


class ChampionSpell(models.Model):
    pk_championspell_id = models.AutoField(primary_key=True)
    cooldownburn = models.CharField(max_length=20)
    costburn = models.CharField(max_length=20)
    costtype = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ForeignKey(Image)
    key = models.CharField(max_length=100)
    maxrank = models.IntegerField()
    name = models.CharField(max_length=100)
    isranged = models.BooleanField()
    rangeburn = models.CharField(max_length=20)
    resource = models.CharField(max_length=100)
    sanitizeddescription = models.TextField()
    sanitizedtooltip = models.TextField()
    tooltip = models.TextField()
    fk_champion = models.ForeignKey(Champion, related_name='spells')


class ChampionSpellCooldown(models.Model):
    pk_championspellcooldown_id = models.AutoField(primary_key=True)
    championspellcooldown = models.DecimalField(max_digits=10, decimal_places=6)
    fk_championspell = models.ForeignKey(ChampionSpell, related_name='cooldown', on_delete=models.CASCADE)


class ChampionSpellCost(models.Model):
    pk_championspellcost_id = models.AutoField(primary_key=True)
    championspellcost = models.IntegerField()
    fk_championspell = models.ForeignKey(ChampionSpell, related_name='cost', on_delete=models.CASCADE)


class ChampionSpellEffectA(models.Model):
    pk_championspelleffects_a_id = models.AutoField(primary_key=True)
    championspelleffect_a = models.DecimalField(max_digits=12, decimal_places=6, null=True)
    fk_championspell = models.ForeignKey(ChampionSpell, related_name='effect', on_delete=models.CASCADE)


class ChampionSpellEffectB(models.Model):
    pk_championspelleffects_b_id = models.AutoField(primary_key=True)
    championspelleffect_b = models.DecimalField(max_digits=12, decimal_places=6)
    fk_championspelleffect_a = models.ForeignKey(ChampionSpellEffectA, related_name='additonal_championspelleffects', on_delete=models.CASCADE)


class ChampionSpellEffectBurn(models.Model):
    pk_championspelleffectburn_id = models.AutoField(primary_key=True)
    championspelleffectburn = models.CharField(max_length=20)
    fk_championspell = models.ForeignKey(ChampionSpell, related_name='effectBurn', on_delete=models.CASCADE)


class LevelTipEffect(models.Model):
    pk_leveltipeffects_id = models.AutoField(primary_key=True)
    leveltipeffect = models.TextField()
    fk_championspell = models.ForeignKey(ChampionSpell, related_name='leveltip_effect', on_delete=models.CASCADE)


class LevelTipLabel(models.Model):
    pk_leveltiplabels_id = models.AutoField(primary_key=True)
    leveltiplabel = models.TextField()
    fk_championspell = models.ForeignKey(ChampionSpell, related_name='leveltip_label', on_delete=models.CASCADE)


class ChampionSpellRange(models.Model):
    pk_championspellrange_id = models.AutoField(primary_key=True)
    championspellrange = models.IntegerField()
    fk_championspell = models.ForeignKey(ChampionSpell, related_name='range', on_delete=models.CASCADE)


class SpellVars(models.Model):
    pk_spellvars_id = models.AutoField(primary_key=True)
    dyn = models.CharField(max_length=20)
    key = models.CharField(max_length=20)
    link = models.CharField(max_length=20)
    rankswith = models.CharField(max_length=20)
    fk_championspell = models.ForeignKey(ChampionSpell, related_name='vars', on_delete=models.CASCADE)


class SpellVarsCoeff(models.Model):
    pk_spellvarscoeff_id = models.AutoField(primary_key=True)
    coeff = models.DecimalField(max_digits=10, decimal_places=6)
    fk_spellvars = models.ForeignKey(SpellVars, related_name='coeff', on_delete=models.CASCADE)