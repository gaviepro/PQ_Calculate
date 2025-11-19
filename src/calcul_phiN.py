import argparse
import os
import multiprocessing as mp
from math import *
import re 
import textwrap
from tabulate import tabulate

DEFAULT_WORKERS = os.cpu_count() or 1
DEFAULT_SORT_CHUNKS = DEFAULT_WORKERS  # même nombre que workers, par défaut

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def calcul(n,phi):
    n = int(n)
    phi = int(phi)
    sum_pq = n-phi+1
    delta = sum_pq*sum_pq -4*n
    if delta <= 0 :
        print(bcolors.FAIL+"ERREUR : delta est inf ou egal à 0")
        return 0,0
    p = (sum_pq - isqrt(delta)) // 2
    q = (sum_pq + isqrt(delta)) // 2

    return p,q

def wrap_table(data, width=40, cols=None):
    wrapped = []
    for row in data:
        new_row = []
        for i, cell in enumerate(row):
            cell_str = str(cell)
            if cols is None or i in cols:
                cell_str = textwrap.fill(cell_str, width=width)
            new_row.append(cell_str)
        wrapped.append(new_row)
    return wrapped

def verif(p,q,n,phi):
    phi_test = (p-1)*(q-1)
    n_test =p*q
    if n_test == n:
        return True
    if phi_test == phi :
        return True

def main():
    """
    Point d'entrée principal du programme
    """
    parser = argparse.ArgumentParser(description="Calcul de p et q à paritr de N et phi(n)")
    parser.add_argument("-N",type=int,default=None,help="Entrée N")
    parser.add_argument("--phi","-p",type=int,default=None,help="Entrez Phi(N)")
    parser.add_argument("--file","-f",type=str,default=None,help="Entrez un chemin de fichier contenant les clés")
    args = parser.parse_args()

    n = args.N
    phi = args.phi
    file = args.file
    name_key = ""
    dict_ = {}
    p = 0
    q = 0

    if (n is None or phi is None) and file is not None:
        with open(file, "r") as f:
            while True:
                parse = f.readline()
                if not parse:
                    break

                parse = parse.strip()
                if not parse:
                    continue

                if re.match(r"^Key", parse):
                    name_key = parse
                    if name_key not in dict_:
                        dict_[name_key] = [None, None]

                elif name_key is not None and re.match(r"^N\s*=", parse):
                    m = re.search(r"(\d+)", parse)
                    if m:
                        n_val = int(m.group(1))
                        dict_[name_key][0] = n_val

                elif name_key is not None and re.match(r"^phi\s*=", parse):
                    m = re.search(r"(\d+)", parse)
                    if m:
                        phi_val = int(m.group(1))
                        dict_[name_key][1] = phi_val

        for key in dict_.keys():
            n_val, phi_val = dict_[key]

            if n_val is None or phi_val is None:
                print(f"Clé {key} incomplète (N ou phi manquant)")
                continue

            p, q = calcul(n_val, phi_val)

            if p == 0 and q == 0:
                return 1

            if verif(p, q, n_val, phi_val):
                data = [[key, n_val, phi_val, p, q]]
                table = tabulate(wrap_table(data),headers=["NAME KEY", "N", "PHI(N)", "P", "Q"],tablefmt="grid",numalign="center",stralign="center",colalign=("center", "center", "center"),)
                print(table)
            else:
                print(bcolors.FAIL + "ERREUR : le calcul de P et Q a échoué" + bcolors.ENDC)
        return 0
    
    elif (n != None and phi != None): 
        p,q = calcul(n,phi)
        if p == 0 and q==0 :
            return 1
        
        if verif(p,q,n,phi):
            data = [[n,phi,p,q]]
            table = tabulate(wrap_table(data), headers=["N", "PHI(N)", "P","Q"],tablefmt="grid",numalign="center",stralign="center",colalign=("center", "center", "center"))
            print(table)
    else:
        return 1

if __name__ == "__main__":
    main()
