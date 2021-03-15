
import csv

with open("spotify-mini.tsv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for linea in tsvreader:
        print(linea[1:])