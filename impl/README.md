PocketSphinx panaudojimas su Lietuvišku modeliu
=================================


Įvadas
--------------

Čia aprašoma kaip naudotis į PocketSphninx lietuvių kalbos šnekos atpažinimui.


Reikalavimai
--------

 * Linux
 
### PocketSphinx

Sukompiliuoti ir įdiegti nightly snapshot sphinxbase ir pocketsphinx iš http://cmusphinx.sourceforge.net/wiki/download/
 

Gramatika grįstas aptikimas
--------------------------

### JSGF

Lengviausiai šnekos atpažinimui yra naudoti kalbos modelio gramatikos žinias. Tarkim norime komanduoti robotui, kuris gali važiuoti pirmyn, atgal sukti kairėn ir dešinėn. Tuomet reikia, kad robotas suprastu komandas " eik pirmyn", "eik penkis metrus atgal", "suk dešinėn" ir pan. Visų pirmiausiai, turime nusakyti komandų gramatiką(kokios žodžių struktūros komandos turėtų būti sakomos). PocketSphinx gramatiką saugo JSGF formatu. Aptartam pavyzdžiui gramatika atrodo taip:

    #JSGF V1.0;

    grammar robot;

    public <command> = <eik> | <suk>;
    <eik> = (eik | varyk ) [ ( vieną | du | tris | keturis | penkis ) metrus ] (pirmyn | atgal);
    <suk> = (suk | gręžkis ) ( kairėn | dešinėn );
  
Ši informacija turi būti saugoma `robot.jsgf` faile.

### Tarimų žodynas

Šnekos atpažinimui yra reikalingas tarimų žodynas šnekai(taip kaip raidynas aprašyti tekstui), kad būtų galima užrašyti žodžių tarimą naudojantis fonemomis.

Pradžioje kuriant tarimų žodyną, sukurkite direktoriją `scripts` su dviems skriptais: `scripts/extract_jsgf_vocabulary.sh` išrenka JSGF bylas, scripts/est-l2p.py sugeneruoja žodžių tarimą. Norint sugeneruoti tarimų žodyną, kuris turi būti `models/lm/robot.jsgf` paleiskite scriptą:

    ./scripts/extract_jsgf_vocabulary.sh models/lm/robot.jsgf | ./scripts/lt-l2p.py > robot.dict

    
Sugeneruota (`robot.dict`):

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

Lengviausias būdas išbandyti šnekos atpažintuvą pasinaudojant komanda `pocketsphinx_continuous`. Paleiskite:

    pocketsphinx_continuous -hmm models/hmm/lt.cd_cont_200 -jsgf models/lm/robot.jsgf -dict robot.dict
    
Ištarkite į mikrofoną `eik penkis metrus pirmyn`. Ekrane turi pasirodyti:

    [..]
    INFO: fsg_search.c(1456): End node <sil>.212:214:220 (-485)
    INFO: fsg_search.c(1456): End node pirmyn.162:190:220 (-505)
    INFO: fsg_search.c(1681): lattice start node <s>.0 end node </s>.221
    INFO: ps_lattice.c(1365): Normalizer P(O) = alpha(</s>:221:221) = -184664
    INFO: ps_lattice.c(1403): Joint P(O,S) = -184677 P(S|O) = -13
    000000001: eik penkis metrus pirmyn
    READY....


### Savarankiškas atpažintuvas

Šnekos atpažintuvas lengva išbandyti su pateiktais audio failais. Direktorijoje `test/audio` rasite 3 failus. Kiekviename faile yra įrašytos ištartos komandos.

Norint išbandyti atpažintuvą su jau esančiais audiofailais reikia naudoti komandą: `pocketsphinx_batch`. Kaip argumento ši komanda reikalauja konfiguracinio failo pvz: `test/pocketsphinx.conf`.

Paleiskite (kataloge `test`):

    pocketsphinx_batch pocketsphinx.conf

Atpažintos komandos bus įrašytos `test.hyp`:
    
    eik tris metrus pirmyn (test1 -4627)
    suk dešinėn (test2 -3687)
    varyk atgal (test3 -4212)

Kiekvienoje eilutėje yra komanda ir skliausteliuose nurodomas failo vardas ir atpažinimo taškai.



### Integracija

PocketSphinx lengva integruoti su kitomis komandomis. Tai turėtų būti aprašoma atskirame apraše.
