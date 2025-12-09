# RBA-using-AIML

RBA-using-AIML is a research project that applies artificial intelligence and machine learning techniques to detect account takeover attacks using an intrusion detection–style pipeline.[file:1] The repository contains Python scripts for data preprocessing, feature preparation, and model training to build a risk-based authentication system.[file:1]

---

## Features

- Data alignment and consolidation from multiple CSV sources into a unified dataset.[file:1]  
- Exploration and one-hot encoding of categorical features for downstream modeling.[file:1]  
- Extraction of attacked-user records to build focused attack datasets.[file:1]  
- Splitting of large datasets into multiple subsets for scalable processing and experimentation.[file:1]  
- Training of machine learning models for real-time or near–real-time account takeover detection.[file:1]  

---

## Installation

1. Clone the repository:
git clone https://github.com/K4-KC/RBA-using-AIML.git
cd RBA-using-AIML

text
2. (Optional but recommended) Create and activate a virtual environment for Python.  
3. Install dependencies:
pip install -r requirements.txt

text
4. Ensure your input CSV files are placed in the expected data directory or update the script paths accordingly.[file:1]  

---

## Usage

The project is organized around several standalone scripts, which can be run step by step or individually depending on your workflow.[file:1]

1. **Align data from different CSVs**  
python allign.py

text
This script merges and aligns data from multiple CSV files into a consistent format.[file:1]

2. **Generate one-hot encodings and unique-value summaries**  
python find_hot_encoding.py

text
Use this to inspect categorical columns and create one-hot–encoded features for model input.[file:1]

3. **Extract attacked-user records**  
python get_attacked_data.py

text
This produces an `attack.csv` file containing data for users identified as attacked in the dataset.[file:1]

4. **Split aligned data into multiple parts**  
python split.py

text
After alignment, this script splits the dataset into 24 separate files for easier handling and experimentation.[file:1]

5. **Train the machine learning model**  
python train.py

text
This script trains an account takeover detection model using the prepared features and datasets.[file:1]

Adjust file paths, hyperparameters, and model settings inside the scripts to match your environment and experimental setup.

---

## Contributing

Contributions, extensions, and reproductions of the experimental results are welcome. If you plan to add new preprocessing steps, models, or evaluation scripts, please:

- Follow standard Python style guidelines (e.g., PEP 8).  
- Add clear docstrings and comments to new functions and modules.  
- Include a brief description of your changes in the pull request.  

---

## Testing

To manually test individual scripts:

1. Navigate to the project root (or the relevant subdirectory, if any).  
2. Run the script with the appropriate Python interpreter:
python split.py
python train.py

etc.
text
3. Inspect console output and any generated files (such as CSVs or model artifacts) to verify that each step behaves as expected.[file:1]  

Automated tests can be added later (for example, with `pytest`) to validate preprocessing and model training pipelines.
