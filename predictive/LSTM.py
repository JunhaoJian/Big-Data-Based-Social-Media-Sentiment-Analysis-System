# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import jieba
import pickle
import logging
import pandas as pd
import matplotlib.pyplot as plt
from gensim.models.word2vec import Word2Vec
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from torch.utils.data import TensorDataset, DataLoader
from torch.nn.utils.rnn import pad_sequence

# -------------------------- 1. Basic Configuration & Data Preprocessing --------------------------
# Matplotlib Chinese display settings (retained for proper character rendering)
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# Load stopwords
def load_stopwords(path='./predictive/hit_stopwords.txt'):
    with open(path, encoding='utf-8-sig') as f:
        stopwords = [i.replace("\n", "") for i in f.readlines()]
    return stopwords

stopwords = load_stopwords()

# Tokenization and stopword removal
def del_stop_words(text):
    if isinstance(text, str):
        text = text.replace("\n", "").strip()
    word_ls = jieba.lcut(text)
    word_ls = [i for i in word_ls if i not in stopwords and len(i) > 0]
    return word_ls

# Load negative/positive sample data
def load_data(neg_path='./predictive/neg.txt', pos_path='./predictive/pos.txt'):
    with open(neg_path, "r", encoding='UTF-8') as f:
        neg_data1 = f.readlines()
    with open(pos_path, "r", encoding='UTF-8') as f:
        pos_data1 = f.readlines()
    
    # Remove duplicates while preserving order
    neg_data = sorted(set(neg_data1), key=neg_data1.index)
    pos_data = sorted(set(pos_data1), key=pos_data1.index)
    
    # Tokenization processing
    neg_data = [del_stop_words(data) for data in neg_data if len(del_stop_words(data)) > 0]
    pos_data = [del_stop_words(data) for data in pos_data if len(del_stop_words(data)) > 0]
    
    return neg_data, pos_data

neg_data, pos_data = load_data()
all_sentences = neg_data + pos_data
print(f'Number of negative samples: {len(neg_data)}, Number of positive samples: {len(pos_data)}')

# -------------------------- 2. Word2Vec Word Embedding Training --------------------------
def train_word2vec(sentences, save_path='./predictive/f.model'):
    model = Word2Vec(
        sentences=sentences,
        vector_size=100,
        min_count=1,
        window=5,
        workers=4
    )
    model.save(save_path)
    return model

# Load/train word2vec model
try:
    w2v_model = Word2Vec.load('./predictive/f.model')
    print("Loaded pre-trained Word2Vec model")
except:
    print("Training new Word2Vec model")
    w2v_model = train_word2vec(all_sentences)

# Create word index and word vector dictionaries
def create_dictionaries(model):
    index_dict = {word: idx+1 for idx, word in enumerate(model.wv.index_to_key)}  # Index starts at 1 (0 for padding)
    word_vectors = {word: model.wv[word] for word in model.wv.index_to_key}
    return index_dict, word_vectors

index_dict, word_vectors = create_dictionaries(w2v_model)

# Save dictionaries
with open('./predictive/dict.txt.pkl', 'wb') as f:
    pickle.dump(index_dict, f)
    pickle.dump(word_vectors, f)

# -------------------------- 3. Data Vectorization & Preprocessing --------------------------
# Hyperparameter configuration
vocab_dim = 100
maxlen = 50
base_batch_size = 64
base_lr = 0.001
base_epochs = 40

# Convert text to index array
def text_to_index_array(p_new_dic, p_sen):
    new_sentences = []
    for sen in p_sen:
        new_sen = []
        for word in sen:
            try:
                new_sen.append(p_new_dic[word])
            except KeyError:
                new_sen.append(0)
        new_sentences.append(new_sen)
    
    # Pad to maxlen
    padded_sentences = [s[:maxlen] + [0]*(maxlen - len(s)) for s in new_sentences]
    return np.array(padded_sentences)

