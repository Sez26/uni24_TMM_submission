function G = categorise_roads(G, h, n)
    % categorise roads labels all roads either verticle or horizontal as a
    % grid network (1-n)
    % G = graph
    % h = plot with x and y coordinates
    % n = key parameter in size of graph

    % assume that all weights are even, find node spacing
    node_int = G.Edges.Weight(1)*2; %0.1 for n = 10

    % Categorise roads
    edge_ori = zeros(numedges(G), 1); % 1 = horiztonal, 2 = vertical
    edge_dir = zeros(numedges(G), 1); % 1 = +ve, 2 = -ve
    rd_idx = zeros(numedges(G), 1); % between 1 - n
    for k = 1:numedges(G)
        src = G.Edges.EndNodes(k, 1); % Source node
        tgt = G.Edges.EndNodes(k, 2); % Target node
    
        % Get the coordinates of the source and target nodes
        x1 = h.XData(src);
        y1 = h.YData(src);
        x2 = h.XData(tgt);
        y2 = h.YData(tgt);
    
        % Classify the edge based on the coordinates
        if y1 == y2  % Same row -> Horizontal edge (Row)

            % The edge belongs to the row determined by y1 (or y2)
            edge_ori(k) = 1;
            rd_idx(k) = round(y1/node_int);
            % Determine the direction: left to right or right to left
            if x1 < x2
                edge_dir(k) = 1;
            elseif x1 > x2
                edge_dir(k) = 2;
            end
        elseif x1 == x2  % Same column -> Vertical edge (Column)
            % The edge belongs to the column determined by x1 (or x2)
            edge_ori(k) = 2;
            rd_idx(k) = round(x1/node_int);
            % Determine the direction: up to down or down to up
            if y1 < y2
                edge_dir(k) = 1;
            elseif y1 > y2
                edge_dir(k) = 2;
            end
        end
    end
    
    % Add the row, column, and direction information as new columns in the G.Edges table
    G.Edges.rd_idx = rd_idx;
    G.Edges.Ori = edge_ori;
    G.Edges.Dir = edge_dir;
end