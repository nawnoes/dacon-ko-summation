"""
submission.csv
   id        summary
[아이디명]     [추출 요약문]
"""
import csv
import torch
from kobert_transformers import get_tokenizer
from eval_dataset import ExtractiveDataset
from model.kobert import KoBERTforExtractiveSummarization

"""
id, article_original

"""
# config
tokenizer = get_tokenizer()
dir_path="."
ckpt_path = f'{dir_path}/checkpoint/kobert-extractive-v81.pth'
csv_path = f'{dir_path}/data/extractive_summary.csv'
ctx = "cuda" if torch.cuda.is_available() else "cpu"
device = torch.device(ctx)

# load data
eval_datas = ExtractiveDataset(tokenizer=tokenizer,data_path='./data/eval_test.jsonl')

# load kobert checkpoint
checkpoint = torch.load(ckpt_path, map_location=device)
model = KoBERTforExtractiveSummarization()
model.load_state_dict(checkpoint['model_state_dict'])

# eval mode
model.eval()

for data in eval_datas:
  id = data['id']
  input = data['input']

  output = model(**input)
  logit = output['logits'][0]
  softmax_logit = torch.softmax(logit, dim=1)
  argmax = torch.argmax(softmax_logit, dim=1)
  print(argmax)

