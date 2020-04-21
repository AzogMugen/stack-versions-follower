import re, pprint
versions = [
"0.0.0",
"0.0.1",
"0.1.2",
# pre-release labels
"9.9.9-aaa",
"9.9.9-AAA",
"9.9.9-Aaa",
"9.9.9-Aaa123",
# build labels
"9.9.9+aaa",
"9.9.9+AAA",
"9.9.9+Aaa",
"20.19.4+Abcdef145",
# pre-release AND build labels
"0.9.4-lowercase+build-label",
"0.9.4-l0w3rc4s3-and-numbers+build-label",
"0.9.4-UPP3RCASE-AND-NUMBERS+buidlowercase",
"0.9.4-UPPERCASE+buidlowercase",
"0.9.4-UPPERCASEPRERELEASE+BUILDUPPERCASE",
"0.9.4-TEST1235+Akindof23.Bad.Test",
"0.9.4-TEST1235+Another123*bAd*Test",
"0.9.4-TEST1235+Another123 baD Test",
# bad versions
" 0.9.4",
"0. 9.4",
"0.9 .4",
"0.9.4 ",
"µ/0.9.4",
"+0.9.4",
"0.9+.4",
"0.9.4+",
"-0.9.4",
"0.9-.4",
"0.9.4-",
"a.9.4",
"0.b.4",
"0.9.c",
"0.9.4//..",
"a.b.c",
"a.9.4",
"(..9.4",
"...4",
]

# You can go test your version against the pattern with tools like https://regex101.com/
for ver in versions :
	if re.search("^[0-9]+\.[0-9]+\.[0-9]+[+0-9A-Za-z-]*$", ver):
	    # pprint.pprint("Version '"+ver+"' / OK")
	    pprint.pprint("Version '{}' :  OK".format(ver))
	else:
	    pprint.pprint("Version '"+ver+"' <------ Bad version")

