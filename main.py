
def welsh_powell(mat):

	dic = {}
	dejaColorier = []
	couleurVertex = {}
	couleur = 0

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
		if couleur == k:
			
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

	return couleur

def check()

def main():

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

	welsh_powell(mat)

if __name__ == "__main__":
	main()