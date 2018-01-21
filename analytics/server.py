from bottle import route, run
import torch
import pickle

def load_model():
    global indices
    global model
    
    with open('datasets/indices.pkl', 'rb') as f:
        indices = pickle.load(f)
    
    with open('models/model.pk', 'rb') as f:
        model = torch.load(model, f)

        
@route('/predict')
def index():
    urls = request.post.urls
    return predict(urls)

def predict(urls):
    global indices
    global model
    return [True, False]


if __name__ == '__main__':
    load_model()
    run(host='', port=8080)
