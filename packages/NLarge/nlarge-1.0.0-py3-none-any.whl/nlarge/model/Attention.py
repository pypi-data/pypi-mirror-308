import torch
import torch.nn as nn
import torch.nn.functional as F


class TextClassifierAttentionNetwork(nn.Module):
    def __init__(
        self, embedding_dim, hidden_dim, output_dim, pretrained_embedding
    ):
        super(TextClassifierAttentionNetwork, self).__init__()
        self.embedding = nn.Embedding.from_pretrained(
            pretrained_embedding, freeze=False
        )
        self.key_layer = nn.Linear(embedding_dim, hidden_dim)
        self.query_layer = nn.Linear(embedding_dim, hidden_dim)
        self.value_layer = nn.Linear(embedding_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, length):
        # Pass input through embedding layer
        embedded = self.embedding(x)

        # Ensure the embedded tensor is of type Float
        embedded = embedded.float()

        keys = self.key_layer(embedded)
        queries = self.query_layer(embedded)
        values = self.value_layer(embedded)

        # Compute attention scores
        attention_scores = torch.bmm(
            queries, keys.transpose(1, 2)
        ) / torch.sqrt(torch.tensor(keys.size(-1), dtype=torch.float32))
        attention_weights = F.softmax(attention_scores, dim=-1)

        # Compute the context vector
        context = torch.bmm(attention_weights, values)

        # Aggregate context vector
        context = context.sum(dim=1)

        # Pass through fully connected layer and sigmoid activation
        output = self.fc(context)
        output = self.sigmoid(output)
        output = output.squeeze(1)

        return output


class MultiHeadAttention(nn.Module):
    def __init__(self, embedding_dim, hidden_dim, num_heads):
        super(MultiHeadAttention, self).__init__()
        self.num_heads = num_heads
        self.hidden_dim = hidden_dim

        self.key_layer = nn.Linear(embedding_dim, hidden_dim * num_heads)
        self.query_layer = nn.Linear(embedding_dim, hidden_dim * num_heads)
        self.value_layer = nn.Linear(embedding_dim, hidden_dim * num_heads)
        self.fc = nn.Linear(hidden_dim * num_heads, hidden_dim)

    def forward(self, x):
        batch_size = x.size(0)

        # Compute keys, queries, and values
        keys = (
            self.key_layer(x)
            .view(batch_size, -1, self.num_heads, self.hidden_dim)
            .transpose(1, 2)
        )
        queries = (
            self.query_layer(x)
            .view(batch_size, -1, self.num_heads, self.hidden_dim)
            .transpose(1, 2)
        )
        values = (
            self.value_layer(x)
            .view(batch_size, -1, self.num_heads, self.hidden_dim)
            .transpose(1, 2)
        )

        # Compute attention scores
        attention_scores = torch.matmul(
            queries, keys.transpose(-2, -1)
        ) / torch.sqrt(torch.tensor(self.hidden_dim, dtype=torch.float32))
        attention_weights = F.softmax(attention_scores, dim=-1)

        # Compute the context vector
        context = (
            torch.matmul(attention_weights, values)
            .transpose(1, 2)
            .contiguous()
            .view(batch_size, -1, self.hidden_dim * self.num_heads)
        )

        # Pass through fully connected layer
        output = self.fc(context)

        return output


class TextClassifierMultiHeadAttentionNetwork(nn.Module):
    def __init__(
        self,
        embedding_dim,
        hidden_dim,
        output_dim,
        num_heads,
        pretrained_embedding,
    ):
        super(TextClassifierMultiHeadAttentionNetwork, self).__init__()
        self.embedding = nn.Embedding.from_pretrained(
            pretrained_embedding, freeze=False
        )
        self.multi_head_attention = MultiHeadAttention(
            embedding_dim, hidden_dim, num_heads
        )
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, lengths):
        # Pass input through embedding layer
        embedded = self.embedding(x)

        # Ensure the embedded tensor is of type Float
        embedded = embedded.float()

        attn_output = self.multi_head_attention(embedded)
        output = self.fc(attn_output)
        output = self.sigmoid(output)
        output = output.squeeze(1)

        return output
