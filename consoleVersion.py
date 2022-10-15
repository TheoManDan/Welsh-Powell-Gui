import sys

def welsh_powell(mat,kLimit):

        dic = {}
        dejaColorier = []
        couleurVertex = {}
        couleur = 0
        kColoriable = True

        taille = len(mat)

        for i in range(0,taille):
                tmp = 0
                for j in range(0,taille):
                        if mat[i][j] == 1:
                                tmp+=1
                dic[i] = tmp
                dejaColorier.append(False)

        dic = dict(sorted(dic.items(), key=lambda item: item[1],reverse=True))
        x = list(dic.keys())

        while False in dejaColorier :

                if couleur >= kLimit:
                        kColoriable = False
                        break
                else:
                        selectedVertex = x[0]
                        dejaColorier[selectedVertex] = True
                        couleurVertex[selectedVertex] = couleur
                        x.remove(selectedVertex)

                        for sommet in x:

                                if mat[selectedVertex][sommet] == 0:
                                        dejaColorier[sommet] = True
                                        couleurVertex[sommet] = couleur
                                        x.remove(sommet)

                        couleur+=1

        return couleur,kColoriable,couleurVertex

def colorAssignement(colorSet):

        for sommet, nombre in colorSet.items():
                print("{} -> {}".format(sommet,nombre))


def check(mat,k):
        tuple = welsh_powell(mat,k)

        if(not tuple[1]):
                print("Le graphe n'est pas k-{} coloriable".format(k))
                colorAssignement(tuple[2])
                print("seulement {} sommets on été coloriés".format(len(tuple[2])))
        else:
                print("Le graphe est bien k-{} coloriable".format(k))
                colorAssignement(tuple[2])

def main():

        if(len(sys.argv) < 2 ):
                print("Usage : consoleVersion.py [Klimit]")
        else:
                k = int(sys.argv[1])

                mat = [
                                [0,0,1,1,0,1,0,0,1],
                                [0,0,1,0,1,0,1,1,0],
                                [1,1,1,1,1,1,1,0,0],
                                [1,0,1,0,0,0,1,0,0],
                                [0,1,1,0,0,1,0,0,0],
                                [1,0,1,0,1,0,0,0,0],
                                [0,1,1,1,0,0,0,0,0],
                                [0,1,0,0,0,0,0,0,0],
                                [1,0,0,0,0,0,0,0,0]
                                ]

                check(mat,k)


if __name__ == "__main__":
        main()