import re

import execjs


# 解析js
def regnext(str_js):
    find_pattren = re.compile(r'p;}\(\'.*?\)\)')
    arg = ''
    try:
        arg = re.search(find_pattren, str_js).group()[4:-2]
    except:
        print(str_js)
    ctx = execjs.compile(""" 
        function aa(){
            return function(p,a,c,k,e,d){
                e=function(c){
                    return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))
                };
                while(c--){
                   d[e(c)]=k[c]||e(c);
                }
                p=p.replace(/\\b\\w+\\b/g,function(e){
                    return d[e]
                });
                return p;
            }
            (""" + arg + """)
        }
    """)
    x = ctx.call("aa", 1)
    ctx = execjs.compile(x)
    x = ctx.call("dm5imagefun", 1)
    return x


# 去除标题中的非法字符 (Windows)
def validateTitle(title):
    # '/\:*?"<>|'
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "", title)
    return new_title
