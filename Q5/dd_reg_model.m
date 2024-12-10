% regression model function
function mdl = dd_reg_model(sen_idx, sen_data, G, cent, predi, train_size)
    model_fit = @(b, x) b(2).*(... % scaling term (betweenness)
    b(1).*sin((2*pi/24).*x(:,1) + (13*pi/12))) ... % daily fluxuation term
    + b(3).*sin((2*pi/5).*x(:,1) + b(5))... % daily traffic pattern term % some phase offset b(5)
    + b(4).*x(:,2) ... % adjacent node 1
    + b(6).*x(:,3); % adjacent node 2
    beta0 = [1 1 1 1 1 1]; % An arbitrary guess

    % creating parameter matrix
    X = [(1:train_size)',...
    predi(1:train_size,sen_idx+1)... % adjacent node
    predi(1:train_size,sen_idx-1)];

    mdl = fitnlm(X,sen_data.count(1:train_size,1),model_fit,beta0);
    

