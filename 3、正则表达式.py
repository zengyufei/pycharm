import re  # 正则表达式必须导入 re 包

# 判断是否匹配
result = re.match(r"[aeiou]", "abcdefg")
print(result)  # <_sre.SRE_Match object; span=(0, 1), match='a'>
print(result is not None)  # True

result = re.match(r"[aeiou]", "cbcdefg")
print(result)  # None
print(result is not None)  # False

#  以第二个参数指定的字符替换原字符串中内容
result = re.sub(r"[aeiou]", "?", "abcdefg")
print(result)  # ?bcd?fg

# 向前向后查找
str = r"<html><body><h1>hello world</h1></body></html>"
key = r"(?<=<h1>).+?(?=</h1>)"  # 看到 (?<=<h1>) 和 (?=<h1>) 了吗？第一个 ?<= 表示在被匹配字符前必须得有 <h1>，后面的 ?= 表示被匹配字符后必须有 <h1>。只要记住 ?<= 后面跟着的是前缀要求，?= 后面跟的是后缀要求。
pattern1 = re.compile(key)
matcher1 = re.search(pattern1, str)
print(matcher1.group(0))  # hello world

strTest = "\\asdasd"
search = re.search(re.compile(r"\\$"), strTest)
if search:
    print(search.group())
else:
    print(search)