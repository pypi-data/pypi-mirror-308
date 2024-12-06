Claro! Aqui está uma versão mais técnica e detalhada da documentação para o README:

---

# AHP-Gaussian Decision Support Library

## Overview

The **AHP-Gaussian Decision Support Library** is a extensible solution designed for multi-criteria decision-making (MCDM) leveraging both traditional and advanced AHP methodologies. It provides an implementation of Saaty's **Analytic Hierarchy Process (AHP)** and an enhanced **Gaussian-based AHP**, developed to handle complex scenarios involving a large number of criteria. This library is structured to facilitate the application of decision-support systems in research, data analysis, and organizational decision-making processes.

### Key Features
- **AHP using Saaty’s Method**: Enables decision analysis with pairwise criteria comparisons, generating consistency-validated weightings.
- **Gaussian-AHP**: Offers a pairwise comparison-free alternative, ideal for scalability, by assigning weights based on sensitivity analysis through the Gaussian distribution.
- **Configurable Settings**: Allows fine-tuning via YAML configuration, including parameters for consistency thresholds and optimization objectives.
- **Comprehensive Visualization**: Supports graphical output of decision matrices, judgment matrices, and preference rankings for clear insight into each step of the decision-making process.

## Project Structure

```plaintext
.
├── ahp_gaussian.py         # Gaussian-AHP class for advanced MCDM with Gaussian factors
├── ahp_saaty.py            # Traditional AHP class implementing Saaty’s methodology
├── config_manager.py       # YAML-based configuration manager
├── create_csv_files.py     # Script to generate sample CSV files for testing
├── data/                   # Folder to store decision and judgment matrices
├── decision_helper.py      # Helper functions for matrix validation, normalization, and aggregation
├── main.py                 # Primary script to execute decision-making processes
├── requirements.txt        # Library dependencies
├── results/                # Folder to save result outputs, including CSVs and visualizations
├── settings/               # Configuration directory with YAML settings
└── tests/                  # Unit tests for functional validation
```

Each module is structured to allow modular application and customization for specific decision-making frameworks.

## Installation

To use this library, clone the repository and install the required dependencies:

```bash
git clone <repository_url>
cd <repository_name>
pip install -r requirements.txt
```

## Usage

### Overview of Execution
The `main.py` script is designed as the primary entry point, which initializes configurations, loads matrices, and executes both AHP-Saaty and AHP-Gaussian analyses. It automatically saves output results in the `results/` directory and provides optional visualizations.

#### Step-by-Step Execution
1. **Data Preparation**: Ensure that `decision_matrix.csv` and `judgment_matrix.csv` are available in the `data/` directory. These files should represent the decision criteria and pairwise comparisons, respectively.
   - **Decision Matrix**: Rows represent alternatives, and columns represent criteria.
   - **Judgment Matrix**: A square matrix representing pairwise comparison for criteria weight calculation.

2. **Run Analysis**: Execute the main script:
   ```bash
   python main.py
   ```

3. **Results**: Results are stored in the `results/` directory. The directory includes global and local preference CSV files and graphical representations.

### Example File Generation

The `create_csv_files.py` script provides an example decision matrix and judgment matrix. Execute it to generate sample data for testing purposes:

```bash
python create_csv_files.py
```

## Module Descriptions

### `ahp_gaussian.py`

The `AHPGaussian` class is a novel, scalable approach to multi-criteria decision-making. By analyzing the sensitivity of criteria weights using Gaussian distribution factors, this method circumvents the need for pairwise comparison, allowing it to handle large matrices efficiently.

- **Attributes**:
  - `local_preference`: Matrix of alternatives' local preferences for each criterion.
  - `gaussian_factor`: Represents the criteria's variance as a proportion of the mean, essential for weight calculation.
  - `weights`: Weighting of each criterion based on Gaussian sensitivity analysis.

- **Core Methods**:
  - `global_preference()`: Ranks alternatives by global preference scores.
  - `visualize_decision_matrix()`, `visualize_local_preference()`, `visualize_global_preference()`: Visualize decision matrices and preferences.

