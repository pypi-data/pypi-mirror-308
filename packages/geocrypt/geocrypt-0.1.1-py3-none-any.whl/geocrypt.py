import sympy
import random
import sys
version="0.1.1"
sys.set_int_max_str_digits(100000)
hexa=["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
class CodeError(Exception):
    pass
class DecodeError(Exception):
    pass
class Droite:
    def __init__(self,x0,y0,slope):
        self.x0=x0
        self.y0=y0
        self.slope=slope
    def get_point(self,t):
        x_new=self.x0+t
        y_new=self.slope*(x_new-self.x0)+self.y0
        return (x_new,y_new)
class Key:
    def __init__(self):
        self.x=0
        self.t=0
        self.a=0
        self.b=0
        self.c=0
        self.map={}
    def generate(self):
        xv=""
        for i in range(128):
            xv=xv+str(random.randint(0,1))
        self.x=int(xv,2)
        av=""
        for i in range(32768):
            av=av+str(str(random.randint(0,1)))
        self.a=int(av,2)
        bv=""
        for i in range(32768):
            bv=bv+str(str(random.randint(0,1)))
        self.b=int(bv,2)
        cv=""
        for i in range(32768):
            cv=cv+str(str(random.randint(0,1)))
        self.c=int(cv,2)
        self.t=random.randint(10**99,10**100)
        random.seed(self.x)
        for i in range(len(hexa)):
            val=random.randint(123,954)
            while val in self.map.values():
                val=random.randint(123,954)
            self.map[hexa[i]]=val
def code(text,key:Key):
    for i in text:
        if not i in hexa:
            raise CodeError(i+" isn't encodable.")
    if not type(key)==Key:
        raise TypeError("key should be from the Key class.")
    if key.a==0 or key.b==0 or key.c==0 or key.x==0 or key.t==0 or key.map=={}:
        raise KeyError("key isn't generated.")
    a,b,c,x,t=sympy.symbols("a b c x t")
    f=a*x**2+b*x+c
    fp=sympy.diff(f,x)
    der=fp.evalf(subs={x:key.x,a:key.a,b:key.b,c:key.c})
    y=f.subs({x: key.x, a: key.a, b: key.b, c: key.c}).evalf()
    tan=Droite(key.x,y,der)
    co=tan.get_point(key.t)
    number=co[0]*co[1]
    fin=int(str(int((x**(1/900)).subs(x,number).evalf()))[len(str(int((x**(1/850)).subs(x,number).evalf())))-3:len(str(int((x**(1/850)).subs(x,number).evalf())))])
    newlist=[]
    for i in range(len(text)):
        newlist.append(key.map[text[i]])
    newtext=""
    for i in range(len(newlist)):
        ob=""
        for y in range(fin):
            ob=ob+str(random.randint(0,9))
        newtext=newtext+str(newlist[i])+ob
    return newtext
def decode(text,key:Key):
    for i in text:
        try:
            int(i)
        except:
            raise DecodeError(i+" isn't decodable.")
    if not type(key)==Key:
        raise TypeError("key should be from the Key class.")
    if key.a==0 or key.b==0 or key.c==0 or key.x==0 or key.t==0 or key.map=={}:
        raise KeyError("key isn't generated.")
    a,b,c,x,t=sympy.symbols("a b c x t")
    f=a*x**2+b*x+c
    fp=sympy.diff(f,x)
    der=fp.evalf(subs={x:key.x,a:key.a,b:key.b,c:key.c})
    y=f.subs({x: key.x, a: key.a, b: key.b, c: key.c}).evalf()
    tan=Droite(key.x,y,der)
    co=tan.get_point(key.t)
    number=co[0]*co[1]
    fin=int(str(int((x**(1/900)).subs(x,number).evalf()))[len(str(int((x**(1/850)).subs(x,number).evalf())))-3:len(str(int((x**(1/850)).subs(x,number).evalf())))])
    dedict={}
    for i in range(len(hexa)):
        dedict[list(key.map.values())[i]]=list(key.map.keys())[i]
    delist=[]
    for i in range(0,len(text),fin+3):
        delist.append(int(text[i:i+3]))
    newtext=""
    for i in delist:
        newtext=newtext+dedict[i]
    return newtext
if __name__=="__main__":
    k=Key()
    k.generate()
    c=code("664487875ABFECD",k)
    print(c)
    print(decode(c,k))