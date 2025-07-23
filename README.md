# RGSS-rxdata-extractor

## Description

This is a tool for extracting RPG(Role Playing Game) related data that has `.rxdata`, `.rvdata`, `.json` and `.js` ext.
The structure is extensible as you can add your 'processer' to src/processers.

## Usage

```shell
bash ./init_dev_env.sh
# edit config.json to set the game data you want to extract from
python ./run.py
```

## Supported game data file type

- `Rxdata`

- `Rvdata`

- `Json`

- Plugins with `.js` ext

## Todo

- [x] Multi-threaded file-writing

- [x] Decode Scripts.rxdata

- [ ] Parse Scripts.rxdata

- [ ] Recognizing illegal words and phrases

- [x] Merge my another format module into this

- [ ] GUI

- [x] Make reader module more extensible to support other format like json

- [x] Auto guessing the main file type under the set path

- [x] Support cli arguments, see `argParser.py`