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
    #    "Problem Characteristics [Partial evaluations possible]",
       "Problem Characteristics [Multiple fidelities]":"multi-fidelity", 
       "Problem Source":"source (real-world/artificial)",
       "Link to Implementation" :"implementation", 
       "Short description of problem(s)":"textual description",
    #    "Do you wish to provide some more detailed information about the proposed problems?",
    #    "Full name of suite", 
    #    "Constraint Properties", 
    #    "Number of constraints",
    #    "Type of Dynamicism", 
    #    "Form of noise model", 
    #    "Type of noise space",
    #    "Other noise properties", 
    #    "Description of multimodality",
       "Citation / reference": "reference", 
    #    "Key challenges / characteristics",
    #    "Scientific motivation for the proposed suite / problem / generator",
    #    "Limitations of  the proposed suite / problem / generator",
    #    "Implemenation languages", 
    #    "Links to implementations",
    #    "Approximate time to evaluate a single solution (or times if e.g. multi-fidelity)",
    #    "Links to examples of usage of the proposed suite / problem / generator",
       "Other relevant information":"other info", 
    #    "Feedback about the form"
}

# Read the csv file
data = pd.read_csv(csv_file)

# Handle empty cells being read as 'NaN', by emptying them again
data = data.fillna("")
data2 = data.rename(columns=translations)
data2.drop(columns=[col for col in data2.columns if col not in translations.values()], inplace=True)
data2 = data2[data2['name'] != 'test']

# Write the yaml file
with open(yaml_file, "a") as out_file:
    yaml.dump(data2.to_dict(orient="records"), out_file,
              sort_keys=False)  # Prevent columns being reordered alphabetically