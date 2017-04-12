import dbfunctions

dbfunctions.create_article('test1','whatever1')
dbfunctions.create_article('test2','whatever2')
dbfunctions.create_article('test3','whatever3')
dbfunctions.create_article('test4','whatever4')
dbfunctions.create_article('test5','whatever5')

dbfunctions.cur.execute('SELECT * FROM articles;')
thingy = dbfunctions.cur.fetchall()

for thing in thingy:
  print(thing)