# Create embedding matrix
def create_embedding_matrix(index_dict, word_vectors, vocab_dim):
    n_symbols = len(index_dict) + 1
    embedding_weights = np.zeros((n_symbols, vocab_dim))
    for w, index in index_dict.items():
        embedding_weights[index, :] = word_vectors[w]
    return embedding_weights

embedding_weights = create_embedding_matrix(index_dict, word_vectors, vocab_dim)

# Convert data to word vector tensors
def creat_wordvec_tensor(embedding_weights, X_T):
    batch_size, seq_len = X_T.shape
    X_tt = np.zeros((batch_size, seq_len, vocab_dim))
    for i in range(batch_size):
        for j in range(seq_len):
            X_tt[i, j, :] = embedding_weights[int(X_T[i, j]), :]
    return X_tt

# Data splitting and preprocessing
label_list = [0]*len(neg_data) + [1]*len(pos_data)
X_train_l, X_test_l, y_train_l, y_test_l = train_test_split(
    all_sentences, label_list, test_size=0.2, random_state=42
)

# Convert to index arrays
X_train = text_to_index_array(index_dict, X_train_l)
X_test = text_to_index_array(index_dict, X_test_l)

# Convert to word vector tensors
X_train = creat_wordvec_tensor(embedding_weights, X_train)
X_test = creat_wordvec_tensor(embedding_weights, X_test)

# Convert to tensors
y_train = np.array(y_train_l)
y_test = np.array(y_test_l)

# Create DataLoader
def create_dataloader(X, y, batch_size, shuffle=True):
    dataset = TensorDataset(torch.from_numpy(X).float(), torch.from_numpy(y).long())
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

# -------------------------- 4. LSTM Model Definition --------------------------
class LSTMModel(nn.Module):
    def __init__(self, input_dim=100, hidden_dim=64, output_dim=2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            batch_first=True,
            num_layers=2,
            dropout=0.2
        )
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        out, (h_n, c_n) = self.lstm(x)
        out = out[:, -1, :]  # Take output from last time step
        out = self.fc(out)
        return out

# -------------------------- 5. Training & Evaluation Functions --------------------------
import torch
import torch.nn as nn

