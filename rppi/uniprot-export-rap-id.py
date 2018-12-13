
import pandas

def descartes(df1, df2):
  df1['__descartes_key__'] = 0
  df2['__descartes_key__'] = 0
  result = pandas.merge(df1, df2, how='left', on='__descartes_key__')
  del result['__descartes_key__']
  return result

def export_rap_id_of(uniprot):
  # df = pandas.read_csv(uniprot+'.tab', sep='\t')
  df = pandas.read_csv(uniprot+'.tab', sep='\t')[0:7]
  # print(df)
  result = pandas.DataFrame({'rap_id':df['To']})
  # print(result)
  result = result.drop_duplicates()
  # print(result)
  # result.to_csv(uniprot+'.rap_id', index=False)
  return result

prefixs = [ 
'uniprot-20181210-Oryza sativa subsp japonica', 
]

locations = [ 
'cytoplasm', 
'endoplasmic reticulim', 
'golgi apparatus', 
'mitochondrion', 
'nucleus', 
'peroxisome', 
'vacuole', 
]

for prefix in prefixs:
  results = []
  all = pandas.DataFrame(columns=('rap_id', ))
  descartes_all = pandas.DataFrame(columns=('rap_id_x', 'rap_id_y', ))
  for location in locations:
    result = export_rap_id_of('./'+prefix+'-tabs/'+prefix+'-'+location)
    results.append(result)
    all = pandas.concat([all, result])
    all = all.drop_duplicates()
    descartes_all = pandas.concat([descartes_all, descartes(result, result)])
    descartes_all = descartes_all.drop_duplicates()
  # all.to_csv(prefix+'.all_rap_id', index=False)
  result = descartes(all, all)
  result = result.append(descartes_all)
  result = result.append(descartes_all)
  result = result.drop_duplicates(keep=False)
  # print(result)
  result.to_csv('Subcellular-localization-RAP.csv', index=False)
