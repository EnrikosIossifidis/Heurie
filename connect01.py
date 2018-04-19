'''Connect houses to batteries in most basic way - returns total cable distance and capacity distribution (and which houses are assigned to which battery)'''
def connect01(batteries, houses, distancetable):
    # performance indicators are capacity distribution and cable distance
    cap_fill = [0]*len(batteries)
    dist_fill = [0]*len(batteries)

    # meaning: battery[0] does not connect to to_house[0]
    to_house = [0]*len(batteries)
    h_save = 0

    for n in range(len(batteries)):
        for h in range(h_save, len(houses)):
            if cap_fill[n] < float(batteries[n][2])-float(houses[h][2]):
                cap_fill[n] += float(houses[h][2])
                dist_fill[n] += int(distancetable[n][h])
            else:
                h_save = h
                to_house[n] = h
                break
            
    print("The maximum capacity that can occur in this situation per battery is: " + str(cap_fill))
    print("The total length of the cables leading to every battery is: " + str(dist_fill))
    print("The total cable length is: " + str(sum(dist_fill)))