import pandas as pd

def convert(file):
  data = pd.read_excel(io=file, sheet_name=0).dropna(axis=1, how='all').dropna(axis=0, how='any')
  lov = pd.read_excel(io=file, sheet_name=1)

  consent_id = lov['consent_id'].to_list()
  purpose_id = lov['purpose_id'].to_list()
  consent_purpose_id = dict(zip(consent_id, purpose_id))

  data['purpose_id'] = data['consent_id'].map(lambda x: consent_purpose_id[x])

  all_cif = data['cif'].unique()
  all_customer_consent_purpose_id = []
  all_nik = []
  all_full_name = []
  all_source_id = []
  all_source_name = []
  for cif in all_cif:
      customer_data = data[data['cif'] == cif]
      customer_purpose_id = customer_data['purpose_id'].to_list()
      flags = customer_data['a.flag_status']
      consent_flag = dict(sorted(dict(zip(customer_purpose_id, flags)).items(), key=(lambda x: x[0]%max(purpose_id))))
      
      all_customer_consent_purpose_id.append(consent_flag)
      all_nik.append(customer_data['NIK'].to_list()[0])
      all_full_name.append(customer_data['full_name'].to_list()[0])
      all_source_id.append(customer_data['a.source'].to_list()[0])
      all_source_name.append(customer_data['source_name'].to_list()[0])

  new_data = pd.DataFrame({'nik': all_nik,
                      'cif': all_cif,
                      'full_name': all_full_name,
                      'source_id': all_source_id,
                      'source_name': all_source_name,
                      'consent_flag': all_customer_consent_purpose_id})
  
  return new_data.to_csv(index=False).encode("utf-8")