def train_model(model, train_loader, test_loader, criterion, optimizer, epochs, device):
    """
    Trains the neural network model and records training/testing loss and accuracy metrics.
    Compatible with both CrossEntropyLoss (for classification tasks) and MSELoss (requires one-hot label conversion).
    
    Args:
        model (torch.nn.Module): The neural network model to train
        train_loader (torch.utils.data.DataLoader): DataLoader for training data
        test_loader (torch.utils.data.DataLoader): DataLoader for testing/validation data
        criterion (torch.nn.Module): Loss function (CrossEntropyLoss/MSELoss)
        optimizer (torch.optim.Optimizer): Optimization algorithm (Adam/SGD etc.)
        epochs (int): Maximum number of training epochs
        device (torch.device): Training device (cuda/cpu)
    
    Returns:
        tuple: (trained_model, train_losses, train_accs, test_losses, test_accs)
            - trained_model: The trained model
            - train_losses: List of training loss values per epoch
            - train_accs: List of training accuracy values per epoch
            - test_losses: List of testing loss values per epoch
            - test_accs: List of testing accuracy values per epoch
    """
    # Initialize metric tracking lists
    train_losses = []
    train_accuracies = []
    test_losses = []
    test_accuracies = []
    
    # Early stopping configuration
    best_test_loss = float('inf')
    patience = 5  # Number of epochs to wait for improvement
    patience_counter = 0
    
    # Duplicate logging prevention (track printed epochs)
    printed_epochs = set()
    
    for epoch in range(epochs):
        # -------------------------- Training Phase --------------------------
        model.train()  # Set model to training mode
        total_train_loss = 0.0
        correct_train_predictions = 0
        total_train_samples = 0
        
        for batch_idx, (inputs, labels) in enumerate(train_loader):
            # Move data to target device
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            # Forward pass
            optimizer.zero_grad()  # Reset gradients
            outputs = model(inputs)
            
            # Calculate loss (handle MSELoss with one-hot encoding)
            if isinstance(criterion, nn.MSELoss):
                # Convert scalar labels to one-hot vectors (for MSELoss compatibility)
                one_hot_labels = torch.zeros_like(outputs)
                one_hot_labels.scatter_(1, labels.unsqueeze(1), 1.0)
                loss = criterion(outputs, one_hot_labels)
            else:
                # Use raw labels for CrossEntropyLoss (classification default)
                loss = criterion(outputs, labels)
            
            # Backward pass and optimization
            loss.backward()
            optimizer.step()
            
            # Update training metrics
            total_train_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            correct_train_predictions += torch.sum(predicted == labels.data)
            total_train_samples += inputs.size(0)
        
        # Calculate epoch-level training metrics
        avg_train_loss = total_train_loss / total_train_samples
        train_accuracy = correct_train_predictions.double() / total_train_samples
        
        # -------------------------- Testing Phase --------------------------
        model.eval()  # Set model to evaluation mode
        total_test_loss = 0.0
        correct_test_predictions = 0
        total_test_samples = 0
        
        with torch.no_grad():  # Disable gradient computation for efficiency
            for inputs, labels in test_loader:
                # Move data to target device
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                # Forward pass
                outputs = model(inputs)
                
                # Calculate loss (consistent with training phase)
                if isinstance(criterion, nn.MSELoss):
                    one_hot_labels = torch.zeros_like(outputs)
                    one_hot_labels.scatter_(1, labels.unsqueeze(1), 1.0)
                    loss = criterion(outputs, one_hot_labels)
                else:
                    loss = criterion(outputs, labels)
                
                # Update testing metrics
                total_test_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs, 1)
                correct_test_predictions += torch.sum(predicted == labels.data)
                total_test_samples += inputs.size(0)
        
        # Calculate epoch-level testing metrics
        avg_test_loss = total_test_loss / total_test_samples
        test_accuracy = correct_test_predictions.double() / total_test_samples
        
        # -------------------------- Metric Tracking --------------------------
        # Save epoch metrics to lists
        train_losses.append(avg_train_loss)
        train_accuracies.append(train_accuracy.item())
        test_losses.append(avg_test_loss)
        test_accuracies.append(test_accuracy.item())
        
        # -------------------------- Logging & Early Stopping --------------------------
        # 1. Print progress (prevent duplicate logging)
        current_epoch = epoch + 1
        if current_epoch % 5 == 0 and current_epoch not in printed_epochs:
            print(f'Epoch [{current_epoch}/{epochs}], '
                  f'Train Loss: {avg_train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}, '
                  f'Test Loss: {avg_test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}')
            printed_epochs.add(current_epoch)
        
        # 2. Early stopping logic (stop if test loss stops improving)
        if avg_test_loss < best_test_loss:
            best_test_loss = avg_test_loss
            patience_counter = 0  # Reset counter on improvement
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping triggered at epoch {current_epoch} (no test loss improvement for {patience} epochs)")
                break  # Terminate training loop
    
    # Return trained model and complete metrics
    return model, train_losses, train_accuracies, test_losses, test_accuracies

# -------------------------- 6. Base Model Training (Default Parameters) --------------------------
# Create DataLoaders
train_loader_base = create_dataloader(X_train, y_train, base_batch_size)
test_loader_base = create_dataloader(X_test, y_test, base_batch_size, shuffle=False)

model_base = LSTMModel().to(device)

# Loss function and optimizer
criterion_base = nn.CrossEntropyLoss()
optimizer_base = torch.optim.Adam(model_base.parameters(), lr=base_lr)

# Train the base model
print("===== Base Model Training (CrossEntropyLoss, lr=0.001, batch_size=64) =====")
model_base, train_losses_base, train_accs_base, test_losses_base, test_accs_base = train_model(
    model_base, train_loader_base, test_loader_base,
    criterion_base, optimizer_base, base_epochs, device
)

# -------------------------- 7. Different Loss Function Comparison --------------------------
# MSELoss comparison
model_mse = LSTMModel().to(device)
criterion_mse = nn.MSELoss()  # MSE loss for regression (requires label conversion for classification)
optimizer_mse = torch.optim.Adam(model_mse.parameters(), lr=base_lr)

