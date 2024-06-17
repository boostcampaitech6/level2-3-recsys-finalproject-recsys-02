import torch
import numpy as np
import mlflow
from tqdm import tqdm


# for training, data sampling
def random_neg(l, r, s):
    # log에 존재하는 아이템과 겹치지 않도록 sampling
    t = np.random.randint(l, r)
    while t in s:
        t = np.random.randint(l, r)
    return t


def sample_batch(user_train, num_user, num_item, batch_size, max_len):
    def sample():

        user = np.random.randint(num_user)  # user를 임의로 선택

        # 미리 max_len에 해당하는 array 생성, zero padding
        seq = np.zeros([max_len], dtype=np.int32)
        pos = np.zeros([max_len], dtype=np.int32)
        neg = np.zeros([max_len], dtype=np.int32)
        nxt = user_train[user][-1]
        idx = max_len - 1

        # negative sample은 train sequence에 없는 item 사용
        train_item = set(user_train[user])
        for i in reversed(user_train[user][:-1]):
            # 미리 정의된 sequence를 역순으로 채움, ex: seq = [0,0,0,1,2,3] (0은 pad)
            seq[idx] = i
            pos[idx] = nxt
            if nxt != 0:
                neg[idx] = random_neg(1, num_item + 1, train_item)
            nxt = i
            idx -= 1
            if idx == -1: break
        return (user, seq, pos, neg)
    user, seq, pos, neg = zip(*[sample() for _ in range(batch_size)])
    user, seq, pos, neg = np.array(user), np.array(seq), np.array(pos), np.array(neg)
    return user, seq, pos, neg


def train(model, optimizer, criterion, num_epochs, num_batch,
          user_train, num_user, num_item, batch_size, max_len, device):
    # training
    for epoch in range(1, num_epochs + 1):
        tbar = tqdm(range(num_batch))
        for step in tbar: # num_batch만큼 sampling
            user, seq, pos, neg = sample_batch(user_train, num_user, num_item, batch_size, max_len)
            pos_logits, neg_logits = model(seq, pos, neg)
            pos_labels, neg_labels = torch.ones(pos_logits.shape, device=device), torch.zeros(neg_logits.shape, device=device)

            optimizer.zero_grad()
            indices = np.where(pos != 0)
            loss = criterion(pos_logits[indices], pos_labels[indices])
            loss += criterion(neg_logits[indices], neg_labels[indices])
            loss.backward()
            optimizer.step()

            tbar.set_description(f'Epoch: {epoch:3d}| Step: {step:3d}| Train loss: {loss:.5f}')

        #torch.save(model.state_dict(), "SASRec_model.pt")
        mlflow.log_metric("loss", loss)
            
def evaluate(model, num_user, user_train, user_valid, num_item, args):
    model.eval()

    NDCG = 0.0 # NDCG@10
    HIT = 0.0 # HIT@10

    num_item_sample = num_item
    num_user_sample = num_user // 3
    users = np.random.randint(0, num_user, num_user_sample) # 1000개만 sampling 하여 evaluation
    for u in users:
        seq = user_train[u][-args.max_len:]
        rated = set(user_train[u] + user_valid[u])
        item_idx = user_valid[u] + [random_neg(1, num_item + 1, rated) for _ in range(num_item_sample)]

        with torch.no_grad():
            predictions = -model.predict(np.array([seq]), np.array(item_idx))
            predictions = predictions[0]
            rank = predictions.argsort().argsort()[0].item()

        if rank < 10: # 만약 예측 성공시
            NDCG += 1 / np.log2(rank + 2)
            HIT += 1
    print(f'NDCG@10: {NDCG/num_user_sample}| HIT@10: {HIT/num_user_sample}')
    mlflow.log_metric("HIT_10", HIT/num_user_sample)