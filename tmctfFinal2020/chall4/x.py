#!/usr/bin/env ipython

import angr
from claripy import *
import signal
from IPython import embed
import logging

decrypt_ref = [
    0x0010ce63,
    0x0010e9b1,
    0x001104e7,
    0x00111fed,
    0x00113b27,
    0x0011558f,
    0x001170ee,
    0x00118c3f,
    0x0011a773,
    0x0011c1d1,
    0x0011dd61,
    0x0011f880,
    0x0012136f,
    0x00122f13,
    0x00124a7e,
    0x00126627,
    0x001280fb,
    0x00129b7e,
    0x0012b6e2,
    0x0012d253,
    0x0012eda8,
    0x00130905,
    0x0013245c,
    0x00133f9a,
    0x00135a7d,
    0x00137636,
    0x0013919b,
    0x0013ac44,
    0x0013c72b,
    0x0013e2ac,
    0x0013fe29,
    0x0014187a,
    0x001433e0,
    0x00144eae,
    0x00146a10,
    0x001485f9,
    0x0014a133,
    0x0014bcbb,
    0x0014d8b3,
    0x0014f452,
    0x00150f6e,
    0x00152a2b,
    0x001545d8,
    0x0015610e,
    0x00157c29,
    0x001597f6,
    0x0015b2ae,
    0x0015cdfa,
    0x0015e90b,
    0x00160462,
    0x00161ffc,
    0x00163b0a,
    0x00165611,
    0x001671ce,
    0x00168d2e,
    0x0016a879,
    0x0016c36c,
    0x0016dea5,
    0x0016f9a7,
    0x0017147e,
    0x00172fdb,
    0x00174b2b,
    0x0017669a,
    0x0017816b,
    0x00179c9b,
    0x0017b72e,
    0x0017d21c,
    0x0017eca6,
    0x001806b4,
    0x001821fe,
    0x00183cc5,
    0x001857a4,
    0x001872ae,
    0x00188e15,
    0x0018a9f2,
    0x0018c559,
    0x0018e09e,
    0x0018fb46,
    0x00191709,
    0x001932a7,
    0x00194df9,
    0x001968f6,
    0x001983c9,
    0x00199ebc,
    0x0019bacb,
    0x0019d60f,
    0x0019f1d1,
    0x001a0cd1,
    0x001a2842,
    0x001a43a3,
    0x001a5eb2,
    0x001a79f2,
    0x001a94dd,
    0x001aafce,
    0x001acb4d,
    0x001ae6a4,
    0x001b019a,
    0x001b1c9f,
    0x001b37b5,
    0x001b5338,
    0x001b6e6a,
    0x001b88e9,
    0x001ba436,
    0x001bbf7f,
    0x001bda5f,
    0x001bf554,
    0x001c10b8,
    0x001c2bb3,
    0x001c46a3,
    0x001c62ab,
    0x001c7e20,
    0x001c993b,
    0x001cb3c6,
    0x001cce99,
    0x001ce9fd,
    0x001d0511,
    0x001d1f8a,
    0x001d3ac5,
    0x001d5689,
    0x001d719f,
    0x001d8c6c,
    0x001da7da,
    0x001dc304,
    0x001dddba,
    0x001df959,
    0x001e142f,
    0x001e2f4e,
    0x001e4a1e,
    0x001e657a,
    0x001e80e4,
    0x001e9cf5,
    0x001eb8cf,
    0x001ed40a,
    0x001eefc4,
    0x001f0b13,
    0x001f2699,
    0x001f41f8,
    0x001f5ccf,
    0x001f7777,
    0x001f9254,
    0x001fadb0,
    0x001fc89a,
    0x001fe3ba,
    0x001ffef4,
    0x00201a79,
    0x002035cf,
    0x00205132,
    0x00206c87,
    0x00208825,
    0x0020a339,
    0x0020be51,
    0x0020d9e4,
    0x0020f517,
    0x002110db,
    0x00212b94,
    0x00214735,
    0x00216185,
    0x00217cf3,
    0x0021977e,
    0x0021b2cf,
    0x0021ce7a,
    0x0021e9dc,
    0x00220438,
    0x00221f78,
    0x00223a56,
    0x0022562e,
    0x002270df,
    0x00228bef,
    0x0022a73f,
    0x0022c221,
    0x0022de1f,
    0x0022f943,
    0x002314f5,
    0x0023302f,
    0x00234b78,
    0x0023672b,
    0x0023826e,
    0x00239d75,
    0x0023b8bc,
    0x0023d3a3,
    0x0023ef4a,
    0x002409d8,
    0x00242542,
    0x002440b8,
    0x00245bc1,
    0x002476da,
    0x00249291,
    0x0024adc8,
    0x0024c85f,
    0x0024e401,
    0x0024ff2e,
    0x00251a11,
    0x002535dc,
    0x0025512e,
    0x00256cda,
    0x002588ab,
    0x0025a373,
    0x0025bf2d,
    0x0025d9f8,
    0x0025f53c,
    0x00260ffe,
    0x00262b82,
    0x0026467e,
    0x002661ff,
    0x00267dbb,
    0x0026993d,
    0x0026b4e8,
    0x0026d03a,
    0x0026ebf9,
    0x00270789,
    0x0027233d,
    0x00273e0b,
    0x0027597b,
    0x00277470,
    0x00278f02,
    0x0027aa2f,
    0x0027c533,
    0x0027e08a,
    0x0027fc0b,
    0x002816ca,
    0x00283254,
    0x00284de4,
    0x0028692a,
    0x002884b5,
    0x00289fa2,
    0x0028ba1b,
    0x0028d50f,
    0x0028f0d9,
    0x00290b1f,
    0x00292678,
    0x002941c8,
    0x00295d23,
    0x002978ac,
    0x00299353,
    0x0029ae29,
    0x0029c922,
    0x0029e48c,
    0x0029ffb6,
    0x002a1a78,
    0x002a35dd,
    0x002a5123,
    0x002a6c30,
    0x002a8782,
    0x002aa2c8,
    0x002abe12,
    0x002ad99b,
    0x002af4d3,
    0x002b1005,
    0x002b2b2a,
    0x002b45a5,
    0x002b6110,
    0x002b7c3e,
    0x002b9767,
    0x002bb251,
    0x002bcd3f,
    0x002be8cf,
    0x002c0409,
    0x002c1f13,
    0x002c3ae7,
    0x002c55f1,
    0x002c717e,
    0x002c8c4f,
    0x002ca729,
    0x002cc2bc,
    0x002cdd7b,
    0x002cf845,
    0x002d13e7,
    0x002d2ef7,
    0x002d49d1,
    0x002d64fa,
    0x002d7fee,
    0x002d9a6c,
    0x002db634,
    0x002dd13d,
    0x002dec5c,
    0x002e07a0,
    0x002e227d,
    0x002e3de1,
    0x002e5913,
    0x002e73a7,
    0x002e8ea8,
    0x002ea8fc,
    0x002ec332,
    0x002ede8a,
    0x002ef910,
    0x002f14b5,
    0x002f2fac,
    0x002f4a5d,
    0x002f6546,
    0x002f8047,
    0x002f9bf3,
    0x002fb715,
    0x002fd282,
    0x002fed89,
    0x00300894,
    0x003023b8,
    0x00303ee1,
    0x00305951,
    0x00307486,
    0x00309020,
    0x0030ab97,
    0x0030c688,
    0x0030e223,
    0x0030fd7f,
    0x0031183c,
    0x003133be,
    0x00314f45,
    0x00316990,
    0x00318472,
    0x0031a00e,
    0x0031ba87,
    0x0031d4ad,
    0x0031f00c,
    0x00320bb5,
    0x003226b3,
    0x003241c2,
    0x00325d9d,
    0x003278d7,
    0x00329437,
    0x0032b05e,
    0x0032cb7c,
    0x0032e716,
    0x0033011d,
    0x00331c7b,
    0x003337e2,
    0x00335395,
    0x00336faf,
    0x00338b40,
    0x0033a527,
    0x0033c046,
    0x0033dbe2,
    0x0033f776,
    0x0034130d,
    0x00342ea6,
    0x00344989,
    0x003464ee,
    0x00348005,
    0x00349b2f,
    0x0034b62c,
    0x0034d15f,
    0x0034ed2a,
    0x003508f0,
    0x0035236c,
    0x00353ec5,
    0x00355a7e,
    0x0035759a,
    0x00359074,
    0x0035ac46,
    0x0035c727,
    0x0035e246,
    0x0035fda6,
    0x00361881,
    0x00363419,
    0x00364f60,
    0x00366abd,
    0x0036867a,
    0x0036a176,
    0x0036bcbf,
    0x0036d8e3,
    0x0036f421,
    0x00370f49,
    0x00372a5f,
    0x003745d9,
    0x00376100,
    0x00377c37,
    0x003797a4,
    0x0037b351,
    0x0037cdd4,
    0x0037e901,
    0x0038039c,
    0x00381f64,
    0x00383af2,
    0x00385645,
    0x003871d7,
    0x00388cfe,
    0x0038a731,
    0x0038c1d6,
    0x0038dcdb,
    0x0038f7d2,
    0x00391332,
    0x00392df8,
    0x00394886,
    0x003963f5,
    0x00397f8a,
    0x00399a93,
    0x0039b57a,
    0x0039d11f,
    0x0039ec78,
    0x003a075a,
    0x003a22a3,
    0x003a3d74,
    0x003a58a4,
    0x003a738c,
    0x003a8ded,
    0x003aa8ac,
    0x003ac47c,
    0x003adf60,
    0x003afa47,
    0x003b1534,
    0x003b30d1,
    0x003b4ca3,
    0x003b67c8,
    0x003b825f,
    0x003b9e78,
    0x003bb9c5,
    0x003bd4b1,
    0x003bef6f,
    0x003c0ac6,
    0x003c2598,
    0x003c405b,
    0x003c5b15,
    0x003c76dd,
    0x003c9207,
    0x003cad04,
    0x003cc824,
    0x003ce35d,
    0x003cfe68,
    0x003d19a6,
    0x003d352e,
    0x003d5017,
    0x003d6bca,
    0x003d8722,
    0x003da255,
    0x003dbdae,
    0x003dd956,
    0x003df565,
    0x003e1050,
    0x003e2b2e,
    0x003e465f,
    0x003e618e,
    0x003e7c2e,
    0x003e96a4,
    0x003eb295,
    0x003ecdd4,
    0x003ee8fc,
    0x003f0450,
    0x003f1f93,
    0x003f3b15,
    0x003f568a,
    0x003f71e6,
    0x003f8c71,
    0x003fa778,
    0x003fc2ce,
    0x003fde37,
    0x003ff9bb,
    0x004014c1,
    0x00402fe9,
    0x00404b2d,
    0x00406696,
    0x004081fa,
    0x00409dcb,
    0x0040b991,
    0x0040d4b0,
    0x0040f028,
    0x00410b03,
    0x004126a0,
    0x00414162,
    0x00415c17,
    0x00417691,
    0x004191df,
    0x0041ac8f,
    0x0041c7fd,
    0x0041e2ee,
    0x0041fe67,
    0x00421a0d,
    0x00423519,
    0x00425057,
    0x00426c0c,
    0x004287b2,
    0x0042a359,
    0x0042bf03,
    0x0042da5c,
    0x0042f500,
    0x00431073,
    0x00432b63,
    0x00434713,
    0x004361ce,
    0x00437cfd,
    0x0043982f,
    0x0043b30b,
    0x0043ce53,
    0x0043e975,
    0x004404ea,
    0x0044200c,
    0x00443c06,
    0x0044579e,
    0x004472c2,
    0x00448e28,
    0x0044a99a,
    0x0044c471,
    0x0044dece,
    0x0044f9e4,
    0x00451487,
    0x00453042,
    0x00454bac,
    0x0045668c,
    0x004581c8,
    0x00459c6e,
    0x0045b729,
    0x0045d2bc,
    0x0045eea5,
    0x00460a05,
    0x00462594,
    0x00464128,
    0x00465c9e,
    0x004677cb,
    0x00469348,
    0x0046ae9c,
    0x0046ca70,
    0x0046e54b,
    0x00470086,
    0x00471b81,
    0x004736bb,
    0x00475214,
    0x00476de7,
    0x00478942,
    0x0047a433,
    0x0047bf5d,
    0x0047da3d,
    0x0047f40e,
    0x00480f33,
    0x0048299f,
    0x004845ab,
    0x0048600c,
    0x00487aad,
    0x004895f9,
    0x0048b1b9,
    0x0048cd4f,
    0x0048e873,
    0x004903ed,
    0x00491ea7,
    0x00493aa9,
    0x00495604,
    0x004971cf,
    0x00498cc9,
    0x0049a83c,
    0x0049c361,
    0x0049de40,
    0x0049f9cc,
    0x004a1472,
    0x004a2f49,
    0x004a4ad8,
    0x004a65f6,
    0x004a812d,
    0x004a9cd4,
    0x004ab7aa,
    0x004ad31e,
    0x004aeee0,
    0x004b09bc,
    0x004b24e5,
    0x004b401c,
    0x004b5bed,
    0x004b77a6,
    0x004b9288,
    0x004bae2a,
    0x004bc924,
    0x004be484,
    0x004bff50,
    0x004c1a65,
    0x004c3597,
    0x004c50f1,
    0x004c6b9e,
    0x004c872f,
    0x004ca24d,
    0x004cbdd1,
    0x004cd95a,
    0x004cf413,
    0x004d0f4b,
    0x004d2ac7,
    0x004d463e,
    0x004d617b,
    0x004d7d04,
    0x004d97c7,
    0x004db367,
    0x004dce45,
    0x004de929,
    0x004e0444,
    0x004e1f3b,
    0x004e3a25,
    0x004e54e8,
    0x004e6f6d,
    0x004e89f8,
    0x004ea56d,
    0x004ec14b,
    0x004edc39,
    0x004ef735,
    0x004f1235,
    0x004f2dee,
    0x004f4811,
    0x004f6312,
    0x004f7e8e,
    0x004f99f5,
    0x004fb5a8,
    0x004fd0af,
    0x004fec53,
    0x005006d6,
    0x005021ae,
    0x00503ce2,
    0x00505840,
    0x0050737b,
    0x00508ea4,
    0x0050a9e2,
    0x0050c4e8,
    0x0050e074,
    0x0050fbb3,
    0x005116b1,
    0x0051322c,
    0x00514e58,
    0x005169fb,
    0x005185f5,
    0x0051a14f,
    0x0051bb95,
    0x0051d743,
    0x0051f2ae,
    0x00520e3f,
    0x0052297f,
    0x005244bd,
    0x00526053,
    0x00527bd6,
    0x00529632,
    0x0052b1c4,
    0x0052ccfa,
    0x0052e87d,
    0x00530497,
    0x00531f8a,
    0x00533a8e,
    0x005355c7,
    0x00537123,
    0x00538c2d,
    0x0053a72f,
    0x0053c238,
    0x0053dd45,
    0x0053f8be,
    0x0054148a,
    0x00542fcb,
    0x00544af7,
    0x005465c4,
    0x005480b7,
    0x00549bce,
    0x0054b7c0,
    0x0054d312,
    0x0054ef0f,
    0x00550a08,
    0x00552498,
    0x00554016,
    0x00555b6a,
    0x005576fe,
    0x005591a9,
    0x0055ad47,
    0x0055c854,
    0x0055e337,
    0x0055fe72,
    0x00561973,
    0x005634f1,
    0x00565057,
    0x00566c07,
    0x00568770,
    0x0056a2d2,
    0x0056beb2,
    0x0056da17,
    0x0056f499,
    0x00570fe2,
    0x00572bc5,
    0x005747b7,
    0x0057636e,
    0x00577e20,
    0x005799c5,
    0x0057b4ab,
    0x0057cf5f,
    0x0057eaae,
    0x00580544,
    0x00582000,
    0x00583b4f,
    0x005856d3,
    0x005872e5,
    0x00588edb,
    0x0058a9ec,
    0x0058c42c,
    0x0058df08,
    0x0058fa0d,
    0x005914a5,
    0x00593027,
    0x00594b23,
    0x00596660,
    0x0059820e,
    0x00599cf9,
    0x0059b8b8,
    0x0059d3d6,
    0x0059ef2b,
    0x005a09f5,
    0x005a2503,
    0x005a40f2,
    0x005a5c18,
    0x005a778d,
    0x005a9328,
    0x005aae0c,
    0x005ac98a,
    0x005ae4b0,
    0x005aff9b,
    0x005b1ae1,
    0x005b35c0,
    0x005b50be,
    0x005b6bd0,
    0x005b86a5,
    0x005ba1b2,
    0x005bbd35,
    0x005bd903,
    0x005bf418,
    0x005c0fab,
    0x005c2b59,
    0x005c46d4,
    0x005c61a2,
    0x005c7d29,
    0x005c98a5,
    0x005cb323,
    0x005ccf2c,
    0x005ceac8,
    0x005d05ab,
    0x005d20c9,
    0x005d3b69,
    0x005d56e2,
    0x005d71c3,
    0x005d8ca5,
    0x005da818,
    0x005dc3a9,
    0x005ddf0f,
    0x005dfad7,
    0x005e1659,
    0x005e318c,
    0x005e4ce6,
    0x005e682c,
    0x005e8358,
    0x005e9e08,
    0x005eb9ef,
    0x005ed51c,
    0x005ef002,
    0x005f0ada,
    0x005f262e,
    0x005f40f5,
    0x005f5bc5,
    0x005f76c3,
    0x005f91c5,
    0x005fac58,
    0x005fc793,
    0x005fe2d9,
    0x005ffddc,
    0x00601943,
    0x006034c9,
    0x00604fed,
    0x00606aaf,
    0x00608554,
    0x0060a127,
    0x0060bba6,
    0x0060d6b3,
    0x0060f222,
    0x00610cf0,
    0x006127d6,
    0x00614377,
    0x00615e2f,
    0x006179e3,
    0x006194d0,
    0x0061b0ac,
    0x0061cc35,
    0x0061e7a7,
    0x00620367,
    0x00621eb2,
    0x00623983,
    0x00625563,
    0x00626fc2,
    0x00628aaf,
    0x0062a569,
    0x0062c0af,
    0x0062dbb5,
    0x0062f6e4,
    0x006311e8,
    0x00632ceb,
    0x006347bd,
    0x006362d7,
    0x00637e1b,
    0x00639977,
    0x0063b3db,
    0x0063cec4,
    0x0063ea3c,
    0x006405f3,
    0x00642150,
    0x00643c66,
    0x0064577f,
    0x006472d4,
    0x00648dd3,
    0x0064a8c7,
    0x0064c451,
    0x0064df5c,
    0x0064fa3b,
    0x006515d0,
    0x00653167,
    0x00654ca1,
    0x0065674e,
    0x0065824a,
    0x00659d20,
    0x0065b84c,
    0x0065d45e,
    0x0065ef4d,
    0x00660a4a,
    0x0066256d,
    0x006640bb,
    0x00665bcd,
    0x006676de,
    0x00669232,
    0x0066ac8b,
    0x0066c871,
    0x0066e3ad,
    0x0066fe87,
    0x00671952,
    0x00673444,
    0x00674f4e,
    0x00676a17,
    0x00678568,
    0x0067a0dd,
    0x0067bb9d,
    0x0067d634,
    0x0067f10a,
    0x00680bb1,
    0x0068273d,
    0x00684274,
    0x00685d66,
    0x006877a7,
    0x006891d8,
    0x0068ad45,
    0x0068c841,
    0x0068e378,
    0x0068fe93,
    0x006919b6,
    0x0069346f,
    0x00694f38,
    0x00696a4f,
    0x00698525,
    0x0069a063,
    0x0069bb42,
    0x0069d63e,
    0x0069f103,
    0x006a0c04,
    0x006a26af,
    0x006a413d,
    0x006a5c83,
    0x006a77e6,
    0x006a9325,
    0x006aae7a,
    0x006aca20,
    0x006ae628,
    0x006b0143,
    0x006b1c2e,
    0x006b37b7,
    0x006b5343,
    0x006b6e00,
    0x006b8928,
    0x006ba437,
    0x006bbea9,
    0x006bd99f,
    0x006bf4b8,
    0x006c102a,
    0x006c2aff,
    0x006c4662,
    0x006c61cb,
    0x006c7cdf,
    0x006c9867,
    0x006cb423,
    0x006ccf27,
    0x006cea2a,
    0x006d05ef,
    0x006d20b4,
    0x006d3bc6,
    0x006d56b9,
    0x006d7235,
    0x006d8ce8,
    0x006da7af,
    0x006dc34a,
    0x006dde73,
    0x006dfa0a,
    0x006e1503,
    0x006e307c,
    0x006e4b6e,
    0x006e6695,
    0x006e81d6,
    0x006e9d8f,
    0x006eb942,
    0x006ed458,
    0x006eef65,
    0x006f0a7c,
    0x006f258a,
    0x006f409f,
    0x006f5b65,
    0x006f75d7,
    0x006f917f,
    0x006fac76,
    0x006fc742,
    0x006fe28d,
    0x006ffd97,
    0x007018f3,
    0x0070339e,
    0x00704fa6,
    0x00706aba,
    0x007085f6,
    0x0070a112,
    0x0070bc38,
    0x0070d6d6,
    0x0070f292,
    0x00710da7,
    0x00712953,
    0x007144a5,
    0x00715ff4,
    0x00717bd1,
    0x00719668,
    0x0071b1ee,
    0x0071ccf6,
    0x0071e822,
    0x007203d5,
    0x00721fd6,
    0x00723bc6,
    0x007256d6,
    0x0072733b,
    0x00728dc5,
    0x0072a907,
    0x0072c417,
    0x0072dff9,
    0x0072fb2e,
    0x007315f2,
    0x00733136,
    0x00734bbb,
    0x0073669c,
    0x0073818e,
    0x00739d55,
    0x0073b852,
    0x0073d372,
    0x0073ee97,
    0x007409fd,
    0x0074255a,
    0x007440d1,
    0x00745c38,
    0x00747795,
    0x007492d8,
    0x0074add3,
    0x0074c83d,
    0x0074e321,
    0x0074fe0a,
    0x00751984,
    0x007534dc,
    0x00755103,
    0x00756c10,
    0x007586aa,
    0x0075a19b,
    0x0075bd7c,
    0x0075d833,
    0x0075f36b,
    0x00760e54,
    0x00762962,
    0x0076447a,
    0x0076601b,
    0x00767af4,
    0x00769678,
    0x0076b1e6,
    0x0076cdad,
    0x0076e940,
    0x00770457,
    0x00771fe7,
    0x00773b57,
    0x0077561d,
    0x0077715b,
    0x00778d0a,
    0x0077a7d1,
    0x0077c335,
    0x0077de65,
    0x0077f930,
    0x0078144a,
    0x00782f43,
    0x00784a01,
    0x0078657f,
    0x007880fa,
    0x00789c73,
    0x0078b82f,
    0x0078d34c,
    0x0078eea3,
    0x00790a5a,
    0x00792537,
    0x007940a3,
    0x00795c9e,
    0x00797734,
    0x007991d3,
    0x0079ad8e,
    0x0079c805,
    0x0079e40b,
    0x0079fe93,
    0x007a196c,
    0x007a34ea,
    0x007a4ff9,
    0x007a6b10,
    0x007a8605,
    0x007aa1ec,
    0x007abcc7,
    0x007ad7ba
]

