Sphinx mokymo procedūros aprašai(Antra Fazė)
=================================

Šis mokymas naudoja liepa garyno direktorijų struktūrą. Pagrindai yra naudoti iš pirmos mokymo fazės:  [Sphinx mokymo procedūros aprašai(Pirma fazė)](..)

Reikalavimai
--------

 * Linux


Pasiruošimas apmokymui
--------
Pagrindinės apmokymui direktorijos:
*   `training/lt-faze2/etc` - konfigūraciniai failai
*   `training/lt-faze2/tool` - apmokymo paruošimo įrankiai
*   `training/lt-faze2/wav` - garsynai(dėl dydžio ištrinti) ir sakinių transkripcija txt formatu.
  *   `training/lt-faze2/wav/S003Aa` - S003Aa diktoriaus direktorija. Rankomis kurti nereikia.
  *   `training/lt-faze2/wav/S003Aa/001_01-S003Aa.wav` - Sakinio garso failas. S003Aa diktoriaus kodas, 001_01 sakinio unikalus kodas.Rankomis kurti nereikia.
*   `training/lt-faze2/wav22` - turi būti saugomi mswav 16bit 22kHz formatu. skriptai iš šio katalogo transformuos į 16kHz 16bit formatą, kuris tinka Sphinx.Rankomis kurti nereikia.
  *   `training/lt-faze2/wav22/D00` - Diktoriaus direktorija. Rankomis kurti nereikia.
  *   `training/lt-faze2/wav22/D00/S00` - Sakinių direktorija. Rankomis kurti nereikia.
  *   `training/lt-faze2/wav22/D00/S00/S003Aa_001_01.wav` - Sakinio garso failas. S003Aa diktoriaus kodas, 001_01 sakinio unikalus kodas. Rankomis kurti nereikia.
*   `training/lt-faze2/target` - Laikini skaičiavimo failai scriptų. Reikia sukurti rankomis




###  Garsyno Sphinx paruošimo procedūra

*   Pakeiskite absoliutų kelią iki apmokinimo direktorijos konfigūraciniame faile `training/lt-faze2/etc/sphinx_train.cfg`. `$CFG_BASE_DIR=$SOURCE_DIR/lt-pocketsphinx-tutorial/training/lt` vietoj $SOURCE_DIR turėtumete įrašyti kur nesiklonavote repozitorija.
*   Pakeiskite absoliutų kelią iki wav22 direktorijos skript faile `training/lt-faze2/tool/01_transform_files.py`. `src_dir = "<CORPUS_DIR>"` vietoj <CORPUS_DIR> turėtumete įrašyti kur yra garsynas diske.
*   Sukurkite klaidų loginimo direktoriją `/tmp/liepa/transform_files.log`. jei norite logus rašyti kitur skript faile `training/lt-faze2/tool/01_transform_files.py` pakeiskite `logging.basicConfig(filename='/tmp/liepa/transform_files.log',level=logging.DEBUG)`
   * Scriptas pakeis patikrins ar nėra klaidų struktūroje, katalogų struktūra, failų vardūs ir kvandavimo dažnį iš 22kHz į 16kHz. Naudojama sox bilioteka
*   Paleiksite `training/lt-faze2/tool/01_transform_files.py`. jei viskas gerai užsipildys wav direktorija
*   Paleiskite `training/lt-faze2/tool/02_extract_dict.py` - skriptas iš failų esančių `wav` direktorijoje sukonstruos `target` direktorijoje  `*.transcription` ir `*.fileids` failus. 
  *   Skriptas unifikuos kodavimą į utf-8. Bus vykdoma patikra nekorektiškų simbolių, gramatikos klaidos su `hunspell` biblioteka.
*   Paleiskite `training/lt-faze2/tool/03_combine_sentences.py` - skriptas iš failų esnačių target direkotorijoje sujungs transkripsijos failus ir sukurs apmokymo ir testavimo duomenų aibes `_test.transcription`, `_train.transcription`,  `_test.fileids`, `_train.fileids`
*   Paleiskite `training/lt-faze2/tool/04_generate_phonemes.py` - naudojant `transcribe.exe`(nėra sukomitinta, reik prašyti atskirai), bus transformuoti visų sakinių žodžiai iš grafemų į fonemas. taip sukuriant žodyną `*.dic` ir visų fonemų sąrašą: `*.phone` 
* iš `target` į `etc` nukopijuokite rankomis failus: `liepa_all.transcription, liepa.dic, liepa.phone, liepa_test.fileids, liepa_test.transcription, liepa_train.fileids, liepa_train.transcription`.
* Paleiskite scipta kalbos modelio eksperimentui sukurti: `training/lt-faze2/etc/languageModel/make_lang_model.sh`. jis paims `etc/liepa_all.transcription` ir sugeneruos `etc/liepa.lm.DMP`
* Paleiskite skripta `start_training.sh`. Mokymas prasidėjo

Apmokymas
--------

Daugiau detalių  [Sphinx mokymo procedūros aprašai(Pirma fazė)](..).

Pasibaigus apmokymams rezultatus galite surasti `liepa.html` faile. Aš gavau tokius rezultatus:

        SENTENCE ERROR: 41.6% (247/594) WORD ERROR RATE: 10.4% (572/5481)

