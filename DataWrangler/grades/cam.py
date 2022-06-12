import tabula

res = tabula.read_pdf('dir.pdf', area=[131.175, 25.08, 537.075, 769.56], pandas_options={'header': None})
print(res)