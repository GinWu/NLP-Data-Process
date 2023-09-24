## 脚本运行
1、脚本运行依赖见：requirements.txt，若环境中无相应包，首次运行脚本前先执行 pip install -r requirements.txt 安装
2、执行如下命令即可：
python reader.py \
    --src_dir <pdf_source_dir> \
    --out_dir <json_output_dir> 
其中 <pdf_source_dir>、<json_output_dir> 自行替换成待转换 pdf 所在目录，<json_output_dir> 为转换后输出目录。若不设置，则分别默认为 ./src、./outputs
## 功能说明
1、该脚本支持法规条款文件由 PDF 解析转换为 json 文件
2、该脚本转换限制原 PDF 文件格式如下：
    - 包含页头、页脚
    - 包含页号，且页号为 "- n -" 格式(n 代表页号)
    - 一个 PDF 仅含一篇法规文件
    - 页面内容布局需为如下固定结构（具体参照：./src/101.pdf）：
        标题
        第x章 xxx
        第x条 xxxxx
        ...
        第xx章 xxx
        第xx条 xxx
3、输出 json 目录结构为：
    {
        "head": "", # 页头
        "tail": "", # 页脚
        "title": "", # 标题
        "contents": [
            {
                "chapter": "", # 第几章
                "chapter_title": "", # 章节标题
                "sections": [
                    {
                        "section": "", # 第几条
                        "content": "" # 条款内容
                    }
                ]
            },
            {
                "chapter": "",
                "chapter_title": "",
                "sections": [
                    {
                        "section": "",
                        "content": ""
                    }
                ]
            }
        ]
    }
