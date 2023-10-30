from math import *
from chesstk import *

class Chess:
    def __init__(self,largeur=500,hauteur=500,titre=''):
        cree_fenetre(largeur,hauteur,titre)
        
tour,cavalier,fou,reine,roi,pion='♖','♘','♗','♕','♔','♙'
Tournoir1,Cavaliernoir1,Founoir1,Reinenoir,Roinoir,Founoir2,Cavaliernoir2,Tournoir2=[(1,8)],[(2,8)],[(3,8)],[(4,8)],[(5,8)],[(6,8)],[(7,8)],[(8,8)]
Pionnoir1,Pionnoir2,Pionnoir3,Pionnoir4,Pionnoir5,Pionnoir6,Pionnoir7,Pionnoir8=[(1,7)],[(2,7)],[(3,7)],[(4,7)],[(5,7)],[(6,7)],[(7,7)],[(8,7)]
Pionblanc1,Pionblanc2,Pionblanc3,Pionblanc4,Pionblanc5,Pionblanc6,Pionblanc7,Pionblanc8=[(1,2)],[(2,2)],[(3,2)],[(4,2)],[(5,2)],[(6,2)],[(7,2)],[(8,2)]
Tourblanc1,Cavalierblanc1,Foublanc1,Reineblanc,Roiblanc,Foublanc2,Cavalierblanc2,Tourblanc2=[(1,1)],[(2,1)],[(3,1)],[(4,1)],[(5,1)],[(6,1)],[(7,1)],[(8,1)]
etats,deplacements,promu=[],[],[]
for i in range(16):
    promu.append(pion)
def annule(deplacements):
    deplacementreciproque(deplacements[-1])
    del(deplacements[-1])
def autorise(piece,case,etats,Pion=True):
    a,b=def_lst(piece)[-1]
    x,y=case
    dx,dy,noirs,blancs=fabs(a-x),fabs(b-y),etats[:32],etats[32:]
    if ((def_typ(piece)==tour and dx*dy==0)
        or(def_typ(piece)==fou and dx==dy)
        or(def_typ(piece)==reine and ((dx*dy==0) or (dx==dy)))
        or(def_typ(piece)==cavalier and (dx*dy==2))
        or(def_typ(piece)==pion and autorisepion(piece,case,etats) and Pion)
        or(def_typ(piece)==roi and (roque(piece,case,etats,deplacements) or dx*dy==1 or dx+dy==1))) :
        return True
    else:
        return False
def autorisetourfou(piece,case,etats):
    a,b=def_lst(piece)[-1]
    x,y=case
    dx,dy,noirs,blancs=int(x-a),int(y-b),etats[:32],etats[32:]
    if def_typ(piece) not in [reine,tour,fou]:
        return True
    if (a,b)==(x,y):
        return False
    if dy == 0:
        for i in range(a,x-signe(dx),signe(dx)):
            if (signe(dx)+i,b) in etats:
                return False
    elif dx == 0:
        for i in range(b,y-signe(dy),signe(dy)):
            if (a,signe(dy)+i) in etats:
                return False
    elif dx-dy == 0:
        for i in range(0,dx-signe(dx),signe(dx)):
            if (a+i+signe(dx),b+i+signe(dx)) in etats:
                return False
    elif dx+dy == 0:
        for i in range(0,dx-signe(dx),signe(dx)):
            if (a+i+signe(dx),b-i+signe(dy)) in etats:
                return False
    return True
def autorisepion(piece,case,etats):
    a,b=def_lst(piece)[-1]
    x,y=case
    dx,dy,noirs,blancs=fabs(a-x),fabs(b-y),etats[:32],etats[32:]
    if def_typ(piece)!=pion:
        return True
    if y==b+sens(piece) and case not in etats and dx==0:
        return True
    elif y==b+2*sens(piece) and b in [2,7] and case not in etats and (x,y-sens(piece)) not in etats and dx==0:
        return True
    elif y==b+sens(piece) and dx == 1 and case in etats:
        return True
    elif prise_en_passant(piece,case,etats,deplacements):
        return True
    return False
