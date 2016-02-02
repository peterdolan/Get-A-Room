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
        features_tup = tuple((has_projector, has_window, has_board))
        tup = tuple((room_name, bldg_name, capacity, features_tup))
        rooms.append(tup)

    # print "------------"
    # print "ROOMS LIST =", rooms
    return rooms

def populate():
    rooms_list = read_file()

    for room in rooms_list:
        add_room(room[0], room[1], room[2], room[3])

    # Print out what we have added to the user.
    # for c in Category.objects.all():
    #     for p in Page.objects.filter(category=c):
    #         print "- {0} - {1}".format(str(c), str(p))

    for r in Room.objects.all():
        print str(r)

def add_room(room_name, bldg_name, capacity, features):
    r = Room.objects.get_or_create(name=room_name, building=bldg_name, capacity=capacity, has_projector=features[0], has_windows=features[1], has_whiteboard=features[2])[0]
    return r


# Start execution here!
if __name__ == '__main__':
    print "Starting booker population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'getaroom.settings')
    from booker.models import Room, Reservation
    populate()