'''class AllCOUNT3:
    def __init__(self, a,b,c):
        self.a = a
        self.b = b
        self.c = c
    def sum(self):
        d = self.a+self.b+self.c
        print(d)

al = AllCOUNT3(1,2,3)

al.sum()'''

class n_mzero:
    def __init__(self,a):
        self.a = a
        self.t = []

    def temp_count(self,):
        for _ in range(self.a):
            b = float(input())
            if b>0:
                self.t.append(b)
        return self.t

class uwu:
     global aa
     global bb
     def __init__(self,aa,bb):
        self.aa = aa
        self.bb = bb
     def calc(self):
         cass = input()
         if cass == "*":
             print(self.aa*self.bb)
         elif cass == "+":
             print(self.aa+self.bb)
         elif cass == "-":
             print(self.aa-self.bb)
         elif cass == "/":
             print(self.aa/self.bb)

