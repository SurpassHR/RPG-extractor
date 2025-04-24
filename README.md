# RGSS-rxdata-extractor

## Description

This is a tool for extracting RPG(Role Playing Game) related data that has `.rxdata` or `.rvdata` ext.

## Usage

```shell
bash ./init_dev_env.sh
# edit config.json
python ./extractor.py
```

## Todo

- [x] Multi-threaded file-writing

- [x] Decode Scripts.rxdata

- [ ] Parse Scripts.rxdata

- [ ] Recognizing illegal words and phrases

- [ ] Merge my another format module into this

- [ ] GUI

- [ ] Make reader module more extensible to support other format like json

## 代码重构

- Extractor 承担总体的提取任务，包括读取文件、解析文件、写入文件等，它会协调使用 Reader、Parser、Formatter、Exporter 等模块来完成具体的任务。
    - Extractor 初始化时接受入参，包括输入文件路径、输出文件路径、处理文件格式，这三个参数由 ConfigLoader 提供。
    - Reader 初始化时接受入参，为文件列表，由 Extractor 预处理提供。
        - Reader 对外提供 read 方法，读取后存储相关数据在 Reader 内部。
        - Reader 对外提供 get 方法，返回存储的数据。
        - Reader 存储的数据对外不展示具体数据结构，由一 Any 类型的 data 表示。
    - Parser 初始化时接受入参，为 Reader 的 data，由 Extractor 提供。
        - Parser 对外提供 parse 方法，解析后存储相关数据在 Parser 内部。
        - Parser 对外提供 get 方法，返回存储的数据。
        - Parser 存储的数据对外不展示具体数据结构，由一 Any 类型的 data 表示。
    - Formatter 初始化时接受入参，为 Parser 的 data，由 Extractor 提供。
        - Formatter 对外提供 format 方法，格式化后存储相关数据在 Formatter 内部。
        - Formatter 对外提供 get 方法，返回存储的数据。
        - Formatter 存储的数据对外不展示具体数据结构，由一 Any 类型的 data 表示。
    - Exporter 初始化时接受入参，为 Formatter 的 data，由 Extractor 提供。
        - Exporter 对外提供 export 方法，将数据写入文件。
    - 一种文件类型对应一种类型的 Reader、Parser、Formatter、Exporter，保证了 data 在各个模块之间的传递不会出现类型不匹配的问题。

---