def autoriseroi(piece,case,etats):
    a,b=def_lst(piece)[-1]
    x,y=case
    dx,dy,noirs,blancs=fabs(a-x),fabs(b-y),etats[:32],etats[32:]
    if def_typ(piece)!=roi:
        return True
    if couleur(piece)=='white':
        lst=noirs
    elif couleur(piece)=='black':
        lst=blancs
    for i in range(0,32,2):
        if autorise(lst[i],case,etats,False) and autorisetourfou(lst[i],case,etats):
            return False
    if roque(piece,case,etats,deplacements):
        return True
    if dx>1 or dy>1:
        return False
    if couleur(piece)=='white':
        if (x+1,y+1)in noirs[16:] or (x-1,y+1)in noirs[16:]:
            return False
        else:
            return True
    elif couleur(piece)=='black':
        if (x+1,y-1)in blancs[:16] or (x-1,y-1)in blancs[:16]:
            return False
        else:
            return True
    return True
def capture(piece,case,etats,affiche=True):
    a,b=def_lst(piece)[-1]
    for i in range(1,64,2):
        if (case == etats[i]) and (couleur(etats[i-1])!=couleur(piece)):
            if affiche:
                efface(etats[i-1])
                def_lst(etats[i-1]).append((-8,0))
            else:
                def_lst(etats[i-1]).append((0,-8))
    if prise_en_passant(piece,case,etats,deplacements) and def_typ(piece)==pion:
        if couleur(piece)=='white':
            if affiche:
                efface('pionnoir'+str(case[0]))
                def_lst('pionnoir'+str(case[0])).append((-8,0))
            else:
                def_lst('pionnoir'+str(case[0])).append((0,-8))
        elif couleur(piece)=='black':
            if affiche:
                efface('pionblanc'+str(case[0]))
                def_lst('pionblanc'+str(case[0])).append((-8,0))
            else:
                def_lst('pionblanc'+str(case[0])).append((0,-8)) 
    if roque(piece,case,etats,deplacements) and def_typ(piece)==roi:
        if couleur(piece)=='white':
            if case==(7,1):
                deplacement('tourblanc2',(6,1),etats,affiche)
            elif case==(3,1):
                deplacement('tourblanc1',(4,1),etats,affiche)
        elif couleur(piece)=='black':
            if case==(7,8):
                deplacement('tournoir2',(6,8),etats,affiche)
            elif case==(3,8):
                deplacement('tournoir1',(4,8),etats,affiche)
def case_vers_pixel(case):
    i,j = case
    return i * 62.5 - 31.25, 531.25 - j * 62.5
def copie_liste(lst):
    lst0=[]
    for i in range(len(lst)):
        lst0.append(lst[i])
    return lst0
def couleur(piece):
    if piece[-4:]=='noir' or piece[-5:-1]=='noir':
            return 'black'
    elif piece[-5:]=='blanc' or piece[-6:-1]=='blanc':
            return 'white'
    else:
        return ''
def def_typ(piece):
        for i in range(5):
            if ['tour','cavalier','fou','reine','roi'][i] in piece:
                return [tour,cavalier,fou,reine,roi][i]
            elif 'pion' in piece:
                return promu[(sens(piece)+1)*4+int(piece[-1])-1]
def def_lst(piece):
        for i in range(32):
                if['tournoir1','cavaliernoir1','founoir1','reinenoir','roinoir','founoir2','cavaliernoir2','tournoir2','pionnoir1','pionnoir2','pionnoir3','pionnoir4','pionnoir5','pionnoir6','pionnoir7','pionnoir8',
                   'pionblanc1','pionblanc2','pionblanc3','pionblanc4','pionblanc5','pionblanc6','pionblanc7','pionblanc8','tourblanc1','cavalierblanc1','foublanc1','reineblanc','roiblanc','foublanc2','cavalierblanc2','tourblanc2'][i]==piece:
                        return [Tournoir1,Cavaliernoir1,Founoir1,Reinenoir,Roinoir,Founoir2,Cavaliernoir2,Tournoir2,Pionnoir1,Pionnoir2,Pionnoir3,Pionnoir4,Pionnoir5,Pionnoir6,Pionnoir7,Pionnoir8,
                                Pionblanc1,Pionblanc2,Pionblanc3,Pionblanc4,Pionblanc5,Pionblanc6,Pionblanc7,Pionblanc8,Tourblanc1,Cavalierblanc1,Foublanc1,Reineblanc,Roiblanc,Foublanc2,Cavalierblanc2,Tourblanc2][i]
def deplacement(piece,arr,etats,affiche=True):
    if affiche:
        efface(piece)
    i,j = case_vers_pixel(arr)
    if affiche:
        texte(i,j,def_typ(piece),couleur(piece),'center','Purisa',48,piece)
    def_lst(piece).append(arr)
    if affiche:
        deplacements.append(piece)
