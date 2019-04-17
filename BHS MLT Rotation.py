import random
'''providers dictionary: Name:[Days Working] 1=Monday,2=Tuesday,3=Wednesday,4=Thursday,5=Friday'''
providers = {"Brenda": [1, 3, 4, 5], "Jody": [2, 3, 4, 5], "Jarim": [1, 2, 3, 4, 5], "Katrina": [1, 2, 4], "Mike": [1, 2, 3, 4],
             "Susan": [2, 3, 4, 5], "Margaret": [1, 2, 3, 4], "Dael": [1, 2, 3, 4], "Lynette": [1, 2, 3, 4, 5]}
prov_list = list(providers.keys())


def chooserand():
    return random.randint(0, len(providers)-1)


def check_day(randint, day):
    if day in providers[prov_list[randint]]:
        return True
    else:
        return False


def check_list(rand, count, rev, prov_list, bhaurgentlist):
    mv_fwrd_chk = 0
    if count == 1:
        return True
    elif count < 4:
        for num in range(count):
            if prov_list[rand] == bhaurgentlist[(len(bhaurgentlist)-1)-num]:
                mv_fwrd_chk += 1
    else:
        for num in range(rev):
            if prov_list[rand] == bhaurgentlist[(len(bhaurgentlist)-1)-num]:
                mv_fwrd_chk += 1
    if mv_fwrd_chk == 0:
        return True
    else:
        return False


def run_list_randomizer():
    bhaurgentlist = []
    num_assigned = {"Brenda": 0, "Jody": 0, "Jarim": 0, "Katrina": 0, "Mike": 0,
                    "Susan": 0, "Margaret": 0, "Dael": 0, "Lynette": 0}
    day = 1
    count = 1
    rev = int(len(providers)*(.5))
    move_fwrd_day = False
    move_fwrd_list = False
    rand = 0
    equitable = True
    run_number = 200
    while count < run_number and equitable:
        rand = chooserand()
        move_fwrd_day = check_day(rand, day)
        if move_fwrd_day:
            move_fwrd_list = check_list(
                rand, count, rev, prov_list, bhaurgentlist)
            if move_fwrd_list:
                count += 1
                bhaurgentlist.append(prov_list[rand])
                num_assigned[prov_list[rand]] += 1
                if num_assigned[prov_list[rand]] > run_number/len(prov_list) + 2:
                    equitable = False
                day += 1
                if day > 5:
                    day = 1
    return [bhaurgentlist, num_assigned]


test_list = run_list_randomizer()
while max(test_list[1].values()) - min(test_list[1].values()) > 2:
    test_list = run_list_randomizer()
outfile = open("bhamltlist.csv", "w")
for nm in test_list:
    outfile.write("{},".format(nm))
outfile.close()