import execjs

x = execjs.eval("'red yellow blue'.split(' ')")
print(x)
ctx = execjs.compile(""" 
    function add(x, y) { 
        return x + y; 
    } 
""")
x = ctx.call('add', 1, 2)
print(x)
ctx = execjs.compile(""" 
    function aa(){
        return function(a){
            return a;
        }
        ('h8(){
            1 5=3;1 7="9";1 6="g://f-k-j-a-b.e.c/l/q/3";1 2=["/p.4","/r.4"];
            m(1 i=0;i<2.n;i++){
                2[i]=6+2[i]+"?5=3&7=9"
            }o 2
          }1 d;
          d=8();
          ',
        28,
        28,
        '|var|pvalue|586848|jpg|cid|pix|key|dm5imagefun|62bc7aeb82482c7a1ac4dd0e5dc6bffc|50|98|com||cdndm5|manhua1032|http|function||174|61|34|for|length|return|1_3254|33771|2_9445'.split('|'))
    }
""")
x = ctx.call("aa")
print(x)
