import re


# 去除标题中的非法字符 (Windows)
def validateTitle(title):
    # '/\:*?"<>|'
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "", title)
    return new_title


# 去除标题中的非法字符 (Windows)
def replaceText(title):
    # '/\:*?"<>|'
    rstr = r'『.*/』|先给自己定个小目标：比如收藏：. 手机版网址：m.|' \
           '记住手机版网址：|nt|正在手打中，请稍等片刻，|内容更新后，请重新刷新页面，即可获取最新更新！|\(.*?棉花糖小说网\)' \
           '|（.*?无弹窗广告）|\[.*?超多好看小说\]|（.*?好看的小说|\[棉花糖小说网.*?想看的书' \
           '|www\.mht\.la想看的书几乎都有啊，比一般的小说网站要稳定很多更新还快，全文字的没有广告。\]' \
           '|Mianhuatang\.cc更新快，网站页面清爽，广告少，无弹窗，最喜欢这种网站了，一定要好评\]' \
           '|(www\.mht\.la 棉花糖小说网)|\(www\.mht\.la 棉、花‘糖’小‘说’\)' \
           '|比一般的小说网站要稳定很多更新还快，全文字的没有广告。\]|\[看本书最新章节请到棉花糖小说网www\.mht\.la\]|\[.*?棉花糖小说网.*?\]' \
           '|\[看本书最新章节请到.*?www.mht.la\]|mht\.la'
    new_title = re.sub(rstr, "", title)
    return new_title
