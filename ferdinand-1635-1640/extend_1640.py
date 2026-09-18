#!/usr/bin/env python3
"""Reproduce the explicitly post-transfer 1640 supplement; no 1635 value changes."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import decoder

ROOT = Path(__file__).resolve().parent
# Value, selection/corroboration context. Contexts are cryptanalytic readings,
# not an independently available plaintext witness or a blind holdout.
SUPPLEMENT = {
'21': ('o', 'P1.C26 dilectione; P1.C01 dilectioni; P1.C13 collectionem'),
'36': ('x', 'P2.C03 expositurus; P2.C10 expressum; P2.C12 expendant'),
'41': ('le', 'P1.C05 electore; P1.C26 dilectione; P1.C10 celeri'),
'42': ('li', 'P1.C04 militis; P1.C06 illius/circuli; P1.C18 circulus'),
'43': ('lo', 'P1.C05 coloniae; P1.C04 circulo; P2.C06 florenos'),
'44': ('lu', 'P1.C10 illud; P1.C18 circulus'),
'45': ('na', 'P1.C13 festinanter; P1.C19 ordinauimus; P2.C13 consignari'),
'46': ('ne', 'P1.C03 Castagneti; P1.C10 negotium; P1.C18 ne'),
'47': ('ni', 'P1.C05 coloniae; P1.C07 boni; P2.C03 omni'),
'48': ('no', 'P1.C03 nouum; P1.C25 nobis; P2.C07 nostrorum'),
'49': ('nu', 'P1.C14 numerum; P1.C26 denuo; P2.C01 quatenus'),
'50': ('ra', 'P1.C03 apparatum; P1.C22 transferre; P2.C05 grauitate'),
'51': ('re', 'P1.C05 electore; P1.C18 praecauere; P2.C04 habere'),
'52': ('ri', 'P1.C19 arbitrio; P1.C22 operi; P2.C08 commissariorum'),
'53': ('ro', 'P1.C11 pro; P1.C20 propter; P2.C07 nostrorum'),
'54': ('ru', 'P1.C14 numerum; P2.C03 expositurus; P2.C08 commissariorum'),
'pla': ('ta', 'P1.C05 statibus; P1.C23 celeritate; P2.C05 grauitate'),
'ple': ('te', 'P1.C05 electore; P1.C13 festinanter; P2.C01 quatenus'),
'pli': ('ti', 'P1.C04 militis; P1.C26 petimus/dilectione; P2.C03 distinctius'),
'plo': ('to', 'P1.C05 electore; P2.C02 orator; P2.C05 desideratos'),
'plu': ('tu', 'P1.C03 apparatum; P1.C16 instituamus; P2.C03 expositurus'),
'ca': ('ma', 'P1.C02 marchio; P1.C23 manum; P2.C10 mandatum'),
'ce': ('me', 'P1.C11 medio; P1.C14 numerum; P1.C20 comes'),
'ci': ('mi', 'P1.C04 militis; P1.C13 militis; P2.C06 mille'),
'co': ('mo', 'P1.C12 modus; P1.C08-09 incommoda; P2.C04 omnimodam'),
'cu': ('mu', 'P1.C16 instituamus; P1.C26 petimus; P2.C09 iniungimus'),
'ap': ('ca', 'P1.C02 catolici; P1.C03 circa; P1.C18 praecauere'),
'ep': ('ce', 'P1.C06 inceptum; P1.C10 celeri; P2.C06 centum'),
'ip': ('ci', 'P1.C04 circulo; P1.C07 iudicium; P1.C19 subiiciatur'),
'op': ('co', 'P1.C05 coloniae; P1.C13 collectionem; P2.C08 commissariorum'),
'up': ('cu', 'P1.C04 circulo; P1.C09 secum; P2.C13 curare'),
'ha': ('da', 'P1.C09 incommoda; P1.C15 extendat; P2.C10 mandatum'),
'he': ('de', 'P1.C26 denuo; P2.C04 fidem; P2.C05 desideratos'),
'hi': ('di', 'P1.C26 dilectione; P2.C02 praedictus; P2.C03 distinctius'),
'hu': ('du', 'P1.C12 modus'),
'an': ('sa', 'P1.C25 necessariis; P2.C08 commissariorum'),
'en': ('se', 'P1.C02 serenissimi; P1.C09 secum; P1.C17 seruare'),
'in': ('si', 'P1.C16 si; P2.C02 sibi; P2.C04 considerata'),
'un': ('su', 'P1.C19 subiiciatur; P1.C25 sumptibus; P2.C10 expressum'),
'tes': ('be', 'P1.C16-17 liberam; P1.C24 debeat; P2.C04 habere'),
'tis': ('bi', 'P1.C19 arbitrio; P1.C25 nobis; P2.C02 sibi'),
'tos': ('bo', 'P1.C07 boni'),
'tus': ('bu', 'P1.C05 statibus; P1.C16 partibus; P2.C08 quibus'),
'au': ('pa', 'P1.C03 apparatum; P1.C15 apparatus; P1.C16 partibus'),
'eu': ('pe', 'P1.C22 operi; P1.C26 petimus; P2.C01 perinstanter'),
'ou': ('po', 'P1.C14 potentiorem; P1.C17 dispositionem; P2.C03 expositurus'),
'uu': ('pu', 'P1.C07 publici'),
'me': ('fe', 'P1.C12-13 festinanter; P1.C21 confestim; P1.C22 transferre'),
'mi': ('fi', 'P1.C24 deficientibus; P2.C04 fidem'),
'mu': ('fu', 'P1.C09 fusius'),
'ga': ('ha', 'P2.C02 hac; P2.C04 habere; P2.C05 hactenus; P1.C04 Westphalico after glyph review'),
'gi': ('hi', 'P1.C02 marchio'),
'it': ('gi', 'P1.C02 regis; P2.C09 iniungimus'),
'ot': ('go', 'P1.C10 negotium'),
'et': ('ge', 'P1.C11 indigeat'),
'ko': ('do', 'P1.C08 domus'),
'fu': ('mu', 'P1.C01 comunicabit (single m retained; mmu cannot be excluded from this occurrence alone)'),
'lx': ('oc', 'P1.C12 occurrat (source group lx retained; singleton, provisional)'),
'li': ('xi', 'P2.C07-08 existentium (source group li retained; singleton, provisional)'),
'b': ('m', 'P1.C08 etiam; P1.C12 quam; P1.C14 quam; distinct source label from disputed 6'),
}

# Imported source ambiguities are retained in R1890-working.txt. This is a
# separate image-reviewed layer. Every substitution is logged per occurrence.
REVIEW = {
'c?': ('c', 'I9352: same open c-form as adjacent unqueried c; high confidence'),
'g^.a': ('ga', 'I9352 C04: ga with small mark above; mark has no demonstrated key function'),
'plu_.': ('plu', 'I9352 C06: plu; trailing low stroke retained in source annotation'),
'l/z?p': ('z p', 'I9352 C03 / I9353 C10: looped z-like sign followed by separate p; medium confidence'),
'l/z?6': ('z 6', 'I9352 C07: looped sign then 6-like sign; medium confidence'),
'l/z?': ('z', 'Looped a-encoding sign; choice of label z is provisional, supported by repeated contexts'),
'pla/u?': ('plu', 'I9352 C09: final vowel resembles u; contulimus supports, so not blind paleography'),
'ple/i?': ('pli', 'I9352 C20: final vowel resembles i; quatinus retained, not regularized to quatenus'),
'c/1?o/0?': ('co', 'I9352 C24: joined c-o group, compare other co groups; admouere context supports'),
}

def run():
    base = decoder.read_key(ROOT/'key-expanded-1635.json')
    assert not set(base) & set(SUPPLEMENT), 'Supplement must never overwrite 1635 assignments'
    key = base | {s:v[0] for s,v in SUPPLEMENT.items()}
    assert all(key[s] == v for s,v in base.items())
    src = ROOT/'transcriptions/R1890-working.txt'
    lines, amendments = [], []
    for line in src.read_text().splitlines():
        if not line or line.startswith('#'): continue
        ident, body = line.split(' ',1)
        tokens = body.split()
        new = []
        for position, token in enumerate(tokens,1):
            if token in REVIEW:
                after, reason = REVIEW[token]
                amendments.append([ident,position,token,after,reason])
                new.extend(after.split())
            else: new.append(token)
        lines.append(ident+' '+' '.join(new))
    reviewed = ROOT/'transcriptions/R1890-reviewed.txt'
    reviewed.write_text('# Post-transfer image review, derived by extend_1640.py. See R1890-review.tsv.\n'+'\n'.join(lines)+'\n')
    with (ROOT/'transcriptions/R1890-review.tsv').open('w') as f:
        w=csv.writer(f, delimiter='\t', lineterminator='\n');w.writerow(['row','source_position','before','after','evidence_and_limit']);w.writerows(amendments)
    evidence={}
    inventory=Counter()
    for row,pos,token in decoder.units(reviewed):
        inventory[token]+=1
        evidence.setdefault(token,[]).append(f'{row}:{pos}')
    assert set(SUPPLEMENT) <= set(inventory), 'Do not infer unused grid cells'
    data={'description':'Post-transfer 1640 supplement; 1635 values unchanged. Context-selected, not independently validated.',
          'base_file':'key-expanded-1635.json', 'base_evidence':'key-evidence.tsv',
          'base_sha256':decoder.sha(ROOT/'key-expanded-1635.json'), 'mappings':key,
          'supplement':{s:{'plain':v,'selection_context':ctx,'occurrences':evidence[s],
              'status':'provisional singleton' if len(evidence[s])==1 else 'contextual, corroborated in same letter'} for s,(v,ctx) in SUPPLEMENT.items()}}
    (ROOT/'key-1640-supplemented.json').write_text(json.dumps(data,indent=2)+'\n')
    with (ROOT/'key-1640-evidence.tsv').open('w') as f:
        w=csv.writer(f, delimiter='\t', lineterminator='\n');w.writerow(['symbol','plain','selection_context','all_reviewed_occurrences','status'])
        for s,d in data['supplement'].items():w.writerow([s,d['plain'],d['selection_context'],';'.join(d['occurrences']),d['status']])
    for label,path in [('imported',src),('reviewed',reviewed)]:
        (ROOT/f'results/R1890-supplemented-{label}-literal.txt').write_text('# Post-transfer supplement, no editorial repairs.\n'+decoder.decode_file(path,key))
    unknown={s:n for s,n in inventory.items() if s not in key}
    summary={'base_unchanged':True,'base_mappings':len(base),'added_mappings':len(SUPPLEMENT),
       'base_labels_observed_in_reviewed_1640':len(set(base) & set(inventory)),
       'base_labels_absent_in_reviewed_1640':sorted(set(base)-set(inventory)),
       'total_mappings':len(key),'reviewed_units':sum(inventory.values()),'mapped_units':sum(n for s,n in inventory.items() if s in key),
       'unmapped_units':sum(unknown.values()),'unknown_inventory':unknown,'review_amendments':len(amendments),
       'warning':'Coverage is not accuracy. No independent 1640 plaintext witness; singleton values and glyph reviews qualified in evidence. 14 remains unassigned.'}
    (ROOT/'results/1640-supplement-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':run()
