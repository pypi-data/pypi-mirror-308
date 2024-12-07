![Logo](images/logo.png)

## Machine learning augmented sample demultiplexing of pooled single-cell RNA-seq data
---


![GitHub release (latest SemVer)](https://img.shields.io/badge/Version-v1.1.0-yellowgreen) ![GitHub release (latest SemVer)](https://img.shields.io/badge/Language-python-yellowgreen)

DemuxNet is a computational tool for single-cell RNA sequencing (scRNA-seq) sample demultiplexing. It automates the process of assigning individual cells to their corresponding samples when multiple samples are pooled in a single sequencing run. DemuxNet predicts missing CMO (Cell Multiplexing Oligo) labels for barcodes with incomplete or missing information by leveraging machine learning algorithms. The tool works with sparse single-cell RNA expression matrices in RDS format and trains on known barcodes to predict sample identities for cells with missing or ambiguous CMO lables.
For more information, please refer to our manuscript: [******].

---

### Installation

#### Install demuxnet from source code
```bash
git clone https://github.com/paddi1990/DemuxNet.git
cd DemuxNet
python setup.py install
```
#### Or, you can install it via pip
```bash
pip install demuxnet
```

---

### Data preparation
DemuxNet takes a sparse single-cell expression matrix in RDS format as input. For the preprocessing of your single-cell RNA expression data into the required format, you can follow the steps below::

```bash
************
************
************
************
************
```

---

### Usage

Once installed, DemuxNet can be run from the command line. The tool automatically detects the "CMO" keyword within barcode strings and uses this information for training. For barcodes that do not contain the "CMO" information, DemuxNet will predict and fill in the missing CMO class.

#### Command Line Usage

To run Demuxnet, use the following command:

```bash
demuxnet -i gene_expressioin_matrix.rds -model DNN -feature 6000 -out prediction.csv
```
This command reads the input expression matrix, selects the top 6000 non-sparse features, uses the DNN model for prediction, and outputs the predicted CMO labels into `prediction.csv`.

#### Parameters:
- **`-i`** `gene_expression_matrix.rds`  
  Path to the input file in RDS format, which contains the sparse single-cell RNA expression matrix. This matrix should have rows representing cells and columns representing gene expression levels.
  
- **`-model`** `DNN`  
  The machine learning model to use for predicting the CMO labels. Currently, the available model is `DNN` (Deep Neural Network), but other models may be supported in future versions.
  
- **`-feature`** `6000`  
  The number of top features (genes) to use for training the model, selected based on non-zero counts in the expression matrix. This parameter determines the subset of genes used to train the model and should be tuned according to the dataset size and complexity.
  
- **`-out`** `prediction.csv`  
  The output file where the predicted CMO labels will be saved. The output will be a CSV file with two columns: "Barcode" and "Predicted CMO Label."

---


### Model Training

DemuxNet employs a Deep Neural Network (DNN) architecture for training the model based on the provided input data. The training process involves:

1. **Data Splitting**: The input dataset is split into training, validation, and test sets.
2. **Feature Selection**: The top `n` features (genes) with the highest non-zero counts are selected for training the model.
3. **Model Training**: A DNN model is trained using the selected features and corresponding CMO labels. Cross-entropy loss is used for multi-class classification tasks.
4. **Model Inference**: The trained model is used to predict the missing CMO labels for the test set (i.e., barcodes with missing or ambiguous CMO labels).

### Performance Metrics

- **Validation Accuracy**: DemuxNet provides an accuracy score on the validation set to assess the model's performance.
- **Prediction**: After training, the model performs inference on the test set and generates predictions for the missing CMO labels.

---


### Visualization
To do

---
### Contact
DemuxNet is maintained by Hu lab. For any questions or issues, please feel free to open an issue on the GitHub repository.
If you use DemuxNet in your research, please cite *************************.

---

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Contributing

We welcome contributions! If you have suggestions or improvements, feel free to submit a pull request. For major changes, please open an issue to discuss what you would like to change.