import os
import PyPDF2
import re
import json
import argparse

CHAPTER_PATTERN = "第.*章|第\n*.*\n*章|第\n*.*\n*.*\n章"
SECTION_PATTERN = "第.*条|第\n*.*\n*条|第\n*.*\n*.*\n条"
PAGE_PATTERN = "-\t.*\t-"
LIST_PATTERN = "(?<=[:;])\(.*\)()"


def analyze_test(text):
    outputs = {
        "head": "",
        "tail": "",
        "title": "",
        "contents": []
    }
    text_list = re.split(CHAPTER_PATTERN, text ,maxsplit=0, flags=0)

    head = text_list[0].split("\n")[0]
    tail = text_list[0].split("\n")[2]
    title = "".join(text_list[0].split("\n")[5: -1])
    chapter_list = re.findall(CHAPTER_PATTERN, text, flags=0)
    chapter = {}
    contents = []
    for i in range(len(chapter_list)):
        txt = text_list[i + 1]
        chapter["chapter"] = chapter_list[i].replace("\n", "")
        chapter["chapter_title"] = section_content[0].replace("\n", "").replace("\t", "")
        section_content = re.split(SECTION_PATTERN, txt, maxsplit=0, flags=0)
        section_list = re.findall(SECTION_PATTERN, txt, flags=0)
        sections = []
        for j in range(len(section_list)):
            content = section_content[j+1].replace(head, "").replace(tail, "").replace("\n", "")
            content = "".join(re.split(PAGE_PATTERN, content ,maxsplit=0, flags=0))
            for t in [";(", ":(", "。("]:
                content = content.replace(t, t[0] + "\n\t" + t[1:])
            content = content.strip()
            sections.append({
                                "section": section_list[j].replace("\n", ""), 
                                "content": content
                            })
        chapter["sections"] = sections
        sections = []
        contents.append(chapter)
        chapter = {}
    outputs["contents"] = contents
    outputs["head"] = head
    outputs["tail"] = tail
    outputs["title"] = title
    return outputs

def read_pdf(file_path):
    with open(file_path, "rb") as pdf_file:
        text = ""
        reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(reader.pages)
        for n in range(num_pages):
            page = reader.pages[n]
            
            text += page.extract_text()
    return text

def write_result(outputs, output_file_path):
    
    with open(output_file_path, "w", encoding = "utf-8") as f:
        f.write(json.dumps(outputs, indent = 4, ensure_ascii = False))

def get_pdf_content(src_file_path, output_file_path):
    print("[INFO] analyzing pdf: {}".format(src_file_path))
    text = read_pdf(src_file_path)
    outputs = analyze_test(text)
    print("[INFO] writing result to: {}".format(output_file_path))
    write_result(outputs, output_file_path)

def main():
    project_path = os.path.dirname(os.path.abspath(__file__))
    
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--src_dir", type=str, default = f"{project_path}/src", help = "pdf source root")
    parser.add_argument("--out_dir", type=str, default = f"{project_path}/outputs", help = "output root")
    args = parser.parse_args()
    src_path = args.src_dir
    out_dir = args.out_dir
    print("===========================================================")
    print("start pdf reader...")
    print("project dir: {}".format(project_path))
    print("source dir: {}".format(src_path))
    print("output dir: {}".format(out_dir))
    print("===========================================================")
    pdfs = os.listdir(src_path)
    for pdf in pdfs:
        src_file_path = f"{src_path}/{pdf}"
        
        output_file_path = "{}/{}.json".format(out_dir, ".".join(pdf.split(".")[:-1]))
        get_pdf_content(src_file_path, output_file_path)
    print("finished!")
if __name__ == "__main__":
    main()


