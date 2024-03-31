def mapping(x,min_val,max_val,aim_min,aim_max):
    x = aim_min + abs((x - min_val) / (max_val- min_val) * (aim_max-aim_min))
    return x