def kys():
    os.system('kill %d' % os.getpid())
def sigint_handler(signum, frame):
    print('Stopping Execution for Debug. If you want to kill the programm issue: kys()')
    if not "IPython" in sys.modules:
        import IPython
        IPython.embed()

signal.signal(signal.SIGINT, sigint_handler)

l.setLevel(logging.DEBUG)

p = angr.Project('./tmmaze.so', load_options={'auto_load_libs':False, 'main_opts': {'custom_base_addr': 0x100000}})

p.factory.blank_state()

success = [
    1,
    35,
    78,
    265,
    382,
    708,
    759,
    648,
    802,
    ]

keys = [
    (759, "IJi2eDlOtrAHECKS"),
    (265, "vXEdCHzpOhVoIUF3"),
    (802, "UdKjhzi8p436wY5I"),
    (382, "NL4eoIH2pbylRfWZ"),
    (468, "u2Zf5hJcMPx1s9mX"),
    ]
correct = [
    (1, "2obeKd6Pak3guDCjLn7Vm2RgHMQei0WZ"),
    (78, "FfNYByjPK5uJnA3IQ9ZAq73LPOYfGMHN"),
    (708, "du4o92H0zTP7GaMvIQCfdbiwjYA4T9V0"),
    (35, "emMbC1RD8tyUwIhG9PzNd8OIxq6Ejlwm"),
    (648, "klUySQEsxv3t6Jj2e9gOFilbwKWUhdIc"),

    ]

