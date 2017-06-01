x = 10 * randn([1,100]) + 8;
noise = 10 * randn([1,100]);
y = 5 * (x + noise) + 2;

% 数据中心化，并大致将数据缩放至[-1, 1]区间，（后一步对结果没有影响）
% 实际效果，中心化比标准化好很多
x_cent = x - mean(x);
y_cent = y - mean(y);
x_norm = x_cent / max(x_cent); 
y_norm = y_cent / max(y_cent); 

% 数据标准化，严格缩放至[-1, 1]区间
% x_norm = (x-(max(x)+min(x))/2) / ((max(x)-min(x))/2);
% y_norm = (y-(max(y)+min(y))/2)/((max(y)-min(y))/2);

X = [x_norm;y_norm];
X_cov = X * X';

% V是协方差矩阵X_cov的特征向量，特征向量之间都是正交的（垂直）
% D是特征值，其值大小表示所对应的的特征向量对于区分原数据的贡献度
[V, D] = eig(X_cov); 

t = -1:0.01:1;
v1 = t * V(2,1)/V(1,1);
v2 = t * V(2,2)/V(1,2);

plot(x_norm, y_norm, 'ro'); hold on
plot(t, v1, 'b'); hold on
plot(t, v2, 'k'); hold on
axis([-1.5, 1.5, -1.5, 1.5]);
axis square