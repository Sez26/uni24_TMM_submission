function route_use(G, s_v, targets, Title)
    %%% this function takes inputs of your network graph (G)

    % finds the shortest path for each s-t pair and finds which edges in
    % the network are used the most.

    % from each road node there is a journey to each corner node
    % four journeys
    function count_arr = count_edge_hot(edges, num_edges)
        % generate zero basic count_arr
        count_arr = zeros(num_edges,1);
        % zero check
        if isempty(edges)
        else
            count_arr(edges{:}) = 1;
        end
    end
    route_use = zeros(numedges(G),length(targets));
    for m = 1:length(targets)
        
        [P, d, ep] = arrayfun(@(s,t) shortestpath(G,s,t), s_v, targets(m).*ones(length(s_v),1), UniformOutput=false);

        % edge count
        e_c = arrayfun(@count_edge_hot, ep, height(G.Edges).*ones(size(d)), UniformOutput=false);
        % this is currently an cell array
        
        % converting into a normal array
        e_c_arr = zeros(height(G.Edges), length(s_v)^2);
    
        for i = 1:length(s_v)
            e_c_arr(:,i) = cell2mat(e_c(i));
        end
        
        route_use(:,m) = sum(e_c_arr, 2); % vector for all edges
    end
    
    route_use_sum = sum(route_use,2);

    % visualise
    h = plot(G, EdgeCData=route_use_sum);
    cb = colorbar();
    ylabel(cb,'Maximum Route Usage','Rotation',270)
    h.XData = G.Nodes.PosX;
    h.YData = G.Nodes.PosY;
    axis equal
    title(Title)
end