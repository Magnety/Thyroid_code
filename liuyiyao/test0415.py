import torch
import torch.nn as nn
import torch.nn.functional as F
import os
import numpy as np
np.set_printoptions(threshold=np.inf)
in_planes = 64
out_planes = 64
groups = 8
w=2
image_size = (16,32,64)
group_planes = out_planes//groups
kernel_size = (8,16,32)

x = torch.rand((1,64,16,32,64))
print("x.shape:",x.shape)

conv1 = nn.Conv3d(64,64,kernel_size=7,stride=2,padding=3)
x = conv1(x)
print("conv x.shape:",x.shape)
if w==0:   #length
    x = x.permute(0, 2, 3, 1 ,4)  # N, L, H ,C, W
elif w==1:  #height
    x = x.permute(0, 4, 2, 1, 3)  # N, W, L, C, H
else:  #width
    x = x.permute(0, 3, 4, 1, 2)  # N, H, W, C, L
print("x.shape:",x.shape)

query_index = torch.arange(kernel_size[2-w]).unsqueeze(0)
key_index = torch.arange(kernel_size[2-w]).unsqueeze(1)
print("query_index.shape", query_index.shape)
print("key_index.shape", key_index.shape)
relative_index = key_index - query_index + kernel_size[2-w] - 1
print("relative_index.shape", relative_index.shape)
flatten_index = relative_index.view(-1)
print("flatten_index.shape", flatten_index.shape)
qkv_transform = nn.Conv1d(in_planes, out_planes * 2, kernel_size=1, stride=1, padding=0, bias=False)
relative = nn.Parameter(torch.randn(group_planes * 2, kernel_size[2-w] * 2 - 1), requires_grad=True)

N,W,L,C,H = x.shape
x=x.contiguous().view(N*W*L,C,H)
print("x.shape:",x.shape)


qkv = qkv_transform(x)
print("qkv.shape:",qkv.shape)


q,k,v = torch.split(qkv.reshape(N*W*L,groups,group_planes*2,H),[group_planes//2,group_planes//2,group_planes],dim=2)
print("q.shape:",q.shape)
print("k.shape",k.shape)
print("v.shape",v.shape)
all_embeddings= torch.index_select(relative,1,flatten_index).view(group_planes*2,kernel_size[2-w],kernel_size[2-w])

print("all_embeddings.shape:",all_embeddings.shape)

q_embedding,k_embedding,v_embedding = torch.split(all_embeddings,[group_planes//2,group_planes//2,group_planes],dim=0)
print("q_embedding.shape:",q_embedding.shape)
print("k_embedding.shape:",k_embedding.shape)
print("v_embedding.shape:",v_embedding.shape)

qr = torch.einsum('bgci,cij->bgij',q,q_embedding)
print("/////////////////////////")
print("q.shape:",q.shape)
print("////////////////////////")
print("q_embedding.shape:",q_embedding.shape)
print("////////////////////////")
print("qr.shape:",qr.shape)
kr = torch.einsum('bgci,cij->bgij',k,k_embedding).transpose(2,3)
print("kr.shape:",kr.shape)

qk = torch.einsum('bgci,bgcj->bgij',q,k)
print("qk.shape:",qk.shape)

stack_similarity = torch.cat([qk,qr,kr],dim=1)
stack_similarity = stack_similarity.view(N*W*L,3,groups,H,H).sum(dim=1)
print("stack_similarity.shape:",stack_similarity.shape)

similarity = F.softmax(stack_similarity,dim=3)
print("similarity.shape:",similarity.shape)

sv = torch.einsum('bgij,bgcj->bgci',similarity,v)
print("sv.shape:",sv.shape)

sve = torch.einsum('bgij,cij->bgci',similarity,v_embedding)
print("sve.shape:",sve.shape)

stack_output = torch.cat([sv,sve],dim=-1).view(N*W*L,out_planes*2,H)
print("stack_output.shape:",stack_output.shape)

output = stack_output.view(N,W,L,out_planes,2,H).sum(dim=-2)
print("output.shape:",output.shape)
if w == 0:  # length
    output = output.permute(0, 3, 1, 2, 4)  # N, L, H ,C, W
elif w== 1:  # height
    output = output.permute(0, 3, 2, 4, 1)  # N, W, L, C, H
else:  # width
    output = output.permute(0, 3, 4, 1, 2)  # N, H, W, C, L


print("output.shape:",output.shape)



