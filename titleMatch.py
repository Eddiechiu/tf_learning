import re

string = '<span id="art-abs-title-7420579">Management of a Proton Exchange' \
 ' Membrane Fuel Cell System to Feed a Superconducting Coil</span>'

pattern = re.compile(r'<span id="art-abs-title-\d{7}">(.*?)</span>')
match = pattern.findall(string)

if match:
	print(match)