print("\n===== MSELoss Loss Function Comparison Training =====")
model_mse, train_losses_mse, train_accs_mse, test_losses_mse, test_accs_mse = train_model(
    model_mse, train_loader_base, test_loader_base,
    criterion_mse, optimizer_mse, base_epochs, device
)

# -------------------------- 8. Different Learning Rate Comparison --------------------------
lr_list = [0.1, 0.01, 0.001, 0.0001]
lr_results = {}

print("\n===== Different Learning Rate Comparison Training =====")
for lr in lr_list:
    print(f"\n--- Learning Rate: {lr} ---")
    model_lr = LSTMModel().to(device)
    optimizer_lr = torch.optim.Adam(model_lr.parameters(), lr=lr)
    
    _, train_losses, train_accs, test_losses, test_accs = train_model(
        model_lr, train_loader_base, test_loader_base,
        criterion_base, optimizer_lr, base_epochs, device
    )
    
    lr_results[lr] = {
        'train_losses': train_losses,
        'train_accs': train_accs,
        'test_losses': test_losses,
        'test_accs': test_accs
    }

# -------------------------- 9. Different Batch Size Comparison --------------------------
batch_sizes = [8, 16, 32, 64, 128]
batch_results = {}

print("\n===== Different Batch Size Comparison Training =====")
for bs in batch_sizes:
    print(f"\n--- Batch Size: {bs} ---")
    train_loader_bs = create_dataloader(X_train, y_train, bs)
    test_loader_bs = create_dataloader(X_test, y_test, bs, shuffle=False)
    
    model_bs = LSTMModel().to(device)
    optimizer_bs = torch.optim.Adam(model_bs.parameters(), lr=base_lr)
    
    _, train_losses, train_accs, test_losses, test_accs = train_model(
        model_bs, train_loader_bs, test_loader_bs,
        criterion_base, optimizer_bs, base_epochs, device
    )
    
    batch_results[bs] = {
        'train_losses': train_losses,
        'train_accs': train_accs,
        'test_losses': test_losses,
        'test_accs': test_accs
    }

# -------------------------- 10. Performance Visualization --------------------------
# 10.1 Base Model Performance Curves
def plot_base_performance(train_losses, train_accs, test_losses, test_accs):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Loss curve
    ax1.plot(range(1, base_epochs+1), train_losses, label='Training Loss', marker='o', markersize=2)
    ax1.plot(range(1, base_epochs+1), test_losses, label='Testing Loss', marker='s', markersize=2)
    ax1.set_title('Base Model - Loss Curves (CrossEntropyLoss)')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Accuracy curve
    ax2.plot(range(1, base_epochs+1), train_accs, label='Training Accuracy', marker='o', markersize=2)
    ax2.plot(range(1, base_epochs+1), test_accs, label='Testing Accuracy', marker='s', markersize=2)
    ax2.set_title('Base Model - Accuracy Curves (CrossEntropyLoss)')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.set_ylim(0, 1.1)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('./performance_base.png', dpi=300, bbox_inches='tight')
    plt.show()

