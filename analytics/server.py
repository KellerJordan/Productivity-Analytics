from bottle import route, run, post, request
import torch
import pickle

def load_model():
    global indices
    global model
    
    with open('datasets/indices.pkl', 'rb') as f:
        indices = pickle.load(f)
    
#    with open('models/model.pk', 'rb') as f:
#        model = torch.load(model, f)

        
@post('/predict')
def index():
    print(request.json)
    # urls = request.post.urls
    return '3'

def predict(urls):
    global indices
    global model
    return [True, False]


if __name__ == '__main__':
    load_model()
    run(host='', port=8080)
