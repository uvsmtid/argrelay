
Several sub-dirs here contain files prefixed with an id:

```
XX_NN_NN_NN_NN
```
where:
*   `XX`: prefix depends on type of the doc:
    *   `FS` for `feature_story`
    *   `KI` for `known_issue`
    *   `TD` for `test_data`
    *   ...
*   `NN_NN_NN_NN`: random number

These ids are referenced in other files to bind related places together.

Such ids (instead of simple words or numbers) robust against accidental change in mass renames
and better survive refactoring.

To provide hints, ids are often followed by ignorable mnemonic keywords or abbreviations, for example:

```
FS_53_81_66_18 # TnC
TD_70_69_38_46 # no data
```
