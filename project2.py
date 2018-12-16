import math

def bins(file):
    lista =[]
    with open(file) as f:
        next(f)
        for line in f:
            descriptions = line.strip().split(",")
            passenger = descriptions[0]
            survival = int(descriptions[1])
            pclass = int(descriptions[2])
            name = descriptions[3],descriptions[4]
            sex = descriptions[5]
            age = str(descriptions[6])
            numofsiblings = int(descriptions[7])
            parents = int(descriptions[8])
            fare = float(descriptions[10])
            if age == "":
                if "Master" in name:
                    age = "child"
                elif "Miss" in name:
                    if numofsiblings > 0 or parents > 0:
                        age = "child"
                    else:
                        age = False
                else:
                    age = False
            elif float(age) < 17:
                age = "child"
            elif float(age) in range(17,25):
                age = "young adult"
            elif float(age) in range(25,60):
                age = "adult"
            else:
                age = "aged"
            if sex == "":
                if passenger%2:
                    sex = "male"
                else:
                    sex = "female"
            if numofsiblings > 0:
                siblings = "yes"
            else:
                siblings = "no"
            if parents > 0:
                parents = "yes"
            else:
                parents = "no"
            if age:
                lista.append((survival,pclass,sex,age,siblings,parents,fare,passenger,))
    return lista
    
lista = bins("train.csv")

def entropy(lista):
    cat1, cat2 = 0, 0
    for tupla in lista:
        if tupla[0] == 0:
            cat1 += 1
        elif tupla[0] == 1:
            cat2 += 1
    p1 = cat1/(cat1+cat2)
    p2 = cat2/(cat1+cat2)
    if p1==0 or p2==0:
        return 0
    return -p1*math.log(p1,2) - p2*math.log(p2,2)


## for divide function cVSall = children vs all, cyaVSaag = child and young adult vs adult and aged, agVSall = aged vs all    
## confused
def divide(lista, descrip, sort):
    if descrip == 3:
        if sort == "cVSall":
            return [x for x in lista if str(x[3]) == "child"], [x for x in lista if str(x[3]) != "child"]
        elif sort == "cyaVSaag":
            return [x for x in lista if str(x[descrip]) == "child" or "young adult"], [x for x in lista if str(x[descrip]) == "adult" or str(x[descrip]) == "aged"]
        elif sort == "agVSall":
            return [x for x in lista if str(x[descrip]) == "aged"], [x for x in lista if str(x[descrip]) == "young adult" or str(x[descrip]) == "adult" or str(x[descrip]) == "child"]
    elif descrip == 4 or descrip == 5:
        return [x for x in lista if x[descrip] == "yes"], [x for x in lista if x[descrip] == "no"]
    
    elif descrip == 6:
        return [x for x in lista if float(x[descrip]) <= sort], [x for x in lista if float(x[descrip])> sort]
    elif descrip == 2:
        return [x for x in lista if str(x[descrip]) == "male"],[x for x in lista if str(x[descrip]) == "female"]
    elif descrip == 1:
        return [x for x in lista if int(x[descrip]) <= sort], [x for x in lista if int(x[descrip])> sort]

            

def fares(lista):
    fares = []
    for x in lista:
        fare = x[6]
        fares.append(fare)
    return fares

listb = fares(lista)


        

def gainfare(lista, coordinate):
    bestent = 1
    index = 0
    for i in range(200):
        list1, list2 = divide(lista, coordinate, i)
        if len(list1)<=5 or len(list2)<=5:
            return 0
        new_entropy = len(list1)/(len(list1)+len(list2))*entropy(list1) + len(list2)/(len(list1)+len(list2))*entropy(list2)
        if new_entropy < bestent:
            bestent = new_entropy
            index = i
    return index, bestent

def gain(lista, coordinate, value):
    list1, list2 = divide(lista, coordinate, value)
    if len(list1)<=3 or len(list2)<=3:
        return 0
    new_entropy = len(list1)/(len(list1)+len(list2))*entropy(list1) + len(list2)/(len(list1)+len(list2))*entropy(list2)
    return "List 1: {}-- List 2: {}-- Entropy: {}".format(count(list1),count(list2),(entropy(lista)-new_entropy))


def tree(lista,coordinate,value):
    list1, list2 = divide(lista, coordinate, value)
    if percentded(list1) < .2:
        print("stop list1 80% alive")
    elif percentded(list1) > .8:
        print("stop list1 80% dead")
    elif percentded(list2) < .2:
        print("stop list2 80% alive")
    elif percentded(list2) > .8:
        print("stop list2 80% dead")
    elif len(list1) < 5:
        print("less than 5 in list1")
        print(percentded(list1))
    elif len(list2) < 5:
        print("less than 5 in list2")
        print(percentded(list2))
    else:
        print(percentded(list1),percentded(list2))

listm, listf = divide(lista, 2, 0)

listm1, listm2 = divide(listm, 6, 52)

listm21, listm22 = divide(listm2,1,2)

listm21p, listm21np = divide(listm21,5,0)

list21pc, list21pnc = divide(listm21p,3,"cVSall")

list21npA, list21npNA = divide(listm21np,3,"agVSall")

list21pncA,list21pncNA = divide(list21pnc,3,"agVSall")

##end of male now females
listf1, listf2 = divide(listf, 6, 52)

listf11, listf12 = divide(listf1, 1,2)

listf12A,listf12NA = divide(listf12,3,"agVSall")

listf12NAc,listf12NAnc = divide(listf12NA,4,"cVSall")


def count(lista):
    ct1, ct2 = 0,0
    for tupla in lista:
        if tupla[0] == 0:
            ct1 += 1
        elif tupla[0] == 1:
            ct2 += 1
        else:
            raise ValueError
    return "(dead: {}  Survived: {})".format(ct1,ct2)

def percentded(lista):
    ct1, ct2 = 0,0
    for tupla in lista:
        if tupla[0] == 0:
            ct1 += 1
        elif tupla[0] == 1:
            ct2 += 1
        else:
            raise ValueError
    return ct1/(ct1+ct2)
   
def predict(element):
    if element[2] == "male":
        if element[6] < 52:
            return "dead"
        else:
            if element[1] > 3:
                return "alive"
            else:
                if element[5] == "yes":
                    if element[3] == "child":
                        return "alive"
                    else:
                        return "dead"
                else:
                    return "dead"
    else:
        if element[6] > 52:
            return "alive"
        else:
            if element[1] < 3:
                return "alive"
            else:
                if element[3] == "aged":
                    return "dead"
                else:
                    if element[3] == "child":
                        return "alive"
                    else:
                        return "dead"




            
