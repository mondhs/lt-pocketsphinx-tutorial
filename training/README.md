Sphinx Training notes
=================================

Šiam apmokymui yra naudojami VDU-ISO4 ir VDU_TRI4 garsynas:

@inproceedings{ravskinis2003universal,
  title={Universal annotated VDU Lithuanian speech corpus},
  author={Raškinis, A and Raškinis, G and Kazlauskienė, A},
  booktitle={Proceedings of the conference “Information Technologies 2003”, KTU, Kaunas},
  pages={28--34},
  year={2003}
}

Man nepriklauso garsyno autorystės teisės ir dėl naudojimosi garsynu pirma turi susiekite su jais.


Pagrindinės directorijos:
 * etc - konfigūraciniai failai
 * wav - garsynai(dėl dydžio ištrinti) ir Transkripcija praat Textgrid formatu.
 * wav44 - turi būti saugomi mswav 16bit 44kHz formatu. skriptai iš šio katalogo transformuos į 16kHz 16bit formatą, kuris tinka Sphinx

###  Garsyno Sphinx paruošimo procedūra
 # nukopijuokite wav ir Textgrid failus į wav44. taip kad kiekviena subdirektorija atitiktų vieną kalbėtoją:
 ## wav/bj1/*,
 ## wav/lk1,
 ## wav/tk1
 ## wav/ak1.
 # Anot Sphinx garsyno failo užrašo formatas fx.Textgrid ir fx.wav yra netinkami ir turi būtinai būt pridėtas subdirektorijos vardas: fx-ak1.Textgrid ir fx-ak1.wav. Masiškai pakeisti galima su komandomis atskirai kiekvienoje subdirektorijoje: 
 ## prename  's/^(.*).wav$/$1-$SUBDIR.wav/'  *.wav #$SUBDIR reikia pakeisti į subdirektorijos pavadinimą
 ## prename  's/^(.*).Textgrid$/$1-$SUBDIR.wav/'  *.Textgrid #$SUBDIR reikia pakeisti į subdirektorijos pavadinimą
 # transformuokite iš 44kHz į 16kHz formatą: paleiskite skriptą resample_wav.sh. Šis skriptas su sox komandą transformuos tik wav failus ir transformuotus padės į wav-resample išlaikydamas subdirektorijų tvarką.
 # Rankomis nukopijuokite wav failus iš wav-resample/* ir Textgrid iš wav44/* į wav direktoriją.

### Sphinx konfigūracinių failų paruošimo procedūra
etc direktorijos failai:
 # etc kataloge turi atsidurti failai:
 # lt.dic visų mokyme naudojamų žodžiai su fonemų transkripcijomis
 # lt.phone - visų fonemų sąrašas
 # lt_train.fileids - apmokymui skirtų bylų sąrašas, be wav plėtinio
 # lt_train.transcription - apmokymui skirtų žodžių lygmens transkripcija ir skliausteliuose nusakytas garsinio failo pavadinimas be wav plėtinio
 # lt_test.fileids - testavimui skirtų bylų sąrašas, be wav plėtinio
 # lt_test.transcription - testavimui skirtų žodžių transkripcija ir skliausteliuose nusakytas garsinio failo pavadinimas be wav plėtinio

Kad gautumėte šiuos failus paruošus garsyną paleiskite skriptą: extract-word.sh. Jis iš Textgrid failų transformuos informaciją taip, kad tiktų Sphinx apmokymui ir sudės juos į target/* direktoriją. Iš target/* direktorijos paminėtus failus nukopijuokite į etc direktoriją.

Ampokinto atapintuvo patikrinimui papildomai reikia paruošti šnekos modelį: http://cmusphinx.sourceforge.net/wiki/tutoriallm. target direktorijoje paleiskite komandą:
cat lt_*.transcription >lt_all.transcription .ši komanda sujungs visų subdirektorijų frazių transkripcijas į vieną failą: lt_all.transcription. jį rankomis nukopijuokite į katalogą: /etc/languageModel. ir jame paleiskite make_lang_model.sh skriptą. Jam pasibagus turėtų būti sukrtas failas lt.lm.DMP, kurį rankomis nukopijuokite į /etc direktoriją.




Pasiruošimas baigtas.

### Sphinx apmokymas

Detaliau galite rasti informacijos: http://cmusphinx.sourceforge.net/wiki/tutorialam

Paleiskite komandą: sphinxtrain run

Jai pasibaigus rezultatus galite surasti lt.html faile. Aš gavau tokius rezultatus:

Aligning results to find error rate

SENTENCE ERROR: 18.5% (20/108) WORD ERROR RATE: 3.8% (31/810)

### Sphinx paruošimas naudojimui

Kaip rašoma čia: http://cmusphinx.sourceforge.net/wiki/tutorialadapt

Reikia PocketSphinx, kad failas model_parameters/lt.cd_cont_200/mdef būtų binarinio formato. tuomet paleiskite komanda: pocketsphinx_mdef_convert -bin model_parameters/lt.cd_cont_200/mdef model_parameters/lt.cd_cont_200/mdef

### Sphinx Naudojimas

žiūrėkite daugiau informacijos direktorijoje impl


