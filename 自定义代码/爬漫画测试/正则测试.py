import re

# return p;}('f 7(){1 5=3;1 4=\'8\';1 6="g://j-h-e-9-a.c.b/k/p/3";1 2=["/o.q"];l(1 i=0;i<2.m;i++){2[i]=6+2[i]+\'?5=3&4=8\'}n 2}1 d;d=7();',27,27,'|var|pvalue|586848|key|cid|pix|dm5imagefun|0b6a8129fb5fd59b19a2e975203c43ed|50|98|com|cdndm5||174|function|http|61||manhua1032|34|for|length|return|8_2941|33771|jpg'.split('|'),0,{}))
str_js = 'eval(function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return\'\\w+\'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp(\'\\b\'+e(c)+\'\\b\',\'g\'),k[c]);return p;}(\'f 7(){1 5=3;1 4=\'8\';1 6="g://j-h-e-9-a.c.b/k/p/3";1 2=["/o.q"];l(1 i=0;i<2.m;i++){2[i]=6+2[i]+\'?5=3&4=8\'}n 2}1 d;d=7();\',27,27,\'|var|pvalue|586848|key|cid|pix|dm5imagefun|0b6a8129fb5fd59b19a2e975203c43ed|50|98|com|cdndm5||174|function|http|61||manhua1032|34|for|length|return|8_2941|33771|jpg\'.split(\'|\'),0,{}))'
find_pattren = re.compile(r'p;}\(\'.*?\)\)')
text = re.search(find_pattren, str_js).group()[4:-2]
print(text)