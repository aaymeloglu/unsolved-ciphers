# Reconstructed 1635 alphabet

See [occurrence-level evidence](key-evidence.tsv) and the three alignment tables. These are transliterated glyph labels, not a facsimile of a historical key. Plaintext u/v is combined as u.

| Plain | Cipher labels |
|---|---|
| a | `0`, `n`, `z`, `t`, `o` |
| b | `8`, `9` |
| c | `x`, `7` |
| d | `4`, `3` |
| e | `m`, `p`, `6` |
| f | `5`, `2` |
| g | `17`, `16` |
| h | `10`, `1` |
| i | `h`, `15`, `24`, `11`, `12` |
| l | `18`, `19` |
| m | `d`, `e` |
| n | `22`, `32` |
| o | `f`, `l`, `a` |
| p | `g`, `20` |
| q | `33`, `30` |
| r | `c`, `i`, `q` |
| s | `31`, `25`, `26` |
| t | `37`, `34` |
| u | `y`, `23`, `38`, `35` |
| x | `39` |

`6=e` is disputed outside the training passage: b/6-like forms may have been conflated. It is not valid to switch this glyph to m whenever Latin requires it. The literal output preserves the selected mapping and its resulting errors.

42 assignments belong to frozen v1. E-series evidence adds 17=g, 18=l, 19=l, 16=g, 2=f. F-series evidence adds 9=b, e=m, 30=q, o=a after validation. No null or word/syllable code was recovered from R1889. Other letters or homophones may be missing.

The catalog description of two or three homophones per alphabet letter was not imposed on the data: our transliteration has more alternatives for some vowels. Glyph conflations must be resolved before treating this as a complete historical alphabet.

## 1640 supplement, selected after the unchanged test

The [111-entry supplemented map](key-1640-supplemented.json) retains all 51 values above and adds 60 observed values. [Each new mapping has context and occurrence evidence](key-1640-evidence.tsv). These additions are contextual reconstructions from R1890, not independently validated historical key-sheet entries.

| Cipher family | Plaintext values |
|---|---|
| `41 42 43 44` | le li lo lu |
| `45 46 47 48 49` | na ne ni no nu |
| `50 51 52 53 54` | ra re ri ro ru |
| `pla ple pli plo plu` | ta te ti to tu |
| `ap ep ip op up` | ca ce ci co cu |
| `ca ce ci co cu` | ma me mi mo mu |
| `ha he hi hu` | da de di du |
| `an en in un` | sa se si su |
| `tes tis tos tus` | be bi bo bu |
| `au eu ou uu` | pa pe po pu |
| `me mi mu` | fe fi fu |
| `ga gi` | ha hi |
| `it ot et` | gi go ge |
| `21 36 b` | o x m |
| `ko fu lx li` | do mu oc xi (singletons, provisional) |

Unused grid cells are deliberately omitted. Some singleton labels may conceal a paleographic or segmentation issue. In particular, `fu=mu` yields the historical single-m spelling *comunicabit*, while `mmu` could not be excluded on that word alone. Numeric 14 is not assigned from the proper name alone.

The 1640 distinction `b=m` versus `6=e` is supported by its imported labels and repeated *etiam/quam* versus *praeiudicium/velimus* contexts. This is new evidence relevant to the 1635 b/6 problem; it does not retrospectively identify every ambiguous 1635 sign, and no 1635 occurrence has been changed on that basis.

Of the 51 inherited labels, 46 actually occur in the reviewed 1640 stream; `0`, `1`, `2`, `h`, and `i` do not. Retaining those five values in the supplemented JSON is not a 1640 validation of them.
