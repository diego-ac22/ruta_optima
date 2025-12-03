from db_mongo import rutas_col

print("\nRutas guardadas en MongoDB:\n")
for r in rutas_col.find():
    print(r)