# 10.2 Different Loss Function Comparison
def plot_loss_comparison(base_loss, base_acc, mse_loss, mse_acc):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Loss comparison
    ax1.plot(range(1, base_epochs+1), base_loss['train'], label='CrossEntropy - Training', marker='o', markersize=2)
    ax1.plot(range(1, base_epochs+1), base_loss['test'], label='CrossEntropy - Testing', marker='s', markersize=2)
    ax1.plot(range(1, base_epochs+1), mse_loss['train'], label='MSE - Training', marker='^', markersize=2)
    ax1.plot(range(1, base_epochs+1), mse_loss['test'], label='MSE - Testing', marker='*', markersize=2)
    ax1.set_title('Different Loss Functions - Loss Curve Comparison')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Accuracy comparison
    ax2.plot(range(1, base_epochs+1), base_acc['train'], label='CrossEntropy - Training', marker='o', markersize=2)
    ax2.plot(range(1, base_epochs+1), base_acc['test'], label='CrossEntropy - Testing', marker='s', markersize=2)
    ax2.plot(range(1, base_epochs+1), mse_acc['train'], label='MSE - Training', marker='^', markersize=2)
    ax2.plot(range(1, base_epochs+1), mse_acc['test'], label='MSE - Testing', marker='*', markersize=2)
    ax2.set_title('Different Loss Functions - Accuracy Curve Comparison')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.set_ylim(0, 1.1)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('./performance_loss_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

# 10.3 Different Learning Rate Comparison (Two plots)
def plot_lr_comparison(lr_results):
    # Loss comparison plot
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    for lr, res in lr_results.items():
        ax1.plot(range(1, base_epochs+1), res['train_losses'], label=f'LR={lr} - Training', marker='o', markersize=2)
        ax1.plot(range(1, base_epochs+1), res['test_losses'], label=f'LR={lr} - Testing', marker='s', markersize=2)
    ax1.set_title('Different Learning Rates - Loss Curve Comparison')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    plt.savefig('./performance_lr_loss.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Accuracy comparison plot
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    for lr, res in lr_results.items():
        ax2.plot(range(1, base_epochs+1), res['train_accs'], label=f'LR={lr} - Training', marker='o', markersize=2)
        ax2.plot(range(1, base_epochs+1), res['test_accs'], label=f'LR={lr} - Testing', marker='s', markersize=2)
    ax2.set_title('Different Learning Rates - Accuracy Curve Comparison')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.set_ylim(0, 1.1)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.savefig('./performance_lr_acc.png', dpi=300, bbox_inches='tight')
    plt.show()

# 10.4 Different Batch Size Comparison (Two plots)
def plot_batch_comparison(batch_results):
    # Loss comparison plot
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    for bs, res in batch_results.items():
        ax1.plot(range(1, base_epochs+1), res['train_losses'], label=f'BS={bs} - Training', marker='o', markersize=2)
        ax1.plot(range(1, base_epochs+1), res['test_losses'], label=f'BS={bs} - Testing', marker='s', markersize=2)
    ax1.set_title('Different Batch Sizes - Loss Curve Comparison')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    plt.savefig('./performance_batch_loss.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Accuracy comparison plot
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    for bs, res in batch_results.items():
        ax2.plot(range(1, base_epochs+1), res['train_accs'], label=f'BS={bs} - Training', marker='o', markersize=2)
        ax2.plot(range(1, base_epochs+1), res['test_accs'], label=f'BS={bs} - Testing', marker='s', markersize=2)
    ax2.set_title('Different Batch Sizes - Accuracy Curve Comparison')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.set_ylim(0, 1.1)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.savefig('./performance_batch_acc.png', dpi=300, bbox_inches='tight')
    plt.show()

# 10.5 Top 100 Test Set Predictions Visualization
def plot_predictions(model, test_loader, X_test_l, y_test, top_n=100):
    model.eval()
    preds_list = []
    true_list = []
    text_list = []
    
    with torch.no_grad():
        for i, (data, target) in enumerate(test_loader):
            if len(preds_list) >= top_n:
                break
            data, target = data.to(device), target.to(device)
            output = model(data)
            _, preds = torch.max(output, 1)
            
            # Collect results
            batch_size = data.size(0)
            for j in range(batch_size):
                if len(preds_list) >= top_n:
                    break
                preds_list.append(preds[j].item())
                true_list.append(target[j].item())
                # Restore text (first 20 characters)
                text = ' '.join(X_test_l[len(preds_list)-1])[:20] + '...' if len(X_test_l[len(preds_list)-1]) > 0 else ''
                text_list.append(text)
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'Index': range(1, top_n+1),
        'Text Content': text_list,
        'True Label': ['Negative' if x==0 else 'Positive' for x in true_list],
        'Predicted Label': ['Negative' if x==0 else 'Positive' for x in preds_list],
        'Is Correct': [x==y for x, y in zip(preds_list, true_list)]
    })
    
    # Save results
    results_df.to_csv('./predictions_top100.csv', index=False, encoding='utf-8-sig')
    
    # Visualize table (first 20 rows)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare table data
    table_data = []
    headers = ['Index', 'Text Content', 'True Label', 'Predicted Label', 'Is Correct']
    for i in range(min(20, top_n)):
        table_data.append([
            results_df.iloc[i]['Index'],
            results_df.iloc[i]['Text Content'],
            results_df.iloc[i]['True Label'],
            results_df.iloc[i]['Predicted Label'],
            '√' if results_df.iloc[i]['Is Correct'] else '×'
        ])
    
    # Create table
    table = ax.table(cellText=table_data, colLabels=headers, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    
    # Style table
    for i in range(len(headers)):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(color='white', weight='bold')
    
    # Highlight incorrect predictions
    for i in range(1, len(table_data)+1):
        if table_data[i-1][4] == '×':
            table[(i, 4)].set_facecolor('#FF5252')
            table[(i, 4)].set_text_props(color='white', weight='bold')
    
    plt.title('Top 20 Test Set Predictions', fontsize=14, pad=20)
    plt.savefig('./predictions_top20.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print statistics
    correct_num = sum(results_df['Is Correct'])
    print(f"\nTop {top_n} Test Set Prediction Statistics:")
    print(f"Correct: {correct_num}, Incorrect: {top_n - correct_num}, Accuracy: {correct_num/top_n:.4f}")
    
    return results_df

# -------------------------- 11. Execute All Visualizations --------------------------
# Base model performance curves
plot_base_performance(train_losses_base, train_accs_base, test_losses_base, test_accs_base)

# Different loss function comparison
loss_data = {
    'base_loss': {'train': train_losses_base, 'test': test_losses_base},
    'mse_loss': {'train': train_losses_mse, 'test': test_losses_mse},
    'base_acc': {'train': train_accs_base, 'test': test_accs_base},
    'mse_acc': {'train': train_accs_mse, 'test': test_accs_mse}
}
plot_loss_comparison(loss_data['base_loss'], loss_data['base_acc'], loss_data['mse_loss'], loss_data['mse_acc'])

# Different learning rate comparison
plot_lr_comparison(lr_results)

# Different batch size comparison
plot_batch_comparison(batch_results)

# Prediction results visualization
results_df = plot_predictions(model_base, test_loader_base, X_test_l, y_test, top_n=100)

# -------------------------- 12. Terracotta Army Comment Sentiment Analysis --------------------------
def analyze_bingmayong_comments(model, csv_path='./predictive/bingmayong1.csv'):
    # Load data
    df = pd.read_csv(csv_path)
    df = df.drop_duplicates(subset='content')
    df = df[df['content'].notna() & (df['content'] != '')]
    
    # Prediction function
    def predict_sentiment(text):
        model.eval()
        words = del_stop_words(text)
        index_array = text_to_index_array(index_dict, [words])
        tensor_input = creat_wordvec_tensor(embedding_weights, index_array)
        
        with torch.no_grad():
            output = model(torch.from_numpy(tensor_input).float().to(device))
            _, pred = torch.max(output, 1)
        return 'Positive' if pred.item() == 1 else 'Negative'
    
    # Batch prediction
    df['Predicted Sentiment'] = df['content'].apply(predict_sentiment)
    
    # Save results
    df.to_csv('./predictive/bingmayong1_with_sentiment1.csv', index=False, encoding='utf-8-sig')
    
    # Statistics
    sentiment_counts = df['Predicted Sentiment'].value_counts()
    print("\nTerracotta Army Comment Sentiment Analysis Results:")
    print(sentiment_counts)
    print(f"Positive comment ratio: {sentiment_counts.get('Positive', 0)/len(df):.4f}")
    print(f"Negative comment ratio: {sentiment_counts.get('Negative', 0)/len(df):.4f}")
    
    return df

# Execute Terracotta Army comment analysis
bm_df = analyze_bingmayong_comments(model_base)