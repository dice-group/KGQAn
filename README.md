**Note**: This is a forked version of https://github.com/CoDS-GCS/KGQAn. This repository has been modified to fix the existing bugs and to streamline deployment.
 - - - - -

 KGQAn - A Universal Question-Answering Platform for Knowledge Graphs 
 ---
 - - - - -

Abstract
-------
Knowledge from diverse application domains is organized as knowledge graphs (KGs) that are stored in RDF engines accessible in the web via SPARQL endpoints. Expressing a well-formed SPARQL query requires information about the graph structure and the exact URIs of its components, which is impractical for the average user. Question answering (QA) systems assist by translating natural language questions to SPARQL. Existing QA systems are typically based on application-specific human-curated rules, or require prior information, expensive pre-processing and model adaptation for each targeted KG. Therefore, they are hard to generalize to a broad set of applications and KGs. In this paper, we propose KGQAn, a universal QA system that does not need to be tailored to each target KG. Instead of curated rules, KGQAn introduces a novel formalization of question understanding as a text generation problem to convert a question into an intermediate abstract representation via a neural sequence-to-sequence model. We also develop a just-in-time linker that maps at query time the abstract representation to a SPARQL query for a specific KG, using only the publicly accessible APIs and the existing indices of the RDF store, without requiring any pre-processing. Our experiments with several real KGs demonstrate that KGQAn is easily deployed and outperforms by a large margin the state-of-the-art in terms of quality of answers and processing time, especially for arbitrary KGs, unseen during the training.
![GitHub Logo](logo/KGQAn%20Architecture.png)

This repository is dedicated to our paper titled "A Universal Question-Answering Platform for Knowledge Graphs" published in SIGMOD 2023. The full paper can be accessed [here](https://dl.acm.org/doi/10.1145/3588911).

## Availability and Reproducibility

This system has been awarded the Artifact Available, Artifact Evaluated, and Artifact Reproducible badges from ACM SIGMOD ARI (Availability & Reproducibility Initiative)
 
 ![Artifact Available](Figures/artifacts_available_v1_1_2.png) ![Artifact Evaluated](Figures/artifacts_evaluated_reusable_v1_1_2.png) ![Artifact Reproducible](Figures/results_reproduced_v1_1_2.png)




Running KGQAn
-------------
- - - - 
- KGQAn can run in two modes:
  1. Docker Setup
  2. Local Setup

To reproduce the values in the paper, you can [check](reproducability/Instructions.md)

Running KGQAn in Docker mode 
------------
- - - - 
[Run KGQAn in Dockerized Environment](docker_run.md)

Running KGQAn in Local mode 
------------
- - - - 

### Installation
 
* Clone the repo
* Create `kgqan` Conda environment (Python 3.7) and install pip requirements.
```
conda create --name kgqan python=3.7
conda activate kgqan
pip install -r requirements.txt
```

### Download the required data/models:
- Run the following command to execute the data download script:
- This script will download the trained models and any necessary data for the services.
```shell
./data_download.sh local
```

### Running KGQAn

KGQAn uses a semantic similarity model in two of its phases, a pre-requisite step is to run the server of the
word-embedding based similarity service using the following command
 ```
 conda activate kgqan
 python word_embedding/server.py 127.0.0.1 9600
 ```
You can run KGQAn in two modes:
1. Batch processing: This is used to run benchmarks or pre-defined set of questions
2. Server mode: This is used to answer individual questions

### Batch processing ###
KGQAn takes as an input a JSON file containing all questions in the following format:
```
{
    "question": 
    [
        {
            "string": question text
            "language": "en"
        }
   ],
   "id": question id,
   "answers": []
}
```
* To run KGQAn in this mode, you need a script that opens the questions' file then calls KGQAn module to answer the questions.
* To call the KGQAn module you should use the following code:
```python
from kgqan import KGQAn
my_kgqan = KGQAn()
answers = my_kgqan.ask(question_text=question_text, question_id=question['id'], knowledge_graph=knowledge_graph)
```
* check `evaluation/qald9_eval.py` as an example.
* To run the benchmarks, you need to
  * deploy a Virtuoso Endpoint (04-2016 for Qald 9 and 10-2016 for Lcquad)
  * Update the url of the KG in `knowledge_graph_to_uri` that can be found in `src/kgqan.py` 
### Server ###
KGQAn takes as an input: the question, the knowledge graph and the maximum number of answers the user wants to be returned

To run KGQAn in this mode:
1. Open the KGQAn server by running the following command from the `src` directory
```
conda activate kgqan
python -m kgqan.server
```
2. Wait until the following message shows to be sure the server is running successfully
```
Server started http://0.0.0.0:8899
```
3. Send a POST request to the server with the question, the knowledge graph to query and the maximum number of answers required using
   * Postman
   * CURL
   ```
        curl -X POST -H "Content-Type: application/json" \
        -d '{"question": "Who founded Intel?", "knowledge_graph": "dbpedia", "max_answers": 3}' \
        http://0.0.0.0:8899
   ```

Benchmarks:
-
- - - -
1. QALD-9:
   1. `src/evaluation/data/qald-9-test-multilingual.json`
   2. https://github.com/ag-sc/QALD/blob/master/9/data/qald-9-test-multilingual.json
2. LCQUAD:
   1. `src/evaluation/data/lcquad-qaldformat-test2.json `
   2. https://figshare.com/articles/dataset/LC-QuAD_QALDformat/5818452 
3. YAGO: `src/evaluation/data/qald9_yago100.json ` 
4. DBLP: `src/evaluation/data/qald9_dblp100.json ` 
5. MAG: `src/evaluation/data/qald9_ms100.json` 

Citing Our Work
-
- - - -
```
@article{kgqan,
         title={A Universal Question-Answering Platform for Knowledge Graphs}, 
         author={Reham Omar and Ishika Dhall and Panos Kalnis and Essam Mansour},
         year={2023},
         journal={Proceedings of the International Conference on Management of Data,(SIGMOD)} 
}
```
Contact:
-
- - - -
For any queries, feel free to send an e-mail to `reham.omar@mail.concordia.ca` or `essam.mansour@concordia.ca`. We look forward to receiving your feedback.
