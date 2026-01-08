import pandas as pd
import yaml

csv_file = "OPL_form.csv"
yaml_file = "problems.yaml"


translations = {
    # "Timestamp", 
    #  "Submitter Name", 
    #  "Submitter Email",
       "Short name of Suite / Problem / Generator" : "name", 
       "Type" : "suite/generator/single",
       "Types of input variables" : "variable type",
       "Number of Input variables (number or range or 'scalable')" : "dimensionality",
       "Number of Objectives (number or range or 'scalable')" : "objectives",
       "Problem Characteristics [Constrained]":"constraints",
       "Problem Characteristics [Dynamic]":"dynamic", 
       "Problem Characteristics [Noisy]":"noise",
       "Problem Characteristics [Multi-modal]":"multimodal",
       "Problem Characteristics [Multiple fidelities]":"multi-fidelity", 
       "Problem Source":"source (real-world/artificial)",
       "Link to Implementation" :"implementation", 
       "Short description of problem(s)":"textual description",
       "Citation / reference": "reference", 
}

translations_other = {
      "Short name of Suite / Problem / Generator" : "name", 
      "Other relevant information": "general", 
      "Problem Characteristics [Partial evaluations possible]" :"partial evaluations",
      "Full name of suite" : "full name", 
      "Constraint Properties" : "constraint properties", 
      "Number of constraints" : "number of constraints",
      "Type of Dynamicism" : "type of dynamicism", 
      "Form of noise model" : "form of noise model", 
      "Type of noise space" : "type of noise space",
      "Other noise properties" : "other noise properties",
      "Description of multimodality" : "description of multimodality",
      "Key challenges / characteristics" : "key challenges / characteristics",
      "Scientific motivation for the proposed suite / problem / generator" : "scientific motivation",
      "Limitations of  the proposed suite / problem / generator" : "limitations",
      "Implemenation languages" : "implementation languages", 
      "Links to implementations" : "links to implementations",
      "Approximate time to evaluate a single solution (or times if e.g. multi-fidelity)" : "approximate evaluation time",
      "Links to examples of usage of the proposed suite / problem / generator" : "links to usage examples",
}

# Read the csv file
data = pd.read_csv(csv_file)

# Handle empty cells being read as 'NaN', by emptying them again
data = data.fillna("")
data_main = data.rename(columns=translations)
data_main.drop(columns=[col for col in data_main.columns if col not in translations.values()], inplace=True)
data_main = data_main[data_main['name'] != 'test']
data_other = data.rename(columns=translations_other)
data_other.drop(columns=[col for col in data_other.columns if col not in translations_other.values()], inplace=True)
data_other = data_other[data_other['name'] != 'test']

dict_main = data_main.to_dict(orient="records")
dict_other = data_other.to_dict(orient="records")
for dict_m, dict_o in zip(dict_main, dict_other):
    dict_o['name'] = None  # Remove duplicate name entry
    dict_m['other info'] = dict_o

# Write the yaml file
with open(yaml_file, "a") as out_file:
    yaml.dump(dict_main, out_file,
              sort_keys=False)  # Prevent columns being reordered alphabetically