def deplacementreciproque(piece):
    efface(piece)
    i,j=case_vers_pixel(def_lst(piece)[-2])
    texte(i,j,def_typ(piece),couleur(piece),'center','Purisa',48,piece)
    del(def_lst(piece)[-1])
def echec_non(piece,case,etats,trait):
    return True
    lst0=copie_liste(etats)
    Roque=False
    capture(piece,case,lst0,False)
    if roque(piece,case,lst0,deplacements) and def_typ(piece)==roi:
        Roque=True
    deplacement(piece,case,lst0,False)
    lst0,compteur=[],0
    if trait:
        Roi='roiblanc'
    elif not trait:
        Roi='roinoir'
    for i in range(32):
        a=['tournoir1','cavaliernoir1','founoir1','reinenoir','roinoir','founoir2','cavaliernoir2','tournoir2',
            'pionnoir1','pionnoir2','pionnoir3','pionnoir4','pionnoir5','pionnoir6','pionnoir7','pionnoir8',
            'pionblanc1','pionblanc2','pionblanc3','pionblanc4','pionblanc5','pionblanc6','pionblanc7','pionblanc8',
            'tourblanc1','cavalierblanc1','foublanc1','reineblanc','roiblanc','foublanc2','cavalierblanc2','tourblanc2'][i]
        lst0.append(a)
        lst0.append(def_lst(a)[-1])
    if autoriseroi(Roi,def_lst(Roi)[-1],lst0):
        compteur+=1
    del(def_lst(piece)[-1])
    for i in range(32):
        a=['tournoir1','cavaliernoir1','founoir1','reinenoir','roinoir','founoir2','cavaliernoir2','tournoir2',
           'pionnoir1','pionnoir2','pionnoir3','pionnoir4','pionnoir5','pionnoir6','pionnoir7','pionnoir8',
           'pionblanc1','pionblanc2','pionblanc3','pionblanc4','pionblanc5','pionblanc6','pionblanc7','pionblanc8',
           'tourblanc1','cavalierblanc1','foublanc1','reineblanc','roiblanc','foublanc2','cavalierblanc2','tourblanc2'][i]
        if (0,-8) in def_lst(a):
            del def_lst(a)[def_lst(a).index((0,-8))]
    if Roque:
        for w in range(2):
            if [(6,1),(4,1)][w] in def_lst(['tourblanc2','tourblanc1'][w]) and def_typ(piece)==roi and trait:
                del(def_lst(['tourblanc2','tourblanc1'][w])[-1])
            elif[(6,8),(4,8)][w] in def_lst(['tournoir2','tournoir1'][w]) and def_typ(piece)==roi and not trait:
                del(def_lst(['tournoir2','tournoir1'][w])[-1])
        Roque=False
    if compteur > 0:
        return True
    else:
        return False
def echec(piece,case,etats):
    noirs,blancs,compteur=etats[:32],etats[32:],0
    if couleur(piece)=='white':
        lst=noirs
    elif couleur(piece)=='black':
        lst=blancs
    for i in range(0,32,2):
        if autorise(lst[i],case,etats) and autorisetourfou(lst[i],case,etats):
            compteur+=1
            selec(lst[i+1],'red','echec')
    if compteur>0:
        print('echec aux '+piece[3:]+'s')
        return True
    else:
        return False
def echiquier():
    for i in range(8):
        for j in range(8):
                if (i+j)%2==0:
                        rectangle(i*62.5,j*62.5,(i+1)*62.5,(j+1)*62.5,'','darkgrey')
                else:
                        rectangle(i*62.5,j*62.5,(i+1)*62.5,(j+1)*62.5,'','grey')
        mise_a_jour()
    for i in range(8):
        texte(0,62.5*i,str(8-i),['darkgrey','grey'][(1+i)%2],'nw','Purisa',10,str(8-i))
        texte(62.5*(i+1),500,str(chr(97+i)),['darkgrey','grey'][(i)%2],'se','Purisa',10,str(chr(97+i)))
    mise_a_jour()
