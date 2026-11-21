"""Render the diplomatic sign transcription. A suffix is a superscript."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
base = dict(zip("23456789", ["c","d","g","m","p","r","t","v"]))
base.update({"x":"l","y":"n","d":"r","t":"n","f":"s","s":"m","b":"p","j":"f","z":"c","M":"m","p":"u","k":"?","H":"?","h":"e","C":"?","n":"?","D":"che","r":"s","c":"l","L":"p","v":"?","q":"v"})
vowels = {"1":"u","2":"o","3":"i","4":"e","5":"a"}
whole = {"2":"o","3":"a","0":"c","o":"c","b":"s","6":"s","y":"n","r":"h","h":"e","e":"e","F":"et","P":"per","D":"che","Dn":"con","tt":"tt","ll":"ll","rr":"rr","ss":"ss","ff":"ff","cc":"cc","nn":"nn","mm":"mm","A":"a","Q":"per","O":"c","C":"?","N":"non","yr":"?","@":"?","?":"?"}
def decode(sign):
    if sign in whole: return whole[sign]
    if sign.startswith('['): return sign
    if len(sign)>1 and sign[-1] in vowels:
        letter = sign[:-1]
        if letter=="y": letter="Y"
        return ({'Y':'f'}.get(letter) or base.get(letter,'?'))+vowels[sign[-1]]
    return base.get(sign,"?")
if __name__=="__main__":
    for line in (ROOT/sys.argv[1]).read_text().splitlines():
        if line and not line.startswith('#'):
            row, tokens=line.split(maxsplit=1)
            print(row,''.join(map(decode,tokens.split())))
