x = 10 * randn([1,100]) + 8;
noise = 10 * randn([1,100]);
y = 5 * (x + noise) + 2;

% �������Ļ��������½�����������[-1, 1]���䣬����һ���Խ��û��Ӱ�죩
% ʵ��Ч�������Ļ��ȱ�׼���úܶ�
x_cent = x - mean(x);
y_cent = y - mean(y);
x_norm = x_cent / max(x_cent); 
y_norm = y_cent / max(y_cent); 

% ���ݱ�׼�����ϸ�������[-1, 1]����
% x_norm = (x-(max(x)+min(x))/2) / ((max(x)-min(x))/2);
% y_norm = (y-(max(y)+min(y))/2)/((max(y)-min(y))/2);

X = [x_norm;y_norm];
X_cov = X * X';

% V��Э�������X_cov��������������������֮�䶼�������ģ���ֱ��
% D������ֵ����ֵ��С��ʾ����Ӧ�ĵ�����������������ԭ���ݵĹ��׶�
[V, D] = eig(X_cov); 

t = -1:0.01:1;
v1 = t * V(2,1)/V(1,1);
v2 = t * V(2,2)/V(1,2);

plot(x_norm, y_norm, 'ro'); hold on
plot(t, v1, 'b'); hold on
plot(t, v2, 'k'); hold on
axis([-1.5, 1.5, -1.5, 1.5]);
axis square