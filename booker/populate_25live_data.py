import os
import csv

def remove_room_numbers(bldg_str):
    numerics = "1234567890"
    result = ""
    for piece in bldg_str.split(" "):
        if piece[0] in numerics:
            break
        else:
            result += piece + " "
    return result

def read_file():
    f = open('RegistrarRoomList.csv')
    csv_f = csv.reader(f)

    rooms = []

    #take out header row
    next(csv_f)
    for row in csv_f:
        room_name = row[0]
        bldg_name_str = str(row[1])
        #parse through building names
        comma_idx = bldg_name_str.find(',')
        if comma_idx > 0:
            bldg_name = bldg_name_str[comma_idx+2:]
        else:
            bldg_name = bldg_name_str
        bldg_name = remove_room_numbers(bldg_name)
        capacity = int(row[5])
        features_str = str(row[3])
        if features_str.find("Project") > 0:
            has_projector = True
        else: has_projector = False
        if features_str.find("Window") > 0:
            has_window = True
        else: has_window = False
        if features_str.find("board") > 0:
            has_board = True
        else: has_board = False

        # print room_name, ":", bldg_name, "(", capacity, ")", has_projector, has_window, has_board
        tup = tuple((room_name, bldg_name, capacity, has_projector, has_window, has_board))
        rooms.append(tup)

    print "------------"
    print "ROOMS LIST =", rooms

def populate():
    python_cat = add_cat('Python')

    add_page(cat=python_cat,
        title="Official Python Tutorial",
        url="http://docs.python.org/2/tutorial/")

    add_page(cat=python_cat,
        title="How to Think like a Computer Scientist",
        url="http://www.greenteapress.com/thinkpython/")

    add_page(cat=python_cat,
        title="Learn Python in 10 Minutes",
        url="http://www.korokithakis.net/tutorials/python/")

    django_cat = add_cat("Django")

    add_page(cat=django_cat,
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")

    add_page(cat=django_cat,
        title="Django Rocks",
        url="http://www.djangorocks.com/")

    add_page(cat=django_cat,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/")

    frame_cat = add_cat("Other Frameworks")

    add_page(cat=frame_cat,
        title="Bottle",
        url="http://bottlepy.org/docs/dev/")

    add_page(cat=frame_cat,
        title="Flask",
        url="http://flask.pocoo.org")

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting booker population script..."
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
    from booker.models import Room, Reservation
    read_file()
    # populate()