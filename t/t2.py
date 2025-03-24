import random
#def gen_ar_a():
vars = {
  'lvls': [0,5],
  'ords': [0,5],
  'items': [0,5],
}

    
lvl = random.randint(vars['lvls'][0],vars['lvls'][1])
for x in range(0,lvl+1,1):
    print(x)
#for lvl in lvls
#random.randint(vars['ords'][0],vars['ords'][1])