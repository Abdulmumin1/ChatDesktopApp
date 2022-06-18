import json


def break_sentence(text):
    after = 40
    offset = 5
    # sample = text[:after]
    if len(text) <= after:
        return text
    if len(text)-after < 15:
        offset = 10
    dif = after-offset
    if text[dif] == ' ':
        offset += 1
    # if text[after+offset] == ' ':
    #     offset += 1
    words = text[dif:after+offset]
    new_break_point = words.find(' ')
    if new_break_point != -1:
        after = dif+new_break_point

    firstpart = text[:after]
    lastpart = text[after:]
    lastpart = lastpart.strip()

    if len(lastpart) == 0:
        return firstpart+lastpart
    if len(lastpart) <= after:
        return firstpart+"\n"+lastpart

    return firstpart+'\n'+break_sentence(lastpart)


def json_constructor(type_, message, sender=None):
    data = {'type': type_, 'message': message}
    if sender:
        data['sender'] = sender
    json_data = json.dumps(data)
    return json_data


def recursive_index(names, objects, pre=0):
    index = names.find(' ')
    if index == -1:
        # listr.append(first)
        return index
    # listr.append(first)
    # print(first)
    if pre != 0:
        objects.append(index+pre)
    else:
        objects.append(index)
    pre += index+1
    return recursive_index(names[index+1:], objects, pre)

# def insert_breaks(text):
#     items = text.split(' ')
#     index = 9


# items = []
# recursive_index(names, items)
# print(items)
# print(names[17])
# print(names.find('isbah rahm'))
