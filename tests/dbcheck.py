import dbfunctions


def print_help():
    print("This is a simple database tester:")
    print("Possible Commands:")
    print("C - Add a new article")
    print("U - Update article")
    print("S - Search article")
    print("P - Private get")
    print("L - List current database entries")
    print("Q - Quit this program")
    print("----------------------")

print_help()
dbfunctions.init_db(':memory:')
i = input(">").lower()
while i != 'q':

    print("Input was:",i)

    if i == 'c':
        subject = input("Input Subject:").lower()
        text = input("Text for Article:").lower()
        dbfunctions.create_article(subject,text)
    elif i == 's' or i == 'p':
        subject = input("Subject Search Text:").lower()
        search_list = dbfunctions.search_article(subject)
        print("Results of search")
        print("----------------------")
        for s in search_list:
            print(s)
        print("----------------------")
    elif i == 'u':
        subject = input("Subject to modify:").lower()
        text = input("New Text for Article:").lower()
        dbfunctions.update_article(subject,text)



    print()
    print("Current database entries")
    print("---------------------------------")
    dbfunctions.cur.execute('SELECT * FROM articles;')
    thingy = dbfunctions.cur.fetchall()

    for thing in thingy:
      print(thing)


    print("---------------------------------")
    print()

    print_help()
    i = input(">").lower()

