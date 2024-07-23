text = "fgags"#"WINDOW|hif sfssfsf"

text_list = text.split('|')
title = ""
content = text_list[0]
if (len(text_list)>1):
    title = text_list[0]
    content = text_list[1]

print(text_list)
print(title)
print(content)