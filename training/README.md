Sphinx mokymo procedūros aprašai
=================================


Teisės
--------

Šiam apmokymui yra naudojami VDU-ISO4 ir VDU_TRI4 garsynas:

    @inproceedings{ravskinis2003universal,
      title={Universal annotated VDU Lithuanian speech corpus},
      author={Raškinis, A and Raškinis, G and Kazlauskienė, A},
      booktitle={Proceedings of the conference “Information Technologies 2003”, KTU, Kaunas},
      pages={28--34},
      year={2003}
    }

Man NEpriklauso garsyno autorystės teisės ir dėl naudojimosi garsynu pirma turi susiekite su jais.

Reikalavimai
--------

 * Linux


Pasiruošimas apmokymui
--------

Pagrindinės apmokymui direktorijos:
*   `training/lt/etc` - konfigūraciniai failai
*   `training/lt/wav` - garsynai(dėl dydžio ištrinti) ir Transkripcija praat Textgrid formatu.
*   `training/lt/wav44` - turi būti saugomi mswav 16bit 44kHz formatu. skriptai iš šio katalogo transformuos į 16kHz 16bit formatą, kuris tinka Sphinx

###  Garsyno Sphinx paruošimo procedūra
*   Pakeiskite absoliutų kelią iki apmokinimo direktorijos konfigūraciniame faile `training/lt/etc/sphinx_train.cfg`. `$CFG_BASE_DIR=$SOURCE_DIR/lt-pocketsphinx-tutorial/training/lt` vietoj $SOURCE_DIR turėtumete įrašyti kur nesiklonavote repozitorija.
*   Nukopijuokite wav ir Textgrid failus į wav44. taip kad kiekviena subdirektorija atitiktų vieną kalbėtoją:
    * `training/lt/wav/bj1`,
    * `training/lt/wav/lk1`,
    * `training/lt/wav/tk1`,
    * `training/lt/wav/ak1`.
*   Anot Sphinx garsyno failo užrašo formatas `fx.Textgrid` ir `fx.wav` yra netinkami ir turi būtinai būt pridėtas subdirektorijos vardas: `fx-ak1.Textgrid` ir `fx-ak1.wav`. Masiškai pakeisti galima su komandomis atskirai kiekvienoje subdirektorijoje: 
    * `prename  's/^(.*).wav$/$1-$SUBDIR.wav/'  *.wav` #$SUBDIR reikia pakeisti į subdirektorijos pavadinimą
    * `prename  's/^(.*).Textgrid$/$1-$SUBDIR.wav/'  *.Textgrid` #$SUBDIR reikia pakeisti į subdirektorijos pavadinimą
*   transformuokite iš 44kHz į 16kHz formatą: paleiskite skriptą `resample_wav.sh`. Šis skriptas su `sox` komandą transformuos tik wav failus ir transformuotus padės į `wav-resample` išlaikydamas subdirektorijų tvarką.
*   Rankomis nukopijuokite `*.wav` failus iš `training/lt/wav-resample/*/*.wav` ir Textgrid iš `training/lt/wav44/*/*.Textgrid` į `training/lt/wav` direktoriją.

### Sphinx konfigūracinių failų paruošimo procedūra
`training/lt/etc` direktorijos failai:
*   `training/lt/etc` kataloge turi atsidurti failai:
    * `lt.dic` visų mokyme naudojamų žodžiai su fonemų transkripcijomis
    * `lt.phone` - visų fonemų sąrašas
    * `lt_train.fileids` - apmokymui skirtų bylų sąrašas, be wav plėtinio
    * `lt_train.transcription` - apmokymui skirtų žodžių lygmens transkripcija ir skliausteliuose nusakytas garsinio failo pavadinimas be wav plėtinio
    * `lt_test.fileids` - testavimui skirtų bylų sąrašas, be wav plėtinio
    * `lt_test.transcription` - testavimui skirtų žodžių transkripcija ir skliausteliuose nusakytas garsinio failo pavadinimas be wav plėtinio

Kad gautumėte šiuos failus paruošus garsyną paleiskite skriptą: `extract-word.sh`. Jis iš Textgrid failų transformuos informaciją taip, kad tiktų Sphinx apmokymui ir sudės juos į `training/target/*` direktoriją. Iš `training/lt/target/*` direktorijos paminėtus failus nukopijuokite į `training/lt/etc` direktoriją.

Ampokinto atapintuvo patikrinimui papildomai reikia paruošti šnekos modelį: [Building Language Model](http://cmusphinx.sourceforge.net/wiki/tutoriallm). target direktorijoje paleiskite komandą:
`cat lt_*.transcription >lt_all.transcription` .ši komanda sujungs visų subdirektorijų frazių transkripcijas į vieną failą: `lt_all.transcription`. Jį rankomis nukopijuokite į katalogą: /etc/languageModel. Jame paleiskite `make_lang_model.sh` skriptą. Jam pasibaigus turėtų būti sukurtas failas `lt.lm.DMP`, kurį rankomis nukopijuokite į `training/lt/etc` direktoriją.


Apmokymas
--------


### Sphinx apmokymas

Detaliau galite rasti informacijos: [Training Acoustic Model For CMUSphinx](http://cmusphinx.sourceforge.net/wiki/tutorialam)

Paleiskite komandą: `sphinxtrain run`

Jai pasibaigus rezultatus galite surasti `lt.html` faile. Aš gavau tokius rezultatus:

    Aligning results to find error rate
    SENTENCE ERROR: 18.5% (20/108) WORD ERROR RATE: 3.8% (31/810)

### Sphinx paruošimas naudojimui

Kaip rašoma čia: [Adapting the default acoustic model](http://cmusphinx.sourceforge.net/wiki/tutorialadapt)

Reikia PocketSphinx, kad failas `training/lt/model_parameters/lt.cd_cont_200/mdef` būtų binarinio formato. Norint pakeisti iš tekstinio formato paleiskite komandą: `pocketsphinx_mdef_convert -bin model_parameters/lt.cd_cont_200/mdef model_parameters/lt.cd_cont_200/mdef`

Kas toliau?
--------

### Sphinx Naudojimas

Žiūrėkite daugiau informacijos direktorijoje [impl](../impl).


