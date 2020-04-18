import re, pprint
versions = [
"0.0.0",
"0.0.1",
"0.1.2",
"9.9.9-aaa",
"9.9.9-AAA",
"9.9.9-Aaa",
"9.9.9-Aaa123",
"9.9.9+aaa",
"9.9.9+AAA",
"9.9.9+Aaa",
"9.9.9+Aaa123",
"0.9.4-TEST1235+test",
"20.19.4+abcdef145",
"+-*/0.9.4",
"+0.9.4",
"0.9+.4",
"0.9.4+",
"-0.9.4",
"0.9-.4",
"0.9.4-",
"0.9.4//..",
"a.b.c",
"a.9.4",
"(..9.4",
"...4",
]
for ver in versions :
	if re.search("^[0-9]+\.[0-9]+\.[0-9]+[+0-9A-Za-z-]*$", ver):
	    pprint.pprint("Version '"+ver+"' matches regex")
	else:
	    pprint.pprint("Version '"+ver+"' DOES NOT match regex")

