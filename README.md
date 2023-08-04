# GPT_and_Weak_Supervision_for_NER-Artificial_Intelligence_and_Law_
A repository containing code and dataset used in the paper "Combining prompt-based language models and weak supervision for labeling named entity recognition from legal documents"

The folders in this repository are composed of:

## Code

* `dodfSkweak.py`: script containing label functions for the Weak Supervision labeling

* `GPT3-Extrato de Contrato`: script used for GPT-3 labeling

* `Filtrando_E_preprocessando.ipynb`: script for preprocessing and splitting data

* `ResultadosHUMANO`: script for training and testing the Human-based models

* `ResultadosGPT.ipynb`: script for  training and testing the GPT-based models

* `ResultadosWEAKSUP.ipynb`: script for training and testing the Weak-Supervision-based models

* ` SplitingHUMANO10_10.ipynb`: script to establish percentage combinations between GPT and Human labeling

* `GPTcomHUMANO_BERTIMBAU.ipynb`: script for the training and testing of Human + GPT percentage combination on BERTimbau model

* `GPTcomHUMANO_BERTLENER.ipynb`: script for the training and testing of Human + GPT percentage combination on LenerBR model

* `GPTcomHUMANO_ROBERTA.ipynb`: script for the training and testing of Human + GPT percentage combination on RoBERTa model

* `GPTcomHUMANO_DISTILBERT.ipynb`: script for the training and testing of Human + GPT percentage combination on DistilBERT model 

* `GPTcomWeakSup.ipynb`: script for the training and testing of Weak Supervision + GPT combination 

* `Plots.ipynb`: script for creating plots used in the article

## Data

* `df_base.csv`: .csv file containing training data

* `df_test.csv`: .csv file containing test data

* `df_val.csv`: .csv file containing validation data

* `base_conll_human.conll`: file containing Human labeled training data processed in the IOB conll format

* `base_conll_GPT.conll`: file containing GPT-3 labeled training data processed in the IOB conll format

* `weak_conll.conll`: file containing Weak Supervision labeled training data processed in the IOB conll format

* `val_conll.conll`: file containing Human labeled validation data processed in the IOB conll format
