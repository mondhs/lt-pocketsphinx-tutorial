PocketSphinx panaudojimas su Lietuvišku modeliu
=================================


Įvadas
--------------

Čia aprašoma kaip naudotis į PocketSphninx lietuvių kalbos šnekos atpažinimui.


Reikalavimai
--------

 * Linux
 * Apmokintas Sphinx Model [training](../training). 

### PocketSphinx

Sukompiliuoti ir įdiegti nightly snapshot sphinxbase ir pocketsphinx iš [CMU Sphinx Download](http://cmusphinx.sourceforge.net/wiki/download/)
 

Gramatika grįstas aptikimas
--------------------------

### JSGF

Lengviausiai šnekos atpažinimui yra naudoti kalbos modelio gramatikos žinias. Tarkim norime komanduoti robotui, kuris gali važiuoti pirmyn, atgal sukti kairėn ir dešinėn. Tuomet reikia, kad robotas suprastu komandas " varyk pirmyn", "varyk penkis metrus atgal", "suk dešinėn" ir pan. Visų pirmiausiai, turime nusakyti komandų gramatiką(kokios žodžių struktūros komandos turėtų būti sakomos). PocketSphinx gramatiką saugo JSGF formatu. Aptartam pavyzdžiui gramatika atrodo taip:

    #JSGF V1.0;
    
    grammar robotas;
    
    public <COMMAND> = <EIK> | <SUK>;
    <EIK> = (EIK | VARYK ) [ ( VIENĄ | DU | TRIS | KETURIS | PENKIS ) METRUS ] (PIRMYN | ATGAL);
    <SUK> = (SUK | GRĘŽKIS ) ( KAIRĖN | DEŠINĖN );

Ši informacija turi būti saugoma `impl/models/lm/robotas.gram` faile.

### Tarimų žodynas

Šnekos atpažinimui yra reikalingas tarimų žodynas šnekai(taip kaip raidynas aprašyti tekstui), kad būtų galima užrašyti žodžių tarimą naudojantis fonemomis.

Pradžioje kuriant tarimų žodyną, sukurkite direktoriją `scripts` su dviems skriptais: `scripts/extract_jsgf_vocabulary.sh` išrenka JSGF bylas, scripts/est-l2p.py sugeneruoja žodžių tarimą. Norint sugeneruoti tarimų žodyną, kuris turi būti `models/lm/robotas.gram` paleiskite scriptą:

    ./scripts/extract_jsgf_vocabulary.sh models/lm/robotas.gram | ./scripts/lt-l2p.py > models/dict/robotas.dict

    
Sugeneruota (`robotas.dict`):

    ATGAL A T G A L
    DEŠINĖN D E SH IH N EH N
    DU D UH
    EIK EI K
    GRĘŽKIS G R EA ZH K IH S
    KAIRĖN K AI R EH N
    KETURIS K E T UH R IH S
    METRUS M E T R UH S
    PENKIS P E N K IH S
    PIRMYN P IH R M IY N
    SUK S UH K
    TRIS T R IH S
    VARYK V A R IY K
    VIENĄ V IE N AA


### Paleidimas

Nusikopijuokite rankomis apmokintą garsyno modelį [lt.cd_cont_200](../training/lt/model_parameters/lt.cd_cont_200) į `models/hmm`

Lengviausias būdas išbandyti šnekos atpažintuvą pasinaudojant komanda `pocketsphinx_continuous`. Paleiskite:

    pocketsphinx_continuous -hmm models/hmm/lt.cd_cont_200 -jsgf models/lm/robotas.gram -dict models/dict/robotas.dict
    
Ištarkite į mikrofoną `sul dešinėn`. Ekrane turi pasirodyti:

    [..]
    INFO: fsg_search.c(1417): Start node <sil>.0:2:17
    INFO: fsg_search.c(1417): Start node <sil>.0:2:17
    INFO: fsg_search.c(1417): Start node <sil>.0:2:17
    INFO: fsg_search.c(1456): End node DEŠINĖN.30:60:87 (-1618)
    INFO: fsg_search.c(1680): lattice start node <s>.0 end node DEŠINĖN.30
    INFO: ps_lattice.c(1365): Normalizer P(O) = alpha(DEŠINĖN:30:87) = -59135
    INFO: ps_lattice.c(1403): Joint P(O,S) = -59135 P(S|O) = 0
    000000001: SUK DEŠINĖN
    READY....



### Atpažintuvo patikrinimas

Šnekos atpažintuvas lengva išbandyti su pateiktais audio failais. Direktorijoje `test/audio` rasite 3 failus. Kiekviename faile yra įrašytos ištartos komandos.

Norint išbandyti atpažintuvą su jau esančiais audiofailais reikia naudoti komandą: `pocketsphinx_batch`. Kaip argumento ši komanda reikalauja konfiguracinio failo pavizdys yra  `test/pocketsphinx.conf`.

Paleiskite (kataloge `test`):

    pocketsphinx_batch pocketsphinx.conf

Atpažintos komandos bus įrašytos `target/rezultatai.hyp`:

    VARYK PENKIS METRUS ATGAL (eik_5m_atgal-16k -7555)
    SUK DEŠINĖN (suk_deshinen-16k -3853)
    VARYK PIRMYN (varyk_pirmyn-16k -4927)

Kiekvienoje eilutėje yra komanda ir skliausteliuose nurodomas failo vardas ir atpažinimo taškai.



### Integracija

PocketSphinx lengva integruoti su kitomis komandomis. Tai turėtų būti aprašoma atskirame apraše.