# emMbC1RD8tyUwIhGIQCfdbiwjYA4T9V0
# vXEdCHzpOhVoIUF3IQCfdbiwjYA4T9V0
# IJi2eDlOtrAHECKSIQCfdbiwjYA4T9V0
# klUySQEsxv3t6Jj2IQCfdbiwjYA4T9V0
# UdKjhzi8p436wY5I9PzNd8OIxq6Ejlwm
# UdKjhzi8p436wY5IbrSuV6Ys4zXkKMmO
# vXEdCHzpOhVoIUF3brSuV6Ys4zXkKMmO
# NL4eoIH2pbylRfWZbrSuV6Ys4zXkKMmO
# IJi2eDlOtrAHECKSbrSuV6Ys4zXkKMmO
# u2Zf5hJcMPx1s9mXSbrSuV6Ys4zXkKMmO

def get_ip(state):
    print(hex(state.addr))

for i in range(802,1000):
    room = f"Room{i:03d}"
    print(room)

    ret = BVS("{room}_ret", 64)
    # key = Concat(BVS("key", 16*8), BVV("Ln7Vm2RgHMQei0WZ"))

    # key = Concat(BVS("key", 16*8), BVV("Q9ZAq73LPOYfGMHN"))
    key = Concat(BVS("key", 16*8), BVV("IQCfdbiwjYA4T9V0"))
    # IQCfdbiwjYA4T9V0
    # 9PzNd8OIxq6Ejlwm
    # e9gOFilbwKWUhdIc
    # brSuV6Ys4zXkKMmO


    curr = p.loader.find_symbol(room)

    state = p.factory.call_state(curr.rebased_addr, key, ret)
    state.inspect.b(event_type="instruction", action=get_ip)
    state.options.add(angr.options.LAZY_SOLVES)


    for k in key.chop(bits=8):
        state.add_constraints(Or(And(k >= 48, k <= 58), And(k <= 122, k >= 65)))

    sm = p.factory.simgr(state)

    # def room_found(state):
    #     if state.memory.load(state.regs.eax) == 1:
    #         return True
    #     return False

    def calls_decrypt(state):
        state.addr == 0x10b2a1

    def end(state):
        state.addr > decrypt_ref[i-1]

    # sm.explore(find=end)
    sm.explore(find=0x10b2a1, avoid=end)

    if len(sm.found) > 0:
        try:
            sm.found[0].solver.eval(key)
        except:
            continue
        embed()
