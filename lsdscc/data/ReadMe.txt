1, dataset.txt 
The dataset.txt is the data used for training (85%) and validation(15%) in this paper.
The dialog dataset are collected from the movie discuss threads in the Reddit community, 
with necessary data cleansing and pruning works detailed in the paper.

Each line follows the format: Query <EOS>#TAB# Response


2, test.group.json
The testing set annotated by three volunteers is organized as a json format file.
The annotation details can be found in the paper.

The format is as follows:
{query:{group_id_1:[response 1, response 2, ...],
       group_id_2:[response 1, response 2, ...], ...} , ...}
