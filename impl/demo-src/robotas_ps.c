#include <pocketsphinx.h>	
#define MAXLEN 256

int
main(int argc, char *argv[])
{
	//Argumentai
	/////////////////////////////
	ps_decoder_t *ps;
	cmd_ln_t *config;
	FILE *fh;
	char const *hyp, *uttid;
        int16 buf[512];
	int rv;
	int32 score;

	//Inicializavimas
	/////////////////////////////
	config = cmd_ln_init(NULL, ps_args(), TRUE,
			     "-hmm",  "../models/hmm/lt.cd_cont_200/",
			     "-jsgf",  "../models/lm/robotas.gram",
			     "-dict",  "../models/dict/robotas.dict",
			     "-logfn", "/dev/null",
			     NULL);
	if (config == NULL){
		return 1;
	}
	ps = ps_init(config);
	if (ps == NULL){
		return 1;
	}

	//Failo atidarymas skaitymui
	/////////////////////////////
	fh = fopen("../test/audio/test1.wav", "rb");
	if (fh == NULL) {
		perror("Failed to open test1.wav");
		return 1;
	}

	//Visos bylos turinio dekodavimas
	/////////////////////////////
	rv = ps_decode_raw(ps, fh, "robotas", -1);
	if (rv < 0){
		return 1;
	}
	// Hipotezės ištraukimas
	/////////////////////////////
	hyp = ps_get_hyp(ps, &score, &uttid);
	if (hyp == NULL){
		return 1;
	}
	printf("Atpažinimo hipotezė: %s\n", hyp);

	// Bylos uždarymas
	/////////////////////////////
	fclose(fh);
    ps_free(ps);
	return 0;
}
