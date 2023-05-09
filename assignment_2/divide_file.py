"""splits the given UN-file (doc1.txt) into 50 sub-files"""

f = open("doc1.en", "r", encoding='utf-8')
linecounter = 0
filecount = 1

new_file = open("docs1.txt", "w", encoding='utf-8')
for line in f:
  if linecounter < 20:
    new_file.write(line)
    linecounter += 1

  if linecounter == 20 and filecount <= 49:
    linecounter = 0
    filecount += 1
    new_file = open(f"docs{filecount}.txt", "w", encoding='utf-8')

f.close()




