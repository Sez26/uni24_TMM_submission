%% Predict counts using IDW interpolation
% Inverse Distance Weighting
function predict = IDWprediction(G, tar_idx, counts, sens_idx)
    % disp(counts)
    num_sen = length(sens_idx);
    % find shortest path between tartget node and sensor nodes
    d = zeros(num_sen,1);
    for i = 1:num_sen
        [~, d(i)] = shortestpath(G,sens_idx(i),tar_idx);
    end
    
    % disp (d)
    predict = NaN;
    ids = 1:num_sen;
    if any(d==0) % tar_idx is a sensor
        % do IDW will all other sensors
        ids(d==0) = [];
    end
    % disp(ids)
    
    % get terms
    nom = zeros(length(ids),1);
    denom = zeros(length(ids),1);
    for i = 1:length(ids)
        nom(i) = counts(ids(i))./d(ids(i)).^2;
        denom(i) = 1./d(ids(i)).^2;
    end
    % disp(nom)
    % disp(denom)
    predict = sum(nom)/sum(denom);
end