### `ahp_saaty.py`

The `AHPSaaty` class implements the traditional AHP method, where criteria weights are derived from a reciprocal pairwise comparison matrix. This method validates the consistency of the judgments using Saaty’s Consistency Ratio (CR).

- **Attributes**:
  - `weights`: Criterion weights derived from normalized judgment matrices.
  - `cr`: Consistency ratio to evaluate the matrix's adherence to transitivity.

- **Core Methods**:
  - `local_preference(decision_matrix)`: Computes alternative preferences for each criterion.
  - `global_preference(decision_matrix)`: Provides global ranking based on combined criterion weights.
  - Visualization methods for judgment, local, and global preferences.

### `config_manager.py`

Manages external configuration through a YAML file (`ahp_settings.yaml`), enabling users to define decision-making parameters such as consistency indices and objectives.

**YAML Configuration**:
```yaml
consistency_index:
  "1": 0
  "2": 0
  "3": 0.58
  "4": 0.9
  "5": 1.12
  "6": 1.24
  "7": 1.32
  "8": 1.41
  "9": 1.45
  "10": 1.49
  "11": 1.51
  "12": 1.48
  "13": 1.56
  "14": 1.57
  "15": 1.59
```

### `decision_helper.py`

`DecisionHelper` is a utility class providing essential operations such as:
- **Matrix Validation**: Ensures matrices align with required structure and criteria.
- **Normalization and Aggregation**: Prepares matrices for consistent and valid decision-making.
- **Visualization Tools**: Includes functions for heatmaps and bar charts, enhancing data interpretability.

**Key Methods**:
- `normalize_decision_matrix()`: Adjusts each criterion based on optimization objectives (maximize or minimize).
- `aggregate_matrix()`: Aggregates preferences with weights to produce global rankings.
- `plot_*` functions for detailed visual representations.

## Visualization

The library offers in-depth visual analysis for decision matrices and preferences, with heatmaps and bar charts generated using Matplotlib and Seaborn. These visualizations are essential for interpreting judgment consistency, criterion weighting, and preference rankings.

## Example Workflow

1. **Initialize Configuration and Load Data**: Load settings from YAML and input CSVs.
2. **Analyze with AHP-Saaty**:
   - Calculate local and global preferences.
   - Validate consistency.
   - Generate visualizations and export results.
3. **Analyze with AHP-Gaussian**:
   - Compute preferences using Gaussian factor sensitivity.
   - Rank alternatives by preference scores.
   - Save results and generate graphical insights.

### Example Code Snippet

```python
from ahp_saaty import AHPSaaty
import pandas as pd

# Load judgment matrix
judgment_matrix = pd.read_csv('data/judgment_matrix.csv', index_col=0)

# Perform Saaty's AHP analysis
ahp_saaty = AHPSaaty(judgment_matrix, objective='max')
local_preferences = ahp_saaty.local_preference(decision_matrix)
global_preferences = ahp_saaty.global_preference(decision_matrix)

# Visualize results
ahp_saaty.visualize_judgment_matrix()
ahp_saaty.visualize_global_preference(decision_matrix)
```

## Results

The results are saved as follows:
- **Local Preference (Saaty)**: `results/local_pref_saaty.csv`
- **Global Preference (Saaty)**: `results/global_pref_saaty.csv`
- **Global Preference (Gaussian)**: `results/global_pref_gaussian.csv`

Each output file provides a ranked listing of alternatives based on the respective method's calculated scores.

## Testing and Validation

Unit tests are provided for all core modules under `tests/`. The tests ensure functional accuracy of criteria weighting, consistency validation, preference calculation, and result aggregation. To execute tests:

```bash
pytest tests/
```

## Requirements

- Python 3.10 or later
- Required Libraries:
  - `pandas` for data manipulation
  - `matplotlib` and `seaborn` for data visualization
  - `yaml` for configuration management