def emplacement(pixel):
    i,j = pixel
    return(int(i // 62.5 + 1),int(8 - j // 62.5))
def mat_ou_pat(etats,trait):
    noirs,blancs,compteur=etats[:32],etats[32:],0
    Roque=False
    if trait:
        lst=blancs
        Roi='roiblanc'
    elif not trait:
        lst=noirs
        Roi='roinoir'
    for q in range(0,32,2):
        piece=lst[q]
        for x in range(1,9):
            for y in range(1,9):
                lst0=copie_liste(etats)
                if autorise(piece,(x,y),lst0)and autorisetourfou(piece,(x,y),lst0) and autoriseroi(piece,(x,y),lst0) and (((couleur(piece)=='black')!=((x,y) in noirs)) or (x,y) not in lst0):
                    if roque(piece,(x,y),lst0,deplacements) and def_typ(piece)==roi:
                        Roque=True
                    capture(piece,(x,y),lst0,False)
                    deplacement(piece,(x,y),lst0,False)
                    lst0=[]
                    for i in range(32):
                        a=['tournoir1','cavaliernoir1','founoir1','reinenoir','roinoir','founoir2','cavaliernoir2','tournoir2',
                           'pionnoir1','pionnoir2','pionnoir3','pionnoir4','pionnoir5','pionnoir6','pionnoir7','pionnoir8',
                           'pionblanc1','pionblanc2','pionblanc3','pionblanc4','pionblanc5','pionblanc6','pionblanc7','pionblanc8',
                           'tourblanc1','cavalierblanc1','foublanc1','reineblanc','roiblanc','foublanc2','cavalierblanc2','tourblanc2'][i]
                        lst0.append(a)
                        lst0.append(def_lst(a)[-1])
                    if autoriseroi(Roi,def_lst(Roi)[-1],lst0):
                        compteur+=1
                    del(def_lst(piece)[-1])
                    if Roque:
                        for w in range(2):
                            if [(6,1),(4,1)][w] in def_lst(['tourblanc2','tourblanc1'][w]) and def_typ(piece)==roi and trait:
                                del(def_lst(['tourblanc2','tourblanc1'][w])[-1])
                            elif[(6,8),(4,8)][w] in def_lst(['tournoir2','tournoir1'][w]) and def_typ(piece)==roi and not trait:
                                del(def_lst(['tournoir2','tournoir1'][w])[-1])
                        Roque=False
    for i in range(32):
        a=['tournoir1','cavaliernoir1','founoir1','reinenoir','roinoir','founoir2','cavaliernoir2','tournoir2',
           'pionnoir1','pionnoir2','pionnoir3','pionnoir4','pionnoir5','pionnoir6','pionnoir7','pionnoir8',
           'pionblanc1','pionblanc2','pionblanc3','pionblanc4','pionblanc5','pionblanc6','pionblanc7','pionblanc8',
           'tourblanc1','cavalierblanc1','foublanc1','reineblanc','roiblanc','foublanc2','cavalierblanc2','tourblanc2'][i]
        while (0,-8) in def_lst(a):
            del def_lst(a)[def_lst(a).index((0,-8))]
    if compteur==0:
        if autoriseroi(Roi,def_lst(Roi)[-1],etats):
            return 'Pat'
        elif not autoriseroi(Roi,def_lst(Roi)[-1],etats):
            return 'Echec et mat'
    else:
        return ''
def nom():
    for i in range(8):
        texte(case_vers_pixel((i+1,8))[0],31.25,['♖','♘','♗','♕','♔','♗','♘','♖'][i],'black','center','Purisa',48,['tournoir1','cavaliernoir1','founoir1','reinenoir','roinoir','founoir2','cavaliernoir2','tournoir2'][i])
        texte(case_vers_pixel((i+1,7))[0],93.75,'♙','black','center','Purisa',48,'pionnoir'+str(i+1))
        texte(case_vers_pixel((i+1,1))[0],406.25,'♙','white','center','Purisa',48,'pionblanc'+str(i+1))
        texte(case_vers_pixel((i+1,0))[0],468.75,['♖','♘','♗','♕','♔','♗','♘','♖'][i],'white','center','Purisa',48,['tourblanc1','cavalierblanc1','foublanc1','reineblanc','roiblanc','foublanc2','cavalierblanc2','tourblanc2'][i])
        mise_a_jour()
def notation():
    return
def pixel_vers_case(pixel):
    i,j = pixel
    return int( (i + 31.25) // 62.5 ), int( (531.25 - j) // 62.5 )
def prise_en_passant(piece,case,etats,deplacements):
    a,b=def_lst(piece)[-1]
    x,y=case
    dx,dy=int(x-a),int(y-b)
    if def_typ(piece)!=pion:
        return True
    if b==5 and couleur(piece)=='white':
        if dy==1 and dx**2==1 and 'pionnoir'+str(x)==deplacements[-1] and len(def_lst('pionnoir'+str(x)))==2:
            return True
    elif b==4 and couleur(piece)=='black':
        if dy==-1 and dx**2==1 and 'pionblanc'+str(x)==deplacements[-1] and len(def_lst('pionblanc'+str(x)))==2:
            return True
    return False
def promotion(piece,case,promu):
    if def_typ(piece)==pion and case[1]==int(3.5*sens(piece)+4.5):
        x,y=250,250
        rectangle(25,25,475,475,'black','white',2,'promotion')
        ligne(25,250,475,250,'black',1,'promotion')
        ligne(250,25,250,475,'black',1,'promotion')
        texte(137.5,137.5,reine,'black','center','Purisa',48,'promotion')
        texte(137.5,362.5,tour,'black','center','Purisa',48,'promotion')
        texte(362.5,137.5,fou,'black','center','Purisa',48,'promotion')
        texte(362.5,362.5,cavalier,'black','center','Purisa',48,'promotion')
        while True:
            efface('promoselec')
            ev = donne_evenement()
            ty = type_evenement(ev)
            if ty in ['Deplacement','ClicGauche']:
                x,y=clic_x(ev),clic_y(ev)
            if 25<x and x<250:
                if 25<y and y<250:
                    rectangle(25,25,250,250,'black','',4,'promoselec')
                elif 250<y and y<475:
                    rectangle(25,475,250,250,'black','',4,'promoselec')
            elif 250<x and x<475:
                if 25<y and y<250:
                    rectangle(475,25,250,250,'black','',4,'promoselec')
                elif 250<y and y<475:
                    rectangle(475,475,250,250,'black','',4,'promoselec')
            if ty == 'ClicGauche':
                if 25<x and x<250:
                    if 25<y and y<250:
                        promu[(sens(piece)+1)*4+int(piece[-1])-1]=reine
                    elif 250<y and y<475:
                        promu[(sens(piece)+1)*4+int(piece[-1])-1]=tour
                elif 250<x and x<475:
                    if 25<y and y<250:
                        promu[(sens(piece)+1)*4+int(piece[-1])-1]=fou
                    elif 250<y and y<475:
                        promu[(sens(piece)+1)*4+int(piece[-1])-1]=cavalier
                efface('promoselec')
                efface('promotion')
                efface(piece)
                a,b=case_vers_pixel(case)
                texte(a,b,promu[(sens(piece)+1)*4+int(piece[-1])-1],couleur(piece),'center','Purisa',48,piece)
                break
            mise_a_jour()
def roque(piece,case,etats,deplacements):
    if def_typ(piece)!=roi:
        return True
    if piece=='roiblanc' and piece not in deplacements:
        if case==(7,1) and 'tourblanc2'not in deplacements and autoriseroi(piece,(6,1),etats):
            return True
        elif case==(3,1) and 'tourblanc1' not in deplacements and autoriseroi(piece,(4,1),etats):
            return True
    elif piece=='roinoir' and 'roinoir' not in deplacements:
        if case==(7,8) and 'tournoir2' not in deplacements and autoriseroi(piece,(6,8),etats):
            return True
        elif case==(3,8) and 'tournoir1' not in deplacements and autoriseroi(piece,(4,8),etats):
            return True
    return False
def selec(case,couleur,tag='selec'):
    x,y = case_vers_pixel(case)
    rectangle(x-31.25,y-31.25,x+31.25,y+31.25,couleur,'',1,tag)
def sens(piece):
    if couleur(piece)=='black':
        return -1
    elif couleur(piece)=='white':
        return 1
def signe(nombre):
    try:
        return int(fabs(nombre)/nombre)
    except:
        return 0
def surbrillance(piece,etats,trait):
    noirs,blancs=etats[:32],etats[32:]
    for i in range(8):
        for j in range(8):
            if (i+1,j+1) == def_lst(piece)[-1]:
                continue
            if autorise(piece,(i+1,j+1),etats)and autorisetourfou(piece,(i+1,j+1),etats)and autoriseroi(piece,(i+1,j+1),etats)and echec_non(piece,(i+1,j+1),etats,trait)and ((couleur(piece)=='black' and (i+1,j+1) in blancs) or (couleur(piece)=='white' and (i+1,j+1) in noirs) or ((i+1,j+1) not in etats)):
                if (i+1,j+1)in etats and couleur(piece)!=couleur(etats[etats.index((i+1,j+1))-1]):
                    selec((i+1,j+1),'blue')
                elif not(i+1,j+1)in etats:
                    selec((i+1,j+1),'yellow')
def usr():
        clc,change,trait=False,True,True
        echiquier()
        nom()
        quitte,restart,to=False,False,''
        print('Appuyer sur z pour annuler un coup ou Echap pour sortir')
        while True:
            mise_a_jour()
            if change or restart:
                etats=[]
                for i in range(32):
                    a=['tournoir1','cavaliernoir1','founoir1','reinenoir','roinoir','founoir2','cavaliernoir2','tournoir2',
                       'pionnoir1','pionnoir2','pionnoir3','pionnoir4','pionnoir5','pionnoir6','pionnoir7','pionnoir8',
                       'pionblanc1','pionblanc2','pionblanc3','pionblanc4','pionblanc5','pionblanc6','pionblanc7','pionblanc8',
                       'tourblanc1','cavalierblanc1','foublanc1','reineblanc','roiblanc','foublanc2','cavalierblanc2','tourblanc2'][i]
                    if restart:
                        b=def_lst(a)[0]
                        def_lst(a).clear()
                        def_lst(a).append(b)
                    etats.append(a)
                    etats.append(def_lst(a)[-1])
                change,restart=False,False
                noirs,blancs=etats[:32],etats[32:]
                efface('echec')
                echec('roiblanc',def_lst('roiblanc')[-1],etats)
                echec('roinoir',def_lst('roinoir')[-1],etats)
                if mat_ou_pat(etats,trait) in ['Pat','Echec et mat']:
                    mise_a_jour()
                    rectangle(25,25,475,475,'black','white',2,'matoupat')
                    texte(250,250,mat_ou_pat(etats,trait),'black','center','Purisa',48,'matoupat')
                    texte(250,375,'Rejouer?','black','center')
                    texte(137.5,425,'Oui','black','n')
                    texte(362.5,425,'Non','black','n')
                    while True:
                        ev = donne_evenement()
                        ty = type_evenement(ev)
                        if ty in ['ClicGauche','Deplacement']:
                            efface('curseur')
                            x,y=clic_x(ev),clic_y(ev)
                            if 400<y and y<475 and 25<x and x<475:
                                if x<250:
                                    rectangle(25,400,250,475,'black','',1,'curseur')
                                elif 250<x:
                                    rectangle(250,400,475,475,'black','',1,'curseur')
                        if ty == 'ClicGauche':
                            if 400<y and y<475 and 25<x and x<475:
                                if x<250:
                                    efface_tout()
                                    echiquier()
                                    nom()
                                    clc,change,trait,quitte,restart=False,True,True,False,True
                                    break
                                elif 250<x:
                                    quitte=True
                                    break
                        mise_a_jour()
            if restart:
                continue
            ev = donne_evenement()
            ty = type_evenement(ev)
            if ty in ['ClicGauche','Deplacement']:
                efface('curseur')
                x,y=emplacement((clic_x(ev),clic_y(ev)))
                if trait:
                    selec((x,y),'white','curseur')
                elif not trait:
                    selec((x,y),'black','curseur')
            if ty == 'ClicGauche':
                if (x,y) in etats and not clc:
                    if ((x,y)in blancs and trait) or ((x,y)in noirs and not trait):
                        clc,sel=True,etats[etats.index((x,y))-1]
                        if trait:
                            selec((x,y),'white')
                        if not trait:
                            selec((x,y),'black')
                        surbrillance(sel,etats,trait)
                elif clc and autorise(sel,(x,y),etats)and autorisetourfou(sel,(x,y),etats) and autoriseroi(sel,(x,y),etats) and echec_non(sel,(x,y),etats,trait) and ((couleur(sel)=='black' and (x,y) in blancs) or (couleur(sel)=='white' and (x,y) in noirs) or ((x,y) not in etats)):
                    capture(sel,(x,y),etats)
                    deplacement(sel,(x,y),etats,True)
                    promotion(sel,(x,y),promu)
                    change,clc,trait=True,False,not trait
                    efface('selec')
                elif clc:
                    clc=not clc
                    efface('selec')
            if ty == 'Touche':
                to=touche(ev)
                if to == 'z' or to == 'Z':
                    annule(deplacements)
                    change=True
                    trait=not trait
            if ty == 'Quitte' or quitte or to=='Escape':
                ferme_fenetre()
                break
