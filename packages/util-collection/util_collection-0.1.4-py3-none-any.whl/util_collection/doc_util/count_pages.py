def count_pages(s:str)->int:
    """_summary_

    Args:
        s (str): _description_
    example:
    s="4 25 27 31 38 42-48 50 55 68 71 75 79-83 88 90 92 95 103-109 111 115 117 119 125 127-134 136-137 141 147-148 152-153 162-165 168 170-172 175-178 180 182-184 186-190"
    count_pages(s)
    return 74
    """
    a = 0
    for i in s.split():
        if "-" in i:
            start,end = i.split("-")
            a+=int(end)-int(start)+1
        else:
            a+=1
    return a
