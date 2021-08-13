import pandas as pd
import numpy as np

umuarama = pd.read_csv('/Users/brunojuliani/Desktop/umuarama.txt',header=None, lineterminator='/',
                       names=['ID', 'Nome', 'Nota', 'Coloc','Nota2', 'Class'], index_col='Coloc')

umuarama.loc[16]

curitiba = pd.read_csv('/Users/brunojuliani/Desktop/curitiba.txt',header=None, lineterminator='/',
                       names=['ID', 'Nome', 'Nota', 'Coloc','Nota2', 'Class'], index_col='Coloc')

curitiba
curitiba.loc[56]

guarapuava = pd.read_csv('/Users/brunojuliani/Desktop/guarapuava.txt',header=None, lineterminator='/',
                       names=['ID', 'Nome', 'Nota', 'Coloc','Nota2', 'Class'], index_col='Coloc')

guarapuava
guarapuava.loc[16]

f_beltrao = pd.read_csv('/Users/brunojuliani/Desktop/f_beltrao.txt',header=None, lineterminator='/',
                       names=['ID', 'Nome', 'Nota', 'Coloc','Nota2', 'Class'], index_col='Coloc')

f_beltrao
f_beltrao.loc[16]
