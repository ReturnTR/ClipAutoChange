# 此文件不允许在开头添加任何包，如需添加请在函数中添加

def comma_for_every_line(s):
    s=s.split("\n")
    s=[i for i in s if i]
    s=['"'+i+'"' for i in s]
    s="\n".join(s)
    s.strip("\n")
    return s